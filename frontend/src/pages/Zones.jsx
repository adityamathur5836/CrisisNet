import React, { useState, useEffect } from 'react';
import { fetchZone } from '../services/api';

const Zones = () => {
  const [selectedZoneId, setSelectedZoneId] = useState(1);
  const [zoneData, setZoneData] = useState(null);

  useEffect(() => {
    let active = true;
    const fetchCurrentZone = async () => {
      try {
        const data = await fetchZone(selectedZoneId);
        if (active) setZoneData(data);
      } catch (err) {
        console.error(err);
      }
    };
    
    fetchCurrentZone();
    const interval = setInterval(fetchCurrentZone, 1500);
    
    return () => {
      active = false;
      clearInterval(interval);
    };
  }, [selectedZoneId]);

  if (!zoneData) return <div className="p-8 text-on-surface">Loading Zone Data...</div>;

  const z = zoneData;
  const totalPop = z.healthy + z.injured + z.critical + z.deceased;
  const pHealthy = totalPop > 0 ? ((z.healthy / totalPop) * 100).toFixed(1) : 0;
  const pInjured = totalPop > 0 ? ((z.injured / totalPop) * 100).toFixed(1) : 0;
  const pCritical = totalPop > 0 ? ((z.critical / totalPop) * 100).toFixed(1) : 0;
  const pDeceased = totalPop > 0 ? ((z.deceased / totalPop) * 100).toFixed(1) : 0;

  // Use arbitrary scales for progress bars roughly matching environment.py initial ranges
  const fPct = Math.min(100, (z.food / 500) * 100);
  const wPct = Math.min(100, (z.water / 800) * 100);
  const fuelPct = Math.min(100, (z.fuel / 300) * 100);
  const mPct = Math.min(100, (z.medical / 150) * 100);

  const isCriticalAlert = z.critical > z.hospital_capacity || z.food === 0 || z.water === 0;
  const roadClearance = Math.round(z.road_access * 100);
  const hospCapPct = z.hospital_capacity > 0 ? Math.round((z.critical / z.hospital_capacity) * 100) : 0;

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
                  ZONE-{String(selectedZoneId).padStart(2, '0')}: SECTOR {z.id}
                  <span className="text-label-sm font-normal text-on-surface-variant uppercase tracking-widest border border-outline-variant/20 px-2 py-0.5 rounded">ID: NW-42{z.id}</span>
              </h1>
              <p className="text-on-surface-variant mt-1">Population Density: {totalPop > 2000 ? 'High' : 'Moderate'} | Alert Level: {isCriticalAlert ? 'Critical' : 'Stable'}</p>
          </div>
          <div className="flex gap-2">
              {[1, 2, 3, 4, 5].map(id => (
                  <button 
                      key={id}
                      onClick={() => setSelectedZoneId(id)}
                      className={`px-4 py-2 rounded-lg font-bold text-sm uppercase tracking-widest border transition-colors ${
                          selectedZoneId === id 
                              ? 'bg-surface-variant text-on-surface border-outline/50' 
                              : 'bg-surface-container-high text-on-surface-variant border-outline-variant/15 hover:bg-surface-variant'
                      }`}
                  >
                      Zone {id}
                  </button>
              ))}
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
                                  <span className="text-sm font-mono text-on-surface">37.77{z.id}9° N, 122.41{z.id}4° W</span>
                              </div>
                              <div className="flex items-center gap-4">
                                  <span className="text-xs text-on-surface-variant">ELEVATION</span>
                                  <span className="text-sm font-mono text-on-surface">{50 + z.id * 2}m ASL</span>
                              </div>
                          </div>
                      </div>
                      <div className="flex flex-col gap-2 pointer-events-auto">
                          <button className="bg-surface-container-highest/80 backdrop-blur-md p-2 rounded border border-white/5 text-on-surface">
                              <span className="material-symbols-outlined" data-icon="layers">layers</span>
                          </button>
                      </div>
                  </div>
                  <div className="flex gap-4 pointer-events-auto">
                      <div className="glass-overlay px-4 py-2 rounded-lg border border-white/5 flex items-center gap-2">
                          <span className={`w-2 h-2 rounded-full ${z.road_access < 0.5 ? 'bg-error' : 'bg-secondary'}`}></span>
                          <span className="text-xs font-bold uppercase tracking-widest text-on-surface">{Math.floor((1 - z.road_access) * 10)} Critical Blockages</span>
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
                          <span className="text-xl font-black text-on-surface">{pHealthy}% <span className="text-xs font-normal text-on-surface-variant tracking-tighter">/ {z.healthy}</span></span>
                      </div>
                      <div className="h-2 w-full bg-surface-container-highest rounded-full overflow-hidden flex">
                          <div className="h-full bg-secondary transition-all" style={{ width: `${pHealthy}%` }}></div>
                      </div>
                  </div>

                  {/*  Injured  */}
                  <div>
                      <div className="flex justify-between items-end mb-2">
                          <div className="flex items-center gap-2">
                              <span className="material-symbols-outlined text-sm text-tertiary" data-icon="warning">warning</span>
                              <span className="text-label-md font-bold uppercase tracking-wider text-on-surface-variant">Injured</span>
                          </div>
                          <span className="text-xl font-black text-on-surface">{pInjured}% <span className="text-xs font-normal text-on-surface-variant tracking-tighter">/ {z.injured}</span></span>
                      </div>
                      <div className="h-2 w-full bg-surface-container-highest rounded-full overflow-hidden flex">
                          <div className="h-full bg-tertiary transition-all" style={{ width: `${pInjured}%` }}></div>
                      </div>
                  </div>

                  {/*  Critical  */}
                  <div>
                      <div className="flex justify-between items-end mb-2">
                          <div className="flex items-center gap-2">
                              <span className="material-symbols-outlined text-sm text-error" data-icon="emergency">emergency</span>
                              <span className="text-label-md font-bold uppercase tracking-wider text-on-surface-variant">Critical</span>
                          </div>
                          <span className="text-xl font-black text-on-surface">{pCritical}% <span className="text-xs font-normal text-on-surface-variant tracking-tighter">/ {z.critical}</span></span>
                      </div>
                      <div className="h-2 w-full bg-surface-container-highest rounded-full overflow-hidden flex">
                          <div className="h-full bg-error transition-all" style={{ width: `${pCritical}%` }}></div>
                      </div>
                  </div>

                  {/*  Deceased  */}
                  <div>
                      <div className="flex justify-between items-end mb-2">
                          <div className="flex items-center gap-2">
                              <span className="material-symbols-outlined text-sm opacity-50" data-icon="person_off">person_off</span>
                              <span className="text-label-md font-bold uppercase tracking-wider text-on-surface-variant">Deceased</span>
                          </div>
                          <span className="text-xl font-black text-on-surface">{pDeceased}% <span className="text-xs font-normal text-on-surface-variant tracking-tighter">/ {z.deceased}</span></span>
                      </div>
                      <div className="h-2 w-full bg-surface-container-highest rounded-full overflow-hidden flex">
                          <div className="h-full bg-on-surface-variant/20 transition-all" style={{ width: `${pDeceased}%` }}></div>
                      </div>
                  </div>
              </div>
              
              {isCriticalAlert && (
                  <div className="mt-8 p-4 bg-error/10 border border-error/20 rounded-lg">
                      <p className="text-xs text-error font-medium leading-relaxed">
                          <span className="font-bold">URGENT:</span> 
                          {z.critical > z.hospital_capacity && ` Critical patient influx (${z.critical}) exceeds local medical capacity (${z.hospital_capacity}). `}
                          {z.food === 0 && ` Severe food shortage detected. `}
                          {z.water === 0 && ` Severe water shortage detected. `}
                          Immediate triage requested.
                      </p>
                  </div>
              )}
          </section>

          {/*  Resource Card  */}
          <section className="col-span-12 md:col-span-6 lg:col-span-4 bg-surface-container rounded-xl p-6 border border-outline-variant/10">
              <div className="flex items-center justify-between mb-8">
                  <h3 className="text-title-lg font-extrabold tracking-tight text-on-surface">RESOURCES</h3>
                  <span className="material-symbols-outlined text-tertiary" data-icon="inventory_2">inventory_2</span>
              </div>
              <div className="space-y-6">
                  {/*  Water  */}
                  <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded bg-surface-container-high flex items-center justify-center border border-outline-variant/20">
                          <span className="material-symbols-outlined text-secondary" data-icon="water_drop">water_drop</span>
                      </div>
                      <div className="flex-1">
                          <div className="flex justify-between text-xs font-bold uppercase tracking-widest text-on-surface-variant mb-1">
                              <span>Potable Water</span>
                              <span className={z.water > 0 ? "text-secondary" : "text-error"}>{z.water} Units</span>
                          </div>
                          <div className="flex gap-1 h-2">
                              {Array.from({ length: 7 }).map((_, i) => (
                                  <div key={i} className={`flex-1 ${z.water === 0 ? 'bg-error' : 'bg-secondary'} rounded-sm ${i >= Math.round(wPct / (100/7)) ? 'opacity-30 bg-surface-container-highest' : ''}`}></div>
                              ))}
                          </div>
                      </div>
                  </div>

                  {/*  Food  */}
                  <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded bg-surface-container-high flex items-center justify-center border border-outline-variant/20">
                          <span className="material-symbols-outlined text-tertiary" data-icon="restaurant">restaurant</span>
                      </div>
                      <div className="flex-1">
                          <div className="flex justify-between text-xs font-bold uppercase tracking-widest text-on-surface-variant mb-1">
                              <span>Food Supply</span>
                              <span className={z.food > 0 ? "text-tertiary" : "text-error"}>{z.food} Units</span>
                          </div>
                          <div className="flex gap-1 h-2">
                              {Array.from({ length: 7 }).map((_, i) => (
                                  <div key={i} className={`flex-1 ${z.food === 0 ? 'bg-error' : 'bg-tertiary'} rounded-sm ${i >= Math.round(fPct / (100/7)) ? 'opacity-30 bg-surface-container-highest' : ''}`}></div>
                              ))}
                          </div>
                      </div>
                  </div>

                  {/*  Medical  */}
                  <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded bg-surface-container-high flex items-center justify-center border border-outline-variant/20">
                          <span className="material-symbols-outlined text-error" data-icon="medication">medication</span>
                      </div>
                      <div className="flex-1">
                          <div className="flex justify-between text-xs font-bold uppercase tracking-widest text-on-surface-variant mb-1">
                              <span>Medical Kits</span>
                              <span className="text-error">{z.medical} Units</span>
                          </div>
                          <div className="flex gap-1 h-2">
                              {Array.from({ length: 7 }).map((_, i) => (
                                  <div key={i} className={`flex-1 bg-error rounded-sm ${i >= Math.round(mPct / (100/7)) ? 'opacity-30 bg-surface-container-highest' : ''}`}></div>
                              ))}
                          </div>
                      </div>
                  </div>

                  {/*  Fuel  */}
                  <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded bg-surface-container-high flex items-center justify-center border border-outline-variant/20">
                          <span className="material-symbols-outlined text-secondary" data-icon="local_gas_station">local_gas_station</span>
                      </div>
                      <div className="flex-1">
                          <div className="flex justify-between text-xs font-bold uppercase tracking-widest text-on-surface-variant mb-1">
                              <span>Fuel Reserve</span>
                              <span className="text-secondary">{z.fuel} Units</span>
                          </div>
                          <div className="flex gap-1 h-2">
                              {Array.from({ length: 7 }).map((_, i) => (
                                  <div key={i} className={`flex-1 bg-secondary rounded-sm ${i >= Math.round(fuelPct / (100/7)) ? 'opacity-30 bg-surface-container-highest' : ''}`}></div>
                              ))}
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
                  <div className={`p-4 bg-surface-container-low rounded border ${z.road_access < 0.5 ? 'border-error/30' : 'border-outline-variant/10'}`}>
                      <div className="flex items-center justify-between mb-3">
                          <span className={`material-symbols-outlined ${z.road_access < 0.5 ? 'text-error' : 'text-secondary'}`} data-icon="foundation">foundation</span>
                          <span className={`text-[10px] font-bold uppercase tracking-widest ${z.road_access < 0.5 ? 'text-error' : 'text-secondary'}`}>{z.road_access < 0.5 ? "Degraded" : "Active"}</span>
                      </div>
                      <div className="text-sm font-bold text-on-surface mb-1 uppercase tracking-tight">Roads</div>
                      <div className="text-[10px] text-on-surface-variant uppercase tracking-widest">Clearance: {roadClearance}%</div>
                  </div>
                  <div className={`p-4 bg-surface-container-low rounded border ${hospCapPct > 100 ? 'border-error/30' : 'border-outline-variant/10'}`}>
                      <div className="flex items-center justify-between mb-3">
                          <span className={`material-symbols-outlined ${hospCapPct > 100 ? 'text-error' : 'text-tertiary'}`} data-icon="local_hospital">local_hospital</span>
                          <span className={`text-[10px] font-bold uppercase tracking-widest ${hospCapPct > 100 ? 'text-error' : 'text-tertiary'}`}>{hospCapPct > 100 ? "Overloaded" : "Strained"}</span>
                      </div>
                      <div className="text-sm font-bold text-on-surface mb-1 uppercase tracking-tight">Hospitals</div>
                      <div className="text-[10px] text-on-surface-variant uppercase tracking-widest">Cap: {hospCapPct}%</div>
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
                          <span className="material-symbols-outlined text-secondary" data-icon="sensors">sensors</span>
                          <span className="text-[10px] font-bold uppercase tracking-widest text-secondary">Active</span>
                      </div>
                      <div className="text-sm font-bold text-on-surface mb-1 uppercase tracking-tight">Comms</div>
                      <div className="text-[10px] text-on-surface-variant uppercase tracking-widest">Relay Active</div>
                  </div>
              </div>

              <div className="mt-8">
                 <h4 className="text-xs font-bold text-on-surface-variant uppercase tracking-widest mb-4">Active Teams In Zone</h4>
                 {z.teams_present && z.teams_present.length > 0 ? (
                    <div className="space-y-2">
                       {z.teams_present.map((team, idx) => (
                           <div key={idx} className="flex items-center gap-2 px-3 py-2 bg-surface-container-highest rounded border border-outline-variant/10">
                                <span className="material-symbols-outlined text-sm text-primary" data-icon="engineering">engineering</span>
                                <span className="text-xs font-bold uppercase tracking-widest text-on-surface">{team.replace('_', ' ')}</span>
                           </div>
                       ))}
                    </div>
                 ) : (
                    <div className="text-xs text-on-surface-variant/50 italic p-3 border border-dashed border-outline-variant/20 rounded bg-surface-container-lowest">
                        No field teams currently deployed in this sector.
                    </div>
                 )}
              </div>
          </section>
      </div>
    </>
  );
};

export default Zones;
