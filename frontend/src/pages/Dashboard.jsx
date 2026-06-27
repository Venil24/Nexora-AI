import React, { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { UploadCloud, ShieldCheck, Sparkles, History, Github, ArrowRight, TrendingUp, FileText } from 'lucide-react'
import { useAuth } from '../hooks/useAuth'
import resumeService from '../services/resumeService'
import Card from '../components/ui/Card'
import Badge from '../components/ui/Badge'
import Spinner from '../components/ui/Spinner'
import Button from '../components/ui/Button'

const StatCard = ({ icon: Icon, label, value, color, delay }) => (
  <motion.div
    initial={{ opacity: 0, y: 16 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ delay, duration: 0.4 }}
    className="stat-card"
  >
    <div className={`inline-flex p-3 rounded-xl ${color} mb-4`}>
      <Icon className="h-6 w-6" />
    </div>
    <div className="text-3xl font-extrabold text-gray-900 dark:text-gray-100 mb-1">{value}</div>
    <div className="text-sm text-gray-500 dark:text-gray-400 font-semibold">{label}</div>
  </motion.div>
)

const QuickAction = ({ to, icon: Icon, title, desc, color }) => (
  <Link to={to}>
    <motion.div
      whileHover={{ y: -3, scale: 1.01 }}
      transition={{ duration: 0.2 }}
      className="flex items-start space-x-4 p-4 bg-white dark:bg-gray-950 border border-gray-100 dark:border-gray-900 rounded-2xl shadow-premium hover:shadow-premium-hover cursor-pointer"
    >
      <div className={`p-3 ${color} rounded-xl shrink-0`}>
        <Icon className="h-5 w-5" />
      </div>
      <div>
        <h4 className="font-bold text-sm text-gray-900 dark:text-gray-100">{title}</h4>
        <p className="text-xs text-gray-400 dark:text-gray-500 mt-0.5">{desc}</p>
      </div>
      <ArrowRight className="h-4 w-4 text-gray-300 dark:text-gray-700 self-center ml-auto shrink-0" />
    </motion.div>
  </Link>
)

const Dashboard = () => {
  const { user } = useAuth()
  const [stats, setStats] = useState(null)
  const [loadingStats, setLoadingStats] = useState(true)

  useEffect(() => {
    resumeService.getStats()
      .then(setStats)
      .catch(() => setStats({ total_resumes: 0, analyzed: 0, avg_ats_score: 0 }))
      .finally(() => setLoadingStats(false))
  }, [])

  const quickActions = [
    { to: '/upload', icon: UploadCloud, title: 'Upload New Resume', desc: 'Parse and analyze a fresh PDF', color: 'bg-primary-50 dark:bg-primary-950/40 text-primary-600 dark:text-primary-400' },
    { to: '/ats-analyzer', icon: ShieldCheck, title: 'ATS Score Analyzer', desc: 'Get your ATS compatibility score', color: 'bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 dark:text-emerald-400' },
    { to: '/career-predictor', icon: Sparkles, title: 'Career Path Predictor', desc: 'AI-powered career recommendations', color: 'bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-400' },
    { to: '/github-analyzer', icon: Github, title: 'GitHub Analyzer', desc: 'Analyze your GitHub profile metrics', color: 'bg-amber-50 dark:bg-amber-950/40 text-amber-600 dark:text-amber-400' },
    { to: '/roadmaps', icon: TrendingUp, title: 'Learning Roadmaps', desc: 'Browse career learning paths', color: 'bg-rose-50 dark:bg-rose-950/40 text-rose-600 dark:text-rose-400' },
    { to: '/history', icon: History, title: 'Resume History', desc: 'View all your uploaded resumes', color: 'bg-teal-50 dark:bg-teal-950/40 text-teal-600 dark:text-teal-400' },
  ]

  const greeting = () => {
    const h = new Date().getHours()
    if (h < 12) return 'Good morning'
    if (h < 17) return 'Good afternoon'
    return 'Good evening'
  }

  return (
    <div>
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="page-header"
      >
        <h1 className="page-title">
          {greeting()}, {user?.name?.split(' ')[0]} 👋
        </h1>
        <p className="page-subtitle">Here's your career analytics overview for today.</p>
      </motion.div>

      {/* Stats Row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {loadingStats ? (
          <div className="col-span-4 flex justify-center py-8"><Spinner size="lg" /></div>
        ) : (
          <>
            <StatCard icon={FileText} label="Total Resumes" value={stats?.total_resumes ?? 0} color="bg-primary-50 dark:bg-primary-950/40 text-primary-600 dark:text-primary-400" delay={0.05} />
            <StatCard icon={ShieldCheck} label="Analyzed" value={stats?.analyzed ?? 0} color="bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 dark:text-emerald-400" delay={0.1} />
            <StatCard icon={TrendingUp} label="Avg ATS Score" value={`${stats?.avg_ats_score ?? 0}%`} color="bg-amber-50 dark:bg-amber-950/40 text-amber-600 dark:text-amber-400" delay={0.15} />
            <StatCard icon={Sparkles} label="Career Insights" value="AI Ready" color="bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-400" delay={0.2} />
          </>
        )}
      </div>

      {/* Quick Actions */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.25, duration: 0.4 }}
      >
        <h2 className="section-title">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {quickActions.map((a, i) => (
            <QuickAction key={i} {...a} />
          ))}
        </div>
      </motion.div>

      {/* CTA Banner */}
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.35, duration: 0.4 }}
        className="mt-8 rounded-2xl bg-gradient-to-br from-primary-600 to-indigo-600 p-8 text-white flex flex-col md:flex-row items-center justify-between gap-6"
      >
        <div>
          <h3 className="text-xl font-extrabold mb-1">
            🎯 Ready to boost your resume?
          </h3>
          <p className="text-primary-100 text-sm font-medium">
            Upload your resume and get an instant AI analysis — ATS score, keyword gaps, and career insights.
          </p>
        </div>
        <Link to="/upload">
          <Button variant="outline" size="lg" className="border-white text-white hover:bg-white/10 whitespace-nowrap">
            <UploadCloud className="h-5 w-5 mr-2" />
            Upload Resume Now
          </Button>
        </Link>
      </motion.div>
    </div>
  )
}

export default Dashboard
