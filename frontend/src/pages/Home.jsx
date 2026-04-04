import React from 'react';

const Home = () => {
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
                            <div
                                className="bg-surface-container-lowest/80 backdrop-blur-md px-4 py-2 rounded border border-outline-variant/20">
                                <div className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest">
                                    Active Perimeter</div>
                                <div className="text-xl font-black text-on-surface">DISTRICT 7 - SHIBUYA</div>
                            </div>
                            <div className="flex gap-2">
                                <div
                                    className="bg-surface-container-lowest/80 backdrop-blur-md p-2 rounded border border-outline-variant/20 pointer-events-auto cursor-pointer hover:bg-surface-container-high">
                                    <span className="material-symbols-outlined text-secondary"
                                        data-icon="layers">layers</span>
                                </div>
                                <div
                                    className="bg-surface-container-lowest/80 backdrop-blur-md p-2 rounded border border-outline-variant/20 pointer-events-auto cursor-pointer hover:bg-surface-container-high">
                                    <span className="material-symbols-outlined text-primary"
                                        data-icon="my_location">my_location</span>
                                </div>
                            </div>
                        </div>
                        {/*  Map Pins  */}
                        {/*  Zone 1: Critical  */}
                        <div className="absolute top-[20%] left-[30%] pointer-events-auto flex flex-col items-center">
                            <div className="w-4 h-4 bg-error rounded-full pulse-error relative">
                                <div className="absolute -inset-2 rounded-full border border-error/50 animate-ping"></div>
                            </div>
                            <div
                                className="mt-2 bg-surface-container-highest/90 backdrop-blur-sm px-2 py-1 rounded text-[10px] font-bold text-error border border-error/30">
                                ZONE A: CRITICAL</div>
                        </div>
                        {/*  Zone 2: Severe  */}
                        <div className="absolute top-[60%] left-[15%] pointer-events-auto flex flex-col items-center">
                            <div className="w-4 h-4 bg-primary-container rounded-full relative">
                                <div className="absolute -inset-1 rounded-full border border-primary-container/50"></div>
                            </div>
                            <div
                                className="mt-2 bg-surface-container-highest/90 backdrop-blur-sm px-2 py-1 rounded text-[10px] font-bold text-primary-container border border-primary-container/30">
                                ZONE B: SEVERE</div>
                        </div>
                        {/*  Zone 3: Watch  */}
                        <div className="absolute top-[45%] left-[55%] pointer-events-auto flex flex-col items-center">
                            <div className="w-4 h-4 bg-tertiary rounded-full relative"></div>
                            <div
                                className="mt-2 bg-surface-container-highest/90 backdrop-blur-sm px-2 py-1 rounded text-[10px] font-bold text-tertiary border border-tertiary/30">
                                ZONE C: WATCH</div>
                        </div>
                        {/*  Zone 4: Stable  */}
                        <div className="absolute top-[75%] left-[70%] pointer-events-auto flex flex-col items-center">
                            <div className="w-4 h-4 bg-secondary rounded-full relative"></div>
                            <div
                                className="mt-2 bg-surface-container-highest/90 backdrop-blur-sm px-2 py-1 rounded text-[10px] font-bold text-secondary border border-secondary/30">
                                ZONE D: STABLE</div>
                        </div>
                        {/*  Zone 5: Stable  */}
                        <div className="absolute top-[15%] left-[80%] pointer-events-auto flex flex-col items-center">
                            <div className="w-4 h-4 bg-secondary rounded-full relative"></div>
                            <div
                                className="mt-2 bg-surface-container-highest/90 backdrop-blur-sm px-2 py-1 rounded text-[10px] font-bold text-secondary border border-secondary/30">
                                ZONE E: STABLE</div>
                        </div>
                    </div>
                </section>
                {/*  Right Metrics Panel  */}
                <aside className="flex-1 flex flex-col gap-4 min-w-[320px]">
                    {/*  Survival Rate Hero  */}
                    <div
                        className="bg-surface-container-low p-6 rounded-xl border-t border-surface-bright/20 shadow-xl flex flex-col items-center">
                        <div className="text-[10px] font-bold text-on-surface-variant uppercase tracking-[0.2em] mb-4">
                            Simulation Health</div>
                        <div className="relative w-32 h-32 flex items-center justify-center">
                            <svg className="absolute inset-0 w-full h-full transform -rotate-90">
                                <circle className="text-surface-container-highest" cx="64" cy="64" fill="transparent" r="60"
                                    stroke="currentColor" strokeWidth="8"></circle>
                                <circle className="text-secondary" cx="64" cy="64" fill="transparent" r="60"
                                    stroke="currentColor" strokeDasharray="377" strokeDashoffset="83"
                                    strokeWidth="8"></circle>
                            </svg>
                            <div className="text-4xl font-black tracking-tighter">78<span className="text-lg font-bold">%</span>
                            </div>
                        </div>
                        <div className="mt-4 text-xs font-medium text-secondary uppercase tracking-widest">Survival Rate
                        </div>
                    </div>
                    {/*  Metrics Grid  */}
                    <div className="grid grid-cols-2 gap-4">
                        <div className="bg-surface-container p-4 rounded-lg">
                            <div className="text-[9px] font-bold text-on-surface-variant uppercase tracking-widest mb-1">
                                Active Deaths</div>
                            <div className="text-xl font-bold text-error tracking-tight">1,402</div>
                        </div>
                        <div className="bg-surface-container p-4 rounded-lg">
                            <div className="text-[9px] font-bold text-on-surface-variant uppercase tracking-widest mb-1">
                                Total Relocated</div>
                            <div className="text-xl font-bold text-secondary tracking-tight">12.4k</div>
                        </div>
                    </div>
                    {/*  Resource & Status Stack  */}
                    <div className="bg-surface-container-low p-5 rounded-xl space-y-6">
                        <div className="space-y-3">
                            <div className="flex justify-between items-end">
                                <span
                                    className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest">Medical
                                    Resources</span>
                                <span className="text-xs font-bold text-on-surface">64%</span>
                            </div>
                            <div
                                className="h-4 bg-surface-container-lowest flex segmented-progress-bar rounded-sm overflow-hidden">
                                <div className="bg-secondary-container"></div>
                                <div className="bg-secondary-container"></div>
                                <div className="bg-secondary-container"></div>
                                <div className="bg-secondary-container"></div>
                                <div className="bg-secondary-container"></div>
                                <div className="bg-secondary-container"></div>
                                <div className="bg-secondary-container"></div>
                                <div className="bg-secondary-container opacity-30"></div>
                                <div className="bg-secondary-container opacity-30"></div>
                                <div className="bg-secondary-container opacity-30"></div>
                            </div>
                        </div>
                        <div className="space-y-3">
                            <div className="flex justify-between items-end">
                                <span
                                    className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest">Disease
                                    Risk Index</span>
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
                                        <span className="opacity-80">Alpha-One</span>
                                    </div>
                                    <span className="font-mono text-[10px] opacity-60">LOC: 35.6 N, 139.7 E</span>
                                </div>
                                <div className="flex items-center justify-between text-xs">
                                    <div className="flex items-center gap-2">
                                        <div className="w-1.5 h-1.5 rounded-full bg-error pulse-error"></div>
                                        <span className="opacity-80">Delta-Zero</span>
                                    </div>
                                    <span className="font-mono text-[10px] opacity-60">SIGNAL LOST</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </aside>
            </div>
            {/*  Bottom Decision Log Timeline  */}
            <footer
                className="h-48 bg-surface-container-low rounded-xl border border-outline-variant/10 flex flex-col overflow-hidden">
                <div
                    className="px-6 py-3 border-b border-outline-variant/15 flex justify-between items-center bg-surface-container">
                    <h3 className="text-[10px] font-black uppercase tracking-[0.3em] text-[#ffb3ad]">Decision Log &amp;
                        Reward Timeline</h3>
                    <div className="flex gap-4 items-center">
                        <span className="text-[10px] text-on-surface-variant uppercase">Filtering: High Reward Only</span>
                        <span className="material-symbols-outlined text-sm cursor-pointer hover:text-on-surface"
                            data-icon="filter_list">filter_list</span>
                    </div>
                </div>
                <div className="flex-1 overflow-y-auto p-4 space-y-2">
                    {/*  Log Item 1  */}
                    <div
                        className="flex gap-4 items-start p-3 hover:bg-surface-container-high transition-colors group rounded-md">
                        <div className="text-[10px] font-mono text-on-surface-variant opacity-40 pt-1">12:44:02.11</div>
                        <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                                <span
                                    className="text-xs font-bold uppercase tracking-widest text-secondary">[REDEPLOY]</span>
                                <span className="text-xs font-medium">Agent RL-42 moved to Shibuya Medical Center.</span>
                            </div>
                            <p className="text-[11px] text-on-surface-variant leading-relaxed">Reasoning: Resource density
                                below 20% threshold. Immediate intervention required to prevent zone transition to
                                Critical. Expected reward: +150 Survival Index.</p>
                        </div>
                        <div className="text-right">
                            <div className="text-xs font-bold text-secondary">+150.00</div>
                            <div className="text-[9px] uppercase opacity-40">Reward</div>
                        </div>
                    </div>
                    {/*  Log Item 2  */}
                    <div
                        className="flex gap-4 items-start p-3 hover:bg-surface-container-high transition-colors group rounded-md">
                        <div className="text-[10px] font-mono text-on-surface-variant opacity-40 pt-1">12:43:58.45</div>
                        <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                                <span className="text-xs font-bold uppercase tracking-widest text-error">[CASUALTY]</span>
                                <span className="text-xs font-medium">Evacuation fail at Block-G.</span>
                            </div>
                            <p className="text-[11px] text-on-surface-variant leading-relaxed">Outcome: Fire spread reached
                                Zone A extraction point before arrival. 14 casualties recorded. Penalty applied to Agent
                                Heuristic-7.</p>
                        </div>
                        <div className="text-right">
                            <div className="text-xs font-bold text-error">-420.00</div>
                            <div className="text-[9px] uppercase opacity-40">Penalty</div>
                        </div>
                    </div>
                    {/*  Log Item 3  */}
                    <div
                        className="flex gap-4 items-start p-3 hover:bg-surface-container-high transition-colors group rounded-md">
                        <div className="text-[10px] font-mono text-on-surface-variant opacity-40 pt-1">12:43:12.02</div>
                        <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                                <span
                                    className="text-xs font-bold uppercase tracking-widest text-tertiary">[RATIONING]</span>
                                <span className="text-xs font-medium">Policy update: Energy conservation mode active in
                                    District 3.</span>
                            </div>
                            <p className="text-[11px] text-on-surface-variant leading-relaxed">Reasoning: Grid stability
                                critical. Automated shutdown of non-essential cooling systems to maintain medical core
                                uptime.</p>
                        </div>
                        <div className="text-right">
                            <div className="text-xs font-bold text-tertiary">+12.00</div>
                            <div className="text-[9px] uppercase opacity-40">Reward</div>
                        </div>
                    </div>
                </div>
            </footer>
        
    </>
  );
};

export default Home;
