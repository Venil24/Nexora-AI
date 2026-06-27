import React from 'react'
import { Outlet, Link, Navigate } from 'react-router-dom'
import { FileText } from 'lucide-react'
import { useAuthStore } from '../../store/authStore'

const AuthLayout = () => {
  const { isAuthenticated } = useAuthStore()

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />
  }

  return (
    <div className="min-h-screen flex flex-col justify-center items-center py-12 px-4 sm:px-6 lg:px-8 bg-gray-50 dark:bg-gray-950/40 text-gray-900 dark:text-gray-100">
      <div className="w-full max-w-md">
        {/* Brand/Logo */}
        <div className="flex flex-col items-center mb-8">
          <Link to="/" className="flex items-center space-x-3 mb-2">
            <div className="p-3 bg-primary-600 rounded-xl shadow-premium">
              <FileText className="h-8 w-8 text-white" />
            </div>
            <span className="font-extrabold text-3xl bg-gradient-to-r from-primary-600 to-indigo-500 bg-clip-text text-transparent">
              Nexora AI
            </span>
          </Link>
          <p className="text-sm font-semibold text-gray-500 dark:text-gray-400">
            AI Resume Analyzer & Career Roadmap SaaS
          </p>
        </div>

        {/* Center Card */}
        <div className="bg-white dark:bg-gray-950 border border-gray-100 dark:border-gray-900 rounded-3xl shadow-premium p-8">
          <Outlet />
        </div>
      </div>
    </div>
  )
}

export default AuthLayout
