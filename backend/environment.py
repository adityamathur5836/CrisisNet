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
        # road_access is a float 0.0–1.0 (1.0 = fully operational)
        road_access = round(self._rng.uniform(0.4, 1.0), 2)
        hospital_capacity = self._rng.randint(10, 100)

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
    #  Simulation Step                                                     #
    # ------------------------------------------------------------------ #

    # Road access threshold below which delivery efficiency drops
    ROAD_DEGRADATION_RATE: float = 0.05
    ROAD_EFFICIENCY_THRESHOLD: float = 0.5

    def step(self, action: dict[str, Any]) -> tuple[dict[str, Any], float, bool]:
        """
        Advance the simulation by one time step.

        Each tick applies five systems in order:
            1. Action processing      – apply the agent's chosen action.
            2. Infrastructure decay   – road_access degrades.
            3. Resource consumption    – food & water deplete (scaled by roads).
            4. Resource / infra effects – starvation, shortages, overload.
            5. Population dynamics     – health transitions.

        Infrastructure effects:
            - road_access decreases by ROAD_DEGRADATION_RATE each tick.
            - road_access < 0.5 → resource deliveries are less efficient.
            - hospital overloaded (critical > capacity) → +15% death rate.

        Args:
            action: An action dictionary (validated externally).

        Returns:
            A tuple of (state, reward, done):
                state  – the new environment state.
                reward – weighted score:
                         +20 per heal, −50 per death,
                         −30 per starvation death,
                         −10 per depletion event,
                         −15 per hospital overload event.
                done   – True if time has reached max_time.
        """
        self.time += 1

        # 1. Process action (currently only repair_road)
        self._apply_action(action)

        total_healed = 0
        total_deaths = 0
        total_starvation_deaths = 0
        total_depletion_events = 0
        total_overload_deaths = 0

        for zone in self.zones:
            # 2. Infrastructure decay
            self._tick_infrastructure(zone)

            # 3. Consume resources (scaled by road access)
            self._tick_resources(zone)

            # 4a. Resource-shortage effects
            starvation, depletions = self._tick_resource_effects(zone)
            total_starvation_deaths += starvation
            total_depletion_events += depletions

            # 4b. Hospital overload
            overload_deaths = self._tick_hospital_overload(zone)
            total_overload_deaths += overload_deaths

            # 5. Population dynamics
            has_medical = "medical_team" in zone["teams_present"]
            healed, deaths = self._tick_health(zone, has_medical)
            total_healed += healed
            total_deaths += deaths

        # --- detailed reward --- #
        reward = (
            (20.0 * total_healed)
            + (-50.0 * total_deaths)
            + (-30.0 * total_starvation_deaths)
            + (-10.0 * total_depletion_events)
            + (-15.0 * total_overload_deaths)
        )

        done = self.time >= self.max_time
        state = self.get_state()

        # Attach step metrics to state for observability
        state["step_metrics"] = {
            "healed": total_healed,
            "deaths": total_deaths,
            "starvation_deaths": total_starvation_deaths,
            "overload_deaths": total_overload_deaths,
            "depletion_events": total_depletion_events,
            "reward": reward,
        }

        return state, reward, done

    # ------------------------------------------------------------------ #
    #  Action Processing                                                   #
    # ------------------------------------------------------------------ #

    def _apply_action(self, action: dict[str, Any]) -> None:
        """Process a single agent action."""
        action_type = action.get("type")

        if action_type == "repair_road":
            zone = self._get_zone(action.get("zone"))
            if zone is not None:
                # Repair restores 0.20 road access, capped at 1.0
                zone["road_access"] = min(1.0, round(zone["road_access"] + 0.20, 2))

        # Other action types will be handled here in future expansions.

    def _get_zone(self, zone_id: int | None) -> dict[str, Any] | None:
        """Look up a zone by id. Returns None if not found."""
        if zone_id is None:
            return None
        for zone in self.zones:
            if zone["id"] == zone_id:
                return zone
        return None

    # ------------------------------------------------------------------ #
    #  Infrastructure                                                      #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _tick_infrastructure(zone: dict[str, Any]) -> None:
        """
        Degrade infrastructure each tick.

        road_access decreases by ROAD_DEGRADATION_RATE (0.05) per step,
        floored at 0.0.
        """
        zone["road_access"] = max(0.0, round(zone["road_access"] - 0.05, 2))

    @staticmethod
    def _tick_hospital_overload(zone: dict[str, Any]) -> int:
        """
        Check for hospital overload.

        If critical patients exceed hospital_capacity, the excess
        face an additional 15% death rate.

        Returns:
            Number of additional deaths from overload.
        """
        overflow = zone["critical"] - zone["hospital_capacity"]
        if overflow <= 0:
            return 0

        overload_dead = int(overflow * 0.15)
        zone["critical"] -= overload_dead
        zone["deceased"] += overload_dead
        return overload_dead

    @staticmethod
    def _tick_resources(zone: dict[str, Any]) -> None:
        """
        Consume resources for one time step.

        Consumption is proportional to the living population.
        If road_access < ROAD_EFFICIENCY_THRESHOLD (0.5), incoming
        supply delivery is reduced — modelled as increased effective
        consumption (supplies spoil / get lost in transit).

        Base rates:
            food  – 1 ration per 10 people
            water – 2 litres per 10 people
            fuel  – flat 5 units
        """
        living = zone["healthy"] + zone["injured"] + zone["critical"]

        # Delivery penalty: poor roads → up to 2× consumption
        road = zone["road_access"]
        if road < 0.5:
            # Linear scale: road=0 → 2x, road=0.5 → 1x
            delivery_penalty = 1.0 + (0.5 - road) * 2.0
        else:
            delivery_penalty = 1.0

        food_consumed = int(max(1, living // 10) * delivery_penalty)
        water_consumed = int(max(1, living // 5) * delivery_penalty)
        fuel_consumed = int(5 * delivery_penalty)

        zone["food"] = max(0, zone["food"] - food_consumed)
        zone["water"] = max(0, zone["water"] - water_consumed)
        zone["fuel"] = max(0, zone["fuel"] - fuel_consumed)

    @staticmethod
    def _tick_resource_effects(zone: dict[str, Any]) -> tuple[int, int]:
        """
        Apply consequences of resource shortages.

        Effects:
            food = 0    → 5% of healthy die (starvation)
            medical = 0 → 15% of injured become critical (no supplies)

        Returns:
            (starvation_deaths, depletion_events) for this zone.
        """
        starvation_deaths = 0
        depletion_events = 0

        # --- starvation (no food) --- #
        if zone["food"] == 0:
            starved = int(zone["healthy"] * 0.05)
            zone["healthy"] -= starved
            zone["deceased"] += starved
            starvation_deaths += starved
            depletion_events += 1

        # --- no water worsens injuries --- #
        if zone["water"] == 0:
            dehydrated = int(zone["injured"] * 0.10)
            zone["injured"] -= dehydrated
            zone["critical"] += dehydrated
            depletion_events += 1

        # --- no medical supplies --- #
        if zone["medical"] == 0:
            worsened = int(zone["injured"] * 0.15)
            zone["injured"] -= worsened
            zone["critical"] += worsened
            depletion_events += 1

        return starvation_deaths, depletion_events

    @staticmethod
    def _tick_health(zone: dict[str, Any], has_medical: bool) -> tuple[int, int]:
        """
        Apply one tick of population dynamics to a zone.

        Args:
            zone:        The zone dictionary (mutated in place).
            has_medical: Whether a medical team is present.

        Returns:
            (healed, deaths) counts for this tick.
        """
        healed = 0
        deaths = 0

        if has_medical:
            # --- WITH medical team --- #

            # critical → deceased (reduced: 10%)
            new_deceased = int(zone["critical"] * 0.10)
            zone["critical"] -= new_deceased
            zone["deceased"] += new_deceased
            deaths += new_deceased

            # critical → injured (stabilisation: 60% of remaining)
            stabilised = int(zone["critical"] * 0.60)
            zone["critical"] -= stabilised
            zone["injured"] += stabilised

            # injured → healthy (healing: 40%)
            new_healthy = int(zone["injured"] * 0.40)
            zone["injured"] -= new_healthy
            zone["healthy"] += new_healthy
            healed += new_healthy

        else:
            # --- WITHOUT medical team --- #

            # critical → deceased (30%)
            new_deceased = int(zone["critical"] * 0.30)
            zone["critical"] -= new_deceased
            zone["deceased"] += new_deceased
            deaths += new_deceased

            # injured → critical (20%)
            new_critical = int(zone["injured"] * 0.20)
            zone["injured"] -= new_critical
            zone["critical"] += new_critical

        return healed, deaths

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
