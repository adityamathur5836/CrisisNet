"""
CrisisNet OpenEnv-Compatible FastAPI Server

Provides the standard OpenEnv API:
    POST /reset   — reset environment with optional task param
    POST /step    — take a discrete action (0–24)
    GET  /state   — return current episode metadata
    GET  /health  — health check
    GET  /metadata — environment metadata
    GET  /schema  — Pydantic model schemas
    POST /mcp     — MCP protocol endpoint

This server runs on port 7860 for HuggingFace Spaces
compatibility and OpenEnv standard compliance.
"""

import sys
import os
import uuid

# Ensure project root is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request

from backend.gym_env import CrisisNetGymEnv, OBS_DIM, NUM_ACTIONS
from backend.models import (
    CrisisNetObservation,
    CrisisNetState,
    ResetRequest,
    StepRequest,
)
from backend.tasks import run_task

# ------------------------------------------------------------------ #
#  App                                                                 #
# ------------------------------------------------------------------ #

app = FastAPI(
    title="CrisisNet",
    description="RL environment for disaster response simulation",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global environment instance
env = CrisisNetGymEnv(task="medium", seed=42)
_episode_id = ""
_current_task = "medium"
_cumulative_reward = 0.0
_obs = None


# ------------------------------------------------------------------ #
#  Endpoints                                                           #
# ------------------------------------------------------------------ #

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/reset")
def reset(req: ResetRequest = None):
    """
    Reset the environment.

    Accepts optional task ('easy', 'medium', 'hard') and seed.
    Returns initial observation.
    """
    global env, _episode_id, _current_task, _cumulative_reward, _obs

    task = (req.task if req and req.task else "medium")
    seed = (req.seed if req and req.seed is not None else 42)

    if task not in ("easy", "medium", "hard"):
        raise HTTPException(status_code=400, detail=f"Unknown task: {task}")

    _current_task = task
    _episode_id = str(uuid.uuid4())[:8]
    _cumulative_reward = 0.0

    env = CrisisNetGymEnv(task=task, seed=seed)
    obs, info = env.reset()
    _obs = obs

    return {
        "observation": CrisisNetObservation(values=obs.tolist()).model_dump(),
        "reward": 0.0,
        "done": False,
        "info": {"task": task, "episode_id": _episode_id},
    }


@app.post("/step")
def step(req: StepRequest):
    """
    Take a single step in the environment.

    Accepts a discrete action (0–24).
    Returns observation, reward, done, info.
    """
    global _cumulative_reward, _obs

    action = req.action if req.action is not None else req.action_id
    if action is None or not (0 <= action < NUM_ACTIONS):
        raise HTTPException(
            status_code=400,
            detail=f"action must be 0-{NUM_ACTIONS - 1}, got {action}",
        )

    obs, reward, done, truncated, info = env.step(action)
    _cumulative_reward += reward
    _obs = obs

    return {
        "observation": CrisisNetObservation(values=obs.tolist()).model_dump(),
        "reward": reward,
        "done": done,
        "info": {
            "time": info.get("time", 0),
            "action_dict": info.get("action_dict", {}),
            "cumulative_reward": _cumulative_reward,
        },
    }


@app.get("/state")
def state():
    """Return current episode metadata and score."""
    raw_state = env.raw_env.get_state()

    survivors = sum(
        z["healthy"] + z["injured"] + z["critical"]
        for z in raw_state["zones"]
    )
    total_pop = env._initial_population or 1
    deaths = sum(z["deceased"] for z in raw_state["zones"])

    score = env.compute_score()

    return CrisisNetState(
        episode_id=_episode_id,
        task=_current_task,
        tick=raw_state["time"],
        max_ticks=raw_state["max_time"],
        total_population=total_pop,
        total_survivors=survivors,
        total_deaths=deaths,
        survival_rate=round(survivors / total_pop, 4),
        current_score=score,
        cumulative_reward=round(_cumulative_reward, 2),
    ).model_dump()


@app.get("/metadata")
def metadata():
    """Environment metadata for OpenEnv discovery."""
    return {
        "name": "crisisnet",
        "description": (
            "RL environment for disaster response simulation. "
            "Agent manages 5 crisis zones to maximise survival over 12 time steps."
        ),
        "tasks": ["easy", "medium", "hard"],
        "version": "1.0.0",
        "observation_space": {"type": "array", "shape": [OBS_DIM], "dtype": "float32"},
        "action_space": {"type": "discrete", "n": NUM_ACTIONS},
        "reward_range": [-500.0, 200.0],
    }


@app.get("/schema")
def schema():
    """Return JSON schemas for action, observation, and state."""
    from backend.models import CrisisNetAction, CrisisNetObservation, CrisisNetState
    return {
        "action": CrisisNetAction.model_json_schema(),
        "observation": CrisisNetObservation.model_json_schema(),
        "state": CrisisNetState.model_json_schema(),
    }


@app.post("/mcp")
async def mcp(request: Request):
    """MCP (Model Context Protocol) endpoint."""
    body = {}
    try:
        body = await request.json()
    except Exception:
        pass
    req_id = body.get("id") if isinstance(body, dict) else None
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "result": {
            "name": "crisisnet",
            "description": "AI Disaster Response Simulator",
            "capabilities": {"reset": True, "step": True, "state": True},
        },
    }


@app.get("/grade/{task_name}")
def grade(task_name: str, seed: int = 42):
    """
    Run a task grader and return the score.

    Args:
        task_name: 'easy', 'medium', or 'hard'
        seed: RNG seed (query param, default 42)
    """
    if task_name not in ("easy", "medium", "hard"):
        raise HTTPException(status_code=400, detail=f"Unknown task: {task_name}")

    result = run_task(task_name, seed=seed)
    return result


@app.get("/dashboard")
def dashboard():
    """Dashboard state for external integrations."""
    raw_state = env.raw_env.get_state()
    return {
        "state": raw_state,
        "score": env.compute_score(),
        "cumulative_reward": round(_cumulative_reward, 2),
    }


# ------------------------------------------------------------------ #
#  Main                                                                #
# ------------------------------------------------------------------ #

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860, reload=False)


if __name__ == "__main__":
    main()
