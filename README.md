# CrisisNet — AI Disaster Response Simulator

A multi-agent disaster-response simulation where AI agents compete to save lives across crisis-affected urban zones. Built as a tick-based environment with three decision-making agents, a React dashboard, and a Flask API.

## How It Works

- **5 disaster zones** with population health states (healthy, injured, critical, deceased), resource levels (food, water, medical supplies, fuel), and infrastructure (road access, hospital capacity)
- **12 time steps** — each tick, exactly one action can be taken
- **Actions:** deploy medical teams, allocate food/water/medicine, repair roads
- **Agents** observe all zone states and decide the optimal action
- **Environment** applies health transitions, resource consumption, infrastructure decay, and computes rewards
- **Goal:** maximise survival rate and minimise total deaths

## Agents

| Agent | Strategy | Avg Survival (8 seeds) |
|-------|----------|----------------------|
| **RLAgent** | RL-inspired coverage-rush policy — deploys medical teams to every zone first, then predicts resource depletion using consumption-rate estimates | **68.2%** |
| **HeuristicAgent** | Fixed-priority rules: critical patients → food → water → roads | **52.7%** |
| **RandomAgent** | Random action selection with 50% idle probability | **38.1%** |

## Note on RL Agent

The RL Agent implements an RL-inspired optimal policy — the decision strategy that a trained reinforcement learning system would converge to after learning this environment's reward structure. The policy was hand-crafted by analysing environment dynamics (reward weights, transition rates, action persistence) rather than through neural network training, which would require thousands of episodes beyond hackathon scope.

Key insights exploited:
1. **Medical teams persist permanently** once deployed — making `deploy_medical` the highest-ROI action
2. **Resource allocations are uncapped** — a single large allocation can fix a zone's supply for the entire simulation
3. **Predictive depletion** — the agent estimates ticks-until-resource-exhaustion rather than using raw thresholds

## Tech Stack

- **Backend:** Python 3.12, Flask, discrete event simulation
- **Frontend:** React 18 (Vite), Tailwind CSS
- **API:** REST with Flask-CORS

## Project Structure

```
CrisisNet/
├── backend/
│   ├── environment.py    # Simulation engine (zones, health, resources)
│   ├── agents.py         # RandomAgent, HeuristicAgent, RLAgent
│   ├── actions.py        # Action schema and validation
│   ├── simulation.py     # Benchmark runner and comparison
│   └── app.py            # Flask REST API
├── frontend/
│   └── src/
│       ├── pages/
│       │   ├── Home.jsx          # Dashboard with map, controls, logs
│       │   ├── Agents.jsx        # Agent benchmark comparison
│       │   ├── Zones.jsx         # Zone detail view
│       │   └── Infrastructure.jsx # Infrastructure status
│       ├── components/           # Navbar, Sidebar
│       └── services/api.js       # API client
└── README.md
```

## Setup

### Backend
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=./ python backend/app.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Run Benchmark (CLI)
```bash
source .venv/bin/activate
PYTHONPATH=./ python -m backend.simulation
```

## Architecture

```
React Dashboard ←→ Flask API (/step, /state, /reset, /compare_agents)
                        ↕
                   CrisisNetEnv (simulation engine)
                        ↑
                  Agent.decide(state) → action dict
```

The dashboard supports both **autonomous AI agents** (auto-play mode) and **manual human override** (direct action dispatch), implementing a human-in-the-loop control pattern.
