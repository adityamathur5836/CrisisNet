import React from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';

const MainLayout = ({ children }) => {
    return (
        <div className="bg-background text-on-surface font-body overflow-hidden h-screen flex flex-col">
            <Navbar />
            <div className="flex flex-1 overflow-hidden relative">
                <Sidebar />
                <main className="flex-1 lg:ml-64 p-6 overflow-y-auto">
                    {children}
                </main>
            </div>
            <div className="fixed bottom-6 right-6 z-50 flex flex-col gap-4">
                <button className="kinetic-gradient w-14 h-14 rounded-xl flex items-center justify-center text-on-primary shadow-2xl transition-transform active:scale-90">
                    <span className="material-symbols-outlined" data-icon="add_alert" style={{ fontVariationSettings: "'FILL' 1" }}>add_alert</span>
                </button>
            </div>
        </div>
    );
};

export default MainLayout;
