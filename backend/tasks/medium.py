"""
Medium Task Grader

Balanced disaster scenario — requires thoughtful resource allocation.
A heuristic agent should score ~0.5; an optimised agent can reach ~0.7.
"""

from backend.gym_env import CrisisNetGymEnv


def run(seed: int = 42) -> dict:
    """
    Run the medium task and return a score in [0.0, 1.0].

    Scenario:
        - Standard initial resources (matches original environment)
        - Moderate critical patients
        - Moderate road infrastructure
        - Standard populations per zone

    Scoring (balanced):
        survival_rate × 0.6 + health_quality × 0.25 + resource_eff × 0.15
    """
    env = CrisisNetGymEnv(task="medium", seed=seed)
    obs, info = env.reset()

    total_reward = 0.0
    done = False

    while not done:
        time = env.raw_env.time
        if time < 5:
            action = 0 * 5 + time  # deploy_medical to zone (time+1)
        elif time < 8:
            action = 1 * 5 + ((time - 5) % 5)  # allocate food
        elif time < 11:
            action = 2 * 5 + ((time - 8) % 5)  # allocate water
        else:
            action = 4 * 5 + 0  # repair road zone 1

        obs, reward, done, truncated, step_info = env.step(action)
        total_reward += reward

    score = env.compute_score()

    state = env.raw_env.get_state()
    survivors = sum(
        z["healthy"] + z["injured"] + z["critical"]
        for z in state["zones"]
    )
    initial_pop = env._initial_population
    survival_rate = survivors / max(initial_pop, 1)

    return {
        "task": "medium",
        "score": score,
        "survival_rate": round(survival_rate, 4),
        "total_reward": round(total_reward, 2),
        "details": {
            "initial_population": initial_pop,
            "survivors": survivors,
            "ticks": state["time"],
        },
    }
