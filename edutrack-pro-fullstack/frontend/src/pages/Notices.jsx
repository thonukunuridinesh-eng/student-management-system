import { motion } from "framer-motion";
import { Megaphone } from "lucide-react";
import { useEffect, useState } from "react";

import api, { asList } from "../api/client";
import { EmptyState, ErrorState, LoadingState } from "../components/DataState";

export default function Notices() {
  const [notices, setNotices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadNotices() {
      try {
        const { data } = await api.get("/students/notices/");
        setNotices(asList(data));
      } catch (err) {
        setError(err.response?.data?.message || "Unable to load notices.");
      } finally {
        setLoading(false);
      }
    }

    loadNotices();
  }, []);

  if (loading) {
    return <LoadingState label="Loading notices" />;
  }

  if (error) {
    return <ErrorState message={error} />;
  }

  return (
    <div className="space-y-5">
      <div>
        <p className="text-sm font-semibold uppercase tracking-wide text-teal-700">Notices</p>
        <h2 className="mt-1 text-2xl font-bold text-slate-950">Notice board</h2>
      </div>

      {notices.length === 0 ? (
        <EmptyState label="No notices available" />
      ) : (
        <section className="grid gap-4 lg:grid-cols-2">
          {notices.map((notice) => (
            <motion.article
              key={notice.id}
              initial={{ opacity: 0, y: 14 }}
              animate={{ opacity: 1, y: 0 }}
              className="rounded-lg border border-slate-200 bg-white p-5 shadow-soft"
            >
              <div className="flex items-start justify-between gap-3">
                <div className="grid h-11 w-11 place-items-center rounded-lg bg-teal-50 text-teal-700">
                  <Megaphone size={21} />
                </div>
                <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-bold text-slate-600">
                  {notice.audience}
                </span>
              </div>
              <h3 className="mt-5 text-lg font-bold text-slate-950">{notice.title}</h3>
              <p className="mt-3 text-sm leading-6 text-slate-600">{notice.message}</p>
              <p className="mt-5 text-xs font-semibold uppercase tracking-wide text-slate-400">
                By {notice.created_by_name || "Admin"}
              </p>
            </motion.article>
          ))}
        </section>
      )}
    </div>
  );
}
