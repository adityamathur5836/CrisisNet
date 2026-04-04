import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
    const location = useLocation();
    const currentPath = location.pathname;

    const isActive = (path) => currentPath === path;

    return (
        <header className="flex justify-between items-center w-full px-6 h-16 bg-[#0b1326] dark:bg-slate-950 flex-shrink-0 z-50">
            <div className="flex items-center gap-8">
                <Link to="/" className="text-xl font-black uppercase tracking-tighter text-[#ffb3ad]">CrisisNet Sentinel</Link>
                <nav className="hidden md:flex items-center gap-6 font-inter tracking-tight text-on-surface-variant">
                    <Link className={`transition-colors px-2 py-1 rounded ${isActive('/') ? 'text-[#ffb3ad] border-b-2 border-[#ffb3ad] pb-1' : 'text-[#e4beba] opacity-70 hover:bg-[#222a3d]'}`} to="/">Dashboard</Link>
                    <Link className={`transition-colors px-2 py-1 rounded ${isActive('/agents') ? 'text-[#ffb3ad] border-b-2 border-[#ffb3ad] pb-1' : 'text-[#e4beba] opacity-70 hover:bg-[#222a3d]'}`} to="/agents">Agents</Link>
                    <Link className={`transition-colors px-2 py-1 rounded ${isActive('/zones') ? 'text-[#ffb3ad] border-b-2 border-[#ffb3ad] pb-1' : 'text-[#e4beba] opacity-70 hover:bg-[#222a3d]'}`} to="/zones">Zones</Link>
                </nav>
            </div>
            <div className="flex items-center gap-4">
                <button className="bg-gradient-to-br from-[#ffb3ad] to-[#ff5451] text-[#68000a] px-4 py-2 rounded-lg font-bold text-sm tracking-tight hover:scale-95 transition-transform active:duration-100">
                    Deploy Strategy
                </button>
                <div className="flex items-center gap-3 text-[#ffb3ad]">
                    <span className="material-symbols-outlined cursor-pointer hover:bg-[#222a3d] p-1 rounded transition-colors" data-icon="timer">timer</span>
                    <span className="material-symbols-outlined cursor-pointer hover:bg-[#222a3d] p-1 rounded transition-colors" data-icon="health_and_safety">health_and_safety</span>
                    <span className="material-symbols-outlined cursor-pointer hover:bg-[#222a3d] p-1 rounded transition-colors" data-icon="settings">settings</span>
                    <img alt="Operator Profile" className="w-8 h-8 rounded-full border border-outline-variant/30" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDr1u6K24xjd9kEMs95GUibPNKbvn-W50qjRUrfzcaPx3phkvBBMyL6LPVebUn1mRxJAKndZHc48IrI85Gsr2jJeWAk11Qtp8N_DajykcAXJZIIuGQli0InXAVEHPw0SJ6SO1TINVR1Xxx50bPdkUc7VOx9-d99Rz7lpTlVadRIsvNn9_N42QGqN9yrC_uPj_jFepvtq9-TXiQ0zCi5O2qwKvajsHwoXzMUwO6llYEL82s2-n0YKsBg73C1pGFuKAykvNQmGWu3UFK9" />
                </div>
            </div>
        </header>
    );
};

export default Navbar;
