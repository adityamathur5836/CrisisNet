"""
CrisisNet API Bridge

Provides a REST API to interact with the CrisisNet simulation backend.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

from backend.environment import CrisisNetEnv
from backend.simulation import run_simulation, compare_agents
from backend.agents import RandomAgent, HeuristicAgent, RLAgent

# Map agent names to their classes
AVAILABLE_AGENTS = {
    "RandomAgent": RandomAgent,
    "HeuristicAgent": HeuristicAgent,
    "RLAgent": RLAgent,
}

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global simulation instance for step-by-step UI
env = CrisisNetEnv(seed=42)
env.reset()

# Configure simple logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CrisisNetAPI")


@app.route("/state", methods=["GET"])
def get_state():
    """Return the current state of the global simulation environment."""
    try:
        state = env.get_state()
        return jsonify(state), 200
    except Exception as e:
        logger.error(f"Error in /state: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/step", methods=["POST"])
def step_simulation():
    """
    Advance the simulation by one step.
    Expects JSON either with an action: {"type": "repair_road", "zone": 1, "amount": 100}
    Or an agent string to auto-generate: {"agent": "HeuristicAgent"}
    """
    try:
        action = request.json or {}
        
        # If an agent name is provided instead of a raw action type, use that agent to decide.
        if "agent" in action:
            agent_name = action["agent"]
            if agent_name in AVAILABLE_AGENTS:
                agent_instance = AVAILABLE_AGENTS[agent_name]()
                action = agent_instance.decide(env.get_state())
            else:
                return jsonify({"error": f"Invalid agent '{agent_name}'"}), 400
        elif not action or "type" not in action:
            return jsonify({"error": "Invalid action format. 'type' or 'agent' is required."}), 400

        # Optional: Prevent stepping past max_time
        if env.time >= env.max_time:
            return jsonify({
                "message": "Simulation has already concluded.",
                "state": env.get_state(),
                "done": True
            }), 200

        state, reward, done = env.step(action)
        return jsonify({
            "state": state,
            "reward": reward,
            "done": done
        }), 200
    except Exception as e:
        logger.error(f"Error in /step: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/run_agent", methods=["POST"])
def run_agent_endpoint():
    """
    Run a full simulation (0 to max_time) using a specific agent.
    Expects JSON: {"agent": "HeuristicAgent", "seed": 42}
    """
    try:
        data = request.json or {}
        agent_name = data.get("agent")
        if not agent_name or agent_name not in AVAILABLE_AGENTS:
            return jsonify({"error": f"Valid 'agent' required. Options: {list(AVAILABLE_AGENTS.keys())}"}), 400

        seed = data.get("seed", 42)
        AgentClass = AVAILABLE_AGENTS[agent_name]
        agent_instance = AgentClass()
        
        # We pass the seed to RandomAgent if that's the one selected
        if agent_name == "RandomAgent":
            agent_instance = AgentClass(seed=seed)

        result = run_simulation(agent_instance, seed=seed)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error in /run_agent: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/compare_agents", methods=["GET"])
def compare_agents_endpoint():
    """
    Run all available agents and return a benchmarking comparison.
    Optional query param: ?seed=42
    """
    try:
        seed = request.args.get("seed", 42, type=int)
        
        agents_to_run = [
            RandomAgent(seed=seed),
            HeuristicAgent(),
            RLAgent()
        ]
        
        results = compare_agents(agents_to_run, seed=seed, verbose=False)
        return jsonify(results), 200
    except Exception as e:
        logger.error(f"Error in /compare_agents: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/zone/<int:zone_id>", methods=["GET"])
def get_zone(zone_id):
    """
    Retrieve the current status of a specific zone by ID.
    """
    try:
        state = env.get_state()
        zones = state.get("zones", [])
        
        for zone in zones:
            if zone["id"] == zone_id:
                return jsonify(zone), 200
                
        return jsonify({"error": f"Zone {zone_id} not found."}), 404
    except Exception as e:
        logger.error(f"Error in /zone/{zone_id}: {e}")
        return jsonify({"error": str(e)}), 500


# Utility endpoint to completely reset the global simulation
@app.route("/reset", methods=["POST"])
def reset_simulation():
    """Reset the global simulation to time=0."""
    try:
        data = request.json or {}
        seed = data.get("seed", 42)
        # We recreate the env entirely to ensure fresh RNG based on seed
        global env
        env = CrisisNetEnv(seed=seed)
        state = env.reset()
        return jsonify({"message": "Simulation reset.", "state": state}), 200
    except Exception as e:
        logger.error(f"Error in /reset: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
