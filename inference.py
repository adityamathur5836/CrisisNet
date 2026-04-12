"""
CrisisNet — OpenAI-Compatible Baseline Inference Script

Runs a language model against the CrisisNet environment.
Follows the OpenEnv standard logging format strictly.

MANDATORY VARIABLES:
  OPENAI_API_KEY (or HF_TOKEN, GROQ_API_KEY, GEMINI_API_KEY)

OPTIONAL VARIABLES:
  API_BASE_URL (defaults to OpenAI, overridden for other providers)
  MODEL_NAME   (defaults to gpt-4o-mini)
  ENV_URL      (defaults to http://localhost:7860)
"""

import os
import sys
import textwrap
import time
from typing import Optional

import requests

# ── Credentials & Configuration ────────────────────────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HF_TOKEN       = os.getenv("HF_TOKEN")
GROQ_API_KEY   = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

API_KEY = None
API_BASE_URL = None
MODEL_NAME = None

if OPENAI_API_KEY:
    API_KEY      = OPENAI_API_KEY
    API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
    MODEL_NAME   = os.getenv("MODEL_NAME", "gpt-4o-mini")
elif HF_TOKEN:
    API_KEY      = HF_TOKEN
    API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
    MODEL_NAME   = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
elif GROQ_API_KEY:
    API_KEY      = GROQ_API_KEY
    API_BASE_URL = os.getenv("API_BASE_URL", "https://api.groq.com/openai/v1")
    MODEL_NAME   = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
elif GEMINI_API_KEY:
    API_KEY      = GEMINI_API_KEY
    API_BASE_URL = os.getenv("API_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
    MODEL_NAME   = os.getenv("MODEL_NAME", "gemini-2.0-flash")

ENV_URL   = os.getenv("ENV_URL", "http://localhost:7860")
BENCHMARK = "crisisnet"

TASKS = ["easy", "medium", "hard"]

MAX_STEPS   = 12
TEMPERATURE = 0.0
MAX_TOKENS  = 10

ACTION_DESCRIPTIONS = textwrap.dedent("""
   0- 4  = Deploy medical team to zone 1-5
   5- 9  = Allocate food to zone 1-5
  10-14  = Allocate water to zone 1-5
  15-19  = Allocate medicine to zone 1-5
  20-24  = Repair roads in zone 1-5
""").strip()

SYSTEM_PROMPT = textwrap.dedent(f"""
You are an AI disaster response coordinator managing 5 crisis zones.
Your goal is to maximise survival rate by deploying resources strategically.
Respond with ONLY a single integer 0-24. Do not include explanations.

Available actions:
{ACTION_DESCRIPTIONS}
""").strip()


# ── OpenEnv Logging ────────────────────────────────────────────────
def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val  = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: list[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
        flush=True,
    )


# ── HTTP Environment Client ───────────────────────────────────────
def env_reset(task: str) -> dict:
    resp = requests.post(f"{ENV_URL}/reset", json={"task": task}, timeout=10)
    resp.raise_for_status()
    return resp.json()


def env_step(action_id: int) -> dict:
    resp = requests.post(f"{ENV_URL}/step", json={"action": action_id}, timeout=10)
    resp.raise_for_status()
    return resp.json()


def env_state() -> dict:
    resp = requests.get(f"{ENV_URL}/state", timeout=10)
    resp.raise_for_status()
    return resp.json()


# ── LLM Action Logic ──────────────────────────────────────────────
_LAST_API_CALL = 0.0


def get_action_llm(client, obs: dict, step: int) -> int:
    """Use an LLM to pick an action based on observation."""
    global _LAST_API_CALL

    elapsed = time.time() - _LAST_API_CALL
    if elapsed < 2.1:
        time.sleep(2.1 - elapsed)
    _LAST_API_CALL = time.time()

    # Extract key state info from observation values
    values = obs.get("values", [0] * 55)

    # Build a compact state summary for the LLM
    zone_summaries = []
    for i in range(5):
        offset = i * 11
        zone_summaries.append(
            f"Zone {i+1}: healthy={values[offset]:.2f} injured={values[offset+1]:.2f} "
            f"critical={values[offset+2]:.2f} food={values[offset+4]:.2f} "
            f"water={values[offset+5]:.2f} medical={values[offset+6]:.2f} "
            f"road={values[offset+8]:.2f} has_medteam={values[offset+10]:.0f}"
        )

    user_prompt = textwrap.dedent(f"""
    Step {step} — Current state:
    {chr(10).join(zone_summaries)}

    Choose action (0-24):
    """).strip()

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
        text = (completion.choices[0].message.content or "").strip()

        action_str = "".join(c for c in text.split()[0] if c.isdigit())
        if action_str:
            action_id = int(action_str)
            if 0 <= action_id <= 24:
                return action_id
        return 0  # Default to deploy_medical zone 1

    except Exception as e:
        print(f"[DEBUG] Model request failed: {e}", file=sys.stderr)
        return 0


def get_action_heuristic(obs: dict, step: int) -> int:
    """Simple heuristic fallback when no LLM API key is available."""
    values = obs.get("values", [0] * 55)

    # Phase 1: deploy medical to each zone (steps 1-5)
    if step <= 5:
        return step - 1  # actions 0-4 = deploy_medical zones 1-5

    # Phase 2: allocate food to zone with least food
    food_values = [values[i * 11 + 4] for i in range(5)]
    worst_food = food_values.index(min(food_values))
    return 5 + worst_food  # allocate_food to that zone


def run_episode_with_llm(client, task: str) -> None:
    """Run an episode using LLM for action selection."""
    log_start(task=task, env=BENCHMARK, model=MODEL_NAME or "heuristic")

    rewards: list[float] = []
    steps_taken = 0
    score = 0.0
    success = False

    try:
        result = env_reset(task)
        obs = result["observation"]
        done = result["done"]

        for step_num in range(1, MAX_STEPS + 1):
            if done:
                break

            if client:
                action_id = get_action_llm(client, obs, step_num)
            else:
                action_id = get_action_heuristic(obs, step_num)

            error = None
            try:
                result = env_step(action_id)
                obs = result["observation"]
                reward = float(result["reward"])
                done = result["done"]
            except Exception as env_exc:
                reward = 0.0
                done = True
                error = str(env_exc)

            rewards.append(reward)
            steps_taken = step_num
            log_step(step=step_num, action=str(action_id), reward=reward, done=done, error=error)

        state_info = env_state()
        score = float(state_info.get("current_score", 0.0))
        success = score > 0.4

    except Exception as main_exc:
        print(f"[DEBUG] Episode execution failed: {main_exc}", file=sys.stderr)

    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)


# ── Main ──────────────────────────────────────────────────────────
def main():
    client = None

    if API_KEY:
        try:
            from openai import OpenAI
            client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
            print(
                f"[*] Using LLM: {MODEL_NAME} via {API_BASE_URL}",
                file=sys.stderr,
            )
        except ImportError:
            print("[*] openai package not installed, using heuristic fallback", file=sys.stderr)
    else:
        print("[*] No API key found, using heuristic fallback", file=sys.stderr)

    for task in TASKS:
        run_episode_with_llm(client, task)


if __name__ == "__main__":
    main()
