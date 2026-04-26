import { NavLink } from 'react-router-dom'
import type { ReactNode } from 'react'
import { useTranslation } from 'react-i18next'

type Props = {
  healthStatus: string
  sidebar?: ReactNode
  summary?: ReactNode
  children: ReactNode
}

const DEBUG_MODE = import.meta.env.VITE_DEBUG_MODE === 'true'

export default function Layout({ healthStatus, sidebar, summary, children }: Props) {
  const { t } = useTranslation()

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800">
      <header className="sticky top-0 z-30 border-b border-slate-200/80 bg-white/90 backdrop-blur">
        <div className="mx-auto flex max-w-[1440px] items-center gap-8 px-6 py-4">
          <div>
            <p className="text-xs font-medium uppercase tracking-[0.12em] text-sky-600">OpenMap</p>
            <h1 className="text-lg font-semibold">{t('nav.appTitle')}</h1>
          </div>
          <nav className="flex items-center gap-2 rounded-xl bg-slate-100 p-1">
            <NavItem to="/" label={t('nav.map')} />
            <NavItem to="/charts" label={t('nav.charts')} />
            <NavItem to="/cases" label={t('nav.cases')} />
          </nav>
          {DEBUG_MODE && (
            <div className="ml-auto rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-xs text-slate-600">
              {t('debug.backend')}: <span className="font-semibold">{healthStatus}</span>
            </div>
          )}
        </div>
      </header>

      <div className="mx-auto grid max-w-[1440px] grid-cols-12 gap-4 px-6 py-5">
        <aside className="col-span-12 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm lg:col-span-3">
          {sidebar}
        </aside>
        <main className="col-span-12 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm lg:col-span-6">
          {children}
        </main>
        <section className="col-span-12 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm lg:col-span-3">
          {summary}
        </section>
      </div>
    </div>
  )
}

function NavItem({ to, label }: { to: string; label: string }) {
  return (
    <NavLink
      to={to}
      end={to === '/'}
      className={({ isActive }) =>
        [
          'rounded-lg px-4 py-2 text-sm font-medium transition',
          isActive
            ? 'bg-white text-slate-900 shadow-sm'
            : 'text-slate-600 hover:bg-white/70 hover:text-slate-900',
        ].join(' ')
      }
    >
      {label}
    </NavLink>
  )
}
