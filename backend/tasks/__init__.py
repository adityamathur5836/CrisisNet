"""
CrisisNet Task Graders

Three difficulty levels, each returning a score in [0.0, 1.0].
"""

from backend.tasks.easy import run as run_easy
from backend.tasks.medium import run as run_medium
from backend.tasks.hard import run as run_hard

TASKS = {
    "easy": run_easy,
    "medium": run_medium,
    "hard": run_hard,
}


def run_task(task_name: str, seed: int = 42) -> dict:
    """
    Run a specific task grader.

    Args:
        task_name: 'easy', 'medium', or 'hard'
        seed: RNG seed for reproducibility.

    Returns:
        dict with keys: task, score, survival_rate, total_reward, details
    """
    if task_name not in TASKS:
        raise ValueError(f"Unknown task '{task_name}'. Must be one of {list(TASKS.keys())}")
    return TASKS[task_name](seed=seed)
