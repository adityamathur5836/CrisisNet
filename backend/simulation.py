"""
CrisisNet Simulation Runner

Provides run_simulation() to execute a full experiment with any agent,
and compare_agents() to benchmark multiple agents side-by-side.
"""

from typing import Any

from backend.environment import CrisisNetEnv
from backend.agents import BaseAgent


# ------------------------------------------------------------------ #
#  Single Run                                                          #
# ------------------------------------------------------------------ #

def run_simulation(
    agent: BaseAgent,
    seed: int = 42,
    verbose: bool = False,
) -> dict[str, Any]:
    """
    Run a complete simulation episode with the given agent.

    Args:
        agent:   An agent instance implementing BaseAgent.decide().
        seed:    RNG seed for the environment (reproducibility).
        verbose: If True, print step-by-step details.

    Returns:
        A structured results dictionary:
        {
            "agent":            str,
            "seed":             int,
            "total_population": int,
            "total_survivors":  int,
            "total_deaths":     int,
            "survival_rate":    float,          # 0.0 – 1.0
            "total_healed":     int,
            "total_reward":     float,
            "reward_history":   list[float],    # reward per step
            "death_history":    list[int],       # deaths per step
            "healed_history":   list[int],       # healed per step
            "actions_taken":    dict[str, int],  # action type counts
            "final_state":      dict,            # env state at end
        }
    """
    env = CrisisNetEnv(seed=seed)
    state = env.reset()

    # Compute initial total population (across all zones)
    total_population = sum(
        z["healthy"] + z["injured"] + z["critical"] + z["deceased"]
        for z in state["zones"]
    )

    # Accumulators
    reward_history: list[float] = []
    death_history: list[int] = []
    healed_history: list[int] = []
    actions_taken: dict[str, int] = {}
    total_reward = 0.0
    total_healed = 0
    total_deaths = 0

    # --- main loop --- #
    done = False
    step = 0
    while not done:
        step += 1
        action = agent.decide(state)

        # Track action usage
        atype = action.get("type", "unknown")
        actions_taken[atype] = actions_taken.get(atype, 0) + 1

        state, reward, done = env.step(action)
        metrics = state["step_metrics"]

        step_deaths = (
            metrics["deaths"]
            + metrics["starvation_deaths"]
            + metrics["overload_deaths"]
        )

        total_reward += reward
        total_healed += metrics["healed"]
        total_deaths += step_deaths

        reward_history.append(reward)
        death_history.append(step_deaths)
        healed_history.append(metrics["healed"])

        if verbose:
            print(
                f"  t={step:2d}  "
                f"healed={metrics['healed']:4d}  "
                f"deaths={step_deaths:4d}  "
                f"reward={reward:9.0f}  "
                f"action={atype}"
            )

    # --- final tallies --- #
    total_survivors = sum(
        z["healthy"] + z["injured"] + z["critical"]
        for z in state["zones"]
    )

    survival_rate = total_survivors / total_population if total_population > 0 else 0.0

    return {
        "agent": agent.name,
        "seed": seed,
        "total_population": total_population,
        "total_survivors": total_survivors,
        "total_deaths": total_deaths,
        "survival_rate": round(survival_rate, 4),
        "total_healed": total_healed,
        "total_reward": round(total_reward, 2),
        "reward_history": reward_history,
        "death_history": death_history,
        "healed_history": healed_history,
        "actions_taken": dict(sorted(actions_taken.items())),
        "final_state": state,
    }


# ------------------------------------------------------------------ #
#  Multi-Agent Comparison                                              #
# ------------------------------------------------------------------ #

def compare_agents(
    agents: list[BaseAgent],
    seed: int = 42,
    verbose: bool = False,
) -> list[dict[str, Any]]:
    """
    Run simulations for multiple agents and return all results.

    Args:
        agents:  List of agent instances.
        seed:    Shared seed so all agents face the same scenario.
        verbose: Print step details for each agent.

    Returns:
        List of result dicts (one per agent), sorted by total_reward
        descending (best first).
    """
    results = []
    for agent in agents:
        if verbose:
            print(f"\n{'='*50}")
            print(f"  Running: {agent.name}")
            print(f"{'='*50}")

        result = run_simulation(agent, seed=seed, verbose=verbose)
        results.append(result)

    # Sort best reward first
    results.sort(key=lambda r: r["total_reward"], reverse=True)
    return results


def print_comparison(results: list[dict[str, Any]]) -> None:
    """Pretty-print a comparison table from compare_agents() output."""

    header = (
        f"{'Agent':<20s} {'Reward':>10s} {'Survivors':>10s} "
        f"{'Deaths':>8s} {'Healed':>8s} {'Survival%':>10s}"
    )
    print(header)
    print("-" * len(header))

    for r in results:
        print(
            f"{r['agent']:<20s} {r['total_reward']:>10.0f} "
            f"{r['total_survivors']:>10d} {r['total_deaths']:>8d} "
            f"{r['total_healed']:>8d} {r['survival_rate']*100:>9.1f}%"
        )


# ------------------------------------------------------------------ #
#  CLI entry point                                                     #
# ------------------------------------------------------------------ #

if __name__ == "__main__":
    from backend.agents import RandomAgent, HeuristicAgent, RLAgent

    agents = [RandomAgent(seed=99), HeuristicAgent(), RLAgent()]

    print("CrisisNet Simulation — Agent Comparison")
    print("=" * 50)

    results = compare_agents(agents, seed=42, verbose=False)
    print()
    print_comparison(results)

    print()
    for r in results:
        print(f"\n--- {r['agent']} ---")
        print(f"  Actions: {r['actions_taken']}")
        print(f"  Reward curve: {[int(x) for x in r['reward_history']]}")
