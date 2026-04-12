"""
CrisisNet Gymnasium Wrapper

Wraps the existing CrisisNetEnv into a proper gymnasium.Env so that
Stable-Baselines3 (and any other RL library) can train on it directly.

Observation space : Box(55,)  — 11 normalised features × 5 zones
Action space      : Discrete(25) — 5 action types × 5 zones
"""

from __future__ import annotations

from typing import Any

import gymnasium as gym
import numpy as np
from gymnasium import spaces

from backend.environment import CrisisNetEnv
from backend.actions import make_action


# ------------------------------------------------------------------ #
#  Action mapping                                                      #
# ------------------------------------------------------------------ #

# 5 meaningful action types that the environment actually processes
ACTION_TYPES = [
    "deploy_medical",
    "allocate_food",
    "allocate_water",
    "allocate_medicine",
    "repair_road",
]

NUM_ACTION_TYPES = len(ACTION_TYPES)  # 5
NUM_ZONES = 5
NUM_ACTIONS = NUM_ACTION_TYPES * NUM_ZONES  # 25

# Resource amounts for allocation actions (generous enough to matter)
_ALLOC_AMOUNTS = {
    "allocate_food": 200.0,
    "allocate_water": 200.0,
    "allocate_medicine": 100.0,
}

# Features per zone for the observation vector
FEATURES_PER_ZONE = 11
OBS_DIM = FEATURES_PER_ZONE * NUM_ZONES  # 55


def decode_action(action_id: int) -> dict[str, Any]:
    """
    Convert a flat discrete action id (0–24) into an action dictionary.

    Mapping:  action_id = type_index * 5 + zone_offset
    """
    type_idx = action_id // NUM_ZONES
    zone_offset = action_id % NUM_ZONES
    zone_id = zone_offset + 1  # zones are 1-indexed

    action_type = ACTION_TYPES[type_idx]
    amount = _ALLOC_AMOUNTS.get(action_type)
    return make_action(action_type, zone=zone_id, amount=amount)


# ------------------------------------------------------------------ #
#  Difficulty presets                                                   #
# ------------------------------------------------------------------ #

TASK_CONFIGS = {
    "easy": {
        "food_range": (300, 700),
        "water_range": (400, 900),
        "medical_range": (80, 200),
        "fuel_range": (100, 400),
        "healthy_pct": (0.60, 0.80),
        "injured_pct": (0.15, 0.25),
        "critical_pct": (0.02, 0.06),
        "deceased_pct": (0.00, 0.01),
        "road_range": (0.6, 1.0),
        "hospital_range": (50, 150),
        "population_range": (800, 3000),
    },
    "medium": {
        "food_range": (100, 500),
        "water_range": (200, 800),
        "medical_range": (20, 150),
        "fuel_range": (50, 300),
        "healthy_pct": (0.50, 0.70),
        "injured_pct": (0.20, 0.30),
        "critical_pct": (0.05, 0.10),
        "deceased_pct": (0.00, 0.02),
        "road_range": (0.4, 1.0),
        "hospital_range": (10, 100),
        "population_range": (800, 5000),
    },
    "hard": {
        "food_range": (30, 200),
        "water_range": (50, 300),
        "medical_range": (5, 60),
        "fuel_range": (10, 100),
        "healthy_pct": (0.35, 0.55),
        "injured_pct": (0.25, 0.35),
        "critical_pct": (0.10, 0.20),
        "deceased_pct": (0.01, 0.05),
        "road_range": (0.15, 0.60),
        "hospital_range": (5, 40),
        "population_range": (1500, 6000),
    },
}


# ------------------------------------------------------------------ #
#  Gymnasium Environment                                               #
# ------------------------------------------------------------------ #

class CrisisNetGymEnv(gym.Env):
    """
    Gymnasium-compatible wrapper for CrisisNet.

    Parameters
    ----------
    task : str
        Difficulty preset: 'easy', 'medium', or 'hard'.
    seed : int | None
        Random seed for reproducibility.
    """

    metadata = {"render_modes": ["human"]}

    def __init__(self, task: str = "medium", seed: int | None = None):
        super().__init__()
        self.task = task
        self._seed = seed
        self._config = TASK_CONFIGS.get(task, TASK_CONFIGS["medium"])

        self.observation_space = spaces.Box(
            low=0.0, high=1.0, shape=(OBS_DIM,), dtype=np.float32
        )
        self.action_space = spaces.Discrete(NUM_ACTIONS)

        self._env = CrisisNetEnv(seed=seed)
        self._initial_population = 0
        self._cumulative_reward = 0.0

    # -------------------------------------------------------------- #
    #  Core API                                                        #
    # -------------------------------------------------------------- #

    def reset(
        self, *, seed: int | None = None, options: dict | None = None
    ) -> tuple[np.ndarray, dict]:
        if seed is not None:
            self._seed = seed
        self._env = CrisisNetEnv(seed=self._seed)

        # Apply difficulty-specific zone generation
        self._env.zones = [
            self._create_zone_with_config(zid)
            for zid in range(1, NUM_ZONES + 1)
        ]
        self._env.time = 0

        state = self._env.get_state()
        self._initial_population = sum(
            z["healthy"] + z["injured"] + z["critical"] + z["deceased"]
            for z in state["zones"]
        )
        self._cumulative_reward = 0.0

        obs = self._state_to_obs(state)
        info = {"task": self.task, "time": 0}
        return obs, info

    def step(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict]:
        action_dict = decode_action(int(action))
        state, reward, done = self._env.step(action_dict)
        self._cumulative_reward += reward

        obs = self._state_to_obs(state)
        info = {
            "time": state["time"],
            "step_metrics": state.get("step_metrics", {}),
            "action_dict": action_dict,
        }
        truncated = False
        return obs, reward, done, truncated, info

    # -------------------------------------------------------------- #
    #  Observation builder                                             #
    # -------------------------------------------------------------- #

    @staticmethod
    def _state_to_obs(state: dict[str, Any]) -> np.ndarray:
        """
        Convert the environment state dict into a flat 55-dim vector.

        Per-zone features (11):
            healthy_ratio, injured_ratio, critical_ratio, deceased_ratio,
            food_norm, water_norm, medical_norm, fuel_norm,
            road_access, hospital_load, has_medical_team
        """
        obs = []
        for zone in state["zones"]:
            pop = (
                zone["healthy"]
                + zone["injured"]
                + zone["critical"]
                + zone["deceased"]
            )
            pop = max(pop, 1)  # avoid division by zero

            obs.extend([
                zone["healthy"] / pop,
                zone["injured"] / pop,
                zone["critical"] / pop,
                zone["deceased"] / pop,
                min(zone["food"] / 1000.0, 1.0),
                min(zone["water"] / 1000.0, 1.0),
                min(zone["medical"] / 200.0, 1.0),
                min(zone["fuel"] / 500.0, 1.0),
                zone["road_access"],
                min(zone["critical"] / max(zone["hospital_capacity"], 1), 1.0),
                1.0 if "medical_team" in zone.get("teams_present", []) else 0.0,
            ])

        return np.array(obs, dtype=np.float32)

    # -------------------------------------------------------------- #
    #  Difficulty-based zone generation                                #
    # -------------------------------------------------------------- #

    def _create_zone_with_config(self, zone_id: int) -> dict[str, Any]:
        """Generate a zone using the difficulty-specific config."""
        rng = self._env._rng
        cfg = self._config

        pop = rng.randint(*cfg["population_range"])

        healthy_pct = rng.uniform(*cfg["healthy_pct"])
        injured_pct = rng.uniform(*cfg["injured_pct"])
        critical_pct = rng.uniform(*cfg["critical_pct"])
        deceased_pct = rng.uniform(*cfg["deceased_pct"])

        total_pct = healthy_pct + injured_pct + critical_pct + deceased_pct
        healthy_pct /= total_pct
        injured_pct /= total_pct
        critical_pct /= total_pct
        deceased_pct /= total_pct

        healthy = int(pop * healthy_pct)
        injured = int(pop * injured_pct)
        critical = int(pop * critical_pct)
        deceased = int(pop * deceased_pct)
        healthy += pop - (healthy + injured + critical + deceased)

        return {
            "id": zone_id,
            "healthy": healthy,
            "injured": injured,
            "critical": critical,
            "deceased": deceased,
            "food": rng.randint(*cfg["food_range"]),
            "water": rng.randint(*cfg["water_range"]),
            "medical": rng.randint(*cfg["medical_range"]),
            "fuel": rng.randint(*cfg["fuel_range"]),
            "road_access": round(rng.uniform(*cfg["road_range"]), 2),
            "hospital_capacity": rng.randint(*cfg["hospital_range"]),
            "teams_present": [],
        }

    # -------------------------------------------------------------- #
    #  Scoring (used by task graders)                                  #
    # -------------------------------------------------------------- #

    def compute_score(self) -> float:
        """
        Compute a task-dependent score in [0.0, 1.0].

        Components:
            survival_rate  — fraction of initial population still alive
            healed_bonus   — reward for total healed (capped)
            resource_eff   — remaining resources as proportion of initial

        The task difficulty scales the weights and thresholds.
        """
        state = self._env.get_state()
        survivors = sum(
            z["healthy"] + z["injured"] + z["critical"]
            for z in state["zones"]
        )
        survival_rate = survivors / max(self._initial_population, 1)

        # Resource efficiency — how many resources remain
        total_resources = sum(
            z["food"] + z["water"] + z["medical"] + z["fuel"]
            for z in state["zones"]
        )
        resource_score = min(total_resources / 3000.0, 1.0)

        # Health quality — proportion healthy among survivors
        total_healthy = sum(z["healthy"] for z in state["zones"])
        health_quality = total_healthy / max(survivors, 1)

        if self.task == "easy":
            score = survival_rate * 0.5 + health_quality * 0.3 + resource_score * 0.2
        elif self.task == "medium":
            score = survival_rate * 0.6 + health_quality * 0.25 + resource_score * 0.15
        else:  # hard
            score = survival_rate * 0.7 + health_quality * 0.2 + resource_score * 0.1

        return round(max(0.0, min(1.0, score)), 4)

    @property
    def raw_env(self) -> CrisisNetEnv:
        """Access the underlying CrisisNetEnv."""
        return self._env
