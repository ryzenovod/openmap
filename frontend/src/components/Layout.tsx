import { Link, NavLink } from 'react-router-dom'
import type { ReactNode } from 'react'

type Props = {
  healthStatus: string
  sidebar?: ReactNode
  summary?: ReactNode
  children: ReactNode
}

export default function Layout({ healthStatus, sidebar, summary, children }: Props) {
  return (
    <div className="app-shell">
      <header className="header">
        <Link to="/" className="brand">
          OpenMap MVP
        </Link>
        <nav>
          <NavLink to="/" end>
            Map
          </NavLink>
          <NavLink to="/charts">Charts</NavLink>
          <NavLink to="/cases">Cases</NavLink>
        </nav>
        <div className={`health ${healthStatus === 'ok' ? 'ok' : 'bad'}`}>backend: {healthStatus}</div>
      </header>
      <div className="content-grid">
        <aside className="sidebar">{sidebar}</aside>
        <main className="main">{children}</main>
        <section className="summary">{summary}</section>
      </div>
    </div>
  )
}
