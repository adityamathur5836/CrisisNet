"""
Easy Task Grader

Mild disaster scenario with abundant resources and low casualties.
A basic agent should score ≥ 0.6 easily.
"""

from backend.gym_env import CrisisNetGymEnv


def run(seed: int = 42) -> dict:
    """
    Run the easy task and return a score in [0.0, 1.0].

    Scenario:
        - High initial resources (food, water, medicine)
        - Low critical patient count
        - Good road infrastructure
        - Small populations per zone

    Scoring (lenient):
        survival_rate × 0.5 + health_quality × 0.3 + resource_eff × 0.2
    """
    env = CrisisNetGymEnv(task="easy", seed=seed)
    obs, info = env.reset()

    total_reward = 0.0
    done = False

    while not done:
        # Use a simple heuristic for grading: deploy medical to each zone in order
        time = env.raw_env.time
        if time < 5:
            action = 0 * 5 + time  # deploy_medical to zone (time+1)
        else:
            # Then allocate food to the zone with index (time-5) mod 5
            action = 1 * 5 + ((time - 5) % 5)

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
        "task": "easy",
        "score": score,
        "survival_rate": round(survival_rate, 4),
        "total_reward": round(total_reward, 2),
        "details": {
            "initial_population": initial_pop,
            "survivors": survivors,
            "ticks": state["time"],
        },
    }
