"""
CrisisNet Simulation Environment

Base simulation environment for disaster response scenarios.
Manages zones, populations, resources, and time progression.
"""

import random
from typing import Any


class CrisisNetEnv:
    """
    Base simulation environment for CrisisNet.

    Models a disaster-affected region divided into zones, each with
    population health states, resource levels, and infrastructure status.
    """

    def __init__(self, seed: int | None = None) -> None:
        self.zones: list[dict[str, Any]] = []
        self.time: int = 0
        self.max_time: int = 12
        self._rng = random.Random(seed)

    # ------------------------------------------------------------------ #
    #  Reset & Initialisation                                             #
    # ------------------------------------------------------------------ #

    def reset(self) -> dict[str, Any]:
        """
        Reset the environment to an initial state.

        Creates 5 disaster-affected zones with randomised but realistic
        population distributions and resource levels.

        Returns:
            The full simulation state after reset.
        """
        self.time = 0
        self.zones = [self._create_zone(zone_id) for zone_id in range(1, 6)]
        return self.get_state()

    def _create_zone(self, zone_id: int) -> dict[str, Any]:
        """Generate a single zone with realistic initial conditions."""

        population = self._rng.randint(800, 5000)

        # --- population health distribution (percentages) --- #
        healthy_pct = self._rng.uniform(0.50, 0.70)
        injured_pct = self._rng.uniform(0.20, 0.30)
        critical_pct = self._rng.uniform(0.05, 0.10)
        deceased_pct = self._rng.uniform(0.00, 0.02)

        # Normalise so that percentages sum to 1.0
        total_pct = healthy_pct + injured_pct + critical_pct + deceased_pct
        healthy_pct /= total_pct
        injured_pct /= total_pct
        critical_pct /= total_pct
        deceased_pct /= total_pct

        healthy = int(population * healthy_pct)
        injured = int(population * injured_pct)
        critical = int(population * critical_pct)
        deceased = int(population * deceased_pct)

        # Assign any rounding remainder to healthy
        healthy += population - (healthy + injured + critical + deceased)

        # --- resources (units) --- #
        food = self._rng.randint(100, 500)        # ration packs
        water = self._rng.randint(200, 800)        # litres
        medical = self._rng.randint(20, 150)       # medical kits
        fuel = self._rng.randint(50, 300)          # litres

        # --- infrastructure --- #
        road_access = self._rng.choice([True, False])
        hospital_capacity = self._rng.randint(10, 100) if road_access else self._rng.randint(0, 30)

        return {
            "id": zone_id,
            "healthy": healthy,
            "injured": injured,
            "critical": critical,
            "deceased": deceased,
            "food": food,
            "water": water,
            "medical": medical,
            "fuel": fuel,
            "road_access": road_access,
            "hospital_capacity": hospital_capacity,
            "teams_present": [],
        }

    # ------------------------------------------------------------------ #
    #  State Observation                                                   #
    # ------------------------------------------------------------------ #

    def get_state(self) -> dict[str, Any]:
        """
        Return the full simulation state as a dictionary.

        Returns:
            Dictionary containing the current time step, max time,
            and a deep copy of all zone data.
        """
        return {
            "time": self.time,
            "max_time": self.max_time,
            "zones": [zone.copy() for zone in self.zones],
        }
