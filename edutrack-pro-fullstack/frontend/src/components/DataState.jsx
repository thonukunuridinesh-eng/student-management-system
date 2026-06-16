export function LoadingState({ label = "Loading data" }) {
  return (
    <div className="rounded-lg border border-dashed border-slate-300 bg-white p-8 text-center text-sm font-medium text-slate-500">
      {label}
    </div>
  );
}

export function EmptyState({ label = "No records found" }) {
  return (
    <div className="rounded-lg border border-dashed border-slate-300 bg-white p-8 text-center text-sm font-medium text-slate-500">
      {label}
    </div>
  );
}

export function ErrorState({ message }) {
  return (
    <div className="rounded-lg border border-rose-200 bg-rose-50 p-4 text-sm font-medium text-rose-700">
      {message || "Something went wrong."}
    </div>
  );
}
