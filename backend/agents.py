"""
CrisisNet Agents

Three decision-making agents for the disaster response simulation:
    1. RandomAgent      – picks a random action and zone each step.
    2. HeuristicAgent   – rule-based priorities (critical → food → roads).
    3. RLAgent          – simulated RL agent blending heuristics with
                          long-term strategy (infrastructure first).
"""

import random
from abc import ABC, abstractmethod
from typing import Any

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

        action_type = self._rng.choice(self._ZONE_ACTIONS)
        zone_id = self._rng.choice(zones)["id"]

        amount = None
        if action_type in self._RESOURCE_ACTIONS:
            amount = float(self._rng.randint(10, 100))

        return make_action(action_type, zone=zone_id, amount=amount)


# ------------------------------------------------------------------ #
#  Heuristic Agent                                                     #
# ------------------------------------------------------------------ #

class HeuristicAgent(BaseAgent):
    """
    Rule-based agent with fixed priority ordering:

        1. Zone with highest critical count  → deploy_medical
        2. Zone with lowest food             → allocate_food
        3. Zone with lowest road_access      → repair_road
        4. Fallback                          → do_nothing

    Deterministic and interpretable — a solid mid-range baseline.
    """

    name = "HeuristicAgent"

    # Thresholds that trigger each priority
    CRITICAL_THRESHOLD: int = 20      # act if any zone has ≥ this many critical
    FOOD_THRESHOLD: int = 50          # act if any zone has ≤ this much food
    ROAD_THRESHOLD: float = 0.5       # act if any zone road < this
    FOOD_ALLOCATION: float = 100.0    # amount of food to send

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

        # Priority 3 — worst road → repair
        worst_road = min(zones, key=lambda z: z["road_access"])
        if worst_road["road_access"] < self.ROAD_THRESHOLD:
            return make_action("repair_road", zone=worst_road["id"])

        return make_action("do_nothing")


# ------------------------------------------------------------------ #
#  RL Agent (Simulated)                                                #
# ------------------------------------------------------------------ #

class RLAgent(BaseAgent):
    """
    Simulated reinforcement-learning agent.

    Combines heuristic evaluation with a long-term strategy bias:
        - Prioritises infrastructure repair early (investment phase).
        - Switches to medical / resource allocation in mid-to-late game.
        - Uses a scoring function to pick the best action each step.

    This is *not* a trained model — it simulates what a well-tuned
    RL policy might learn by encoding the key trade-offs.
    """

    name = "RLAgent"

    # Weight multipliers for the scoring function
    W_CRITICAL: float = 3.0
    W_FOOD: float = 2.0
    W_ROAD: float = 5.0        # high weight — long-term payoff
    W_HOSPITAL: float = 1.5
    W_WATER: float = 1.8

    def decide(self, state: dict[str, Any]) -> dict[str, Any]:
        zones = state.get("zones", [])
        if not zones:
            return make_action("do_nothing")

        time = state.get("time", 0)
        max_time = state.get("max_time", 12)
        progress = time / max_time  # 0.0 → 1.0

        # Score every candidate action and pick the best
        candidates = self._generate_candidates(zones, progress)

        if not candidates:
            return make_action("do_nothing")

        best = max(candidates, key=lambda c: c["score"])
        return best["action"]

    def _generate_candidates(
        self,
        zones: list[dict[str, Any]],
        progress: float,
    ) -> list[dict[str, Any]]:
        """
        Generate and score candidate actions.

        Args:
            zones:    List of zone dicts.
            progress: Fraction of simulation elapsed (0.0–1.0).

        Returns:
            List of {"action": ..., "score": float} dicts.
        """
        candidates: list[dict[str, Any]] = []

        # Time-dependent strategy shift:
        #   early game (progress < 0.3)  → favour infrastructure
        #   late  game (progress > 0.6)  → favour immediate rescue
        infra_bonus = max(0.0, 1.0 - progress * 2.0)   # 1.0 → 0.0 over first half
        rescue_bonus = max(0.0, progress * 2.0 - 0.5)   # 0.0 → 1.5 over second half

        for zone in zones:
            zone_id = zone["id"]

            # --- road repair --- #
            if zone["road_access"] < 0.6:
                road_urgency = (0.6 - zone["road_access"]) / 0.6
                score = (self.W_ROAD * road_urgency) + (self.W_ROAD * infra_bonus)
                candidates.append({
                    "action": make_action("repair_road", zone=zone_id),
                    "score": score,
                })

            # --- deploy medical --- #
            if zone["critical"] > 0:
                crit_urgency = zone["critical"] / max(1, zone["hospital_capacity"])
                score = (self.W_CRITICAL * crit_urgency) + (self.W_HOSPITAL * rescue_bonus)
                candidates.append({
                    "action": make_action("deploy_medical", zone=zone_id),
                    "score": score,
                })

            # --- allocate food --- #
            living = zone["healthy"] + zone["injured"] + zone["critical"]
            if living > 0:
                food_urgency = 1.0 - min(1.0, zone["food"] / (living * 0.5))
                if food_urgency > 0.3:
                    score = self.W_FOOD * food_urgency + rescue_bonus
                    candidates.append({
                        "action": make_action("allocate_food", zone=zone_id, amount=100.0),
                        "score": score,
                    })

            # --- allocate water --- #
            if living > 0:
                water_urgency = 1.0 - min(1.0, zone["water"] / (living * 0.5))
                if water_urgency > 0.3:
                    score = self.W_WATER * water_urgency + rescue_bonus
                    candidates.append({
                        "action": make_action("allocate_water", zone=zone_id, amount=100.0),
                        "score": score,
                    })

        return candidates
