// src/api/userApi.js
import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

export const getUsers = async () => {
  const response = await apiClient.get('/users');
  return response.data;
};

export const getUser = async (username) => {
  const response = await apiClient.get(`/users/${username}`);
  return response.data;
};

export const createUser = async (userData) => {
  const response = await apiClient.post('/users', userData);
  return response.data;
};

export const updateUser = async (username, userData) => {
  const response = await apiClient.put(`/users/${username}`, userData);
  return response.data;
};

export const deleteUser = async (username) => {
  const response = await apiClient.delete(`/users/${username}`);
  return response.data;
};
