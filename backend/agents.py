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
        3. Zone with lowest road_access      → repair_road
        4. Fallback                          → do_nothing

    Deterministic and interpretable — a solid mid-range baseline.
    """

    name = "HeuristicAgent"

    # Thresholds that trigger each priority
    CRITICAL_THRESHOLD: int = 5      # act if any zone has ≥ this many critical
    FOOD_THRESHOLD: int = 80          # act if any zone has ≤ this much food
    ROAD_THRESHOLD: float = 0.3       # act if any zone road < this
    FOOD_ALLOCATION: float = 50.0    # amount of food to send

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


class RLAgent(BaseAgent):
    """
    Simulated reinforcement-learning agent.
    Optimized strictly to mathematically maximize survival efficiency.
    """

    name = "RLAgent"
    
    def decide(self, state: dict[str, Any]) -> dict[str, Any]:
        zones = state.get("zones", [])
        if not zones:
            return make_action("do_nothing")

        candidates = self._generate_candidates(zones)

        if not candidates:
            return make_action("do_nothing")

        # Pick the absolute best action
        best = max(candidates, key=lambda c: c["score"])
        return best["action"]

    def _generate_candidates(self, zones: list[dict[str, Any]]) -> list[dict[str, Any]]:
        candidates: list[dict[str, Any]] = []

        for zone in zones:
            zone_id = zone["id"]
            
            critical = zone.get("critical", 0)
            injured = zone.get("injured", 0)
            food = zone.get("food", 0)
            water = zone.get("water", 0)
            road_access = zone.get("road_access", 1.0)
            hospital_capacity = zone.get("hospital_capacity", 0)
            
            total_living = zone.get("healthy", 0) + injured + critical
            
            # Derived metrics
            food_shortage = max(0, (total_living * 1.5) - food)
            water_shortage = max(0, (total_living * 1.5) - water)
            road_damage = max(0, (1.0 - road_access) * 100.0)
            
            # Base danger score using the strictly defined formula
            base_score = (critical * 3.0) + (injured * 1.5) + (food_shortage * 2.0) + (road_damage * 2.5)

            # --- Evaluate repair_road ---
            if road_access < 1.0:
                road_score = base_score
                # Multiplier for severe road blockages
                if road_access < 0.5:
                    road_score *= 5.0
                candidates.append({
                    "action": make_action("repair_road", zone=zone_id),
                    "score": road_score
                })

            # --- Evaluate deploy_medical ---
            if critical > 0 or injured > 0:
                med_score = base_score
                # Severe multiplier if hospitals are overflowing
                if critical > hospital_capacity:
                    med_score *= 4.0
                candidates.append({
                    "action": make_action("deploy_medical", zone=zone_id),
                    "score": med_score
                })
                
            # --- Evaluate allocate_food ---
            if total_living > 0 and food < (total_living * 5):
                food_score = base_score
                # Severe multiplier if pre-crisis threshold breached
                if food < (total_living * 1.5):
                    food_score *= 3.0
                candidates.append({
                    "action": make_action("allocate_food", zone=zone_id, amount=100.0),
                    "score": food_score
                })

            # --- Evaluate allocate_water ---
            if total_living > 0 and water < (total_living * 5):
                # Similar weight to food since starvation and dehydration both cause immediate death
                water_score = base_score + (water_shortage * 2.0)
                if water < (total_living * 1.5):
                    water_score *= 3.0
                candidates.append({
                    "action": make_action("allocate_water", zone=zone_id, amount=100.0),
                    "score": water_score
                })

        return candidates
