import { motion } from "framer-motion";
import { BookOpen, ClipboardList, GraduationCap, Layers, Megaphone, Users } from "lucide-react";
import { useEffect, useState } from "react";

import api, { asList } from "../api/client";
import { ErrorState, LoadingState } from "../components/DataState";
import StatCard from "../components/StatCard";
import { useAuth } from "../context/AuthContext";

export default function Dashboard() {
  const { user } = useAuth();
  const [summary, setSummary] = useState(null);
  const [notices, setNotices] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const [summaryResponse, noticeResponse] = await Promise.all([
          api.get("/students/dashboard/"),
          api.get("/students/notices/"),
        ]);
        setSummary(summaryResponse.data);
        setNotices(asList(noticeResponse.data).slice(0, 3));
      } catch (err) {
        setError(err.response?.data?.message || "Unable to load dashboard.");
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);

  if (loading) {
    return <LoadingState label="Loading dashboard" />;
  }

  if (error) {
    return <ErrorState message={error} />;
  }

  const adminStats = [
    { label: "Departments", value: summary.departments, icon: Layers, tone: "teal" },
    { label: "Teachers", value: summary.teachers, icon: GraduationCap, tone: "indigo" },
    { label: "Students", value: summary.students, icon: Users, tone: "amber" },
    { label: "Courses", value: summary.courses, icon: BookOpen, tone: "rose" },
    { label: "Enrollments", value: summary.enrollments, icon: ClipboardList, tone: "teal" },
    { label: "Grades", value: summary.grades, icon: Megaphone, tone: "indigo" },
  ];

  const teacherStats = [
    { label: "My Courses", value: summary.courses, icon: BookOpen, tone: "teal" },
    { label: "My Students", value: summary.students, icon: Users, tone: "amber" },
    { label: "Attendance Records", value: summary.attendance_records, icon: ClipboardList, tone: "indigo" },
    { label: "Grades Created", value: summary.grades_created, icon: GraduationCap, tone: "rose" },
  ];

  const studentStats = [
    { label: "Enrolled Courses", value: summary.enrolled_courses, icon: BookOpen, tone: "teal" },
    { label: "Present Days", value: summary.present_days, icon: ClipboardList, tone: "indigo" },
    { label: "Absent Days", value: summary.absent_days, icon: Users, tone: "rose" },
    { label: "Average Marks", value: Number(summary.average_marks).toFixed(1), icon: GraduationCap, tone: "amber" },
  ];

  const stats = user?.role === "ADMIN" ? adminStats : user?.role === "TEACHER" ? teacherStats : studentStats;

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-semibold uppercase tracking-wide text-teal-700">{user?.role} dashboard</p>
        <h2 className="mt-1 text-2xl font-bold text-slate-950">Academic overview</h2>
      </div>

      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {stats.map((stat) => (
          <StatCard key={stat.label} {...stat} />
        ))}
      </section>

      <motion.section
        initial={{ opacity: 0, y: 14 }}
        animate={{ opacity: 1, y: 0 }}
        className="rounded-lg border border-slate-200 bg-white p-5 shadow-soft"
      >
        <div className="flex items-center justify-between gap-3">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wide text-teal-700">Notice board</p>
            <h3 className="mt-1 text-lg font-bold text-slate-950">Latest updates</h3>
          </div>
          <Megaphone className="text-teal-700" size={22} />
        </div>

        <div className="mt-5 divide-y divide-slate-100">
          {notices.map((notice) => (
            <article key={notice.id} className="py-4 first:pt-0 last:pb-0">
              <div className="flex flex-wrap items-center gap-2">
                <h4 className="font-bold text-slate-950">{notice.title}</h4>
                <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-bold text-slate-600">
                  {notice.audience}
                </span>
              </div>
              <p className="mt-2 text-sm leading-6 text-slate-600">{notice.message}</p>
            </article>
          ))}
        </div>
      </motion.section>
    </div>
  );
}
