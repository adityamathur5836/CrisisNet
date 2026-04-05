import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:5001',
});

export const fetchState = async () => {
  const response = await API.get('/state');
  return response.data;
};

export const stepSimulation = async (action) => {
  const response = await API.post('/step', action);
  return response.data;
};

export const resetSimulation = async (seed = 42) => {
  const response = await API.post('/reset', { seed });
  return response.data;
};

export default API;
