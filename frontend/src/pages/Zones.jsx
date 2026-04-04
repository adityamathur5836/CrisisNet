import React from 'react';

const Zones = () => {
  return (
    <>
      
{/*  Zone Header  */}
<header className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-8">
<div>
<div className="flex items-center gap-2 mb-2">
<span className="text-xs font-bold uppercase tracking-[0.2em] text-secondary">Operational</span>
<div className="w-2 h-2 rounded-full bg-secondary shadow-[0_0_8px_#4ae176]"></div>
</div>
<h1 className="text-4xl font-extrabold tracking-tighter text-on-surface flex items-center gap-4">
                    ZONE-07: REDWOOD SECTOR
                    <span className="text-label-sm font-normal text-on-surface-variant uppercase tracking-widest border border-outline-variant/20 px-2 py-0.5 rounded">ID: NW-429</span>
</h1>
<p className="text-on-surface-variant mt-1">Socio-Economic Hub | Population Density: High | Alert Level: Gamma</p>
</div>
<div className="flex gap-3">
<button className="bg-surface-container-high text-on-surface px-6 py-2.5 rounded-lg font-bold text-sm uppercase tracking-widest border border-outline-variant/15 hover:bg-surface-variant transition-colors">
                    Evacuation Plan
                </button>
<button className="kinetic-gradient text-on-primary px-6 py-2.5 rounded-lg font-bold text-sm uppercase tracking-widest shadow-xl">
                    Deploy Reinforcements
                </button>
</div>
</header>
{/*  Bento Grid Layout  */}
<div className="grid grid-cols-12 gap-6">
{/*  Map Insight (Asymmetric Large Module)  */}
<section className="col-span-12 lg:col-span-8 bg-surface-container-low rounded-xl overflow-hidden relative border border-outline-variant/5 min-h-[400px]">
<div className="absolute inset-0 z-0 grayscale opacity-40 mix-blend-screen overflow-hidden">
<img alt="Zone Map" className="w-full h-full object-cover" data-alt="detailed blueprint style architectural map of an urban district with glowing red and green tactical overlays" data-location="San Francisco" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBXddIeyCZTGdmG-OwrRproQnJ7RT-fQ5WSIX0w7ev-LcmfH9Q01L9Wmx7472n9tbXbCrjO2TTzWKwpMAl6zAt7Va0aAGf8ZFHo0L5jTKU7NjomEon0wMkCtDadgS7N3cOF-a8FRTnNOPJVvr5768vZMnI1tFMgxigkTOlQUpzOZzUeNgMzfd3NC-ebaVNs_sNdmzGtopXBSYM5AFf4SOq8nvucuBtsj_4GhNb7-9pB9S_5VAaU8j0CRDzQQPhmnsVU29HSA-Lb5T-i"/>
</div>
<div className="absolute inset-0 bg-gradient-to-t from-surface-container-low via-transparent to-transparent z-10"></div>
<div className="relative z-20 p-6 flex flex-col h-full justify-between pointer-events-none">
<div className="flex justify-between items-start pointer-events-auto">
<div className="glass-overlay p-4 rounded-xl border border-white/5">
<h3 className="text-label-md font-bold uppercase tracking-widest text-primary mb-2">Geospatial Awareness</h3>
<div className="space-y-2">
<div className="flex items-center gap-4">
<span className="text-xs text-on-surface-variant">CENTROID</span>
<span className="text-sm font-mono text-on-surface">37.7749° N, 122.4194° W</span>
</div>
<div className="flex items-center gap-4">
<span className="text-xs text-on-surface-variant">ELEVATION</span>
<span className="text-sm font-mono text-on-surface">52m ASL</span>
</div>
</div>
</div>
<div className="flex flex-col gap-2 pointer-events-auto">
<button className="bg-surface-container-highest/80 backdrop-blur-md p-2 rounded border border-white/5 text-on-surface">
<span className="material-symbols-outlined" data-icon="layers">layers</span>
</button>
<button className="bg-surface-container-highest/80 backdrop-blur-md p-2 rounded border border-white/5 text-on-surface">
<span className="material-symbols-outlined" data-icon="my_location">my_location</span>
</button>
</div>
</div>
<div className="flex gap-4 pointer-events-auto">
<div className="glass-overlay px-4 py-2 rounded-lg border border-white/5 flex items-center gap-2">
<span className="w-2 h-2 rounded-full bg-error"></span>
<span className="text-xs font-bold uppercase tracking-widest text-on-surface">2 Critical Blockages</span>
</div>
<div className="glass-overlay px-4 py-2 rounded-lg border border-white/5 flex items-center gap-2">
<span className="w-2 h-2 rounded-full bg-secondary"></span>
<span className="text-xs font-bold uppercase tracking-widest text-on-surface">Safe Corridor Open</span>
</div>
</div>
</div>
</section>
{/*  Population Card (Right Side)  */}
<section className="col-span-12 lg:col-span-4 bg-surface-container rounded-xl p-6 border border-outline-variant/10">
<div className="flex items-center justify-between mb-8">
<h3 className="text-title-lg font-extrabold tracking-tight text-on-surface">POPULATION STATUS</h3>
<span className="material-symbols-outlined text-secondary" data-icon="groups">groups</span>
</div>
<div className="space-y-6">
{/*  Healthy  */}
<div>
<div className="flex justify-between items-end mb-2">
<div className="flex items-center gap-2">
<span className="material-symbols-outlined text-sm text-secondary" data-icon="check_circle">check_circle</span>
<span className="text-label-md font-bold uppercase tracking-wider text-on-surface-variant">Healthy</span>
</div>
<span className="text-xl font-black text-on-surface">62% <span className="text-xs font-normal text-on-surface-variant tracking-tighter">/ 14.2k</span></span>
</div>
<div className="h-2 w-full bg-surface-container-highest rounded-full overflow-hidden flex">
<div className="h-full bg-secondary w-[62%]"></div>
</div>
</div>
{/*  Injured  */}
<div>
<div className="flex justify-between items-end mb-2">
<div className="flex items-center gap-2">
<span className="material-symbols-outlined text-sm text-tertiary" data-icon="warning">warning</span>
<span className="text-label-md font-bold uppercase tracking-wider text-on-surface-variant">Injured</span>
</div>
<span className="text-xl font-black text-on-surface">28% <span className="text-xs font-normal text-on-surface-variant tracking-tighter">/ 6.4k</span></span>
</div>
<div className="h-2 w-full bg-surface-container-highest rounded-full overflow-hidden flex">
<div className="h-full bg-tertiary w-[28%]"></div>
</div>
</div>
{/*  Critical  */}
<div>
<div className="flex justify-between items-end mb-2">
<div className="flex items-center gap-2">
<span className="material-symbols-outlined text-sm text-error" data-icon="emergency">emergency</span>
<span className="text-label-md font-bold uppercase tracking-wider text-on-surface-variant">Critical</span>
</div>
<span className="text-xl font-black text-on-surface">7.5% <span className="text-xs font-normal text-on-surface-variant tracking-tighter">/ 1.7k</span></span>
</div>
<div className="h-2 w-full bg-surface-container-highest rounded-full overflow-hidden flex">
<div className="h-full bg-error w-[7.5%]"></div>
</div>
</div>
{/*  Deceased  */}
<div>
<div className="flex justify-between items-end mb-2">
<div className="flex items-center gap-2">
<span className="material-symbols-outlined text-sm opacity-50" data-icon="person_off">person_off</span>
<span className="text-label-md font-bold uppercase tracking-wider text-on-surface-variant">Deceased</span>
</div>
<span className="text-xl font-black text-on-surface">2.5% <span className="text-xs font-normal text-on-surface-variant tracking-tighter">/ 0.5k</span></span>
</div>
<div className="h-2 w-full bg-surface-container-highest rounded-full overflow-hidden flex">
<div className="h-full bg-on-surface-variant/20 w-[2.5%]"></div>
</div>
</div>
</div>
<div className="mt-8 p-4 bg-error/10 border border-error/20 rounded-lg">
<p className="text-xs text-error font-medium leading-relaxed">
<span className="font-bold">URGENT:</span> Critical patient influx exceeds local medical capacity by 12%. Triage requested.
                    </p>
</div>
</section>
{/*  Resource Card  */}
<section className="col-span-12 md:col-span-6 lg:col-span-4 bg-surface-container rounded-xl p-6 border border-outline-variant/10">
<div className="flex items-center justify-between mb-8">
<h3 className="text-title-lg font-extrabold tracking-tight text-on-surface">RESOURCES</h3>
<span className="material-symbols-outlined text-tertiary" data-icon="inventory_2">inventory_2</span>
</div>
<div className="space-y-6">
{/*  Resource Item  */}
<div className="flex items-center gap-4">
<div className="w-10 h-10 rounded bg-surface-container-high flex items-center justify-center border border-outline-variant/20">
<span className="material-symbols-outlined text-secondary" data-icon="water_drop">water_drop</span>
</div>
<div className="flex-1">
<div className="flex justify-between text-xs font-bold uppercase tracking-widest text-on-surface-variant mb-1">
<span>Potable Water</span>
<span className="text-secondary">12 Days Rem.</span>
</div>
<div className="flex gap-1 h-2">
<div className="flex-1 bg-secondary rounded-sm"></div>
<div className="flex-1 bg-secondary rounded-sm"></div>
<div className="flex-1 bg-secondary rounded-sm"></div>
<div className="flex-1 bg-secondary rounded-sm"></div>
<div className="flex-1 bg-secondary rounded-sm"></div>
<div className="flex-1 bg-surface-container-highest rounded-sm opacity-30"></div>
<div className="flex-1 bg-surface-container-highest rounded-sm opacity-30"></div>
</div>
</div>
</div>
{/*  Resource Item  */}
<div className="flex items-center gap-4">
<div className="w-10 h-10 rounded bg-surface-container-high flex items-center justify-center border border-outline-variant/20">
<span className="material-symbols-outlined text-tertiary" data-icon="restaurant">restaurant</span>
</div>
<div className="flex-1">
<div className="flex justify-between text-xs font-bold uppercase tracking-widest text-on-surface-variant mb-1">
<span>Food Supply</span>
<span className="text-tertiary">4 Days Rem.</span>
</div>
<div className="flex gap-1 h-2">
<div className="flex-1 bg-tertiary rounded-sm"></div>
<div className="flex-1 bg-tertiary rounded-sm"></div>
<div className="flex-1 bg-surface-container-highest rounded-sm opacity-30"></div>
<div className="flex-1 bg-surface-container-highest rounded-sm opacity-30"></div>
<div className="flex-1 bg-surface-container-highest rounded-sm opacity-30"></div>
<div className="flex-1 bg-surface-container-highest rounded-sm opacity-30"></div>
<div className="flex-1 bg-surface-container-highest rounded-sm opacity-30"></div>
</div>
</div>
</div>
{/*  Resource Item  */}
<div className="flex items-center gap-4">
<div className="w-10 h-10 rounded bg-surface-container-high flex items-center justify-center border border-outline-variant/20">
<span className="material-symbols-outlined text-error" data-icon="medication">medication</span>
</div>
<div className="flex-1">
<div className="flex justify-between text-xs font-bold uppercase tracking-widest text-on-surface-variant mb-1">
<span>Medical Kits</span>
<span className="text-error">1 Day Rem.</span>
</div>
<div className="flex gap-1 h-2">
<div className="flex-1 bg-error rounded-sm"></div>
<div className="flex-1 bg-surface-container-highest rounded-sm opacity-30"></div>
<div className="flex-1 bg-surface-container-highest rounded-sm opacity-30"></div>
<div className="flex-1 bg-surface-container-highest rounded-sm opacity-30"></div>
<div className="flex-1 bg-surface-container-highest rounded-sm opacity-30"></div>
<div className="flex-1 bg-surface-container-highest rounded-sm opacity-30"></div>
<div className="flex-1 bg-surface-container-highest rounded-sm opacity-30"></div>
</div>
</div>
</div>
{/*  Resource Item  */}
<div className="flex items-center gap-4">
<div className="w-10 h-10 rounded bg-surface-container-high flex items-center justify-center border border-outline-variant/20">
<span className="material-symbols-outlined text-secondary" data-icon="local_gas_station">local_gas_station</span>
</div>
<div className="flex-1">
<div className="flex justify-between text-xs font-bold uppercase tracking-widest text-on-surface-variant mb-1">
<span>Fuel Reserve</span>
<span className="text-secondary">18 Days Rem.</span>
</div>
<div className="flex gap-1 h-2">
<div className="flex-1 bg-secondary rounded-sm"></div>
<div className="flex-1 bg-secondary rounded-sm"></div>
<div className="flex-1 bg-secondary rounded-sm"></div>
<div className="flex-1 bg-secondary rounded-sm"></div>
<div className="flex-1 bg-secondary rounded-sm"></div>
<div className="flex-1 bg-secondary rounded-sm"></div>
<div className="flex-1 bg-secondary rounded-sm"></div>
</div>
</div>
</div>
</div>
</section>
{/*  Infrastructure Card  */}
<section className="col-span-12 md:col-span-6 lg:col-span-4 bg-surface-container rounded-xl p-6 border border-outline-variant/10">
<div className="flex items-center justify-between mb-8">
<h3 className="text-title-lg font-extrabold tracking-tight text-on-surface">INFRASTRUCTURE</h3>
<span className="material-symbols-outlined text-primary" data-icon="domain">domain</span>
</div>
<div className="grid grid-cols-2 gap-4">
<div className="p-4 bg-surface-container-low rounded border border-outline-variant/10">
<div className="flex items-center justify-between mb-3">
<span className="material-symbols-outlined text-secondary" data-icon="foundation">foundation</span>
<span className="text-[10px] font-bold uppercase tracking-widest text-secondary">Active</span>
</div>
<div className="text-sm font-bold text-on-surface mb-1 uppercase tracking-tight">Roads</div>
<div className="text-[10px] text-on-surface-variant uppercase tracking-widest">Clearance: 92%</div>
</div>
<div className="p-4 bg-surface-container-low rounded border border-outline-variant/10">
<div className="flex items-center justify-between mb-3">
<span className="material-symbols-outlined text-tertiary" data-icon="local_hospital">local_hospital</span>
<span className="text-[10px] font-bold uppercase tracking-widest text-tertiary">Impaired</span>
</div>
<div className="text-sm font-bold text-on-surface mb-1 uppercase tracking-tight">Hospitals</div>
<div className="text-[10px] text-on-surface-variant uppercase tracking-widest">Cap: 112% (Over)</div>
</div>
<div className="p-4 bg-surface-container-low rounded border border-outline-variant/10">
<div className="flex items-center justify-between mb-3">
<span className="material-symbols-outlined text-secondary" data-icon="bolt">bolt</span>
<span className="text-[10px] font-bold uppercase tracking-widest text-secondary">Active</span>
</div>
<div className="text-sm font-bold text-on-surface mb-1 uppercase tracking-tight">Power Grid</div>
<div className="text-[10px] text-on-surface-variant uppercase tracking-widest">Backup Online</div>
</div>
<div className="p-4 bg-surface-container-low rounded border border-outline-variant/10">
<div className="flex items-center justify-between mb-3">
<span className="material-symbols-outlined text-error" data-icon="sensors">sensors</span>
<span className="text-[10px] font-bold uppercase tracking-widest text-error">Down</span>
</div>
<div className="text-sm font-bold text-on-surface mb-1 uppercase tracking-tight">Comms</div>
<div className="text-[10px] text-on-surface-variant uppercase tracking-widest">Node 4 Offline</div>
</div>
</div>
<div className="mt-6 flex items-center justify-between px-2 py-3 bg-surface-container-high rounded border border-outline-variant/5">
<div className="flex items-center gap-2">
<span className="material-symbols-outlined text-sm text-tertiary" data-icon="construction">construction</span>
<span className="text-xs font-bold uppercase tracking-widest text-on-surface">Scheduled Maintenance</span>
</div>
<span className="text-[10px] font-bold text-on-surface-variant">T - 04:22:00</span>
</div>
</section>
{/*  Active Teams Card  */}
<section className="col-span-12 lg:col-span-4 bg-surface-container rounded-xl p-6 border border-outline-variant/10">
<div className="flex items-center justify-between mb-8">
<h3 className="text-title-lg font-extrabold tracking-tight text-on-surface">ACTIVE TEAMS</h3>
<span className="material-symbols-outlined text-secondary" data-icon="engineering">engineering</span>
</div>
<div className="space-y-3">
{/*  Team Row  */}
<div className="flex items-center gap-4 p-3 bg-surface-container-low rounded-lg border border-transparent hover:border-outline-variant/20 transition-all cursor-pointer group">
<div className="relative">
<img alt="Strike Team 7" className="w-10 h-10 rounded" data-alt="tactical strike team patch with shield icon and dark grey colors" src="https://lh3.googleusercontent.com/aida-public/AB6AXuA80e-5RYa6Rj_79YfRGjpYbJ0_AhTs8l1ijsJj9_IqVnH3Mp2TIM-RIBmBkpeFPVIRr2oGNQHMStWAklyLw_9j1A-BZctIBcRSpWtwsk0uDxivYDz0yvrF6BWMDrHXIObiopAjnxt9Fzqlm18wSM6xcAdSAOZPHTHDC7G8BLXlZv_6uDOVh2pOEPRGgJlFoTRVilUBpM25vCJqS4boSSTExcrt2cVz3lNxeVKs4X61PIqTpUCjWteQ0TwPjNsP8nlSX-dQQQ99iPJR"/>
<div className="absolute -bottom-1 -right-1 w-3 h-3 bg-secondary rounded-full border-2 border-surface-container-low"></div>
</div>
<div className="flex-1">
<div className="flex justify-between">
<span className="text-sm font-bold text-on-surface group-hover:text-primary transition-colors">STRIKE TEAM 7</span>
<span className="text-[10px] font-bold text-secondary uppercase tracking-widest">En Route</span>
</div>
<div className="text-xs text-on-surface-variant">Objective: Comms Node 4 Repair</div>
</div>
</div>
{/*  Team Row  */}
<div className="flex items-center gap-4 p-3 bg-surface-container-low rounded-lg border border-transparent hover:border-outline-variant/20 transition-all cursor-pointer group">
<div className="relative">
<img alt="Med Team Alpha" className="w-10 h-10 rounded" data-alt="medical red cross tactical icon on dark background" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDcybWyprmDzqzKzr-ouTWVEyFwbFuaO9sR2ukumEiIP8nz03yGf8PdILSmpB73QvRCuwWDcmIvs6tWKX6szwAnLaYuGR83NpEwfAE49kL3trXQNTpgy-FFbeE7F7TuyHkXayerRyzteunb4VlBwv-avWhU8GHPTaPoVJE6_xPm6bAZm1HWBkvxM-IM7O_d9q_OBod6YqDU4rFkA8Ks_45N431dZ1qCWPjfSM51KvopXg6ILzzVLqDykxk2buDLoUp_2gkVvayVXnoC"/>
<div className="absolute -bottom-1 -right-1 w-3 h-3 bg-tertiary rounded-full border-2 border-surface-container-low"></div>
</div>
<div className="flex-1">
<div className="flex justify-between">
<span className="text-sm font-bold text-on-surface group-hover:text-primary transition-colors">MED-UNIT ALPHA</span>
<span className="text-[10px] font-bold text-tertiary uppercase tracking-widest">Engaged</span>
</div>
<div className="text-xs text-on-surface-variant">Location: Sector Hospital 2</div>
</div>
</div>
{/*  Team Row  */}
<div className="flex items-center gap-4 p-3 bg-surface-container-low rounded-lg border border-transparent hover:border-outline-variant/20 transition-all cursor-pointer group">
<div className="relative">
<img alt="Logistics 4" className="w-10 h-10 rounded" data-alt="cargo truck logistics icon on dark tactical patch" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBcw5zO_IHW5wyeBL1dl3CO074IdzWvirWEVftdMdDQG60_-2rMC5TZjEZGQs2YCMfpo8KN2jCJMLmKTNxXOFopsF0-UYtYjG8QOjZjjte9T1T8rtvid1Xl0ZcdGGS-RaIUkCkMJkxF0V4Yuojy2sUBHw3bAL-LedI19pPdeulq_NrvMbQyAdyZ64rZ1rR3WLPsqu8hhWeRdDC5_ScU6LTuvC6b2clbsAEpQKukdb_brcjHzU8FET1D2uKMF9DYu2Kb85rKfeQu6CCz"/>
<div className="absolute -bottom-1 -right-1 w-3 h-3 bg-secondary rounded-full border-2 border-surface-container-low"></div>
</div>
<div className="flex-1">
<div className="flex justify-between">
<span className="text-sm font-bold text-on-surface group-hover:text-primary transition-colors">LOGISTICS-4</span>
<span className="text-[10px] font-bold text-secondary uppercase tracking-widest">Standby</span>
</div>
<div className="text-xs text-on-surface-variant">HQ Depot A-12</div>
</div>
</div>
</div>
<button className="w-full mt-6 py-2 bg-surface-container-highest text-xs font-bold uppercase tracking-[0.2em] text-on-surface-variant border border-outline-variant/10 rounded-lg hover:bg-surface-variant transition-colors">
                    Manage Deployments
                </button>
</section>
</div>

    </>
  );
};

export default Zones;
