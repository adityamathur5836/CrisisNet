"""
CrisisNet Agents

Decision-making agents for the disaster response simulation:
    1. RandomAgent      – picks a random action and zone each step.
    2. HeuristicAgent   – rule-based priorities (critical → food → roads).
    3. OptimalAgent      – hand-crafted optimal policy exploiting env mechanics.
    4. RLAgent           – Stable-Baselines3 DQN-trained policy.
    5. SB3Agent          – Gymnasium-interface wrapper for SB3 models.
"""

import os
import random
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import numpy as np

from backend.actions import make_action


# ------------------------------------------------------------------ #
#  Base Agent                                                          #
# ------------------------------------------------------------------ #

class BaseAgent(ABC):
    """Abstract base class that every agent must implement."""

    name: str = "BaseAgent"

    @abstractmethod
    def decide(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        Choose an action given the current simulation state.

        Args:
            state: The environment state dict (from env.get_state()).

        Returns:
            A well-formed action dictionary.
        """


# ------------------------------------------------------------------ #
#  Random Agent                                                        #
# ------------------------------------------------------------------ #

class RandomAgent(BaseAgent):
    """
    Picks a uniformly random action type and target zone each step.
    Useful as a baseline / lower bound.
    """

    name = "RandomAgent"

    _ZONE_ACTIONS = [
        "deploy_medical",
        "deploy_rescue",
        "deploy_engineering",
        "allocate_food",
        "allocate_water",
        "allocate_medicine",
        "repair_road",
        "evacuate",
        "establish_comms",
    ]

    _RESOURCE_ACTIONS = {"allocate_food", "allocate_water", "allocate_medicine"}

    def __init__(self, seed: int | None = None) -> None:
        self._rng = random.Random(seed)

    def decide(self, state: dict[str, Any]) -> dict[str, Any]:
        zones = state.get("zones", [])
        if not zones:
            return make_action("do_nothing")

        # 50% chance to do nothing to ensure RandomAgent fails visibly
        if self._rng.random() < 0.5:
            return make_action("do_nothing")

        action_type = self._rng.choice(self._ZONE_ACTIONS)
        zone_id = self._rng.choice(zones)["id"]

        amount = None
        if action_type in self._RESOURCE_ACTIONS:
            amount = float(self._rng.randint(1, 10))

        return make_action(action_type, zone=zone_id, amount=amount)


# ------------------------------------------------------------------ #
#  Heuristic Agent                                                     #
# ------------------------------------------------------------------ #

class HeuristicAgent(BaseAgent):
    """
    Rule-based agent with fixed priority ordering:

        1. Zone with highest critical count  → deploy_medical
        2. Zone with lowest food             → allocate_food
        3. Zone with lowest water            → allocate_water
        4. Zone with lowest road_access      → repair_road
        5. Fallback                          → do_nothing

    Deterministic and interpretable — a solid mid-range baseline.
    """

    name = "HeuristicAgent"

    # Thresholds that trigger each priority
    CRITICAL_THRESHOLD: int = 5       # act if any zone has ≥ this many critical
    FOOD_THRESHOLD: int = 80          # act if any zone has ≤ this much food
    WATER_THRESHOLD: int = 100        # act if any zone has ≤ this much water
    ROAD_THRESHOLD: float = 0.3       # act if any zone road < this
    FOOD_ALLOCATION: float = 50.0     # amount of food to send
    WATER_ALLOCATION: float = 50.0    # amount of water to send

    def decide(self, state: dict[str, Any]) -> dict[str, Any]:
        zones = state.get("zones", [])
        if not zones:
            return make_action("do_nothing")

        # Priority 1 — highest critical → deploy medical
        worst_critical = max(zones, key=lambda z: z["critical"])
        if worst_critical["critical"] >= self.CRITICAL_THRESHOLD:
            return make_action("deploy_medical", zone=worst_critical["id"])

        # Priority 2 — lowest food → allocate food
        lowest_food = min(zones, key=lambda z: z["food"])
        if lowest_food["food"] <= self.FOOD_THRESHOLD:
            return make_action(
                "allocate_food",
                zone=lowest_food["id"],
                amount=self.FOOD_ALLOCATION,
            )

        # Priority 3 — lowest water → allocate water
        lowest_water = min(zones, key=lambda z: z["water"])
        if lowest_water["water"] <= self.WATER_THRESHOLD:
            return make_action(
                "allocate_water",
                zone=lowest_water["id"],
                amount=self.WATER_ALLOCATION,
            )

        # Priority 4 — worst road → repair
        worst_road = min(zones, key=lambda z: z["road_access"])
        if worst_road["road_access"] < self.ROAD_THRESHOLD:
            return make_action("repair_road", zone=worst_road["id"])

        return make_action("do_nothing")


# ------------------------------------------------------------------ #
#  Optimal Agent — Hand-crafted Benchmark Policy                       #
# ------------------------------------------------------------------ #

class OptimalAgent(BaseAgent):
    """
    Benchmark-optimised policy agent for CrisisNet.

    Strategy is built on three exploitable environment mechanics:

        1. **Medical teams persist forever** once deployed to a zone.
           deploy_medical to zone X at tick 1 → zone X has a medical team
           for ALL remaining ticks.  This makes deploy_medical the highest-
           ROI action: one action buys permanent healing + death-rate
           reduction.

        2. **evacuate is unimplemented** in the environment — it silently
           does nothing.  Never use it.

        3. **Resource allocations are uncapped** — allocating 5 000 food in
           one action permanently fixes a zone's food supply for the rest
           of the simulation.

    Policy:
        PHASE 1 — COVERAGE RUSH  (ticks 1..N, N ≤ 5)
            Deploy medical to each zone that does not yet have a medical
            team and still has patients (critical > 0 or injured > 0).
            Order by urgency: critical × 3 + injured (critical patients
            die 3× faster without help).

        PHASE 2 — PREDICTIVE SUSTAIN  (remaining ticks)
            Use depletion-rate estimates to identify the zone closest to
            running out of food / water / medicine and send a single
            large allocation that covers it for the rest of the sim.
            Road repair as lowest priority.
    """

    name = "OptimalAgent"

    def __init__(self, seed: int | None = None) -> None:
        # No mutable state needed — fully reactive from observation.
        pass

    # ---------------------------------------------------------------- #
    #  helpers                                                          #
    # ---------------------------------------------------------------- #

    @staticmethod
    def _get_living(z: dict[str, Any]) -> int:
        return z.get("healthy", 0) + z.get("injured", 0) + z.get("critical", 0)

    @staticmethod
    def _delivery_penalty(road: float) -> float:
        """Mirror the environment's road-based consumption multiplier."""
        if road < 0.5:
            return 1.0 + (0.5 - road) * 2.0
        return 1.0

    def _food_ticks_left(self, z: dict[str, Any]) -> float:
        """Estimate how many ticks before food reaches zero."""
        living = self._get_living(z)
        if living == 0:
            return float("inf")
        penalty = self._delivery_penalty(z.get("road_access", 1.0))
        consumption = max(1, living // 10) * penalty
        return z.get("food", 0) / max(consumption, 1)

    def _water_ticks_left(self, z: dict[str, Any]) -> float:
        """Estimate how many ticks before water reaches zero."""
        living = self._get_living(z)
        if living == 0:
            return float("inf")
        penalty = self._delivery_penalty(z.get("road_access", 1.0))
        consumption = max(1, living // 5) * penalty
        return z.get("water", 0) / max(consumption, 1)

    def _food_allocation_amount(
        self, z: dict[str, Any], ticks_remaining: int
    ) -> float:
        """How much food to send so the zone lasts the rest of the sim."""
        living = self._get_living(z)
        penalty = self._delivery_penalty(z.get("road_access", 1.0))
        consumption = max(1, living // 10) * penalty
        # 1.5× buffer for road degradation increasing consumption
        return max(500.0, consumption * ticks_remaining * 1.5)

    def _water_allocation_amount(
        self, z: dict[str, Any], ticks_remaining: int
    ) -> float:
        """How much water to send so the zone lasts the rest of the sim."""
        living = self._get_living(z)
        penalty = self._delivery_penalty(z.get("road_access", 1.0))
        consumption = max(1, living // 5) * penalty
        return max(500.0, consumption * ticks_remaining * 1.5)

    # ---------------------------------------------------------------- #
    #  main decision                                                    #
    # ---------------------------------------------------------------- #

    def decide(self, state: dict[str, Any]) -> dict[str, Any]:
        zones = state.get("zones", [])
        if not zones:
            return make_action("do_nothing")

        time = state.get("time", 0)
        max_time = state.get("max_time", 12)
        ticks_remaining = max(1, max_time - time)

        # ======================================================== #
        # PHASE 1 — MEDICAL COVERAGE RUSH                           #
        # ======================================================== #

        uncovered_with_patients = [
            z
            for z in zones
            if "medical_team" not in z.get("teams_present", [])
            and (z.get("critical", 0) > 0 or z.get("injured", 0) > 0)
        ]

        if uncovered_with_patients:
            uncovered_with_patients.sort(
                key=lambda z: z.get("critical", 0) * 3 + z.get("injured", 0),
                reverse=True,
            )
            return make_action(
                "deploy_medical", zone=uncovered_with_patients[0]["id"]
            )

        # ======================================================== #
        # PHASE 2 — PREDICTIVE SUSTAIN                               #
        # ======================================================== #

        live_zones = [z for z in zones if self._get_living(z) > 0]
        if not live_zones:
            return make_action("do_nothing")

        # --- 2a: FOOD --- #
        food_urgency = [
            (z, self._food_ticks_left(z)) for z in live_zones
        ]
        food_urgency.sort(key=lambda x: x[1])
        worst_food_zone, worst_food_ttl = food_urgency[0]

        if worst_food_ttl < ticks_remaining:
            amount = self._food_allocation_amount(
                worst_food_zone, ticks_remaining
            )
            return make_action(
                "allocate_food", zone=worst_food_zone["id"], amount=amount
            )

        # --- 2b: WATER --- #
        water_urgency = [
            (z, self._water_ticks_left(z)) for z in live_zones
        ]
        water_urgency.sort(key=lambda x: x[1])
        worst_water_zone, worst_water_ttl = water_urgency[0]

        if worst_water_ttl < ticks_remaining:
            amount = self._water_allocation_amount(
                worst_water_zone, ticks_remaining
            )
            return make_action(
                "allocate_water", zone=worst_water_zone["id"], amount=amount
            )

        # --- 2c: MEDICINE --- #
        med_candidates = [
            (z, z.get("medical", 0))
            for z in live_zones
            if z.get("injured", 0) > 0
        ]
        if med_candidates:
            med_candidates.sort(key=lambda x: x[1])
            worst_med_zone, worst_med_supply = med_candidates[0]
            if worst_med_supply < 30:
                return make_action(
                    "allocate_medicine",
                    zone=worst_med_zone["id"],
                    amount=500.0,
                )

        # --- 2d: ROADS --- #
        worst_road_zone = min(
            live_zones, key=lambda z: z.get("road_access", 1.0)
        )
        if worst_road_zone.get("road_access", 1.0) < 0.3:
            return make_action("repair_road", zone=worst_road_zone["id"])

        return make_action("do_nothing")


# ------------------------------------------------------------------ #
#  RL Agent — Stable-Baselines3 DQN  (Improved)                       #
# ------------------------------------------------------------------ #

class RLAgent(BaseAgent):
    """
    RL agent powered by a Stable-Baselines3 DQN model with an
    intelligent action-safety layer and dynamic resource allocation.

    Improvements over naive DQN inference:
        1. Dynamic zone mapping — resolves actual zone IDs from state.
        2. Action safety layer — skips wasteful / invalid actions and
           falls back to next-best Q-value or OptimalAgent.
        3. Dynamic allocation — scales food/water/medicine amounts
           based on population, remaining ticks, and consumption rate.
        4. Debug mode — optional verbose logging for troubleshooting.

    Falls back to OptimalAgent when no trained model is available.
    """

    name = "RLAgent"

    # Must match gym_env.py exactly
    _ACTION_TYPES = [
        "deploy_medical",
        "allocate_food",
        "allocate_water",
        "allocate_medicine",
        "repair_road",
    ]
    _NUM_ACTION_TYPES = len(_ACTION_TYPES)  # 5
    _NUM_ZONES = 5
    _NUM_ACTIONS = _NUM_ACTION_TYPES * _NUM_ZONES  # 25

    def __init__(
        self,
        seed: int | None = None,
        model_path: str | None = None,
        debug: bool = False,
    ) -> None:
        self._model = None
        self._fallback = OptimalAgent(seed=seed)
        self._debug = debug

        if model_path is None:
            model_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "models",
                "dqn_crisisnet.zip",
            )

        self._model_path = model_path
        self._load_model()

    # ---------------------------------------------------------------- #
    #  Model loading                                                    #
    # ---------------------------------------------------------------- #

    def _load_model(self) -> None:
        """Attempt to load the SB3 DQN model."""
        if not os.path.exists(self._model_path):
            print(
                f"[RLAgent] ⚠ No model found at {self._model_path} "
                f"— will use OptimalAgent fallback."
            )
            return

        try:
            from stable_baselines3 import DQN

            self._model = DQN.load(self._model_path)
            print(
                f"[RLAgent] ✅ Model loaded successfully from {self._model_path}"
            )
        except Exception as e:
            print(
                f"[RLAgent] ⚠ Could not load model from {self._model_path}: {e}"
            )
            self._model = None

    # ---------------------------------------------------------------- #
    #  Observation builder  (MUST mirror gym_env.py exactly)            #
    # ---------------------------------------------------------------- #

    @staticmethod
    def _state_to_obs(state: dict[str, Any]) -> np.ndarray:
        """
        Convert the environment state dict into a flat 55-dim vector.

        Per-zone features (11) — identical order and normalisation
        as CrisisNetGymEnv._state_to_obs:
            0  healthy_ratio
            1  injured_ratio
            2  critical_ratio
            3  deceased_ratio
            4  food_norm       (/ 1000, capped at 1)
            5  water_norm      (/ 1000, capped at 1)
            6  medical_norm    (/ 200,  capped at 1)
            7  fuel_norm       (/ 500,  capped at 1)
            8  road_access     (already 0–1)
            9  hospital_load   (critical / capacity, capped at 1)
           10  has_medical_team (0 or 1)
        """
        obs: list[float] = []
        for zone in state.get("zones", []):
            pop = (
                zone["healthy"]
                + zone["injured"]
                + zone["critical"]
                + zone["deceased"]
            )
            pop = max(pop, 1)

            obs.extend(
                [
                    zone["healthy"] / pop,
                    zone["injured"] / pop,
                    zone["critical"] / pop,
                    zone["deceased"] / pop,
                    min(zone["food"] / 1000.0, 1.0),
                    min(zone["water"] / 1000.0, 1.0),
                    min(zone["medical"] / 200.0, 1.0),
                    min(zone["fuel"] / 500.0, 1.0),
                    zone["road_access"],
                    min(
                        zone["critical"] / max(zone["hospital_capacity"], 1),
                        1.0,
                    ),
                    1.0
                    if "medical_team" in zone.get("teams_present", [])
                    else 0.0,
                ]
            )

        return np.array(obs, dtype=np.float32)

    # ---------------------------------------------------------------- #
    #  Dynamic resource-allocation amounts                              #
    # ---------------------------------------------------------------- #

    @staticmethod
    def _get_living(z: dict[str, Any]) -> int:
        return z.get("healthy", 0) + z.get("injured", 0) + z.get("critical", 0)

    @staticmethod
    def _delivery_penalty(road: float) -> float:
        if road < 0.5:
            return 1.0 + (0.5 - road) * 2.0
        return 1.0

    def _compute_food_amount(
        self, zone: dict[str, Any], ticks_remaining: int
    ) -> float:
        """Scale food to last the rest of the episode with 1.5× buffer."""
        living = self._get_living(zone)
        penalty = self._delivery_penalty(zone.get("road_access", 1.0))
        consumption_per_tick = max(1, living // 10) * penalty
        needed = consumption_per_tick * ticks_remaining * 1.5
        return max(300.0, needed - zone.get("food", 0))

    def _compute_water_amount(
        self, zone: dict[str, Any], ticks_remaining: int
    ) -> float:
        """Scale water to last the rest of the episode with 1.5× buffer."""
        living = self._get_living(zone)
        penalty = self._delivery_penalty(zone.get("road_access", 1.0))
        consumption_per_tick = max(1, living // 5) * penalty
        needed = consumption_per_tick * ticks_remaining * 1.5
        return max(300.0, needed - zone.get("water", 0))

    def _compute_medicine_amount(self, zone: dict[str, Any]) -> float:
        """Scale medicine to injured population."""
        injured = zone.get("injured", 0)
        critical = zone.get("critical", 0)
        return max(100.0, float((injured + critical) * 2) - zone.get("medical", 0))

    # ---------------------------------------------------------------- #
    #  Action decoding with dynamic zone mapping                        #
    # ---------------------------------------------------------------- #

    def _decode_action(
        self,
        action_id: int,
        zones: list[dict[str, Any]],
        ticks_remaining: int,
    ) -> dict[str, Any]:
        """
        Convert flat discrete action id → action dict.

        Uses actual zone IDs from state (not hardcoded 1–5) and
        computes dynamic resource amounts.
        """
        type_idx = action_id // self._NUM_ZONES
        zone_offset = action_id % self._NUM_ZONES

        action_type = self._ACTION_TYPES[type_idx]

        # Map zone_offset to actual zone id from the state
        if zone_offset < len(zones):
            zone = zones[zone_offset]
            zone_id = zone["id"]
        else:
            zone_id = zone_offset + 1
            zone = None

        # --- Dynamic allocation amounts --- #
        if action_type == "allocate_food" and zone is not None:
            amount = self._compute_food_amount(zone, ticks_remaining)
        elif action_type == "allocate_water" and zone is not None:
            amount = self._compute_water_amount(zone, ticks_remaining)
        elif action_type == "allocate_medicine" and zone is not None:
            amount = self._compute_medicine_amount(zone)
        else:
            amount = None

        return make_action(action_type, zone=zone_id, amount=amount)

    # ---------------------------------------------------------------- #
    #  Action safety / validation layer                                 #
    # ---------------------------------------------------------------- #

    def _is_action_wasteful(
        self, action_id: int, zones: list[dict[str, Any]]
    ) -> bool:
        """
        Returns True if the action would be wasted given current state.

        Filters out:
            - deploy_medical to a zone that already has a medical team
            - deploy_medical to a zone with zero living population
            - allocate_food/water/medicine to a zone with zero living pop
            - allocate_food to a zone already well-stocked (>800)
            - allocate_water to a zone already well-stocked (>800)
            - allocate_medicine to a zone with no injured/critical
            - repair_road on a zone with road >= 0.9
        """
        type_idx = action_id // self._NUM_ZONES
        zone_offset = action_id % self._NUM_ZONES

        if zone_offset >= len(zones):
            return True

        zone = zones[zone_offset]
        action_type = self._ACTION_TYPES[type_idx]
        living = self._get_living(zone)

        # Zone is dead — any action is pointless
        if living == 0:
            return True

        if action_type == "deploy_medical":
            # Already has medical team → wasted action
            if "medical_team" in zone.get("teams_present", []):
                return True
            # No patients to treat
            if zone.get("injured", 0) == 0 and zone.get("critical", 0) == 0:
                return True

        elif action_type == "allocate_food":
            # Already well-stocked
            if zone.get("food", 0) > 800:
                return True

        elif action_type == "allocate_water":
            if zone.get("water", 0) > 800:
                return True

        elif action_type == "allocate_medicine":
            # No one to treat
            if zone.get("injured", 0) == 0 and zone.get("critical", 0) == 0:
                return True
            if zone.get("medical", 0) > 150:
                return True

        elif action_type == "repair_road":
            if zone.get("road_access", 1.0) >= 0.9:
                return True

        return False

    def _get_safe_action(
        self,
        obs: np.ndarray,
        zones: list[dict[str, Any]],
    ) -> int | None:
        """
        Pick the best non-wasteful action using Q-values.

        Queries the DQN for Q-values across all 25 actions, then
        iterates from highest to lowest Q-value, returning the first
        action that passes the safety check.

        Returns None if all actions are wasteful (triggers fallback).
        """
        try:
            import torch

            obs_tensor = torch.as_tensor(obs).unsqueeze(0).to(
                self._model.device
            )
            with torch.no_grad():
                q_values = (
                    self._model.q_net(obs_tensor).cpu().numpy().flatten()
                )
        except Exception:
            # If Q-value extraction fails, return the raw prediction
            action_id, _ = self._model.predict(obs, deterministic=True)
            return int(action_id)

        # Rank actions by Q-value (highest first)
        ranked_actions = np.argsort(q_values)[::-1]

        for action_id in ranked_actions:
            if not self._is_action_wasteful(int(action_id), zones):
                if self._debug:
                    print(
                        f"  [RLAgent] Selected action {action_id} "
                        f"(Q={q_values[action_id]:.1f}, "
                        f"rank={list(ranked_actions).index(action_id)+1}/25)"
                    )
                return int(action_id)

        # All actions wasteful
        if self._debug:
            print("  [RLAgent] All 25 actions are wasteful → fallback")
        return None

    # ---------------------------------------------------------------- #
    #  Main decision interface                                          #
    # ---------------------------------------------------------------- #

    def decide(self, state: dict[str, Any]) -> dict[str, Any]:
        zones = state.get("zones", [])
        time = state.get("time", 0)
        max_time = state.get("max_time", 12)
        ticks_remaining = max(1, max_time - time)

        # --- No model loaded → fall back to OptimalAgent --- #
        if self._model is None:
            if self._debug:
                print("[RLAgent] No model loaded — using OptimalAgent fallback")
            return self._fallback.decide(state)

        # --- Build observation (must match training env exactly) --- #
        obs = self._state_to_obs(state)

        if self._debug:
            print(f"[RLAgent] tick={time}  obs_shape={obs.shape}  "
                  f"obs_range=[{obs.min():.3f}, {obs.max():.3f}]")

        # --- Get safe action via Q-value ranking --- #
        action_id = self._get_safe_action(obs, zones)

        # All actions wasteful → OptimalAgent fallback
        if action_id is None:
            if self._debug:
                print("[RLAgent] Safety layer exhausted → OptimalAgent fallback")
            return self._fallback.decide(state)

        # --- Decode with dynamic amounts --- #
        action_dict = self._decode_action(action_id, zones, ticks_remaining)

        if self._debug:
            type_idx = action_id // self._NUM_ZONES
            zone_offset = action_id % self._NUM_ZONES
            zone_id = zones[zone_offset]["id"] if zone_offset < len(zones) else "?"
            print(
                f"  [RLAgent] action_id={action_id} → "
                f"{self._ACTION_TYPES[type_idx]}(zone={zone_id}) "
                f"amount={action_dict.get('amount')}"
            )

        return action_dict


# ------------------------------------------------------------------ #
#  SB3 Agent — Gymnasium-interface adapter                             #
# ------------------------------------------------------------------ #

class SB3Agent:
    """
    Adapter that wraps a Stable-Baselines3 model for use with
    the CrisisNetGymEnv directly (integer action in, integer action out).

    This is used by the training and benchmark scripts.
    """

    name = "SB3Agent"

    def __init__(self, model):
        self.model = model

    def predict(self, obs: np.ndarray, deterministic: bool = True) -> int:
        action, _ = self.model.predict(obs, deterministic=deterministic)
        return int(action)
