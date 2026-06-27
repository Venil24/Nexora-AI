import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Github, Search, Star, GitFork, ExternalLink, Activity } from 'lucide-react'
import githubService from '../services/githubService'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import Badge from '../components/ui/Badge'
import Progress from '../components/ui/Progress'
import SkillsChart from '../components/charts/SkillsChart'

const GitHubAnalyzer = () => {
  const [username, setUsername] = useState('')
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const analyze = async () => {
    if (!username.trim()) return
    setLoading(true)
    setError('')
    setData(null)
    try {
      const result = await githubService.analyzeProfile(username.trim())
      setData(result)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') analyze()
  }

  return (
    <div>
      <motion.div
        initial={{ opacity: 0, y: -8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="page-header"
      >
        <h1 className="page-title">GitHub Profile Analyzer</h1>
        <p className="page-subtitle">Analyze any GitHub profile and get developer activity metrics</p>
      </motion.div>

      {/* Search Input */}
      <Card hoverEffect={false} className="mb-6">
        <div className="flex gap-3">
          <div className="relative flex-1">
            <Github className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Enter GitHub username..."
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              onKeyDown={handleKeyDown}
              className="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/20"
              id="github-username-input"
            />
          </div>
          <Button
            onClick={analyze}
            loading={loading}
            disabled={!username.trim()}
            size="lg"
            id="analyze-github-btn"
          >
            <Search className="h-4 w-4 mr-2" />
            Analyze
          </Button>
        </div>
        {error && (
          <p className="text-sm text-rose-500 mt-2 font-medium">{error}</p>
        )}
      </Card>

      {/* Results */}
      {data && (
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="space-y-6"
        >
          {/* Profile Header */}
          <Card hoverEffect={false}>
            <div className="flex flex-col md:flex-row items-center md:items-start gap-6">
              <img
                src={data.profile?.avatar_url}
                alt={data.profile?.name || username}
                className="h-24 w-24 rounded-2xl object-cover ring-4 ring-primary-500/20"
              />
              <div className="flex-1 text-center md:text-left">
                <h2 className="text-2xl font-extrabold text-gray-900 dark:text-gray-100">
                  {data.profile?.name || username}
                </h2>
                <p className="text-gray-500 dark:text-gray-400 text-sm mb-3">
                  {data.profile?.bio || 'No bio available'}
                </p>
                <div className="flex flex-wrap justify-center md:justify-start gap-3">
                  {data.profile?.location && (
                    <Badge variant="gray">📍 {data.profile.location}</Badge>
                  )}
                  {data.profile?.company && (
                    <Badge variant="gray">🏢 {data.profile.company}</Badge>
                  )}
                  <a href={data.profile?.html_url} target="_blank" rel="noopener noreferrer">
                    <Badge variant="primary">
                      <ExternalLink className="h-3 w-3 mr-1" />View on GitHub
                    </Badge>
                  </a>
                </div>
              </div>

              {/* Scores */}
              <div className="flex gap-4">
                <div className="text-center p-4 bg-primary-50 dark:bg-primary-950/40 rounded-2xl min-w-[80px]">
                  <p className="text-2xl font-extrabold text-primary-600 dark:text-primary-400">{data.skill_score}</p>
                  <p className="text-xs text-gray-500 dark:text-gray-400 font-semibold mt-0.5">Skill Score</p>
                </div>
                <div className="text-center p-4 bg-emerald-50 dark:bg-emerald-950/40 rounded-2xl min-w-[80px]">
                  <p className="text-2xl font-extrabold text-emerald-600 dark:text-emerald-400">{data.activity_score}</p>
                  <p className="text-xs text-gray-500 dark:text-gray-400 font-semibold mt-0.5">Activity</p>
                </div>
              </div>
            </div>

            {/* Stats Bar */}
            <div className="grid grid-cols-4 gap-4 mt-6 pt-6 border-t border-gray-100 dark:border-gray-900">
              {[
                { label: 'Public Repos', value: data.total_repos },
                { label: 'Followers', value: data.followers },
                { label: 'Total Stars', value: data.total_stars },
                { label: 'Total Forks', value: data.total_forks },
              ].map((stat) => (
                <div key={stat.label} className="text-center">
                  <p className="text-xl font-extrabold text-gray-900 dark:text-gray-100">{stat.value}</p>
                  <p className="text-xs text-gray-400 dark:text-gray-500 font-semibold mt-0.5">{stat.label}</p>
                </div>
              ))}
            </div>
          </Card>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Languages */}
            <Card hoverEffect={false}>
              <h3 className="section-title">Top Languages Used</h3>
              <SkillsChart languages={data.languages || {}} />
            </Card>

            {/* Scores */}
            <Card hoverEffect={false}>
              <h3 className="section-title">Profile Score Breakdown</h3>
              <div className="space-y-5 mt-4">
                <Progress label="Skill Score" value={data.skill_score} showLabel size="md" />
                <Progress label="Activity Score" value={data.activity_score} showLabel size="md" />
              </div>
            </Card>
          </div>

          {/* Top Repos */}
          {data.top_repos && data.top_repos.length > 0 && (
            <Card hoverEffect={false}>
              <h3 className="section-title">Top Repositories</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {data.top_repos.map((repo, i) => (
                  <a
                    key={i}
                    href={repo.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="p-4 border border-gray-100 dark:border-gray-900 rounded-xl hover:border-primary-300 dark:hover:border-primary-800 hover:bg-primary-50/10 dark:hover:bg-primary-950/10 transition-all duration-200 block"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <h5 className="font-bold text-sm text-gray-900 dark:text-gray-100 truncate mr-2">{repo.name}</h5>
                      {repo.language && <Badge variant="gray" className="shrink-0">{repo.language}</Badge>}
                    </div>
                    {repo.description && (
                      <p className="text-xs text-gray-400 dark:text-gray-500 mb-2 line-clamp-2">{repo.description}</p>
                    )}
                    <div className="flex gap-4 text-xs text-gray-500">
                      <span className="flex items-center">
                        <Star className="h-3.5 w-3.5 mr-1 text-amber-400" />{repo.stars}
                      </span>
                      <span className="flex items-center">
                        <GitFork className="h-3.5 w-3.5 mr-1 text-blue-400" />{repo.forks}
                      </span>
                    </div>
                  </a>
                ))}
              </div>
            </Card>
          )}
        </motion.div>
      )}
    </div>
  )
}

export default GitHubAnalyzer
