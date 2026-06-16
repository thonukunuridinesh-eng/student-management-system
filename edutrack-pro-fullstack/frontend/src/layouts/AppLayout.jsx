import { BookOpen, ClipboardList, GraduationCap, LayoutDashboard, LogOut, Megaphone, Users } from "lucide-react";
import { NavLink, Outlet } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

const navigation = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard },
  { to: "/students", label: "Students", icon: Users },
  { to: "/courses", label: "Courses", icon: BookOpen },
  { to: "/attendance", label: "Attendance", icon: ClipboardList },
  { to: "/notices", label: "Notices", icon: Megaphone },
];

export default function AppLayout() {
  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen bg-slate-50">
      <aside className="fixed inset-y-0 left-0 z-30 hidden w-72 border-r border-slate-200 bg-white px-5 py-6 lg:block">
        <div className="flex items-center gap-3">
          <div className="grid h-11 w-11 place-items-center rounded-lg bg-teal-600 text-white">
            <GraduationCap size={24} />
          </div>
          <div>
            <p className="text-lg font-bold text-slate-950">EduTrack Pro</p>
            <p className="text-xs font-semibold uppercase tracking-wide text-teal-700">{user?.role}</p>
          </div>
        </div>

        <nav className="mt-8 space-y-1">
          {navigation.map((item) => {
            const Icon = item.icon;

            return (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.to === "/"}
                className={({ isActive }) =>
                  `flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-semibold transition ${
                    isActive ? "bg-teal-50 text-teal-700" : "text-slate-600 hover:bg-slate-100 hover:text-slate-950"
                  }`
                }
              >
                <Icon size={18} />
                {item.label}
              </NavLink>
            );
          })}
        </nav>

        <button
          onClick={logout}
          className="focus-ring absolute bottom-6 left-5 right-5 flex items-center justify-center gap-2 rounded-lg bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-slate-800"
        >
          <LogOut size={18} />
          Logout
        </button>
      </aside>

      <div className="lg:pl-72">
        <header className="sticky top-0 z-20 border-b border-slate-200 bg-white/90 px-4 py-4 backdrop-blur md:px-8">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <p className="text-sm font-medium text-slate-500">Welcome back</p>
              <h1 className="text-xl font-bold text-slate-950">{user?.full_name || user?.email}</h1>
            </div>
            <button
              onClick={logout}
              className="focus-ring inline-flex items-center gap-2 rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-100 lg:hidden"
            >
              <LogOut size={17} />
              Logout
            </button>
          </div>

          <nav className="mt-4 flex gap-2 overflow-x-auto lg:hidden">
            {navigation.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.to === "/"}
                className={({ isActive }) =>
                  `whitespace-nowrap rounded-lg px-3 py-2 text-sm font-semibold ${
                    isActive ? "bg-teal-600 text-white" : "bg-slate-100 text-slate-700"
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        </header>

        <main className="px-4 py-6 md:px-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
