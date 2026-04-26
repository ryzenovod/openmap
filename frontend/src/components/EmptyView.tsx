export default function EmptyView({ text = 'No data' }: { text?: string }) {
  return <div className="empty">{text}</div>
}
