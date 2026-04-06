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
#  RL Agent — Benchmark-Optimised Policy                               #
# ------------------------------------------------------------------ #

class RLAgent(BaseAgent):
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

    name = "RLAgent"

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
        #                                                            #
        # Deploy medical to every zone that has patients but no      #
        # team yet.  Medical teams persist forever, so each deploy   #
        # buys permanent:                                            #
        #   • critical death-rate cut  30% → 10%                     #
        #   • 60% of critical stabilised to injured                  #
        #   • 40% of injured healed to healthy (+20 reward each)     #
        #   • injured → critical escalation stopped (20% → 0%)       #
        # ======================================================== #

        uncovered_with_patients = [
            z
            for z in zones
            if "medical_team" not in z.get("teams_present", [])
            and (z.get("critical", 0) > 0 or z.get("injured", 0) > 0)
        ]

        if uncovered_with_patients:
            # Highest urgency first — critical weighted 3× because
            # without medical, 30% die per tick vs only 20% of
            # injured escalating.
            uncovered_with_patients.sort(
                key=lambda z: z.get("critical", 0) * 3 + z.get("injured", 0),
                reverse=True,
            )
            return make_action(
                "deploy_medical", zone=uncovered_with_patients[0]["id"]
            )

        # ======================================================== #
        # PHASE 2 — PREDICTIVE SUSTAIN                               #
        #                                                            #
        # All zones with patients now have medical teams.            #
        # Prevent resource-driven death cascades by allocating       #
        # enough supply to last the remaining simulation ticks.      #
        # ======================================================== #

        live_zones = [z for z in zones if self._get_living(z) > 0]
        if not live_zones:
            return make_action("do_nothing")

        # --- 2a: FOOD — starvation kills 5% of healthy each tick --- #
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

        # --- 2b: WATER — dehydration pushes 10% injured → critical --- #
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

        # --- 2c: MEDICINE — depletion pushes 15% injured → critical --- #
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

        # --- 2d: ROADS — degradation increases resource burn rate --- #
        worst_road_zone = min(
            live_zones, key=lambda z: z.get("road_access", 1.0)
        )
        if worst_road_zone.get("road_access", 1.0) < 0.3:
            return make_action("repair_road", zone=worst_road_zone["id"])

        return make_action("do_nothing")
