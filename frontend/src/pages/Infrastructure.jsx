import React, { useState, useEffect } from 'react';
import { fetchState } from '../services/api';

const Infrastructure = () => {
    const [simState, setSimState] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        let active = true;
        const load = async () => {
            try {
                const state = await fetchState();
                if (active) setSimState(state);
            } catch(e) {
                console.error(e);
            } finally {
                if (active) setIsLoading(false);
            }
        };
        load();
        const interval = setInterval(load, 2000);
        return () => {
            active = false;
            clearInterval(interval);
        };
    }, []);

    if (isLoading || !simState) return <div className="p-8 text-on-surface">Loading Infrastructure Telemetry...</div>;

    const zones = simState.zones || [];

    return (
        <div className="p-8 pb-32">
            <div className="mb-10 flex flex-col md:flex-row md:justify-between md:items-end gap-6">
                <div>
                    <h1 className="text-4xl font-black tracking-tight text-on-surface mb-2">Global Infrastructure</h1>
                    <p className="text-on-surface-variant font-medium">Real-time status of critical urban arteries, medical installations, and comms grids across sectors.</p>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {zones.map(z => {
                    const hospCapPct = z.hospital_capacity > 0 ? Math.round((z.critical / z.hospital_capacity) * 100) : 0;
                    const roadPct = Math.round(z.road_access * 100);
                    const commsActive = z.road_access > 0.3; // derive comms state

                    return (
                        <div key={z.id} className="bg-surface-container-low p-1 relative overflow-hidden rounded-xl border border-outline-variant/10">
                            <div className="bg-surface-container p-6 h-full">
                                <div className="flex justify-between items-center mb-6">
                                    <h2 className="text-xl font-bold text-on-surface uppercase tracking-widest">Zone {z.id}</h2>
                                    <span className={`px-2 py-1 text-[10px] font-bold uppercase tracking-widest rounded ${z.road_access < 0.5 || hospCapPct > 90 ? 'bg-error/20 text-error' : 'bg-secondary/20 text-secondary'}`}>
                                        {z.road_access < 0.5 || hospCapPct > 90 ? 'Degraded' : 'Nominal'}
                                    </span>
                                </div>

                                <div className="space-y-6">
                                    {/* Road Access */}
                                    <div>
                                        <div className="flex justify-between text-xs font-bold text-on-surface-variant uppercase tracking-widest mb-2">
                                            <span>Road Access</span>
                                            <span className={roadPct < 50 ? 'text-error' : 'text-on-surface'}>{roadPct}%</span>
                                        </div>
                                        <div className="h-2 w-full bg-surface-container-highest rounded-full overflow-hidden">
                                            <div className="h-full transition-all duration-1000 bg-secondary" style={{ width: `${roadPct}%`, backgroundColor: roadPct < 50 ? '#ffb4ab' : '#4ae176' }}></div>
                                        </div>
                                    </div>

                                    {/* Hospital Load */}
                                    <div>
                                        <div className="flex justify-between text-xs font-bold text-on-surface-variant uppercase tracking-widest mb-2">
                                            <span>Hospital Load</span>
                                            <span className={hospCapPct > 100 ? 'text-error' : 'text-on-surface'}>{hospCapPct}%</span>
                                        </div>
                                        <div className="h-2 w-full bg-surface-container-highest rounded-full overflow-hidden">
                                            <div className="h-full transition-all duration-1000 bg-tertiary" style={{ width: `${Math.min(100, hospCapPct)}%`, backgroundColor: hospCapPct > 100 ? '#ffb4ab' : '#ffd9df' }}></div>
                                        </div>
                                        <div className="mt-1 text-[9px] text-on-surface-variant/70 text-right uppercase tracking-widest">
                                            {z.critical} / {z.hospital_capacity} Bed Capacity
                                        </div>
                                    </div>

                                    {/* Communications Array */}
                                    <div className="p-3 bg-surface-container-high rounded-lg flex items-center justify-between border border-outline-variant/5">
                                        <div className="flex items-center gap-3">
                                            <span className={`material-symbols-outlined text-sm ${commsActive ? 'text-secondary' : 'text-error opacity-50'}`} data-icon={commsActive ? "router" : "warning"}>{commsActive ? "router" : "warning"}</span>
                                            <span className="text-xs font-bold uppercase tracking-widest text-on-surface">Comms Relay</span>
                                        </div>
                                        <span className={`text-[10px] font-bold uppercase tracking-widest ${commsActive ? 'text-secondary' : 'text-error'}`}>
                                            {commsActive ? 'Online' : 'Offline'}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default Infrastructure;
