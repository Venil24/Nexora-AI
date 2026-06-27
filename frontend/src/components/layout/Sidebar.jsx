import React from 'react'
import { NavLink, Link } from 'react-router-dom'
import { 
  LayoutDashboard, 
  UploadCloud, 
  History, 
  ShieldCheck, 
  Briefcase, 
  Map, 
  Github, 
  CheckSquare,
  FileText
} from 'lucide-react'

const Sidebar = ({ isOpen, onClose }) => {
  const menuItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'Upload Resume', path: '/upload', icon: UploadCloud },
    { name: 'Resume History', path: '/history', icon: History },
    { name: 'ATS Score Analyzer', path: '/ats-analyzer', icon: ShieldCheck },
    { name: 'JD Matcher', path: '/jd-matcher', icon: CheckSquare },
    { name: 'Career Path Predictor', path: '/career-predictor', icon: Briefcase },
    { name: 'Learning Roadmaps', path: '/roadmaps', icon: Map },
    { name: 'GitHub Analyzer', path: '/github-analyzer', icon: Github },
  ]

  const activeStyle = 'flex items-center space-x-3 px-4 py-3 bg-primary-600 text-white rounded-xl shadow-premium font-semibold transform scale-[1.02] transition-all duration-200'
  const inactiveStyle = 'flex items-center space-x-3 px-4 py-3 text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-900/60 hover:text-gray-900 dark:hover:text-gray-200 rounded-xl transition-all duration-200'

  return (
    <>
      {/* Mobile Sidebar Backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-gray-950/30 backdrop-blur-sm lg:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={`fixed top-0 bottom-0 left-0 z-40 w-64 bg-white dark:bg-gray-950 border-r border-gray-100 dark:border-gray-900 p-6 flex flex-col transition-transform duration-300 lg:translate-x-0 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Brand */}
        <div className="mb-8">
          <Link to="/dashboard" className="flex items-center space-x-3">
            <div className="p-2.5 bg-primary-600 rounded-xl shadow-premium">
              <FileText className="h-6 w-6 text-white" />
            </div>
            <span className="font-extrabold text-xl bg-gradient-to-r from-primary-600 to-indigo-500 bg-clip-text text-transparent">
              Nexora AI
            </span>
          </Link>
        </div>

        {/* Navigation Items */}
        <nav className="flex-1 space-y-2">
          {menuItems.map((item) => {
            const Icon = item.icon
            return (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={onClose}
                className={({ isActive }) => (isActive ? activeStyle : inactiveStyle)}
              >
                <Icon className="h-5 w-5" />
                <span>{item.name}</span>
              </NavLink>
            )
          })}
        </nav>

        {/* Footer */}
        <div className="border-t border-gray-100 dark:border-gray-900 pt-6">
          <div className="flex items-center space-x-3 p-3 bg-gray-50 dark:bg-gray-900/40 rounded-xl">
            <div className="flex-1 min-w-0">
              <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider">
                Production-Ready
              </p>
              <p className="text-sm font-bold text-gray-700 dark:text-gray-300 truncate">
                Nexora Core SaaS
              </p>
            </div>
          </div>
        </div>
      </aside>
    </>
  )
}

export default Sidebar
