import React, { useEffect } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useThemeStore } from './store/themeStore'

// Layouts
import AuthLayout from './components/layout/AuthLayout'
import DashboardLayout from './components/layout/DashboardLayout'
import ProtectedRoute from './components/ProtectedRoute'

// Auth Pages
import Login from './pages/auth/Login'
import Signup from './pages/auth/Signup'
import ForgotPassword from './pages/auth/ForgotPassword'

// Dashboard Pages
import Dashboard from './pages/Dashboard'
import ResumeUpload from './pages/ResumeUpload'
import ResumeHistory from './pages/ResumeHistory'
import ATSAnalyzer from './pages/ATSAnalyzer'
import JDMatcher from './pages/JDMatcher'
import CareerPrediction from './pages/CareerPrediction'
import LearningRoadmap from './pages/LearningRoadmap'
import GitHubAnalyzer from './pages/GitHubAnalyzer'
import NotFound from './pages/NotFound'

const App = () => {
  const { initTheme } = useThemeStore()

  useEffect(() => {
    initTheme()
  }, [initTheme])

  return (
    <BrowserRouter>
      <Routes>
        {/* Default redirect */}
        <Route path="/" element={<Navigate to="/login" replace />} />

        {/* Auth Routes */}
        <Route element={<AuthLayout />}>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
        </Route>

        {/* Protected Dashboard Routes */}
        <Route element={<ProtectedRoute />}>
          <Route element={<DashboardLayout />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/upload" element={<ResumeUpload />} />
            <Route path="/history" element={<ResumeHistory />} />
            <Route path="/ats-analyzer" element={<ATSAnalyzer />} />
            <Route path="/jd-matcher" element={<JDMatcher />} />
            <Route path="/career-predictor" element={<CareerPrediction />} />
            <Route path="/roadmaps" element={<LearningRoadmap />} />
            <Route path="/github-analyzer" element={<GitHubAnalyzer />} />
          </Route>
        </Route>

        {/* 404 */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
