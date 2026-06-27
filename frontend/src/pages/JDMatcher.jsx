import React, { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { CheckSquare, Zap, TrendingUp } from 'lucide-react'
import resumeService from '../services/resumeService'
import analysisService from '../services/analysisService'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import Progress from '../components/ui/Progress'
import Badge from '../components/ui/Badge'

const JDMatcher = () => {
  const [searchParams] = useSearchParams()
  const resumeId = searchParams.get('resumeId')

  const [resumes, setResumes] = useState([])
  const [selectedId, setSelectedId] = useState(resumeId || '')
  const [jdText, setJdText] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    resumeService.getHistory(1, 50).then((d) => setResumes(d.resumes || [])).catch(() => {})
  }, [])

  const runMatch = async () => {
    if (!selectedId || !jdText.trim()) {
      setError('Please select a resume and enter a job description.')
      return
    }
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const data = await analysisService.jdMatch(selectedId, jdText)
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const getMatchColor = (score) => {
    if (score >= 75) return 'success'
    if (score >= 50) return 'warning'
    return 'danger'
  }

  return (
    <div>
      <motion.div
        initial={{ opacity: 0, y: -8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="page-header"
      >
        <h1 className="page-title">Job Description Matcher</h1>
        <p className="page-subtitle">Measure how well your resume matches a specific job description using AI semantic similarity</p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Panel */}
        <div className="space-y-6">
          <Card hoverEffect={false}>
            <h3 className="section-title">1. Select Resume</h3>
            <select
              value={selectedId}
              onChange={(e) => setSelectedId(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/20"
              id="jd-resume-selector"
            >
              <option value="">— Select a resume —</option>
              {resumes.map((r) => (
                <option key={r.id} value={r.id}>{r.original_name}</option>
              ))}
            </select>
          </Card>

          <Card hoverEffect={false}>
            <h3 className="section-title">2. Paste Job Description</h3>
            <textarea
              value={jdText}
              onChange={(e) => setJdText(e.target.value)}
              placeholder="Paste the full job description here... Include requirements, responsibilities, and qualifications for the best match accuracy."
              rows={12}
              className="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 text-sm text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-primary-500/20 resize-none"
              id="jd-text-input"
            />
            <div className="flex justify-between items-center mt-3">
              <span className="text-xs text-gray-400">{jdText.length} characters</span>
              <Button
                onClick={runMatch}
                loading={loading}
                disabled={!selectedId || jdText.length < 50}
                id="run-jd-match"
              >
                <Zap className="h-4 w-4 mr-2" />
                Analyze Match
              </Button>
            </div>
            {error && (
              <p className="text-xs text-rose-500 mt-2 font-medium">{error}</p>
            )}
          </Card>
        </div>

        {/* Results Panel */}
        <div className="space-y-6">
          {!result && !loading && (
            <Card hoverEffect={false} className="text-center py-16">
              <CheckSquare className="h-12 w-12 text-gray-300 dark:text-gray-700 mx-auto mb-4" />
              <h4 className="font-bold text-gray-400 dark:text-gray-600 mb-1">No Results Yet</h4>
              <p className="text-sm text-gray-400 dark:text-gray-600">
                Select a resume and paste a job description to see your match score.
              </p>
            </Card>
          )}

          {loading && (
            <Card hoverEffect={false} className="text-center py-16">
              <div className="flex justify-center mb-4">
                <Zap className="h-10 w-10 text-primary-500 animate-pulse" />
              </div>
              <p className="text-sm font-bold text-gray-600 dark:text-gray-400">
                Running semantic similarity analysis...
              </p>
            </Card>
          )}

          {result && !loading && (
            <motion.div
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4 }}
              className="space-y-5"
            >
              {/* Overall Score */}
              <Card hoverEffect={false} className="text-center">
                <h3 className="section-title text-center">Overall Match Score</h3>
                <div className="text-6xl font-extrabold gradient-text mb-2">
                  {result.overall_match ?? result.match_score ?? 0}%
                </div>
                <Badge variant={getMatchColor(result.overall_match ?? result.match_score ?? 0)} className="text-sm px-4 py-1">
                  {(result.overall_match ?? result.match_score ?? 0) >= 75 ? 'Strong Match' : (result.overall_match ?? result.match_score ?? 0) >= 50 ? 'Moderate Match' : 'Weak Match'}
                </Badge>
              </Card>

              {/* Semantic Score */}
              <Card hoverEffect={false}>
                <h3 className="section-title">Match Breakdown</h3>
                <div className="space-y-4">
                  <Progress label="Semantic Similarity" value={result.semantic_score ?? 0} showLabel size="md" />
                  <Progress label="Keyword Overlap" value={result.keyword_overlap ?? 0} showLabel size="md" />
                  <Progress label="Skills Match" value={result.skills_match_percent ?? 0} showLabel size="md" />
                </div>
              </Card>

              {/* Matched & Missing Skills */}
              <Card hoverEffect={false}>
                <h3 className="section-title">Skill Gap Analysis</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Matched */}
                  <div>
                    <p className="text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider mb-2">
                      ✅ Matched Skills ({(result.matched_skills || []).length})
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {(result.matched_skills || []).map((s, i) => (
                        <Badge key={i} variant="success">{s}</Badge>
                      ))}
                      {(result.matched_skills || []).length === 0 && <p className="text-xs text-gray-400">None detected</p>}
                    </div>
                  </div>
                  {/* Missing */}
                  <div>
                    <p className="text-xs font-bold text-rose-600 dark:text-rose-400 uppercase tracking-wider mb-2">
                      ❌ Missing Skills ({(result.missing_skills || []).length})
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {(result.missing_skills || []).map((s, i) => (
                        <Badge key={i} variant="danger">{s}</Badge>
                      ))}
                      {(result.missing_skills || []).length === 0 && <p className="text-xs text-gray-400">All skills matched!</p>}
                    </div>
                  </div>
                </div>
              </Card>

              {/* Recommendation */}
              {result.recommendation && (
                <Card hoverEffect={false} className="bg-primary-50/30 dark:bg-primary-950/10 border-primary-100 dark:border-primary-900/30">
                  <div className="flex items-start space-x-3">
                    <TrendingUp className="h-5 w-5 text-primary-600 dark:text-primary-400 shrink-0 mt-0.5" />
                    <div>
                      <h4 className="text-sm font-bold text-primary-800 dark:text-primary-300 mb-1">AI Recommendation</h4>
                      <p className="text-sm text-primary-700/80 dark:text-primary-400/80">{result.recommendation}</p>
                    </div>
                  </div>
                </Card>
              )}
            </motion.div>
          )}
        </div>
      </div>
    </div>
  )
}

export default JDMatcher
