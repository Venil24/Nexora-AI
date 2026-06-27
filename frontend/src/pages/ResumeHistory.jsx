import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { UploadCloud, Search, RefreshCw } from 'lucide-react'
import resumeService from '../services/resumeService'
import analysisService from '../services/analysisService'
import ResumeCard from '../components/resume/ResumeCard'
import Spinner from '../components/ui/Spinner'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'

const ResumeHistory = () => {
  const [resumes, setResumes] = useState([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [pages, setPages] = useState(1)
  const [loading, setLoading] = useState(true)
  const [analyzing, setAnalyzing] = useState(null)
  const [search, setSearch] = useState('')

  const loadHistory = async (p = 1) => {
    setLoading(true)
    try {
      const data = await resumeService.getHistory(p, 9)
      setResumes(data.resumes || [])
      setTotal(data.total || 0)
      setPages(data.pages || 1)
      setPage(p)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadHistory(1)
  }, [])

  const handleDelete = async (resumeId) => {
    if (!window.confirm('Are you sure you want to delete this resume? This action cannot be undone.')) return
    try {
      await resumeService.deleteResume(resumeId)
      setResumes((prev) => prev.filter((r) => r.id !== resumeId))
      setTotal((prev) => prev - 1)
    } catch (err) {
      alert(err.message)
    }
  }

  const handleAnalyze = async (resumeId) => {
    setAnalyzing(resumeId)
    try {
      await analysisService.runAnalysis(resumeId)
      setResumes((prev) =>
        prev.map((r) => (r.id === resumeId ? { ...r, status: 'analyzed' } : r))
      )
    } catch (err) {
      alert(err.message)
    } finally {
      setAnalyzing(null)
    }
  }

  const filtered = search
    ? resumes.filter((r) => r.original_name.toLowerCase().includes(search.toLowerCase()))
    : resumes

  return (
    <div>
      <motion.div
        initial={{ opacity: 0, y: -8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="page-header flex flex-col md:flex-row md:items-center justify-between gap-4"
      >
        <div>
          <h1 className="page-title">Resume History</h1>
          <p className="page-subtitle">{total} resume{total !== 1 ? 's' : ''} uploaded</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search resumes..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-9 pr-4 py-2 text-sm border border-gray-200 dark:border-gray-800 rounded-xl bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500/20"
            />
          </div>
          <Button onClick={() => loadHistory(page)} variant="outline" size="md">
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
          <Link to="/upload">
            <Button size="md">
              <UploadCloud className="h-4 w-4 mr-2" />
              Upload New
            </Button>
          </Link>
        </div>
      </motion.div>

      {loading ? (
        <div className="flex justify-center py-20">
          <Spinner size="lg" />
        </div>
      ) : filtered.length === 0 ? (
        <Card hoverEffect={false} className="text-center py-16">
          <UploadCloud className="h-12 w-12 text-gray-300 dark:text-gray-700 mx-auto mb-4" />
          <h3 className="text-lg font-bold text-gray-500 dark:text-gray-400 mb-2">
            {search ? 'No matching resumes found' : 'No resumes uploaded yet'}
          </h3>
          <p className="text-sm text-gray-400 dark:text-gray-600 mb-6">
            Upload your first resume to get started with AI analysis.
          </p>
          <Link to="/upload">
            <Button>Upload Resume</Button>
          </Link>
        </Card>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            <AnimatePresence>
              {filtered.map((resume, i) => (
                <motion.div
                  key={resume.id}
                  initial={{ opacity: 0, y: 16 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, scale: 0.95 }}
                  transition={{ delay: i * 0.04, duration: 0.3 }}
                >
                  <ResumeCard
                    resume={resume}
                    onDelete={handleDelete}
                    onAnalyze={analyzing === resume.id ? () => {} : handleAnalyze}
                  />
                </motion.div>
              ))}
            </AnimatePresence>
          </div>

          {/* Pagination */}
          {pages > 1 && (
            <div className="flex justify-center items-center space-x-3 mt-8">
              <Button
                onClick={() => loadHistory(page - 1)}
                disabled={page <= 1}
                variant="outline"
                size="sm"
              >
                Previous
              </Button>
              <span className="text-sm text-gray-500 dark:text-gray-400 font-semibold">
                Page {page} of {pages}
              </span>
              <Button
                onClick={() => loadHistory(page + 1)}
                disabled={page >= pages}
                variant="outline"
                size="sm"
              >
                Next
              </Button>
            </div>
          )}
        </>
      )}
    </div>
  )
}

export default ResumeHistory
