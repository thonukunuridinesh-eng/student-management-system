import { motion } from "framer-motion";
import { CalendarCheck } from "lucide-react";
import { useEffect, useState } from "react";

import api, { asList } from "../api/client";
import { EmptyState, ErrorState, LoadingState } from "../components/DataState";

const statusTone = {
  PRESENT: "bg-emerald-50 text-emerald-700",
  ABSENT: "bg-rose-50 text-rose-700",
  LATE: "bg-amber-50 text-amber-700",
};

export default function Attendance() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadAttendance() {
      try {
        const { data } = await api.get("/students/attendance/");
        setRecords(asList(data));
      } catch (err) {
        setError(err.response?.data?.message || "Unable to load attendance.");
      } finally {
        setLoading(false);
      }
    }

    loadAttendance();
  }, []);

  if (loading) {
    return <LoadingState label="Loading attendance" />;
  }

  if (error) {
    return <ErrorState message={error} />;
  }

  return (
    <div className="space-y-5">
      <div>
        <p className="text-sm font-semibold uppercase tracking-wide text-teal-700">Attendance</p>
        <h2 className="mt-1 text-2xl font-bold text-slate-950">Attendance records</h2>
      </div>

      {records.length === 0 ? (
        <EmptyState label="No attendance records available" />
      ) : (
        <motion.div initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} className="overflow-hidden rounded-lg border border-slate-200 bg-white shadow-soft">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-200">
              <thead className="bg-slate-50">
                <tr>
                  {["Date", "Student", "Course", "Status", "Remarks"].map((heading) => (
                    <th key={heading} className="px-4 py-3 text-left text-xs font-bold uppercase tracking-wide text-slate-500">
                      {heading}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {records.map((record) => (
                  <tr key={record.id} className="hover:bg-slate-50">
                    <td className="px-4 py-4">
                      <div className="flex items-center gap-2 text-sm font-semibold text-slate-700">
                        <CalendarCheck size={17} className="text-teal-700" />
                        {record.date}
                      </div>
                    </td>
                    <td className="px-4 py-4">
                      <p className="font-semibold text-slate-950">{record.student_name}</p>
                      <p className="text-sm text-slate-500">{record.roll_number}</p>
                    </td>
                    <td className="px-4 py-4 text-sm font-semibold text-slate-700">{record.course_code}</td>
                    <td className="px-4 py-4">
                      <span className={`rounded-full px-2.5 py-1 text-xs font-bold ${statusTone[record.status] || "bg-slate-100 text-slate-700"}`}>
                        {record.status}
                      </span>
                    </td>
                    <td className="px-4 py-4 text-sm text-slate-600">{record.remarks || "No remarks"}</td>
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
