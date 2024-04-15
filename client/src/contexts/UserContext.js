// src/contexts/UserContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';

const UserContext = createContext({
    user: null,
    setUser: () => {}
});

export const UserProvider = ({ children }) => {
    const [user, setUser] = useState(() => {
        const storedUser = localStorage.getItem('user');
        return storedUser ? JSON.parse(storedUser).user : null;
    });

    useEffect(() => {
        // Optionally, listen to storage events to synchronize state across tabs
        const handleStorageChange = (event) => {
            if (event.key === 'user') {
                setUser(event.newValue ? JSON.parse(event.newValue).user : null);
            }
        };

        window.addEventListener('storage', handleStorageChange);

        return () => {
            window.removeEventListener('storage', handleStorageChange);
        };
    }, []);

    return (
        <UserContext.Provider value={{ user, setUser }}>
            {children}
        </UserContext.Provider>
    );
};

export const useUser = () => useContext(UserContext);
