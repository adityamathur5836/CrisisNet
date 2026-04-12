"""
CrisisNet Pydantic Models

Typed data models for the OpenEnv-compatible API.
Defines observation, action, state, and step-result schemas.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional


# ------------------------------------------------------------------ #
#  Observation                                                         #
# ------------------------------------------------------------------ #

class CrisisNetObservation(BaseModel):
    """
    55-dimensional normalised observation vector.

    Layout: 11 features × 5 zones (zone order 1..5).
    Per-zone features (all normalised to roughly 0.0–1.0):
        0  healthy_ratio        (healthy / population)
        1  injured_ratio        (injured / population)
        2  critical_ratio       (critical / population)
        3  deceased_ratio       (deceased / population)
        4  food_norm            (food / 1000)
        5  water_norm           (water / 1000)
        6  medical_norm         (medical / 200)
        7  fuel_norm            (fuel / 500)
        8  road_access          (already 0–1)
        9  hospital_load        (critical / max(hospital_capacity, 1))
        10 has_medical_team     (1.0 or 0.0)
    """

    values: list[float] = Field(
        min_length=55,
        max_length=55,
        description="Flat observation vector of length 55",
    )

    def to_list(self) -> list[float]:
        return list(self.values)


# ------------------------------------------------------------------ #
#  Action                                                              #
# ------------------------------------------------------------------ #

class CrisisNetAction(BaseModel):
    """
    Single discrete action in range [0, 24].

    Mapping:  action_id = action_type_index * 5 + (zone_id - 1)
        action_type_index:
            0 = deploy_medical
            1 = allocate_food
            2 = allocate_water
            3 = allocate_medicine
            4 = repair_road
        zone_id: 1..5  →  offset 0..4
    """

    action_id: int = Field(ge=0, le=24)


# ------------------------------------------------------------------ #
#  State                                                               #
# ------------------------------------------------------------------ #

class CrisisNetState(BaseModel):
    """Episode metadata returned by the /state endpoint."""

    episode_id: str = ""
    task: str = "easy"
    tick: int = 0
    max_ticks: int = 12
    total_population: int = 0
    total_survivors: int = 0
    total_deaths: int = 0
    survival_rate: float = 0.0
    current_score: float = 0.0
    cumulative_reward: float = 0.0


# ------------------------------------------------------------------ #
#  Step Result                                                         #
# ------------------------------------------------------------------ #

class StepResult(BaseModel):
    """Value returned by /step."""

    observation: CrisisNetObservation
    reward: float
    done: bool
    info: dict = {}


# ------------------------------------------------------------------ #
#  Reset Request                                                       #
# ------------------------------------------------------------------ #

class ResetRequest(BaseModel):
    task: Optional[str] = "easy"
    seed: Optional[int] = None


class StepRequest(BaseModel):
    action: Optional[int] = None
    action_id: Optional[int] = None
