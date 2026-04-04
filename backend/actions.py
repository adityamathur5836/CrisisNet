"""
CrisisNet Action Definitions

Defines the action schema, supported action types, and validation
utilities for the simulation. No execution logic lives here — only
structure and validation.
"""

from typing import Any


# ------------------------------------------------------------------ #
#  Supported Action Types                                             #
# ------------------------------------------------------------------ #

ACTION_TYPES: list[str] = [
    "deploy_medical",       # Deploy a medical team to a zone
    "deploy_rescue",        # Deploy a search-and-rescue team to a zone
    "deploy_engineering",   # Deploy an engineering team to a zone
    "allocate_food",        # Send food rations to a zone
    "allocate_water",       # Send water supply to a zone
    "allocate_medicine",    # Send medical supplies to a zone
    "repair_road",          # Begin road repair in a zone
    "evacuate",             # Evacuate population from a zone
    "establish_comms",      # Set up communications in a zone
    "do_nothing",           # Skip this time step (no-op)
]

# Actions that require an amount parameter
_AMOUNT_REQUIRED: set[str] = {
    "allocate_food",
    "allocate_water",
    "allocate_medicine",
}

# Actions that require a target zone
_ZONE_REQUIRED: set[str] = {
    "deploy_medical",
    "deploy_rescue",
    "deploy_engineering",
    "allocate_food",
    "allocate_water",
    "allocate_medicine",
    "repair_road",
    "evacuate",
    "establish_comms",
}


# ------------------------------------------------------------------ #
#  Action Schema                                                      #
# ------------------------------------------------------------------ #

def make_action(
    action_type: str,
    zone: int | None = None,
    amount: float | None = None,
) -> dict[str, Any]:
    """
    Build a well-formed action dictionary.

    Args:
        action_type: One of the values in ACTION_TYPES.
        zone:        Target zone id (required for most actions).
        amount:      Quantity for resource-allocation actions.

    Returns:
        Action dictionary with keys: type, zone, amount.
    """
    return {
        "type": action_type,
        "zone": zone,
        "amount": amount,
    }


# ------------------------------------------------------------------ #
#  Validation                                                         #
# ------------------------------------------------------------------ #

def validate_action(action: dict[str, Any], env_state: dict[str, Any]) -> tuple[bool, str]:
    """
    Validate an action against the current environment state.

    Checks:
        1. action is a dict with the required 'type' key.
        2. action type is one of the supported ACTION_TYPES.
        3. zone is provided and valid when required.
        4. amount is provided and positive when required.

    Args:
        action:    The action dictionary to validate.
        env_state: The current simulation state (from env.get_state()).

    Returns:
        A tuple of (is_valid, message).
        - (True, "ok") if the action passes all checks.
        - (False, "<reason>") otherwise.
    """
    # --- basic structure --- #
    if not isinstance(action, dict):
        return False, "Action must be a dictionary."

    action_type = action.get("type")
    if action_type is None:
        return False, "Action must include a 'type' key."

    if action_type not in ACTION_TYPES:
        return False, f"Unknown action type '{action_type}'. Must be one of {ACTION_TYPES}."

    # --- do_nothing needs no further checks --- #
    if action_type == "do_nothing":
        return True, "ok"

    # --- zone validation --- #
    zone_id = action.get("zone")

    if action_type in _ZONE_REQUIRED:
        if zone_id is None:
            return False, f"Action '{action_type}' requires a 'zone' parameter."

        valid_zone_ids = {z["id"] for z in env_state.get("zones", [])}
        if zone_id not in valid_zone_ids:
            return False, f"Zone {zone_id} does not exist. Valid zones: {sorted(valid_zone_ids)}."

    # --- amount validation --- #
    amount = action.get("amount")

    if action_type in _AMOUNT_REQUIRED:
        if amount is None:
            return False, f"Action '{action_type}' requires an 'amount' parameter."
        if not isinstance(amount, (int, float)) or amount <= 0:
            return False, f"'amount' must be a positive number, got {amount}."

    return True, "ok"
