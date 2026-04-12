"""
Hard Task Grader

Severe disaster scenario — scarce resources, high casualties, damaged
infrastructure.  Only an optimised policy can score > 0.5.
"""

from backend.gym_env import CrisisNetGymEnv


def run(seed: int = 42) -> dict:
    """
    Run the hard task and return a score in [0.0, 1.0].

    Scenario:
        - Scarce initial resources
        - High critical patient count
        - Severely damaged roads
        - Large populations under stress
        - Low hospital capacity

    Scoring (harsh):
        survival_rate × 0.7 + health_quality × 0.2 + resource_eff × 0.1
    """
    env = CrisisNetGymEnv(task="hard", seed=seed)
    obs, info = env.reset()

    total_reward = 0.0
    done = False

    while not done:
        time = env.raw_env.time
        if time < 5:
            action = 0 * 5 + time  # deploy_medical to zone (time+1)
        elif time < 7:
            action = 3 * 5 + ((time - 5) % 5)  # allocate medicine
        elif time < 10:
            action = 1 * 5 + ((time - 7) % 5)  # allocate food
        else:
            action = 4 * 5 + ((time - 10) % 5)  # repair road

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
        "task": "hard",
        "score": score,
        "survival_rate": round(survival_rate, 4),
        "total_reward": round(total_reward, 2),
        "details": {
            "initial_population": initial_pop,
            "survivors": survivors,
            "ticks": state["time"],
        },
    }
