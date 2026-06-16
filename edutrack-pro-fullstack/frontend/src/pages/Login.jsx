import { motion } from "framer-motion";
import { GraduationCap, Lock, Mail } from "lucide-react";
import { useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

const demoUsers = [
  { label: "Admin", email: "admin@edutrack.com", password: "Admin@12345" },
  { label: "Teacher", email: "teacher@edutrack.com", password: "Teacher@12345" },
  { label: "Student", email: "student@edutrack.com", password: "Student@12345" },
];

export default function Login() {
  const navigate = useNavigate();
  const { isAuthenticated, login, loading } = useAuth();
  const [form, setForm] = useState(demoUsers[0]);
  const [error, setError] = useState("");

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  const updateField = (event) => {
    setForm((current) => ({ ...current, [event.target.name]: event.target.value }));
  };

  const submit = async (event) => {
    event.preventDefault();
    setError("");

    try {
      await login(form);
      navigate("/");
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed. Check backend server and credentials.");
    }
  };

  return (
    <main className="grid min-h-screen bg-slate-50 lg:grid-cols-[1.05fr_0.95fr]">
      <section className="hidden bg-teal-700 px-12 py-12 text-white lg:flex lg:flex-col lg:justify-between">
        <div className="flex items-center gap-3">
          <div className="grid h-12 w-12 place-items-center rounded-lg bg-white text-teal-700">
            <GraduationCap size={27} />
          </div>
          <span className="text-xl font-bold">EduTrack Pro</span>
        </div>

        <div className="max-w-xl">
          <p className="text-sm font-semibold uppercase tracking-wide text-teal-100">Student Management System</p>
          <h1 className="mt-4 text-5xl font-bold leading-tight">Academic operations in one focused dashboard.</h1>
          <p className="mt-5 text-lg leading-8 text-teal-50">
            Track departments, courses, enrollments, attendance, grades, and notices with role-based access.
          </p>
        </div>

        <div className="grid grid-cols-3 gap-3 text-sm">
          {["Admin control", "Teacher tools", "Student view"].map((item) => (
            <div key={item} className="rounded-lg bg-white/12 p-4 font-semibold ring-1 ring-white/15">
              {item}
            </div>
          ))}
        </div>
      </section>

      <section className="flex items-center justify-center px-4 py-10">
        <motion.div
          initial={{ opacity: 0, y: 18 }}
          animate={{ opacity: 1, y: 0 }}
          className="w-full max-w-md rounded-lg border border-slate-200 bg-white p-6 shadow-soft"
        >
          <div className="mb-6 flex items-center gap-3 lg:hidden">
            <div className="grid h-11 w-11 place-items-center rounded-lg bg-teal-600 text-white">
              <GraduationCap size={23} />
            </div>
            <div>
              <p className="text-lg font-bold text-slate-950">EduTrack Pro</p>
              <p className="text-sm text-slate-500">Student Management System</p>
            </div>
          </div>

          <h2 className="text-2xl font-bold text-slate-950">Sign in</h2>
          <p className="mt-2 text-sm text-slate-500">Use a demo account to open the dashboard.</p>

          <div className="mt-5 grid grid-cols-3 gap-2">
            {demoUsers.map((demo) => (
              <button
                key={demo.email}
                type="button"
                onClick={() => setForm(demo)}
                className={`focus-ring rounded-lg border px-3 py-2 text-sm font-semibold ${
                  form.email === demo.email
                    ? "border-teal-600 bg-teal-50 text-teal-700"
                    : "border-slate-200 bg-white text-slate-600 hover:bg-slate-50"
                }`}
              >
                {demo.label}
              </button>
            ))}
          </div>

          <form onSubmit={submit} className="mt-6 space-y-4">
            <label className="block">
              <span className="text-sm font-semibold text-slate-700">Email</span>
              <div className="mt-2 flex items-center gap-2 rounded-lg border border-slate-200 bg-white px-3 py-2.5">
                <Mail size={18} className="text-slate-400" />
                <input
                  name="email"
                  value={form.email}
                  onChange={updateField}
                  className="w-full bg-transparent text-sm text-slate-950 outline-none"
                  type="email"
                  required
                />
              </div>
            </label>

            <label className="block">
              <span className="text-sm font-semibold text-slate-700">Password</span>
              <div className="mt-2 flex items-center gap-2 rounded-lg border border-slate-200 bg-white px-3 py-2.5">
                <Lock size={18} className="text-slate-400" />
                <input
                  name="password"
                  value={form.password}
                  onChange={updateField}
                  className="w-full bg-transparent text-sm text-slate-950 outline-none"
                  type="password"
                  required
                />
              </div>
            </label>

            {error && <p className="rounded-lg bg-rose-50 px-3 py-2 text-sm font-medium text-rose-700">{error}</p>}

            <button
              disabled={loading}
              className="focus-ring w-full rounded-lg bg-teal-600 px-4 py-3 text-sm font-bold text-white transition hover:bg-teal-700 disabled:cursor-not-allowed disabled:bg-slate-300"
            >
              {loading ? "Signing in..." : "Open dashboard"}
            </button>
          </form>
        </motion.div>
      </section>
    </main>
  );
}
