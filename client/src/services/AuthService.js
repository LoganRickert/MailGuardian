// src/services/AuthService.js
import axios from 'axios';

const API_URL = `${process.env.REACT_APP_API_URL}/api/v1/login`;

export const login = async (username, password) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    try {
        const response = await axios.post(API_URL, formData, {
            headers: {
                'Content-Type': 'multipart/form-data', // or 'application/x-www-form-urlencoded' if more appropriate
            },
        });

        if (response.data.access_token) {
            localStorage.setItem('user', JSON.stringify(response.data));
        }
        
        return response.data;
    } catch (error) {
        console.error('Login error:', error.response);
        throw error;
    }
};

export const logout = () => {
    localStorage.removeItem('user');
};

export const getCurrentUser = () => {
    return JSON.parse(localStorage.getItem('user'));
};