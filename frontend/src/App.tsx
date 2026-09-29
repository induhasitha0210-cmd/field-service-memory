import { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import type { UserRole } from './components/Header';

import DashboardPage from './pages/DashboardPage';
import ServiceRequestsPage from './pages/ServiceRequestsPage';
import ServiceRequestDetailPage from './pages/ServiceRequestDetailPage';
import TechniciansPage from './pages/TechniciansPage';
import CustomersPage from './pages/CustomersPage';
import SitesPage from './pages/SitesPage';
import EquipmentListPage from './pages/EquipmentListPage';
import EquipmentDetailPage from './pages/EquipmentDetailPage';
import MemoryExplorerPage from './pages/MemoryExplorerPage';
import MemoryMapPage from './pages/MemoryMapPage';
import InsightsPage from './pages/InsightsPage';
import DemoPage from './pages/DemoPage';
import SettingsPage from './pages/SettingsPage';

export default function App() {
  const [currentRole, setCurrentRole] = useState<UserRole>('manager');

  return (
    <BrowserRouter>
      <div className="flex h-screen bg-[#0b0f19] text-slate-100 font-sans antialiased overflow-hidden">
        {/* Left Navigation Sidebar */}
        <Sidebar />

        {/* Main Content Area */}
        <div className="flex-1 flex flex-col min-w-0 h-full overflow-hidden">
          {/* Top Bar with Role Switcher & Status */}
          <Header currentRole={currentRole} onRoleChange={setCurrentRole} />

          {/* Route Content Area */}
          <main className="flex-1 overflow-y-auto">
            <Routes>
              <Route path="/" element={<DashboardPage />} />
              <Route path="/service-requests" element={<ServiceRequestsPage />} />
              <Route path="/service-requests/:id" element={<ServiceRequestDetailPage />} />
              <Route path="/technicians" element={<TechniciansPage />} />
              <Route path="/customers" element={<CustomersPage />} />
              <Route path="/sites" element={<SitesPage />} />
              <Route path="/equipment" element={<EquipmentListPage />} />
              <Route path="/equipment/:id" element={<EquipmentDetailPage />} />
              <Route path="/memory" element={<MemoryExplorerPage />} />
              <Route path="/memory-map" element={<MemoryMapPage />} />
              <Route path="/insights" element={<InsightsPage />} />
              <Route path="/demo" element={<DemoPage />} />
              <Route path="/settings" element={<SettingsPage />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
}
