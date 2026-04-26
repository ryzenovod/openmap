export default function EmptyView({ text }: { text: string }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-slate-50 p-8 text-center text-slate-600">
      {text}
    </div>
  )
}
