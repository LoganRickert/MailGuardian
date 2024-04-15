// src/components/Dashboard.js
import React, { useState } from 'react';
import DashboardTopBar from './DashboardTopBar';
import DashboardSidebar from './DashboardSidebar';
import EmailList from './EmailList';
import { useUser } from '../contexts/UserContext';  // Make sure you have this hook

function Dashboard() {
    const { user } = useUser();  // Retrieve user from context
    const [selectedEmail, setSelectedEmail] = useState('');  // Initial state can be an empty string or a default value

    return (
        <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
            <DashboardTopBar selectedEmail={selectedEmail} setSelectedEmail={setSelectedEmail} user={user} />
            <div style={{ display: 'flex', flexGrow: 1 }}>
                <DashboardSidebar />
                <EmailList emailFilter={selectedEmail} />
            </div>
        </div>
    );
}

export default Dashboard;
