"""
CrisisNet DQN Training Script

Trains a Stable-Baselines3 DQN agent on the CrisisNetGymEnv.
Saves the trained model to models/dqn_crisisnet.zip.

Usage:
    PYTHONPATH=./ python train_rl.py [--timesteps 50000] [--task medium]
"""

import argparse
import os
import sys

import numpy as np
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import BaseCallback, EvalCallback
from stable_baselines3.common.monitor import Monitor

from backend.gym_env import CrisisNetGymEnv


# ------------------------------------------------------------------ #
#  Custom Logging Callback                                             #
# ------------------------------------------------------------------ #

class TrainingLogger(BaseCallback):
    """Log training metrics every N steps."""

    def __init__(self, log_interval: int = 1000, verbose: int = 1):
        super().__init__(verbose)
        self.log_interval = log_interval
        self._episode_rewards: list[float] = []
        self._current_reward = 0.0

    def _on_step(self) -> bool:
        # Accumulate reward
        reward = self.locals.get("rewards", [0.0])
        if isinstance(reward, np.ndarray):
            self._current_reward += reward.sum()
        else:
            self._current_reward += sum(reward) if hasattr(reward, '__iter__') else reward

        # Check for episode end
        dones = self.locals.get("dones", [False])
        if isinstance(dones, np.ndarray):
            done = dones.any()
        else:
            done = any(dones) if hasattr(dones, '__iter__') else dones

        if done:
            self._episode_rewards.append(self._current_reward)
            self._current_reward = 0.0

        # Log periodically
        if self.num_timesteps % self.log_interval == 0:
            recent = self._episode_rewards[-10:] if self._episode_rewards else [0]
            avg = np.mean(recent)
            print(
                f"  Step {self.num_timesteps:>7d}  |  "
                f"Episodes: {len(self._episode_rewards):>4d}  |  "
                f"Avg Reward (last 10): {avg:>10.1f}"
            )

        return True


# ------------------------------------------------------------------ #
#  Training Function                                                   #
# ------------------------------------------------------------------ #

def train(
    total_timesteps: int = 50_000,
    task: str = "medium",
    seed: int = 42,
    save_path: str = "models/dqn_crisisnet",
    eval_freq: int = 2000,
) -> None:
    """
    Train a DQN agent and save the model.

    Args:
        total_timesteps: Total training steps.
        task: Difficulty level for training ('easy', 'medium', 'hard').
        seed: Random seed.
        save_path: Path to save the model (without .zip extension).
        eval_freq: Evaluation frequency (steps).
    """
    print("=" * 60)
    print("  CrisisNet DQN Training")
    print("=" * 60)
    print(f"  Task:           {task}")
    print(f"  Timesteps:      {total_timesteps:,}")
    print(f"  Seed:           {seed}")
    print(f"  Save path:      {save_path}.zip")
    print("=" * 60)

    # Create training environment
    train_env = Monitor(CrisisNetGymEnv(task=task, seed=seed))

    # Create evaluation environment (different seed)
    eval_env = Monitor(CrisisNetGymEnv(task=task, seed=seed + 1000))

    # Ensure save directory exists
    os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)

    # Create DQN model
    model = DQN(
        "MlpPolicy",
        train_env,
        learning_rate=1e-3,
        buffer_size=50_000,
        learning_starts=500,
        batch_size=64,
        gamma=0.99,
        tau=1.0,
        target_update_interval=500,
        exploration_fraction=0.3,
        exploration_initial_eps=1.0,
        exploration_final_eps=0.05,
        train_freq=4,
        gradient_steps=1,
        policy_kwargs={"net_arch": [128, 128]},
        verbose=0,
        seed=seed,
    )

    # Callbacks
    eval_callback = EvalCallback(
        eval_env,
        best_model_save_path=os.path.dirname(save_path) or ".",
        log_path=os.path.dirname(save_path) or ".",
        eval_freq=eval_freq,
        n_eval_episodes=5,
        deterministic=True,
        verbose=0,
    )
    logger_callback = TrainingLogger(log_interval=2000)

    print("\nTraining started...")
    model.learn(
        total_timesteps=total_timesteps,
        callback=[eval_callback, logger_callback],
    )

    # Save final model
    model.save(save_path)
    print(f"\n✅ Model saved to {save_path}.zip")

    # ---- Quick evaluation ---- #
    print("\n--- Post-training Evaluation ---")
    for eval_task in ["easy", "medium", "hard"]:
        env = CrisisNetGymEnv(task=eval_task, seed=99)
        rewards = []
        scores = []

        for ep in range(5):
            obs, _ = env.reset(seed=99 + ep)
            total_reward = 0.0
            done = False
            while not done:
                action, _ = model.predict(obs, deterministic=True)
                obs, reward, done, truncated, info = env.step(action)
                total_reward += reward
            rewards.append(total_reward)
            scores.append(env.compute_score())

        avg_reward = np.mean(rewards)
        avg_score = np.mean(scores)
        print(
            f"  {eval_task:>6s}:  avg_reward = {avg_reward:>8.1f}  |  "
            f"avg_score = {avg_score:.3f}"
        )

    train_env.close()
    eval_env.close()
    print("\n✅ Training complete!")


# ------------------------------------------------------------------ #
#  CLI                                                                 #
# ------------------------------------------------------------------ #

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train CrisisNet DQN agent")
    parser.add_argument(
        "--timesteps", type=int, default=50_000,
        help="Total training timesteps (default: 50000)",
    )
    parser.add_argument(
        "--task", type=str, default="medium",
        choices=["easy", "medium", "hard"],
        help="Training difficulty (default: medium)",
    )
    parser.add_argument(
        "--seed", type=int, default=42,
        help="Random seed (default: 42)",
    )
    parser.add_argument(
        "--save-path", type=str, default="models/dqn_crisisnet",
        help="Model save path without .zip (default: models/dqn_crisisnet)",
    )

    args = parser.parse_args()
    train(
        total_timesteps=args.timesteps,
        task=args.task,
        seed=args.seed,
        save_path=args.save_path,
    )
