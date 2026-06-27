import React from 'react'
import { FileText, Trash2, ShieldCheck, Eye, CheckSquare, Sparkles } from 'lucide-react'
import { Link } from 'react-router-dom'
import Card from '../ui/Card'
import Badge from '../ui/Badge'
import Button from '../ui/Button'

const ResumeCard = ({ resume, onDelete, onAnalyze }) => {
  const getStatusBadge = (status) => {
    switch (status) {
      case 'analyzed':
        return <Badge variant="success">Analyzed</Badge>
      case 'parsed':
        return <Badge variant="info">Parsed</Badge>
      case 'uploaded':
        return <Badge variant="primary">Uploaded</Badge>
      case 'error':
        return <Badge variant="danger">Error</Badge>
      default:
        return <Badge variant="gray">{status}</Badge>
    }
  }

  const formattedDate = new Date(resume.created_at).toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })

  return (
    <Card className="flex flex-col h-full justify-between" hoverEffect={true}>
      <div>
        <div className="flex justify-between items-start mb-4">
          <div className="p-3 bg-primary-50 dark:bg-primary-950/40 text-primary-600 dark:text-primary-400 rounded-xl">
            <FileText className="h-6 w-6" />
          </div>
          <div>{getStatusBadge(resume.status)}</div>
        </div>

        <h4 className="text-base font-bold text-gray-900 dark:text-gray-100 truncate mb-1" title={resume.original_name}>
          {resume.original_name}
        </h4>
        
        <p className="text-xs text-gray-400 dark:text-gray-500 mb-4">
          Uploaded on {formattedDate}
        </p>

        <div className="space-y-2 mb-6">
          <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400">
            <span>Pages:</span>
            <span className="font-semibold">{resume.page_count}</span>
          </div>
          <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400">
            <span>Size:</span>
            <span className="font-semibold">{(resume.file_size / 1024 / 1024).toFixed(2)} MB</span>
          </div>
        </div>
      </div>

      <div className="flex flex-col space-y-2">
        {resume.status !== 'analyzed' ? (
          <Button
            onClick={() => onAnalyze(resume.id)}
            variant="solid"
            size="sm"
            className="w-full justify-center"
          >
            <ShieldCheck className="h-4 w-4 mr-2" />
            Analyze ATS Score
          </Button>
        ) : (
          <Link to={`/ats-analyzer?resumeId=${resume.id}`} className="w-full">
            <Button variant="solid" size="sm" className="w-full justify-center">
              <Eye className="h-4 w-4 mr-2" />
              View ATS Score
            </Button>
          </Link>
        )}

        <div className="grid grid-cols-2 gap-2">
          {resume.status === 'analyzed' && (
            <Link to={`/jd-matcher?resumeId=${resume.id}`} className="w-full">
              <Button variant="outline" size="sm" className="w-full justify-center px-1">
                <CheckSquare className="h-4 w-4 mr-1.5" />
                JD Match
              </Button>
            </Link>
          )}
          {resume.status === 'analyzed' && (
            <Link to={`/career-predictor?resumeId=${resume.id}`} className="w-full">
              <Button variant="outline" size="sm" className="w-full justify-center px-1">
                <Sparkles className="h-4 w-4 mr-1.5" />
                Predict Career
              </Button>
            </Link>
          )}
        </div>

        <Button
          onClick={() => onDelete(resume.id)}
          variant="ghost"
          size="sm"
          className="w-full text-rose-600 dark:text-rose-400 hover:bg-rose-50 dark:hover:bg-rose-950/20 hover:text-rose-700 justify-center"
        >
          <Trash2 className="h-4 w-4 mr-2" />
          Delete Resume
        </Button>
      </div>
    </Card>
  )
}

export default ResumeCard
