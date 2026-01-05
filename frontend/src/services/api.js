import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Obtiene el Top 5 de CEDEARs con mayor fortaleza técnica.
 */
export const getTop5Cedears = async (includeBreakdown = true) => {
  try {
    const response = await apiClient.get('/top5-cedears', {
      params: { include_breakdown: includeBreakdown },
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching top 5 CEDEARs:', error);
    throw error;
  }
};

/**
 * Obtiene todos los CEDEARs analizados.
 */
export const getAllCedears = async (includeBreakdown = false) => {
  try {
    const response = await apiClient.get('/cedears', {
      params: { include_breakdown: includeBreakdown },
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching all CEDEARs:', error);
    throw error;
  }
};

/**
 * Obtiene el detalle de un CEDEAR específico.
 */
export const getCedearDetail = async (ticker) => {
  try {
    const response = await apiClient.get(`/cedears/${ticker}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching CEDEAR ${ticker}:`, error);
    throw error;
  }
};

/**
 * Obtiene el universo de CEDEARs disponibles.
 */
export const getUniverse = async () => {
  try {
    const response = await apiClient.get('/universe');
    return response.data;
  } catch (error) {
    console.error('Error fetching universe:', error);
    throw error;
  }
};

/**
 * Verifica el estado del backend.
 */
export const healthCheck = async () => {
  try {
    const response = await apiClient.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw error;
  }
};

export default apiClient;
