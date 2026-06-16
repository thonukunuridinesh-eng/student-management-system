import axios from "axios";

export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8001/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  const accessToken = localStorage.getItem("edutrack_access");

  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }

  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("edutrack_access");
      localStorage.removeItem("edutrack_refresh");
      localStorage.removeItem("edutrack_user");
    }

    return Promise.reject(error);
  },
);

export function asList(payload) {
  if (Array.isArray(payload)) {
    return payload;
  }

  return payload?.results || [];
}

export default api;
