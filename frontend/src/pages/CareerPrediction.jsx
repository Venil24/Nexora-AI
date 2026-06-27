import React, { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Sparkles, Play, Map } from 'lucide-react'
import resumeService from '../services/resumeService'
import careerService from '../services/careerService'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import Badge from '../components/ui/Badge'
import Progress from '../components/ui/Progress'
import CareerChart from '../components/charts/CareerChart'

const CareerPrediction = () => {
  const [searchParams] = useSearchParams()
  const resumeId = searchParams.get('resumeId')

  const [resumes, setResumes] = useState([])
  const [selectedId, setSelectedId] = useState(resumeId || '')
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [questions, setQuestions] = useState([])
  const [loadingQ, setLoadingQ] = useState(false)

  useEffect(() => {
    resumeService.getHistory(1, 50).then((d) => setResumes(d.resumes || [])).catch(() => {})
  }, [])

  const runPrediction = async () => {
    if (!selectedId) return
    setLoading(true)
    setError('')
    setPrediction(null)
    try {
      const data = await careerService.predictCareer(selectedId)
      setPrediction(data)
      loadQuestions(data.predicted_career)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const loadQuestions = async (career) => {
    setLoadingQ(true)
    try {
      const data = await careerService.getInterviewQuestions(career)
      setQuestions(data.questions || [])
    } catch {
      setQuestions([])
    } finally {
      setLoadingQ(false)
    }
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
          <h1 className="page-title">Career Path Predictor</h1>
          <p className="page-subtitle">AI-powered career prediction based on your skills and experience</p>
        </div>
        <Button
          onClick={runPrediction}
          loading={loading}
          disabled={!selectedId}
          id="run-career-prediction"
        >
          <Play className="h-4 w-4 mr-2" />
          {prediction ? 'Re-Predict' : 'Predict My Career'}
        </Button>
      </motion.div>

      {/* Resume Selector */}
      <Card hoverEffect={false} className="mb-6">
        <label className="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400 mb-1.5 block">
          Select Resume
        </label>
        <select
          value={selectedId}
          onChange={(e) => setSelectedId(e.target.value)}
          className="w-full px-4 py-2.5 rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/20"
          id="career-resume-selector"
        >
          <option value="">— Select a resume —</option>
          {resumes.map((r) => (
            <option key={r.id} value={r.id}>{r.original_name}</option>
          ))}
        </select>
      </Card>

      {error && (
        <div className="mb-6 p-4 bg-rose-50 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-900/50 rounded-xl text-sm text-rose-700 dark:text-rose-400 font-medium">
          {error}
        </div>
      )}

      {!prediction && !loading && (
        <Card hoverEffect={false} className="text-center py-20">
          <Sparkles className="h-14 w-14 text-gray-300 dark:text-gray-700 mx-auto mb-4 animate-pulse" />
          <h3 className="text-lg font-bold text-gray-500 dark:text-gray-400 mb-2">Ready to Predict</h3>
          <p className="text-sm text-gray-400 dark:text-gray-600">Select a resume and click "Predict My Career" to see results.</p>
        </Card>
      )}

      {prediction && (
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="space-y-6"
        >
          {/* Top Prediction Banner */}
          <div className="rounded-2xl bg-gradient-to-br from-primary-600 to-indigo-600 p-8 text-white">
            <p className="text-primary-200 text-sm font-semibold mb-1">🎯 Best Career Match</p>
            <h2 className="text-3xl font-extrabold mb-2">{prediction.predicted_career}</h2>
            <div className="flex items-center space-x-4">
              <div className="bg-white/20 rounded-xl px-4 py-2">
                <p className="text-xs text-primary-200">Confidence</p>
                <p className="text-xl font-extrabold">{prediction.confidence?.toFixed(1)}%</p>
              </div>
              {prediction.model_used && (
                <div className="bg-white/20 rounded-xl px-4 py-2">
                  <p className="text-xs text-primary-200">Model</p>
                  <p className="text-sm font-bold">{prediction.model_used}</p>
                </div>
              )}
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Top Careers Chart */}
            <Card hoverEffect={false}>
              <h3 className="section-title">Top Career Matches</h3>
              <CareerChart topCareers={prediction.top_careers || []} />
            </Card>

            {/* Skills Detected */}
            <Card hoverEffect={false}>
              <h3 className="section-title">Skills Detected in Resume</h3>
              <div className="flex flex-wrap gap-2 max-h-48 overflow-y-auto">
                {(prediction.detected_skills || []).map((s, i) => (
                  <Badge key={i} variant="primary">{s}</Badge>
                ))}
                {(prediction.detected_skills || []).length === 0 && (
                  <p className="text-sm text-gray-400">No skills data found. Please re-upload resume.</p>
                )}
              </div>

              {prediction.skills_gap && prediction.skills_gap.length > 0 && (
                <div className="mt-4">
                  <p className="text-xs font-bold text-amber-600 dark:text-amber-400 uppercase tracking-wider mb-2">
                    Skills to Add for {prediction.predicted_career}
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {prediction.skills_gap.map((s, i) => (
                      <Badge key={i} variant="warning">{s}</Badge>
                    ))}
                  </div>
                </div>
              )}
            </Card>
          </div>

          {/* Career Details */}
          {prediction.salary_range && (
            <Card hoverEffect={false}>
              <h3 className="section-title">Career Insights</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {prediction.salary_range && (
                  <div className="p-4 bg-gray-50 dark:bg-gray-900/40 rounded-xl text-center">
                    <p className="text-xs text-gray-400 font-semibold mb-1">Avg. Salary</p>
                    <p className="font-extrabold text-emerald-600 dark:text-emerald-400">{prediction.salary_range}</p>
                  </div>
                )}
                {prediction.market_demand && (
                  <div className="p-4 bg-gray-50 dark:bg-gray-900/40 rounded-xl text-center">
                    <p className="text-xs text-gray-400 font-semibold mb-1">Market Demand</p>
                    <p className="font-extrabold text-primary-600 dark:text-primary-400">{prediction.market_demand}</p>
                  </div>
                )}
              </div>
            </Card>
          )}

          {/* Interview Questions */}
          {questions.length > 0 && (
            <Card hoverEffect={false}>
              <h3 className="section-title">Top Interview Questions for {prediction.predicted_career}</h3>
              <div className="space-y-3">
                {questions.slice(0, 8).map((q, i) => (
                  <div key={i} className="flex items-start space-x-3 p-3 bg-gray-50 dark:bg-gray-900/40 rounded-xl">
                    <span className="flex items-center justify-center h-6 w-6 rounded-lg bg-primary-50 dark:bg-primary-950/40 text-primary-600 dark:text-primary-400 text-xs font-extrabold shrink-0">
                      {i + 1}
                    </span>
                    <p className="text-sm text-gray-700 dark:text-gray-300">{q}</p>
                  </div>
                ))}
              </div>
            </Card>
          )}
        </motion.div>
      )}
    </div>
  )
}

export default CareerPrediction
