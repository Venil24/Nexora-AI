import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Map, Clock, DollarSign, BookOpen, ChevronDown, ChevronUp, Search } from 'lucide-react'
import careerService from '../services/careerService'
import Card from '../components/ui/Card'
import Badge from '../components/ui/Badge'
import Spinner from '../components/ui/Spinner'

const LearningRoadmap = () => {
  const [roadmaps, setRoadmaps] = useState([])
  const [selected, setSelected] = useState(null)
  const [detail, setDetail] = useState(null)
  const [loadingList, setLoadingList] = useState(true)
  const [loadingDetail, setLoadingDetail] = useState(false)
  const [search, setSearch] = useState('')
  const [expanded, setExpanded] = useState({})

  useEffect(() => {
    careerService.getRoadmaps()
      .then(setRoadmaps)
      .catch(() => setRoadmaps([]))
      .finally(() => setLoadingList(false))
  }, [])

  const selectRoadmap = async (career) => {
    if (selected === career) { setSelected(null); setDetail(null); return }
    setSelected(career)
    setDetail(null)
    setLoadingDetail(true)
    try {
      const d = await careerService.getRoadmap(career)
      setDetail(d)
    } catch {
      setDetail(null)
    } finally {
      setLoadingDetail(false)
    }
  }

  const togglePhase = (phase) => setExpanded((prev) => ({ ...prev, [phase]: !prev[phase] }))

  const filtered = search
    ? roadmaps.filter((r) => r.career?.toLowerCase().includes(search.toLowerCase()))
    : roadmaps

  const difficultyColor = (d) => {
    if (!d) return 'gray'
    if (d.toLowerCase().includes('beginner')) return 'success'
    if (d.toLowerCase().includes('advanced')) return 'danger'
    return 'warning'
  }

  return (
    <div>
      <motion.div
        initial={{ opacity: 0, y: -8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="page-header flex flex-col md:flex-row md:items-center justify-between gap-4"
      >
        <div>
          <h1 className="page-title">Learning Roadmaps</h1>
          <p className="page-subtitle">Structured step-by-step career learning paths curated by AI</p>
        </div>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search careers..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-9 pr-4 py-2 text-sm border border-gray-200 dark:border-gray-800 rounded-xl bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500/20"
          />
        </div>
      </motion.div>

      {loadingList ? (
        <div className="flex justify-center py-20"><Spinner size="lg" /></div>
      ) : filtered.length === 0 ? (
        <Card hoverEffect={false} className="text-center py-16">
          <Map className="h-12 w-12 text-gray-300 dark:text-gray-700 mx-auto mb-4" />
          <h3 className="text-lg font-bold text-gray-500 dark:text-gray-400">No roadmaps found</h3>
          <p className="text-sm text-gray-400 dark:text-gray-600 mt-1">
            Run <code className="bg-gray-100 dark:bg-gray-900 px-2 py-0.5 rounded text-xs">python database/seed.py</code> to populate roadmaps.
          </p>
        </Card>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Roadmap List */}
          <div className="lg:col-span-1 space-y-3">
            {filtered.map((r, i) => (
              <motion.button
                key={r.career}
                initial={{ opacity: 0, x: -16 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.04 }}
                onClick={() => selectRoadmap(r.career)}
                className={`w-full text-left p-4 rounded-2xl border transition-all duration-200 ${
                  selected === r.career
                    ? 'border-primary-500 bg-primary-50/40 dark:bg-primary-950/20 shadow-premium'
                    : 'border-gray-100 dark:border-gray-900 bg-white dark:bg-gray-950 hover:border-primary-300 dark:hover:border-primary-800'
                }`}
              >
                <h4 className="font-bold text-sm text-gray-900 dark:text-gray-100 mb-2">{r.career}</h4>
                <div className="flex flex-wrap gap-2">
                  {r.duration_weeks && (
                    <span className="inline-flex items-center text-xs text-gray-500 dark:text-gray-400">
                      <Clock className="h-3 w-3 mr-1" />{r.duration_weeks}w
                    </span>
                  )}
                  {r.avg_salary && (
                    <span className="inline-flex items-center text-xs text-emerald-600 dark:text-emerald-400">
                      <DollarSign className="h-3 w-3" />{r.avg_salary}
                    </span>
                  )}
                  {r.difficulty && (
                    <Badge variant={difficultyColor(r.difficulty)} className="text-xs">{r.difficulty}</Badge>
                  )}
                </div>
              </motion.button>
            ))}
          </div>

          {/* Roadmap Detail */}
          <div className="lg:col-span-2">
            {!selected && (
              <Card hoverEffect={false} className="text-center py-20">
                <Map className="h-12 w-12 text-gray-300 dark:text-gray-700 mx-auto mb-4" />
                <h4 className="font-bold text-gray-400 dark:text-gray-600">Select a career to view its roadmap</h4>
              </Card>
            )}

            {selected && loadingDetail && (
              <div className="flex justify-center py-20"><Spinner size="lg" /></div>
            )}

            {selected && detail && !loadingDetail && (
              <motion.div
                initial={{ opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4 }}
                className="space-y-5"
              >
                {/* Header */}
                <Card hoverEffect={false} className="bg-gradient-to-br from-primary-600 to-indigo-600 border-0 text-white">
                  <h2 className="text-xl font-extrabold mb-1">{detail.career || detail.title}</h2>
                  <div className="flex flex-wrap gap-4 mt-3">
                    {detail.duration_weeks && (
                      <div className="flex items-center text-sm text-primary-100">
                        <Clock className="h-4 w-4 mr-1.5" />
                        {detail.duration_weeks} Weeks
                      </div>
                    )}
                    {detail.avg_salary && (
                      <div className="flex items-center text-sm text-primary-100">
                        <DollarSign className="h-4 w-4 mr-1.5" />
                        {detail.avg_salary}/year
                      </div>
                    )}
                    {detail.difficulty && (
                      <div className="flex items-center text-sm text-primary-100">
                        <BookOpen className="h-4 w-4 mr-1.5" />
                        {detail.difficulty}
                      </div>
                    )}
                  </div>
                </Card>

                {/* Phases */}
                {(detail.phases || detail.steps || []).map((phase, i) => (
                  <Card key={i} hoverEffect={false}>
                    <button
                      onClick={() => togglePhase(i)}
                      className="w-full flex items-center justify-between"
                    >
                      <div className="flex items-center space-x-3">
                        <span className="flex items-center justify-center h-8 w-8 rounded-xl bg-primary-50 dark:bg-primary-950/40 text-primary-600 dark:text-primary-400 text-sm font-extrabold">
                          {i + 1}
                        </span>
                        <div className="text-left">
                          <h4 className="font-bold text-sm text-gray-900 dark:text-gray-100">
                            {phase.phase || phase.title || `Phase ${i + 1}`}
                          </h4>
                          {phase.duration && (
                            <p className="text-xs text-gray-400">~{phase.duration}</p>
                          )}
                        </div>
                      </div>
                      {expanded[i] ? <ChevronUp className="h-4 w-4 text-gray-400" /> : <ChevronDown className="h-4 w-4 text-gray-400" />}
                    </button>

                    <AnimatePresence>
                      {expanded[i] && (
                        <motion.div
                          initial={{ opacity: 0, height: 0 }}
                          animate={{ opacity: 1, height: 'auto' }}
                          exit={{ opacity: 0, height: 0 }}
                          transition={{ duration: 0.25 }}
                          className="overflow-hidden"
                        >
                          <div className="pt-4 mt-4 border-t border-gray-100 dark:border-gray-900 space-y-3">
                            {(phase.topics || phase.skills || []).map((item, j) => (
                              <div key={j} className="flex items-center space-x-2">
                                <span className="h-1.5 w-1.5 rounded-full bg-primary-500 shrink-0" />
                                <span className="text-sm text-gray-700 dark:text-gray-300">{typeof item === 'string' ? item : item.name || item.topic}</span>
                              </div>
                            ))}
                            {(phase.resources || []).map((r, j) => (
                              <a
                                key={j}
                                href={r.url || '#'}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="flex items-center space-x-2 text-sm text-primary-600 dark:text-primary-400 hover:underline"
                              >
                                <BookOpen className="h-3.5 w-3.5 shrink-0" />
                                <span>{r.title || r}</span>
                              </a>
                            ))}
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </Card>
                ))}

                {/* Skills to learn */}
                {detail.skills_to_learn && detail.skills_to_learn.length > 0 && (
                  <Card hoverEffect={false}>
                    <h3 className="section-title">Skills You'll Master</h3>
                    <div className="flex flex-wrap gap-2">
                      {detail.skills_to_learn.map((s, i) => (
                        <Badge key={i} variant="primary">{s}</Badge>
                      ))}
                    </div>
                  </Card>
                )}
              </motion.div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default LearningRoadmap
