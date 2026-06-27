import React, { useState, useEffect } from 'react'
import { useSearchParams, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ShieldCheck, Play, Download, UploadCloud } from 'lucide-react'
import resumeService from '../services/resumeService'
import analysisService from '../services/analysisService'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import Spinner from '../components/ui/Spinner'
import ATSScore from '../components/analysis/ATSScore'
import ScoreBreakdown from '../components/analysis/ScoreBreakdown'
import Suggestions from '../components/analysis/Suggestions'
import ScoreRadar from '../components/charts/ScoreRadar'

const ATSAnalyzer = () => {
  const [searchParams] = useSearchParams()
  const resumeId = searchParams.get('resumeId')

  const [resumes, setResumes] = useState([])
  const [selectedId, setSelectedId] = useState(resumeId || '')
  const [analysis, setAnalysis] = useState(null)
  const [running, setRunning] = useState(false)
  const [loading, setLoading] = useState(false)
  const [downloading, setDownloading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    resumeService.getHistory(1, 50).then((data) => {
      setResumes(data.resumes || [])
    }).catch(() => {})
  }, [])

  useEffect(() => {
    if (selectedId) {
      loadExistingAnalysis(selectedId)
    }
  }, [selectedId])

  const loadExistingAnalysis = async (id) => {
    setLoading(true)
    setAnalysis(null)
    setError('')
    try {
      const data = await analysisService.getAnalysis(id)
      setAnalysis(data)
    } catch {
      // No analysis yet — that's fine
    } finally {
      setLoading(false)
    }
  }

  const runAnalysis = async () => {
    if (!selectedId) return
    setRunning(true)
    setError('')
    try {
      const data = await analysisService.runAnalysis(selectedId)
      setAnalysis(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setRunning(false)
    }
  }

  const downloadReport = async () => {
    if (!selectedId) return
    setDownloading(true)
    try {
      const blob = await analysisService.downloadReportBlob(selectedId)
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `nexora_report_${selectedId.slice(0, 8)}.pdf`
      a.click()
      window.URL.revokeObjectURL(url)
    } catch (err) {
      alert(err.message)
    } finally {
      setDownloading(false)
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
          <h1 className="page-title">ATS Score Analyzer</h1>
          <p className="page-subtitle">Measure resume compatibility with Applicant Tracking Systems</p>
        </div>
        <div className="flex items-center gap-3">
          {analysis && (
            <Button onClick={downloadReport} loading={downloading} variant="outline" size="md">
              <Download className="h-4 w-4 mr-2" />
              Download Report
            </Button>
          )}
          <Button onClick={runAnalysis} loading={running} disabled={!selectedId} size="md" id="run-ats-analysis">
            <Play className="h-4 w-4 mr-2" />
            {analysis ? 'Re-Analyze' : 'Run Analysis'}
          </Button>
        </div>
      </motion.div>

      {/* Resume Selector */}
      <Card hoverEffect={false} className="mb-6">
        <label className="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400 mb-1.5 block">
          Select Resume to Analyze
        </label>
        {resumes.length === 0 ? (
          <div className="flex items-center justify-between p-4 bg-amber-50 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-900/50 rounded-xl">
            <p className="text-sm text-amber-700 dark:text-amber-400 font-medium">
              No resumes found. Upload one first.
            </p>
            <Link to="/upload">
              <Button size="sm" variant="outline">
                <UploadCloud className="h-4 w-4 mr-2" />
                Upload
              </Button>
            </Link>
          </div>
        ) : (
          <select
            value={selectedId}
            onChange={(e) => setSelectedId(e.target.value)}
            className="w-full px-4 py-2.5 rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/20"
            id="resume-selector"
          >
            <option value="">— Choose a resume —</option>
            {resumes.map((r) => (
              <option key={r.id} value={r.id}>{r.original_name}</option>
            ))}
          </select>
        )}
      </Card>

      {error && (
        <div className="mb-6 p-4 bg-rose-50 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-900/50 rounded-xl text-sm text-rose-700 dark:text-rose-400 font-medium">
          {error}
        </div>
      )}

      {loading && (
        <div className="flex justify-center py-20"><Spinner size="lg" /></div>
      )}

      {!loading && analysis && (
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="grid grid-cols-1 lg:grid-cols-3 gap-6"
        >
          {/* Overall ATS Score + Radar */}
          <div className="lg:col-span-1 space-y-6">
            <Card hoverEffect={false}>
              <ATSScore score={analysis.overall_score ?? 0} />
            </Card>
            <Card hoverEffect={false}>
              <h3 className="section-title text-center">Score Radar</h3>
              <ScoreRadar scores={analysis} />
            </Card>
          </div>

          {/* Breakdown + Suggestions */}
          <div className="lg:col-span-2 space-y-6">
            <Card hoverEffect={false}>
              <h3 className="section-title">Score Breakdown</h3>
              <ScoreBreakdown analysis={analysis} />
            </Card>

            <Card hoverEffect={false}>
              <h3 className="section-title">Optimization Guide</h3>
              <Suggestions
                suggestions={analysis.suggestions || []}
                strengths={analysis.strengths || []}
                weaknesses={analysis.weaknesses || []}
              />
            </Card>
          </div>
        </motion.div>
      )}

      {!loading && !analysis && selectedId && (
        <Card hoverEffect={false} className="text-center py-16">
          <ShieldCheck className="h-12 w-12 text-gray-300 dark:text-gray-700 mx-auto mb-4" />
          <h3 className="text-lg font-bold text-gray-500 dark:text-gray-400 mb-2">No Analysis Yet</h3>
          <p className="text-sm text-gray-400 dark:text-gray-600 mb-6">Click "Run Analysis" to get your ATS score.</p>
          <Button onClick={runAnalysis} loading={running} id="run-first-analysis">
            <Play className="h-4 w-4 mr-2" />
            Run ATS Analysis
          </Button>
        </Card>
      )}
    </div>
  )
}

export default ATSAnalyzer
