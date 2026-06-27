import React, { useState } from 'react'
import { Sun, Moon, LogOut, User, Menu } from 'lucide-react'
import { useAuth } from '../../hooks/useAuth'
import { useTheme } from '../../hooks/useTheme'
import { Link } from 'react-router-dom'

const Navbar = ({ onToggleSidebar }) => {
  const { user, logout } = useAuth()
  const { darkMode, toggleTheme } = useTheme()
  const [dropdownOpen, setDropdownOpen] = useState(false)

  return (
    <nav className="sticky top-0 z-40 bg-white/80 dark:bg-gray-950/80 backdrop-blur-md border-b border-gray-100 dark:border-gray-900 px-6 py-4 flex items-center justify-between">
      {/* Mobile Toggle & Brand */}
      <div className="flex items-center space-x-4">
        <button
          onClick={onToggleSidebar}
          className="lg:hidden p-2 text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-900 rounded-lg"
        >
          <Menu className="h-5 w-5" />
        </button>
        <span className="lg:hidden font-extrabold text-xl bg-gradient-to-r from-primary-600 to-indigo-500 bg-clip-text text-transparent">
          Nexora AI
        </span>
      </div>

      <div className="flex items-center space-x-4 ml-auto">
        {/* Dark Mode Toggle */}
        <button
          onClick={toggleTheme}
          className="p-2.5 text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-900 rounded-xl transition-all duration-200"
          aria-label="Toggle theme"
        >
          {darkMode ? <Sun className="h-5 w-5 text-amber-500" /> : <Moon className="h-5 w-5 text-indigo-500" />}
        </button>

        {/* User Menu */}
        {user && (
          <div className="relative">
            <button
              onClick={() => setDropdownOpen(!dropdownOpen)}
              className="flex items-center space-x-3 p-1.5 hover:bg-gray-100 dark:hover:bg-gray-900 rounded-xl transition-all duration-200"
            >
              <img
                src={user.avatar_url || `https://api.dicebear.com/7.x/avataaars/svg?seed=${user.name}`}
                alt={user.name}
                className="h-8 w-8 rounded-lg object-cover ring-2 ring-primary-500/20"
              />
              <span className="hidden md:inline text-sm font-semibold text-gray-700 dark:text-gray-200">
                {user.name}
              </span>
            </button>

            {dropdownOpen && (
              <>
                <div
                  className="fixed inset-0 z-10"
                  onClick={() => setDropdownOpen(false)}
                />
                <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-950 border border-gray-100 dark:border-gray-900 rounded-xl shadow-2xl p-2 z-20">
                  <Link
                    to="/dashboard"
                    onClick={() => setDropdownOpen(false)}
                    className="flex items-center space-x-2 px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-primary-50 dark:hover:bg-primary-950/40 hover:text-primary-700 dark:hover:text-primary-300 rounded-lg transition-colors"
                  >
                    <User className="h-4 w-4" />
                    <span>My Profile</span>
                  </Link>
                  <button
                    onClick={() => {
                      setDropdownOpen(false)
                      logout()
                    }}
                    className="w-full flex items-center space-x-2 px-3 py-2 text-sm text-rose-600 dark:text-rose-400 hover:bg-rose-50 dark:hover:bg-rose-950/20 rounded-lg transition-colors"
                  >
                    <LogOut className="h-4 w-4" />
                    <span>Logout</span>
                  </button>
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </nav>
  )
}

export default Navbar
