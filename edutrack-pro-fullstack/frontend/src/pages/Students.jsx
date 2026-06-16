import { motion } from "framer-motion";
import { Search, Users } from "lucide-react";
import { useEffect, useMemo, useState } from "react";

import api, { asList } from "../api/client";
import { EmptyState, ErrorState, LoadingState } from "../components/DataState";

export default function Students() {
  const [students, setStudents] = useState([]);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadStudents() {
      try {
        const { data } = await api.get("/students/profiles/");
        setStudents(asList(data));
      } catch (err) {
        setError(err.response?.data?.message || "Unable to load students.");
      } finally {
        setLoading(false);
      }
    }

    loadStudents();
  }, []);

  const filteredStudents = useMemo(() => {
    const value = query.toLowerCase();

    return students.filter((student) =>
      [student.user_name, student.user_email, student.roll_number, student.department_name]
        .join(" ")
        .toLowerCase()
        .includes(value),
    );
  }, [students, query]);

  if (loading) {
    return <LoadingState label="Loading students" />;
  }

  if (error) {
    return <ErrorState message={error} />;
  }

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-sm font-semibold uppercase tracking-wide text-teal-700">Students</p>
          <h2 className="mt-1 text-2xl font-bold text-slate-950">Student records</h2>
        </div>
        <div className="flex min-w-0 items-center gap-2 rounded-lg border border-slate-200 bg-white px-3 py-2">
          <Search size={17} className="shrink-0 text-slate-400" />
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search students"
            className="w-52 bg-transparent text-sm outline-none"
          />
        </div>
      </div>

      {filteredStudents.length === 0 ? (
        <EmptyState label="No students match your search" />
      ) : (
        <motion.div initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} className="overflow-hidden rounded-lg border border-slate-200 bg-white shadow-soft">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-200">
              <thead className="bg-slate-50">
                <tr>
                  {["Student", "Roll No", "Department", "Status", "Guardian"].map((heading) => (
                    <th key={heading} className="px-4 py-3 text-left text-xs font-bold uppercase tracking-wide text-slate-500">
                      {heading}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredStudents.map((student) => (
                  <tr key={student.id} className="hover:bg-slate-50">
                    <td className="px-4 py-4">
                      <div className="flex items-center gap-3">
                        <div className="grid h-10 w-10 place-items-center rounded-lg bg-teal-50 text-teal-700">
                          <Users size={18} />
                        </div>
                        <div>
                          <p className="font-semibold text-slate-950">{student.user_name}</p>
                          <p className="text-sm text-slate-500">{student.user_email}</p>
                        </div>
                      </div>
                    </td>
                    <td className="px-4 py-4 text-sm font-semibold text-slate-700">{student.roll_number}</td>
                    <td className="px-4 py-4 text-sm text-slate-600">{student.department_name}</td>
                    <td className="px-4 py-4">
                      <span className="rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-bold text-emerald-700">
                        {student.status}
                      </span>
                    </td>
                    <td className="px-4 py-4 text-sm text-slate-600">{student.guardian_name || "Not added"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </motion.div>
      )}
    </div>
  );
}
