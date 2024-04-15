// src/components/Sidebar.js
import React from 'react';

function DashboardSidebar() {
    return (
        <div className="d-flex flex-column flex-shrink-0 p-3 bg-light" style={{width: "280px"}}>
            <ul className="nav nav-pills flex-column mb-auto">
                <li className="nav-item"><a href="#" className="nav-link active" aria-current="page">Inbox</a></li>
                <li className="nav-item"><a href="#" className="nav-link">Starred</a></li>
                <li className="nav-item"><a href="#" className="nav-link">Sent</a></li>
                <li className="nav-item"><a href="#" className="nav-link">Drafts</a></li>
                <li className="nav-item"><a href="#" className="nav-link">Spam</a></li>
                <li className="nav-item"><a href="#" className="nav-link">Trash</a></li>
            </ul>
        </div>
    );
}

export default DashboardSidebar;
