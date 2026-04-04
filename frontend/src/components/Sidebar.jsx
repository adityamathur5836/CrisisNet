import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Sidebar = () => {
    const location = useLocation();
    const currentPath = location.pathname;

    const isActive = (path) => currentPath === path;

    return (
        <aside className="fixed left-0 top-0 h-full flex flex-col py-6 bg-[#131b2e] dark:bg-slate-900 border-r border-[#5b403e]/15 w-64 z-40 pt-20">
            <div className="px-6 mb-8">
                <div className="flex items-center gap-3 mb-2">
                    <div className="w-10 h-10 bg-surface-container-highest flex items-center justify-center rounded">
                        <span className="material-symbols-outlined text-primary" data-icon="emergency_home">emergency_home</span>
                    </div>
                    <div>
                        <div className="text-lg font-bold text-[#ffb3ad]">Simulation Engine</div>
                        <div className="text-[10px] text-on-surface-variant uppercase tracking-widest">Active Session: Alpha-9</div>
                    </div>
                </div>
            </div>
            <div className="flex-1 space-y-1 px-4">
                <div className="text-[10px] font-bold text-on-surface-variant/50 px-2 mb-2 tracking-[0.2em] uppercase">Control Deck</div>
                <div className="bg-[#2d3449] border-l-4 border-[#ffb3ad] p-3 rounded-r-md mb-4">
                    <div className="flex justify-between items-center gap-2">
                        <button className="p-2 hover:bg-surface-container-high rounded transition-colors text-secondary"><span className="material-symbols-outlined" data-icon="play_arrow">play_arrow</span></button>
                        <button className="p-2 hover:bg-surface-container-high rounded transition-colors text-tertiary"><span className="material-symbols-outlined" data-icon="pause">pause</span></button>
                        <button className="p-2 hover:bg-surface-container-high rounded transition-colors text-on-surface-variant"><span className="material-symbols-outlined" data-icon="step_over">step_over</span></button>
                        <button className="p-2 hover:bg-surface-container-high rounded transition-colors text-error"><span className="material-symbols-outlined" data-icon="restart_alt">restart_alt</span></button>
                    </div>
                </div>
                <div className="space-y-4">
                    <div>
                        <label className="text-[10px] font-bold text-on-surface-variant/50 px-2 tracking-[0.2em] uppercase block mb-2">Agent Logic</label>
                        <select className="w-full bg-surface-container-low border-none text-on-surface text-sm rounded-md focus:ring-1 focus:ring-primary p-2">
                            <option>RL - Deep Sentinel v4</option>
                            <option>Heuristic - Priority Path</option>
                            <option>Random - Baseline</option>
                        </select>
                    </div>
                    <div className="space-y-1">
                        <label className="text-[10px] font-bold text-on-surface-variant/50 px-2 tracking-[0.2em] uppercase block mb-2">Core Assets</label>
                        <Link to="/" className={`flex items-center gap-3 px-2 py-2 font-inter text-sm font-medium uppercase tracking-widest transition-all ${isActive('/') ? 'text-[#ffb3ad] bg-[#2d3449] border-l-4 border-[#ffb3ad]' : 'text-[#e4beba] hover:bg-[#171f33]'}`}>
                            <span className="material-symbols-outlined text-sm" data-icon="emergency_home">emergency_home</span>
                            <span>Dashboard</span>
                        </Link>
                        <Link to="/agents" className={`flex items-center gap-3 px-2 py-2 font-inter text-sm font-medium uppercase tracking-widest transition-all ${isActive('/agents') ? 'text-[#ffb3ad] bg-[#2d3449] border-l-4 border-[#ffb3ad]' : 'text-[#e4beba] hover:bg-[#171f33]'}`}>
                            <span className="material-symbols-outlined text-sm" data-icon="smart_toy">smart_toy</span>
                            <span>Agents</span>
                        </Link>
                        <Link to="/zones" className={`flex items-center gap-3 px-2 py-2 font-inter text-sm font-medium uppercase tracking-widest transition-all ${isActive('/zones') ? 'text-[#ffb3ad] bg-[#2d3449] border-l-4 border-[#ffb3ad]' : 'text-[#e4beba] hover:bg-[#171f33]'}`}>
                            <span className="material-symbols-outlined text-sm" data-icon="map">map</span>
                            <span>Zones</span>
                        </Link>
                        <Link to="/infrastructure" className={`flex items-center gap-3 px-2 py-2 font-inter text-sm font-medium uppercase tracking-widest transition-all ${isActive('/infrastructure') ? 'text-[#ffb3ad] bg-[#2d3449] border-l-4 border-[#ffb3ad]' : 'text-[#e4beba] hover:bg-[#171f33]'}`}>
                            <span className="material-symbols-outlined text-sm" data-icon="domain">domain</span>
                            <span>Infrastructure</span>
                        </Link>
                    </div>
                </div>
            </div>
            <div className="px-4 mt-auto pt-4 border-t border-outline-variant/15">
                <button className="w-full bg-[#2d3449] text-[#ffb3ad] py-2 rounded font-bold text-xs uppercase tracking-widest hover:bg-[#222a3d] transition-colors">Start Simulation</button>
                <div className="mt-4 space-y-1">
                    <div className="flex items-center gap-3 px-2 py-1 text-[#e4beba] text-xs uppercase tracking-tighter opacity-70 hover:opacity-100 transition-opacity cursor-pointer">
                        <span className="material-symbols-outlined text-sm" data-icon="memory">memory</span>
                        <span>System Status</span>
                    </div>
                </div>
            </div>
        </aside>
    );
};

export default Sidebar;
