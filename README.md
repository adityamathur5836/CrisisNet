# CrisisNet — AI Disaster Response Simulator

> *A multi-agent reinforcement learning environment for disaster response management, built as an OpenEnv-compatible simulation with real RL training, benchmarking, and deployment support.*

---

## 🏗 Overview

CrisisNet models a disaster-affected region divided into **5 crisis zones**, each with:

- **Population health states:** healthy, injured, critical, deceased
- **Resource levels:** food, water, medical supplies, fuel
- **Infrastructure:** road access (0–1), hospital capacity

An AI agent observes the full state and takes **1 action per time step** over **12 ticks** to maximise survival and minimise deaths.

### Actions (5 types × 5 zones = 25 discrete actions)

| Action | Effect |
|--------|--------|
| `deploy_medical(zone)` | Deploys a permanent medical team — reduces death rate, heals injured |
| `allocate_food(zone)` | Sends food rations to prevent starvation |
| `allocate_water(zone)` | Sends water to prevent dehydration |
| `allocate_medicine(zone)` | Sends medical kits to prevent injury escalation |
| `repair_road(zone)` | Repairs road access by +0.20 (improves supply delivery) |

### Environment Dynamics

- **Infrastructure decay:** Roads degrade by 0.05 per tick
- **Resource consumption:** Scales with population and road quality
- **Starvation:** Food = 0 → 5% healthy die per tick
- **Dehydration:** Water = 0 → 10% injured become critical
- **Medical shortage:** Medical = 0 → 15% injured become critical
- **Hospital overload:** Critical > capacity → 15% excess die
- **Medical team (present):** 10% critical die, 60% stabilise, 40% injured heal
- **No medical team:** 30% critical die, 20% injured escalate

### Reward Function

```
reward = (+20 × healed) + (−50 × deaths) + (−30 × starvation_deaths)
       + (−10 × depletion_events) + (−15 × hospital_overload_deaths)
```

---

## 🤖 Agents

| Agent | Strategy | Type |
|-------|----------|------|
| **RandomAgent** | Random action with 50% idle probability | Baseline (lower bound) |
| **HeuristicAgent** | Fixed-priority rules: critical → food → water → roads | Rule-based |
| **OptimalAgent** | Hand-crafted optimal policy exploiting env mechanics | Expert heuristic |
| **RLAgent** | Stable-Baselines3 DQN with action safety layer | Reinforcement learning |

### RL Agent Details

The RL agent uses **DQN (Deep Q-Network)** from Stable-Baselines3:

- **Architecture:** MLP with 2 hidden layers (128, 128)
- **Observation:** 55-dimensional normalised vector (11 features × 5 zones)
- **Action space:** Discrete(25) — 5 action types × 5 zones
- **Action safety layer:** Q-value ranked selection filtering wasteful actions
- **Dynamic allocation:** Resource amounts scaled by population, consumption rate, remaining time
- **Fallback:** If no trained model or all actions wasteful → OptimalAgent

---

## 📋 Tasks & Grading

Three difficulty levels, each returning a score in [0.0, 1.0]:

| Task | Description | Scoring Weights |
|------|-------------|-----------------|
| **Easy** | Mild disaster, abundant resources | 50% survival + 30% health + 20% resources |
| **Medium** | Balanced scenario (default environment) | 60% survival + 25% health + 15% resources |
| **Hard** | Severe disaster, scarce resources, damaged roads | 70% survival + 20% health + 10% resources |

---

## 🌐 OpenEnv API

CrisisNet provides an OpenEnv-compatible REST API via FastAPI (port 7860):

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/reset` | POST | Reset environment. Body: `{"task": "easy", "seed": 42}` |
| `/step` | POST | Take action. Body: `{"action": 0}` (0–24) |
| `/state` | GET | Current episode metadata + score |
| `/health` | GET | Health check |
| `/metadata` | GET | Environment metadata |
| `/schema` | GET | JSON schemas for action/observation/state |
| `/grade/{task}` | GET | Run task grader. Returns score (0–1) |
| `/mcp` | POST | MCP protocol endpoint |

### Observation Vector (55 dimensions)

11 features per zone × 5 zones:

```
[healthy_ratio, injured_ratio, critical_ratio, deceased_ratio,
 food_norm, water_norm, medical_norm, fuel_norm,
 road_access, hospital_load, has_medical_team] × 5 zones
```

### Action Mapping (Discrete 0–24)

```
 0- 4  = deploy_medical to zone 1-5
 5- 9  = allocate_food to zone 1-5
10-14  = allocate_water to zone 1-5
15-19  = allocate_medicine to zone 1-5
20-24  = repair_road in zone 1-5
```

---

## 📁 Project Structure

```
CrisisNet/
├── backend/
│   ├── environment.py     # Core simulation engine
│   ├── gym_env.py         # Gymnasium wrapper for SB3
│   ├── agents.py          # All agents (Random, Heuristic, Optimal, RL)
│   ├── actions.py         # Action schema and validation
│   ├── simulation.py      # Benchmark runner and comparison
│   ├── models.py          # Pydantic data models
│   ├── app.py             # Flask REST API
│   └── tasks/
│       ├── __init__.py    # Task dispatcher
│       ├── easy.py        # Easy task grader
│       ├── medium.py      # Medium task grader
│       └── hard.py        # Hard task grader
├── server/
│   └── app.py             # FastAPI OpenEnv server (port 7860)
├── train_rl.py            # DQN training script
├── inference.py           # OpenEnv inference script
├── openenv.yaml           # OpenEnv metadata
├── Dockerfile             # HuggingFace Spaces deployment
├── validate-submission.sh # Submission validator
├── requirements.txt       # Python dependencies
└── README.md
```

---

## 🚀 Setup & Usage

### Prerequisites

- Python 3.10+

### 1. Install Dependencies

```bash
cd CrisisNet
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run OpenEnv Server (primary)

```bash
PYTHONPATH=./ uvicorn server.app:app --host 0.0.0.0 --port 7860
```

### 3. Run Flask API (optional, for debugging)

```bash
PYTHONPATH=./ python backend/app.py
# Runs on http://localhost:5001
```

### 4. Train RL Agent

```bash
PYTHONPATH=./ python train_rl.py --timesteps 50000 --task medium
# Saves model to models/dqn_crisisnet.zip
```

### 5. Run Benchmark (CLI)

```bash
PYTHONPATH=./ python -m backend.simulation
```

### 6. Run Inference

```bash
# With LLM (set one of: OPENAI_API_KEY, GROQ_API_KEY, HF_TOKEN, GEMINI_API_KEY)
PYTHONPATH=./ python inference.py

# Without LLM (uses heuristic fallback)
PYTHONPATH=./ python inference.py
```

### 7. Run Task Graders

```bash
# Via API:
curl http://localhost:7860/grade/easy
curl http://localhost:7860/grade/medium
curl http://localhost:7860/grade/hard
```

---

## 🐳 Docker Deployment

```bash
# Build
docker build -t crisisnet .

# Run
docker run -p 7860:7860 crisisnet

# Validate submission
bash validate-submission.sh https://your-space.hf.space
```

### HuggingFace Spaces

1. Create a new Space (Docker SDK)
2. Push this repo to the Space
3. The Dockerfile will auto-build and expose port 7860

---

## 🏗 Architecture

```
OpenEnv Clients ←→ FastAPI Server (:7860)   /reset, /step, /state, /grade
                         ↕
                    CrisisNetGymEnv (Gymnasium wrapper)
                         ↕
                    CrisisNetEnv (simulation engine)
                         ↑
                   Agent.decide(state) → action dict
```

---

## 📊 Benchmark Results

Results averaged over seeds [42, 99, 123]:

| Agent | Task | Survival% | Score |
|-------|------|-----------|-------|
| RLAgent | Easy | ~62% | ~0.757 |
| OptimalAgent | Easy | ~63% | ~0.745 |
| HeuristicAgent | Easy | ~62% | ~0.741 |
| RandomAgent | Easy | ~54% | ~0.695 |
| OptimalAgent | Hard | ~47% | ~0.530 |
| RLAgent | Hard | ~44% | ~0.510 |
| HeuristicAgent | Hard | ~46% | ~0.528 |
| RandomAgent | Hard | ~36% | ~0.454 |

*Run `PYTHONPATH=./ python -m backend.simulation` for exact numbers.*

---

## 📜 License

MIT
