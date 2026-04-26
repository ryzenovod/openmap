import { Route, Routes } from 'react-router-dom'
import { useEffect, useState } from 'react'
import Layout from './components/Layout'
import MapPage from './pages/MapPage'
import ChartsPage from './pages/ChartsPage'
import CasesPage from './pages/CasesPage'
import CaseDetailsPage from './pages/CaseDetailsPage'
import { api } from './api/endpoints'

export default function App() {
  const [healthStatus, setHealthStatus] = useState('checking')

  useEffect(() => {
    api
      .health()
      .then((resp) => setHealthStatus(resp.status))
      .catch(() => setHealthStatus('unreachable'))
  }, [])

  return (
    <Routes>
      <Route path="/" element={<MapPage healthStatus={healthStatus} />} />
      <Route
        path="/charts"
        element={
          <Layout healthStatus={healthStatus} summary={<div>Charts summary</div>}>
            <ChartsPage />
          </Layout>
        }
      />
      <Route
        path="/cases"
        element={
          <Layout healthStatus={healthStatus} summary={<div>Cases list</div>}>
            <CasesPage />
          </Layout>
        }
      />
      <Route
        path="/cases/:id"
        element={
          <Layout healthStatus={healthStatus} summary={<div>Case details</div>}>
            <CaseDetailsPage />
          </Layout>
        }
      />
    </Routes>
  )
}
