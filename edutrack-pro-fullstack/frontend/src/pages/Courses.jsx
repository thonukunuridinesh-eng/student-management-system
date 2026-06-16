import { motion } from "framer-motion";
import { BookOpen } from "lucide-react";
import { useEffect, useState } from "react";

import api, { asList } from "../api/client";
import { EmptyState, ErrorState, LoadingState } from "../components/DataState";

export default function Courses() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadCourses() {
      try {
        const { data } = await api.get("/students/courses/");
        setCourses(asList(data));
      } catch (err) {
        setError(err.response?.data?.message || "Unable to load courses.");
      } finally {
        setLoading(false);
      }
    }

    loadCourses();
  }, []);

  if (loading) {
    return <LoadingState label="Loading courses" />;
  }

  if (error) {
    return <ErrorState message={error} />;
  }

  return (
    <div className="space-y-5">
      <div>
        <p className="text-sm font-semibold uppercase tracking-wide text-teal-700">Courses</p>
        <h2 className="mt-1 text-2xl font-bold text-slate-950">Course catalog</h2>
      </div>

      {courses.length === 0 ? (
        <EmptyState label="No courses available" />
      ) : (
        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {courses.map((course) => (
            <motion.article
              key={course.id}
              initial={{ opacity: 0, y: 14 }}
              animate={{ opacity: 1, y: 0 }}
              className="rounded-lg border border-slate-200 bg-white p-5 shadow-soft"
            >
              <div className="flex items-start justify-between gap-3">
                <div className="grid h-11 w-11 place-items-center rounded-lg bg-amber-50 text-amber-700">
                  <BookOpen size={21} />
                </div>
                <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-bold text-slate-600">
                  {course.code}
                </span>
              </div>
              <h3 className="mt-5 text-lg font-bold text-slate-950">{course.name}</h3>
              <p className="mt-2 text-sm text-slate-500">{course.department_name}</p>
              <div className="mt-5 grid grid-cols-2 gap-3 text-sm">
                <div className="rounded-lg bg-slate-50 p-3">
                  <p className="font-medium text-slate-500">Teacher</p>
                  <p className="mt-1 font-bold text-slate-950">{course.teacher_name || "Not assigned"}</p>
                </div>
                <div className="rounded-lg bg-slate-50 p-3">
                  <p className="font-medium text-slate-500">Credits</p>
                  <p className="mt-1 font-bold text-slate-950">{course.credits}</p>
                </div>
              </div>
            </motion.article>
          ))}
        </section>
      )}
    </div>
  );
}
