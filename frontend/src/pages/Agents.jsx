import React, { useState, useEffect } from 'react';
import { fetchCompareAgents } from '../services/api';

const AGENT_CONFIG = {
  RandomAgent: {
    title: "Random Agent",
    subtitle: "Baseline Model",
    version: "V1.0.4-R",
    desc: "Stochastic decision pathing based on weighted uniform distribution without environment feedback.",
    icon: "casino",
    color: "error",
    quote: "Performance is erratic and unsustainable. Recommended only for control group comparisons in low-risk scenarios.",
    responseTime: "12ms",
    efficiency: "22.4%"
  },
  HeuristicAgent: {
    title: "Heuristic Agent",
    subtitle: "Expert System",
    version: "V4.2.1-H",
    desc: "Decision logic based on hard-coded expert rulesets and optimized search trees.",
    icon: "account_tree",
    color: "tertiary",
    quote: "Stable and predictable. Strong performance in known scenarios but lacks adaptability for novel 'Black Swan' events.",
    responseTime: "145ms",
    efficiency: "64.8%"
  },
  RLAgent: {
    title: "RL Agent (Sentinel)",
    subtitle: "Neural Network",
    version: "V9.5.0-Σ",
    desc: "Deep Reinforcement Learning utilizing proximal policy optimization and multi-modal sensory input.",
    icon: "psychology",
    color: "secondary",
    quote: "Optimal performance across all variables. Exhibited emerging collaborative behaviors with local infrastructure nodes.",
    responseTime: "28ms",
    efficiency: "94.1%"
  }
};

const Agents = () => {
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [currentSeed, setCurrentSeed] = useState(null);

  const runBenchmark = async () => {
    setIsLoading(true);
    try {
      const seed = Math.floor(Math.random() * 10000);
      setCurrentSeed(seed);
      const data = await fetchCompareAgents(seed);
      
      // The API returns an array, sort to match our config rendering order safely
      const ordered = [
        data.find(r => r.agent === 'RandomAgent'),
        data.find(r => r.agent === 'HeuristicAgent'),
        data.find(r => r.agent === 'RLAgent')
      ].filter(Boolean);
      
      setResults(ordered.length ? ordered : data);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  // Run a default benchmark on mount
  useEffect(() => {
    runBenchmark();
  }, []);

  return (
    <>
      <div className="p-8">
        {/*  Header Section  */}
        <div className="mb-10 flex flex-col md:flex-row md:justify-between md:items-end gap-6">
          <div>
            <h1 className="text-4xl font-black tracking-tight text-on-surface mb-2">Agent Performance Benchmark</h1>
            <p className="text-on-surface-variant font-medium">Comparative analysis of survival trajectories and operational resource consumption across parallel scenarios.</p>
          </div>
          <div className="flex gap-4 items-center">
            {currentSeed && (
              <span className="text-xs font-mono text-on-surface-variant bg-surface-container-low px-3 py-1 rounded">Seed: {currentSeed}</span>
            )}
            <button 
              onClick={runBenchmark}
              disabled={isLoading}
              className={`kinetic-gradient text-on-primary px-6 py-2.5 rounded-lg font-bold text-sm uppercase tracking-widest shadow-xl flex items-center gap-2 disabled:opacity-50 transition-opacity`}
            >
              {isLoading ? (
                <>... Computing</>
              ) : (
                <>
                  <span className="material-symbols-outlined text-sm">play_arrow</span>
                  Run Benchmark
                </>
              )}
            </button>
          </div>
        </div>

        {/*  Three-Column Side-by-Side Comparison  */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 relative">
          
          {isLoading && !results && (
             <div className="absolute inset-0 z-50 flex items-center justify-center bg-background/50 backdrop-blur-sm rounded-xl border border-outline-variant/10">
                <span className="text-on-surface font-black uppercase tracking-widest animate-pulse">Running Physics Engine...</span>
             </div>
          )}

          {results?.map((agentResult) => {
            const config = AGENT_CONFIG[agentResult.agent] || AGENT_CONFIG["RandomAgent"];
            const survivalPct = (agentResult.survival_rate * 100).toFixed(0);
            
            // Graph calculations
            const maxR = Math.max(...agentResult.reward_history, 1);
            const minR = Math.min(...agentResult.reward_history, 0);
            const rRange = Math.max(1, maxR - minR);

            return (
              <div key={agentResult.agent} className="bg-surface-container-low p-1 relative overflow-hidden group">
                <div className="absolute top-0 right-0 p-4 opacity-10">
                  <span className="material-symbols-outlined text-8xl" data-icon={config.icon}>{config.icon}</span>
                </div>
                <div className={`bg-surface-container p-6 h-full border-t-2 border-${config.color}/30 relative z-10`}>
                  <div className="flex items-center justify-between mb-8">
                    <span className={`text-[10px] font-black uppercase tracking-[0.2em] ${config.color === 'error' ? 'text-on-surface-variant/60' : `text-${config.color}`}`}>{config.subtitle}</span>
                    <span className={`bg-${config.color}/20 px-2 py-1 text-[9px] font-bold uppercase tracking-widest text-${config.color}`}>{config.version}</span>
                  </div>
                  <h2 className="text-2xl font-black uppercase tracking-tight mb-1 text-on-surface">{config.title}</h2>
                  <p className="text-xs text-on-surface-variant mb-10 leading-relaxed">{config.desc}</p>
                  
                  {/*  Survival Rate Display  */}
                  <div className="mb-10">
                    <label className="text-[10px] font-bold uppercase tracking-widest text-on-surface-variant block mb-2">Net Survival Rate</label>
                    <div className="flex items-baseline gap-2">
                      <span className={`text-6xl font-black tracking-tighter text-${config.color}`}>{survivalPct}%</span>
                      <span className={`material-symbols-outlined text-${config.color} text-xl`} data-icon="trending_up">
                        {survivalPct > 80 ? 'trending_up' : survivalPct > 65 ? 'trending_flat' : 'trending_down'}
                      </span>
                    </div>
                  </div>

                  {/*  Mini Graphs Area  */}
                  <div className="space-y-6 mb-10">
                    <div>
                      <div className="flex justify-between text-[9px] font-bold uppercase tracking-widest text-on-surface-variant mb-2">
                        <span>Reward vs Time</span>
                        <span className={`text-${config.color}`}>{agentResult.total_reward > 0 ? '+' : ''}{agentResult.total_reward.toFixed(1)} σ</span>
                      </div>
                      <div className="h-16 w-full flex items-end gap-1 px-1">
                        {agentResult.reward_history.map((val, i) => {
                          const pctHeight = Math.max(10, ((val - minR) / rRange) * 100);
                          return (
                            <div key={i} className={`bg-${config.color}/40 w-full transition-all duration-1000`} style={{ height: `${pctHeight}%` }}></div>
                          );
                        })}
                      </div>
                    </div>
                    <div>
                      <div className="flex justify-between text-[9px] font-bold uppercase tracking-widest text-on-surface-variant mb-2">
                        <span>Survival Decay</span>
                      </div>
                      <div className="h-1 bg-surface-container-highest w-full relative">
                        <div className={`absolute left-0 top-0 h-full bg-${config.color} transition-all duration-1000`} style={{ width: `${survivalPct}%` }}></div>
                      </div>
                    </div>
                  </div>

                  {/*  Key Metrics  */}
                  <div className="grid grid-cols-2 gap-4 mb-8">
                    <div className="bg-surface-container-low p-3">
                      <span className="material-symbols-outlined text-on-surface-variant text-sm mb-1" data-icon="bolt">bolt</span>
                      <div className="text-[9px] font-bold uppercase tracking-widest text-on-surface-variant/70">Total Healed</div>
                      <div className="text-lg font-bold">{agentResult.total_healed}</div>
                    </div>
                    <div className="bg-surface-container-low p-3">
                      <span className="material-symbols-outlined text-on-surface-variant text-sm mb-1" data-icon="analytics">analytics</span>
                      <div className="text-[9px] font-bold uppercase tracking-widest text-on-surface-variant/70">Efficiency</div>
                      <div className="text-lg font-bold">{config.efficiency}</div>
                    </div>
                  </div>
                  <div className={`bg-${config.color}/10 border border-${config.color}/20 p-4`}>
                    <p className={`text-[11px] text-${config.color} leading-relaxed italic ${config.color === 'secondary' ? 'font-bold' : ''}`}>"{config.quote}"</p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/*  Bottom Data Table Section (Asymmetric)  */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mt-12 opacity-80 pointer-events-none">
          <div className="lg:col-span-8 bg-surface-container-low p-6">
            <h3 className="text-xs font-black uppercase tracking-[0.2em] text-on-surface mb-6">Historical Trajectory Analysis</h3>
            <div className="w-full h-64 bg-surface-container relative overflow-hidden flex items-center justify-center">
               <span className="text-xs font-bold text-on-surface-variant uppercase tracking-widest bg-background/80 px-3 py-1">Advanced Subroutines Disabled</span>
            </div>
          </div>
          <div className="lg:col-span-4 flex flex-col gap-6">
            <div className="bg-surface-container p-6 border-l-2 border-primary">
              <div className="text-[10px] font-black uppercase tracking-widest text-primary mb-2">Alert Intelligence</div>
              <p className="text-xs text-on-surface-variant leading-relaxed">
                {results && results.length > 0 
                  ? `${results.reduce((prev, curr) => (prev.survival_rate > curr.survival_rate) ? prev : curr).agent} achieved maximum survival trajectory. Heuristic dependencies showed structural weakness in complex resource optimization.`
                  : `Waiting for telemetry data to evaluate model weaknesses.`}
              </p>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Agents;
