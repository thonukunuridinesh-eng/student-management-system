import { motion } from "framer-motion";

export default function StatCard({ icon: Icon, label, value, tone = "teal" }) {
  const tones = {
    teal: "bg-teal-50 text-teal-700 ring-teal-100",
    amber: "bg-amber-50 text-amber-700 ring-amber-100",
    rose: "bg-rose-50 text-rose-700 ring-rose-100",
    indigo: "bg-indigo-50 text-indigo-700 ring-indigo-100",
  };

  return (
    <motion.article
      initial={{ opacity: 0, y: 14 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-lg border border-slate-200 bg-white p-5 shadow-soft"
    >
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-sm font-medium text-slate-500">{label}</p>
          <p className="mt-2 text-3xl font-bold text-slate-950">{value ?? 0}</p>
        </div>
        <div className={`grid h-12 w-12 place-items-center rounded-lg ring-1 ${tones[tone]}`}>
          <Icon size={22} />
        </div>
      </div>
    </motion.article>
  );
}
