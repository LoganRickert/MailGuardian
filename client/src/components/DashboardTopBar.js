// src/components/DashboardTopBar.js
import React from 'react';

function DashboardTopBar({ selectedEmail, setSelectedEmail, user }) {
    const handleEmailChange = (newEmail) => {
        setSelectedEmail(newEmail);  // Update state in Dashboard component
    };

    console.log("USER", user)

    return (
        <div className="navbar navbar-expand-lg navbar-light bg-light">
            <div className="container-fluid">
                <span className="navbar-brand">{selectedEmail || "Select an Email"}</span>
                <div className="dropdown">
                    <button className="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-expanded="false">
                        Change Email
                    </button>
                    <ul className="dropdown-menu dropdown-menu-end" aria-labelledby="dropdownMenuButton">
                        {/* Dynamically list emails the user has access to */}
                        {user && user.permissions.map((perm, index) => (
                            perm.emails.map(email => (
                                <li key={`${email}-${index}`}>
                                    <button className="dropdown-item" onClick={() => handleEmailChange(email)}>
                                        {email}
                                    </button>
                                </li>
                            ))
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
}

export default DashboardTopBar;
