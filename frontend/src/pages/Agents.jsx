import React from 'react';

const Agents = () => {
  return (
    <>
      
<div className="p-8">
{/*  Header Section  */}
<div className="mb-10 flex justify-between items-end">
<div>
<h1 className="text-4xl font-black tracking-tight text-on-surface mb-2">Agent Performance Benchmark</h1>
<p className="text-on-surface-variant font-medium">Comparative analysis of survival trajectories and operational resource consumption across Alpha-9 scenarios.</p>
</div>
<div className="flex gap-2">
<div className="bg-surface-container-low px-4 py-2 flex items-center gap-2">
<span className="w-2 h-2 rounded-full bg-secondary"></span>
<span className="text-[10px] font-bold uppercase tracking-widest">System Stable</span>
</div>
</div>
</div>
{/*  Three-Column Side-by-Side Comparison  */}
<div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
{/*  Column 1: Random Agent  */}
<div className="bg-surface-container-low p-1 relative overflow-hidden group">
<div className="absolute top-0 right-0 p-4 opacity-10">
<span className="material-symbols-outlined text-8xl" data-icon="casino">casino</span>
</div>
<div className="bg-surface-container p-6 h-full border-t-2 border-outline-variant/30">
<div className="flex items-center justify-between mb-8">
<span className="text-[10px] font-black uppercase tracking-[0.2em] text-on-surface-variant/60">Baseline Model</span>
<span className="bg-surface-container-highest px-2 py-1 text-[9px] font-bold uppercase tracking-widest text-on-surface-variant">V1.0.4-R</span>
</div>
<h2 className="text-2xl font-black uppercase tracking-tight mb-1 text-on-surface">Random Agent</h2>
<p className="text-xs text-on-surface-variant mb-10 leading-relaxed">Stochastic decision pathing based on weighted uniform distribution without environment feedback.</p>
{/*  Survival Rate Display  */}
<div className="mb-10">
<label className="text-[10px] font-bold uppercase tracking-widest text-on-surface-variant block mb-2">Net Survival Rate</label>
<div className="flex items-baseline gap-2">
<span className="text-6xl font-black tracking-tighter text-error">55%</span>
<span className="material-symbols-outlined text-error text-xl" data-icon="trending_down">trending_down</span>
</div>
</div>
{/*  Mini Graphs Area  */}
<div className="space-y-6 mb-10">
<div>
<div className="flex justify-between text-[9px] font-bold uppercase tracking-widest text-on-surface-variant mb-2">
<span>Reward vs Time</span>
<span className="text-error">-124.0 σ</span>
</div>
<div className="h-16 w-full flex items-end gap-1 px-1">
{/*  Visualizing a erratic graph  */}
<div className="bg-error/40 w-full h-[20%]"></div>
<div className="bg-error/40 w-full h-[60%]"></div>
<div className="bg-error/40 w-full h-[40%]"></div>
<div className="bg-error/40 w-full h-[80%]"></div>
<div className="bg-error/40 w-full h-[30%]"></div>
<div className="bg-error/40 w-full h-[10%]"></div>
<div className="bg-error/40 w-full h-[50%]"></div>
<div className="bg-error/40 w-full h-[25%]"></div>
</div>
</div>
<div>
<div className="flex justify-between text-[9px] font-bold uppercase tracking-widest text-on-surface-variant mb-2">
<span>Survival Decay</span>
</div>
<div className="h-1 bg-surface-container-highest w-full relative">
<div className="absolute left-0 top-0 h-full bg-error w-[55%]"></div>
</div>
</div>
</div>
{/*  Key Metrics  */}
<div className="grid grid-cols-2 gap-4 mb-8">
<div className="bg-surface-container-low p-3">
<span className="material-symbols-outlined text-on-surface-variant text-sm mb-1" data-icon="bolt">bolt</span>
<div className="text-[9px] font-bold uppercase tracking-widest text-on-surface-variant/70">Response Time</div>
<div className="text-lg font-bold">12ms</div>
</div>
<div className="bg-surface-container-low p-3">
<span className="material-symbols-outlined text-on-surface-variant text-sm mb-1" data-icon="analytics">analytics</span>
<div className="text-[9px] font-bold uppercase tracking-widest text-on-surface-variant/70">Efficiency</div>
<div className="text-lg font-bold">22.4%</div>
</div>
</div>
<div className="bg-error/10 border border-error/20 p-4">
<p className="text-[11px] text-on-error-container leading-relaxed italic">"Performance is erratic and unsustainable. Recommended only for control group comparisons in low-risk scenarios."</p>
</div>
</div>
</div>
{/*  Column 2: Heuristic Agent  */}
<div className="bg-surface-container-low p-1 relative overflow-hidden group">
<div className="absolute top-0 right-0 p-4 opacity-10">
<span className="material-symbols-outlined text-8xl" data-icon="account_tree">account_tree</span>
</div>
<div className="bg-surface-container p-6 h-full border-t-2 border-tertiary/30">
<div className="flex items-center justify-between mb-8">
<span className="text-[10px] font-black uppercase tracking-[0.2em] text-on-surface-variant/60">Expert System</span>
<span className="bg-tertiary/20 px-2 py-1 text-[9px] font-bold uppercase tracking-widest text-tertiary">V4.2.1-H</span>
</div>
<h2 className="text-2xl font-black uppercase tracking-tight mb-1 text-on-surface">Heuristic Agent</h2>
<p className="text-xs text-on-surface-variant mb-10 leading-relaxed">Decision logic based on hard-coded expert rulesets and optimized search trees.</p>
{/*  Survival Rate Display  */}
<div className="mb-10">
<label className="text-[10px] font-bold uppercase tracking-widest text-on-surface-variant block mb-2">Net Survival Rate</label>
<div className="flex items-baseline gap-2">
<span className="text-6xl font-black tracking-tighter text-tertiary">72%</span>
<span className="material-symbols-outlined text-tertiary text-xl" data-icon="trending_flat">trending_flat</span>
</div>
</div>
{/*  Mini Graphs Area  */}
<div className="space-y-6 mb-10">
<div>
<div className="flex justify-between text-[9px] font-bold uppercase tracking-widest text-on-surface-variant mb-2">
<span>Reward vs Time</span>
<span className="text-tertiary">+42.5 σ</span>
</div>
<div className="h-16 w-full flex items-end gap-1 px-1">
<div className="bg-tertiary/40 w-full h-[40%]"></div>
<div className="bg-tertiary/40 w-full h-[45%]"></div>
<div className="bg-tertiary/40 w-full h-[48%]"></div>
<div className="bg-tertiary/40 w-full h-[52%]"></div>
<div className="bg-tertiary/40 w-full h-[50%]"></div>
<div className="bg-tertiary/40 w-full h-[55%]"></div>
<div className="bg-tertiary/40 w-full h-[58%]"></div>
<div className="bg-tertiary/40 w-full h-[60%]"></div>
</div>
</div>
<div>
<div className="flex justify-between text-[9px] font-bold uppercase tracking-widest text-on-surface-variant mb-2">
<span>Survival Decay</span>
</div>
<div className="h-1 bg-surface-container-highest w-full relative">
<div className="absolute left-0 top-0 h-full bg-tertiary w-[72%]"></div>
</div>
</div>
</div>
{/*  Key Metrics  */}
<div className="grid grid-cols-2 gap-4 mb-8">
<div className="bg-surface-container-low p-3">
<span className="material-symbols-outlined text-on-surface-variant text-sm mb-1" data-icon="bolt">bolt</span>
<div className="text-[9px] font-bold uppercase tracking-widest text-on-surface-variant/70">Response Time</div>
<div className="text-lg font-bold">145ms</div>
</div>
<div className="bg-surface-container-low p-3">
<span className="material-symbols-outlined text-on-surface-variant text-sm mb-1" data-icon="analytics">analytics</span>
<div className="text-[9px] font-bold uppercase tracking-widest text-on-surface-variant/70">Efficiency</div>
<div className="text-lg font-bold">64.8%</div>
</div>
</div>
<div className="bg-tertiary/10 border border-tertiary/20 p-4">
<p className="text-[11px] text-tertiary leading-relaxed italic">"Stable and predictable. Strong performance in known scenarios but lacks adaptability for novel 'Black Swan' events."</p>
</div>
</div>
</div>
{/*  Column 3: RL Agent  */}
<div className="bg-surface-container-low p-1 relative overflow-hidden group">
<div className="absolute top-0 right-0 p-4 opacity-10">
<span className="material-symbols-outlined text-8xl" data-icon="psychology">psychology</span>
</div>
<div className="bg-surface-container p-6 h-full border-t-2 border-secondary/30">
<div className="flex items-center justify-between mb-8">
<span className="text-[10px] font-black uppercase tracking-[0.2em] text-secondary">Neural Network</span>
<span className="bg-secondary/20 px-2 py-1 text-[9px] font-bold uppercase tracking-widest text-secondary">V9.5.0-Σ</span>
</div>
<h2 className="text-2xl font-black uppercase tracking-tight mb-1 text-on-surface">RL Agent (Sentinel)</h2>
<p className="text-xs text-on-surface-variant mb-10 leading-relaxed">Deep Reinforcement Learning utilizing proximal policy optimization and multi-modal sensory input.</p>
{/*  Survival Rate Display  */}
<div className="mb-10">
<label className="text-[10px] font-bold uppercase tracking-widest text-on-surface-variant block mb-2">Net Survival Rate</label>
<div className="flex items-baseline gap-2">
<span className="text-6xl font-black tracking-tighter text-secondary">89%</span>
<span className="material-symbols-outlined text-secondary text-xl" data-icon="trending_up">trending_up</span>
</div>
</div>
{/*  Mini Graphs Area  */}
<div className="space-y-6 mb-10">
<div>
<div className="flex justify-between text-[9px] font-bold uppercase tracking-widest text-on-surface-variant mb-2">
<span>Reward vs Time</span>
<span className="text-secondary">+318.2 σ</span>
</div>
<div className="h-16 w-full flex items-end gap-1 px-1">
<div className="bg-secondary/40 w-full h-[15%]"></div>
<div className="bg-secondary/40 w-full h-[25%]"></div>
<div className="bg-secondary/40 w-full h-[45%]"></div>
<div className="bg-secondary/40 w-full h-[70%]"></div>
<div className="bg-secondary/40 w-full h-[85%]"></div>
<div className="bg-secondary/40 w-full h-[95%]"></div>
<div className="bg-secondary/40 w-full h-[90%]"></div>
<div className="bg-secondary/40 w-full h-[100%]"></div>
</div>
</div>
<div>
<div className="flex justify-between text-[9px] font-bold uppercase tracking-widest text-on-surface-variant mb-2">
<span>Survival Decay</span>
</div>
<div className="h-1 bg-surface-container-highest w-full relative">
<div className="absolute left-0 top-0 h-full bg-secondary w-[89%] shadow-[0_0_8px_rgba(74,225,118,0.5)]"></div>
</div>
</div>
</div>
{/*  Key Metrics  */}
<div className="grid grid-cols-2 gap-4 mb-8">
<div className="bg-surface-container-low p-3">
<span className="material-symbols-outlined text-secondary text-sm mb-1" data-icon="bolt">bolt</span>
<div className="text-[9px] font-bold uppercase tracking-widest text-on-surface-variant/70">Response Time</div>
<div className="text-lg font-bold">28ms</div>
</div>
<div className="bg-surface-container-low p-3">
<span className="material-symbols-outlined text-secondary text-sm mb-1" data-icon="analytics">analytics</span>
<div className="text-[9px] font-bold uppercase tracking-widest text-on-surface-variant/70">Efficiency</div>
<div className="text-lg font-bold">94.1%</div>
</div>
</div>
<div className="bg-secondary/10 border border-secondary/20 p-4">
<p className="text-[11px] text-secondary leading-relaxed font-bold italic">"Optimal performance across all variables. Exhibited emerging collaborative behaviors with local infrastructure nodes."</p>
</div>
</div>
</div>
</div>
{/*  Bottom Data Table Section (Asymmetric)  */}
<div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mt-12">
<div className="lg:col-span-8 bg-surface-container-low p-6">
<h3 className="text-xs font-black uppercase tracking-[0.2em] text-on-surface mb-6">Historical Trajectory Analysis</h3>
<div className="w-full h-64 bg-surface-container relative overflow-hidden">
{/*  Mock Map Background  */}
<div className="absolute inset-0 opacity-20 grayscale mix-blend-overlay">
<img className="w-full h-full object-cover" data-alt="Dark stylized topo map of a coastal city area with digital grid overlays and technical indicators" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCPH5GfBvx_ovcGkoQJa4hOsNU4chFb6jAqs4F7sRVFbLRNe1goY3FnyBtPxhjWa-XV3WfSFJ-YqNljk547_CVAn7pho3YCC3LyDThyvEH9Jf-i8Ko4Oeoq-ZIb3cSYKjH5zsdV0qPiXImt0XEKgkjvVDM21q7PV-2L-WsYznwfgqmZ2uh-slFsDE5iIupS9zs2N5gZtveOMM7ojzBxmXXI8UKRWAcqBTanhwZ6Wo_0ujf_EGFxJRdSbUjNICUs7CPyhhaMbIHQt2Gf"/>
</div>
<div className="absolute inset-0 flex flex-col items-center justify-center">
<span className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest bg-background/80 px-3 py-1">Cross-Agent Simulation Visualizer Active</span>
</div>
</div>
</div>
<div className="lg:col-span-4 flex flex-col gap-6">
<div className="bg-surface-container p-6 border-l-2 border-primary">
<div className="text-[10px] font-black uppercase tracking-widest text-primary mb-2">Alert Intelligence</div>
<p className="text-xs text-on-surface-variant leading-relaxed">Agent RL has identified a recurring failure point in Segment 4B. Recommend immediate logic injection to Heuristic model for hybrid testing.</p>
</div>
<div className="flex-1 bg-surface-container p-6 relative overflow-hidden">
<div className="flex items-center justify-between mb-4">
<div className="text-[10px] font-black uppercase tracking-widest text-on-surface-variant">Resource Load</div>
<span className="text-xs font-mono text-secondary">0.0024ms Lag</span>
</div>
<div className="space-y-3">
{/*  Segmented progress bars  */}
<div className="flex gap-0.5">
<div className="h-2 w-full bg-secondary-fixed"></div>
<div className="h-2 w-full bg-secondary-fixed"></div>
<div className="h-2 w-full bg-secondary-fixed"></div>
<div className="h-2 w-full bg-secondary-fixed"></div>
<div className="h-2 w-full bg-secondary-fixed"></div>
<div className="h-2 w-full bg-secondary-fixed"></div>
<div className="h-2 w-full bg-secondary-fixed opacity-30"></div>
<div className="h-2 w-full bg-secondary-fixed opacity-30"></div>
<div className="h-2 w-full bg-secondary-fixed opacity-30"></div>
<div className="h-2 w-full bg-secondary-fixed opacity-30"></div>
</div>
<div className="flex gap-0.5">
<div className="h-2 w-full bg-tertiary-fixed"></div>
<div className="h-2 w-full bg-tertiary-fixed"></div>
<div className="h-2 w-full bg-tertiary-fixed"></div>
<div className="h-2 w-full bg-tertiary-fixed"></div>
<div className="h-2 w-full bg-tertiary-fixed opacity-30"></div>
<div className="h-2 w-full bg-tertiary-fixed opacity-30"></div>
<div className="h-2 w-full bg-tertiary-fixed opacity-30"></div>
<div className="h-2 w-full bg-tertiary-fixed opacity-30"></div>
<div className="h-2 w-full bg-tertiary-fixed opacity-30"></div>
<div className="h-2 w-full bg-tertiary-fixed opacity-30"></div>
</div>
</div>
</div>
</div>
</div>
</div>

    </>
  );
};

export default Agents;
