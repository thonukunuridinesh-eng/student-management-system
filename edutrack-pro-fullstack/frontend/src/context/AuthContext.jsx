import { createContext, useContext, useMemo, useState } from "react";

import api from "../api/client";

const AuthContext = createContext(null);

const storedUser = () => {
  const value = localStorage.getItem("edutrack_user");
  return value ? JSON.parse(value) : null;
};

export function AuthProvider({ children }) {
  const [user, setUser] = useState(storedUser);
  const [loading, setLoading] = useState(false);

  const login = async ({ email, password }) => {
    setLoading(true);
    try {
      const { data } = await api.post("/auth/login/", { email, password });
      localStorage.setItem("edutrack_access", data.access);
      localStorage.setItem("edutrack_refresh", data.refresh);
      localStorage.setItem("edutrack_user", JSON.stringify(data.user));
      setUser(data.user);
      return data.user;
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    const refresh = localStorage.getItem("edutrack_refresh");

    try {
      if (refresh) {
        await api.post("/auth/logout/", { refresh });
      }
    } catch {
      // Local logout should still happen if the refresh token already expired.
    }

    localStorage.removeItem("edutrack_access");
    localStorage.removeItem("edutrack_refresh");
    localStorage.removeItem("edutrack_user");
    setUser(null);
  };

  const value = useMemo(
    () => ({
      user,
      loading,
      isAuthenticated: Boolean(user),
      login,
      logout,
    }),
    [user, loading],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }

  return context;
}
