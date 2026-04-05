import React, { useState, useEffect } from 'react';
import { fetchState, stepSimulation, resetSimulation } from '../services/api';

const ZONE_POSITIONS = {
  1: { top: '20%', left: '30%' },
  2: { top: '60%', left: '15%' },
  3: { top: '45%', left: '55%' },
  4: { top: '75%', left: '70%' },
  5: { top: '15%', left: '80%' },
};

const getZoneTheme = (zone) => {
  if (zone.critical > 50 || zone.food === 0) {
    return {
      bg: "bg-error", text: "text-error", border: "border-error/30",
      pulseBorder: "border-error/50", label: "CRITICAL", pulse: true, severeBorder: false
    };
  } else if (zone.critical > 10 || zone.road_access < 0.4) {
    return {
      bg: "bg-primary-container", text: "text-primary-container", border: "border-primary-container/30",
      pulseBorder: "", label: "SEVERE", pulse: false, severeBorder: "border-primary-container/50"
    };
  } else if (zone.injured > 50 || zone.food < 100) {
    return {
      bg: "bg-tertiary", text: "text-tertiary", border: "border-tertiary/30",
      pulseBorder: "", label: "WATCH", pulse: false, severeBorder: false
    };
  }
  return {
    bg: "bg-secondary", text: "text-secondary", border: "border-secondary/30",
    pulseBorder: "", label: "STABLE", pulse: false, severeBorder: false
  };
};

const formatTime = (time) => {
  const t = Math.floor(time * 1.5) + 12; // Just a mock time format based on tick
  return `${t}:00:00`;
};

const Home = () => {
  const [simState, setSimState] = useState(null);
  const [logs, setLogs] = useState([]);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // Initial Fetch
  useEffect(() => {
    const init = async () => {
      try {
        const state = await fetchState();
        setSimState(state);
      } catch (err) {
        console.error("Failed to fetch state:", err);
      } finally {
        setIsLoading(false);
      }
    };
    init();
  }, []);

  // Play Loop
  useEffect(() => {
    let interval;
    if (isPlaying) {
      interval = setInterval(() => {
        handleStep();
      }, 1500);
    }
    return () => clearInterval(interval);
  }, [isPlaying]);

  const handleStep = async () => {
    try {
      // Auto-step using the RLAgent
      const response = await stepSimulation({ agent: "RLAgent" });
      setSimState(response.state);
      
      if (response.done) {
        setIsPlaying(false);
      }

      // Add log
      if (response.state.step_metrics) {
        const metrics = response.state.step_metrics;
        const newLog = {
           time: response.state.time,
           type: metrics.deaths > 0 ? "CASUALTY" : "ACTION",
           color: metrics.deaths > 0 ? "error" : "secondary",
           title: `Simulation Step ${response.state.time}`,
           desc: `Healed: ${metrics.healed}, Deaths: ${metrics.deaths}, Starvation: ${metrics.starvation_deaths}`,
           reward: metrics.reward,
           rewardColor: metrics.reward >= 0 ? "secondary" : "error",
           rewardPrefix: metrics.reward >= 0 ? "+" : ""
        };
        setLogs(prev => [newLog, ...prev]);
      }
    } catch (err) {
      console.error(err);
      setIsPlaying(false);
    }
  };

  const handleReset = async () => {
    try {
      setIsPlaying(false);
      const response = await resetSimulation();
      setSimState(response.state);
      setLogs([]);
    } catch (err) {
      console.error(err);
    }
  };

  if (isLoading || !simState) return <div className="p-8 text-on-surface">Loading Interface...</div>;

  const zones = simState.zones || [];
  
  const totalPopulation = zones.reduce((acc, z) => acc + z.healthy + z.injured + z.critical + z.deceased, 0);
  const totalDeceased = zones.reduce((acc, z) => acc + z.deceased, 0);
  const totalSurvivors = zones.reduce((acc, z) => acc + z.healthy + z.injured + z.critical, 0);
  const totalMedical = zones.reduce((acc, z) => acc + z.medical, 0);
  
  const survivalRate = totalPopulation > 0 ? ((totalSurvivors / totalPopulation) * 100).toFixed(1) : "0.0";
  const medicalPercent = Math.min(100, Math.floor((totalMedical / 1000) * 100)); // Arbitrary max 1000 for visuals

  return (
    <>
      <div className="flex flex-1 gap-6 min-h-0">
          {/*  Center Map Panel  */}
          <section className="flex-[3] bg-surface-container-low rounded-xl relative overflow-hidden group">
              {/*  Background Map Visual  */}
              <div className="absolute inset-0 z-0">
                  <img alt="Simulation Map" className="w-full h-full object-cover opacity-30 grayscale contrast-125"
                      data-alt="top-down satellite view of a high-density urban city grid at night with glowing blue and red data lines overlay"
                      data-location="Tokyo"
                      src="https://lh3.googleusercontent.com/aida-public/AB6AXuC6jeJmKfEME4xcZCnLsAic-YRL4_uzaf0V4QJHF3lR4n8NHTTSuO4EdUnTNAv7NKDzayjFjA6EXEiMGVMt5F6mvH_86X5PBpyP2XDorIxX1bA9LXa4Ab79QnyLvD_f4OE9wxow_HSzlkVGdKwZVwyCABtuurNh2z_swbSmetz40J9xvmKvc3XHaLKqDJilY3XAX0mtuhP2fIidAWiMWMgTqqF3vBCcP0FtU0UQqeyL2DAHDfJ8Rnm6vNMHbznzaVev9pk-aX6ndE0L" />
                  <div className="absolute inset-0 map-gradient-overlay"></div>
              </div>
              {/*  UI Overlay for Map  */}
              <div className="absolute inset-0 z-10 p-6 pointer-events-none">
                  <div className="flex justify-between items-start">
                      <div className="bg-surface-container-lowest/80 backdrop-blur-md px-4 py-2 rounded border border-outline-variant/20">
                          <div className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest">
                              Environment Active</div>
                          <div className="text-xl font-black text-on-surface">Time: {formatTime(simState.time)} / {formatTime(simState.max_time)}</div>
                      </div>
                      <div className="flex gap-2">
                          <button onClick={() => setIsPlaying(!isPlaying)} className={`bg-surface-container-lowest/80 backdrop-blur-md p-2 rounded border border-outline-variant/20 pointer-events-auto cursor-pointer hover:bg-surface-container-high transition-colors ${isPlaying ? 'ring-2 ring-primary/50' : ''}`}>
                              <span className="material-symbols-outlined text-primary" style={{fontVariationSettings: "'FILL' 1"}}>{isPlaying ? 'pause' : 'play_arrow'}</span>
                          </button>
                          <button onClick={handleStep} disabled={isPlaying || simState.time >= simState.max_time} className="bg-surface-container-lowest/80 backdrop-blur-md p-2 rounded border border-outline-variant/20 pointer-events-auto cursor-pointer hover:bg-surface-container-high transition-colors disabled:opacity-50">
                              <span className="material-symbols-outlined text-secondary">skip_next</span>
                          </button>
                          <button onClick={handleReset} className="bg-surface-container-lowest/80 backdrop-blur-md p-2 rounded border border-outline-variant/20 pointer-events-auto cursor-pointer hover:bg-surface-container-high transition-colors">
                              <span className="material-symbols-outlined text-error">restart_alt</span>
                          </button>
                      </div>
                  </div>
                  {/*  Dynamic Map Pins  */}
                  {zones.map((zone) => {
                      const pos = ZONE_POSITIONS[zone.id] || { top: '50%', left: '50%' };
                      const theme = getZoneTheme(zone);
                      
                      return (
                          <div key={zone.id} style={{ top: pos.top, left: pos.left }} className="absolute pointer-events-auto flex flex-col items-center">
                              <div className={`w-4 h-4 ${theme.bg} rounded-full relative ${theme.pulse ? 'pulse-error' : ''}`}>
                                  {theme.pulse && <div className={`absolute -inset-2 rounded-full border ${theme.pulseBorder} animate-ping`}></div>}
                                  {theme.severeBorder && <div className={`absolute -inset-1 rounded-full border ${theme.severeBorder}`}></div>}
                              </div>
                              <div className={`mt-2 bg-surface-container-highest/90 backdrop-blur-sm px-2 py-1 rounded text-[10px] font-bold ${theme.text} border ${theme.border}`}>
                                  ZONE {zone.id}: {theme.label}
                              </div>
                          </div>
                      );
                  })}
              </div>
          </section>
          {/*  Right Metrics Panel  */}
          <aside className="flex-1 flex flex-col gap-4 min-w-[320px]">
              {/*  Survival Rate Hero  */}
              <div className="bg-surface-container-low p-6 rounded-xl border-t border-surface-bright/20 shadow-xl flex flex-col items-center">
                  <div className="text-[10px] font-bold text-on-surface-variant uppercase tracking-[0.2em] mb-4">
                      Simulation Health</div>
                  <div className="relative w-32 h-32 flex items-center justify-center">
                      <svg className="absolute inset-0 w-full h-full transform -rotate-90">
                          <circle className="text-surface-container-highest" cx="64" cy="64" fill="transparent" r="60"
                              stroke="currentColor" strokeWidth="8"></circle>
                          <circle className={`${Number(survivalRate) < 50 ? 'text-error' : 'text-secondary'} transition-all duration-1000`} cx="64" cy="64" fill="transparent" r="60"
                              stroke="currentColor" strokeDasharray="377" strokeDashoffset={377 - (377 * Number(survivalRate) / 100)}
                              strokeWidth="8"></circle>
                      </svg>
                      <div className="text-4xl font-black tracking-tighter">{Math.floor(survivalRate)}<span className="text-lg font-bold">%</span>
                      </div>
                  </div>
                  <div className="mt-4 text-xs font-medium text-secondary uppercase tracking-widest">Survival Rate</div>
              </div>
              {/*  Metrics Grid  */}
              <div className="grid grid-cols-2 gap-4">
                  <div className="bg-surface-container p-4 rounded-lg">
                      <div className="text-[9px] font-bold text-on-surface-variant uppercase tracking-widest mb-1">
                          Total Deaths</div>
                      <div className="text-xl font-bold text-error tracking-tight">{totalDeceased.toLocaleString()}</div>
                  </div>
                  <div className="bg-surface-container p-4 rounded-lg">
                      <div className="text-[9px] font-bold text-on-surface-variant uppercase tracking-widest mb-1">
                          Active Survivors</div>
                      <div className="text-xl font-bold text-secondary tracking-tight">{totalSurvivors.toLocaleString()}</div>
                  </div>
              </div>
              {/*  Resource & Status Stack  */}
              <div className="bg-surface-container-low p-5 rounded-xl space-y-6">
                  <div className="space-y-3">
                      <div className="flex justify-between items-end">
                          <span className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest">Global Medical</span>
                          <span className="text-xs font-bold text-on-surface">{medicalPercent}%</span>
                      </div>
                      <div className="h-4 bg-surface-container-lowest flex segmented-progress-bar rounded-sm overflow-hidden">
                          {Array.from({ length: 10 }).map((_, i) => (
                              <div key={i} className={`bg-secondary-container ${i >= Math.round(medicalPercent / 10) ? 'opacity-30' : ''}`}></div>
                          ))}
                      </div>
                  </div>
                  <div className="space-y-3">
                      <div className="flex justify-between items-end">
                          <span className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest">Disease Risk Index</span>
                          <span className="text-xs font-bold text-tertiary">MODERATE</span>
                      </div>
                      <div className="h-2 bg-surface-container-lowest rounded-full overflow-hidden">
                          <div className="h-full bg-tertiary w-3/5"></div>
                      </div>
                  </div>
                  <div className="pt-4 border-t border-outline-variant/15">
                      <div className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest mb-3">
                          Field Team Status</div>
                      <div className="space-y-2">
                          <div className="flex items-center justify-between text-xs">
                              <div className="flex items-center gap-2">
                                  <div className="w-1.5 h-1.5 rounded-full bg-secondary"></div>
                                  <span className="opacity-80">CrisisNet Model</span>
                              </div>
                              <span className="font-mono text-[10px] opacity-60">ACTIVE: RL-AGENT</span>
                          </div>
                      </div>
                  </div>
              </div>
          </aside>
      </div>
      {/*  Bottom Decision Log Timeline  */}
      <footer className="h-48 bg-surface-container-low rounded-xl border border-outline-variant/10 flex flex-col overflow-hidden">
          <div className="px-6 py-3 border-b border-outline-variant/15 flex justify-between items-center bg-surface-container">
              <h3 className="text-[10px] font-black uppercase tracking-[0.3em] text-[#ffb3ad]">Decision Log &amp; Reward Timeline</h3>
              <div className="flex gap-4 items-center">
                  <span className="text-[10px] text-on-surface-variant uppercase">Time {simState.time} / {simState.max_time}</span>
              </div>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-2">
              {logs.length === 0 ? (
                  <div className="text-xs text-on-surface-variant opacity-60 p-2">No actions recorded yet. Press Step to begin.</div>
              ) : logs.map((log, i) => (
                  <div key={i} className="flex gap-4 items-start p-3 hover:bg-surface-container-high transition-colors group rounded-md">
                      <div className="text-[10px] font-mono text-on-surface-variant opacity-40 pt-1">Tick {log.time}</div>
                      <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                              <span className={`text-xs font-bold uppercase tracking-widest text-${log.color}`}>[{log.type}]</span>
                              <span className="text-xs font-medium">{log.title}</span>
                          </div>
                          <p className="text-[11px] text-on-surface-variant leading-relaxed">{log.desc}</p>
                      </div>
                      <div className="text-right">
                          <div className={`text-xs font-bold text-${log.rewardColor}`}>{log.rewardPrefix}{log.reward.toFixed(2)}</div>
                          <div className="text-[9px] uppercase opacity-40">Reward</div>
                      </div>
                  </div>
              ))}
          </div>
      </footer>
    </>
  );
};

export default Home;
