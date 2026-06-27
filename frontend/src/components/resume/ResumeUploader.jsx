import React, { useState, useRef } from 'react'
import { Upload, FileText, AlertCircle, CheckCircle } from 'lucide-react'
import Button from '../ui/Button'
import Progress from '../ui/Progress'

const ResumeUploader = ({ onUploadSuccess, maxFiles = 1 }) => {
  const [dragActive, setDragActive] = useState(false)
  const [file, setFile] = useState(null)
  const [progress, setProgress] = useState(0)
  const [status, setStatus] = useState('idle') // idle, uploading, success, error
  const [error, setError] = useState('')
  const inputRef = useRef(null)

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0]
      validateAndSetFile(droppedFile)
    }
  }

  const handleChange = (e) => {
    e.preventDefault()
    if (e.target.files && e.target.files[0]) {
      validateAndSetFile(e.target.files[0])
    }
  }

  const validateAndSetFile = (selectedFile) => {
    if (selectedFile.type !== 'application/pdf') {
      setError('Only PDF documents are allowed')
      setStatus('error')
      setFile(null)
      return
    }
    if (selectedFile.size > 10 * 1024 * 1024) {
      setError('File size must be under 10MB')
      setStatus('error')
      setFile(null)
      return
    }
    setError('')
    setStatus('idle')
    setFile(selectedFile)
  }

  const triggerInput = () => {
    inputRef.current.click()
  }

  const startUpload = async () => {
    if (!file) return
    setStatus('uploading')
    setProgress(10)
    
    try {
      import('../../services/resumeService').then(async (module) => {
        const resumeService = module.default
        const result = await resumeService.uploadResume(file, (progressEvent) => {
          const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          setProgress(percent)
        })
        setStatus('success')
        if (onUploadSuccess) {
          onUploadSuccess(result)
        }
      }).catch((err) => {
        setError(err.message || 'Network error during upload')
        setStatus('error')
      })
    } catch (err) {
      setError(err.message || 'Upload failed')
      setStatus('error')
    }
  }

  const removeFile = () => {
    setFile(null)
    setProgress(0)
    setStatus('idle')
    setError('')
  }

  return (
    <div className="w-full">
      {/* Drop Zone */}
      {status !== 'uploading' && status !== 'success' && (
        <div
          onDragEnter={handleDrag}
          onDragOver={handleDrag}
          onDragLeave={handleDrag}
          onDrop={handleDrop}
          onClick={triggerInput}
          className={`flex flex-col items-center justify-center border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all duration-200 ${
            dragActive
              ? 'border-primary-500 bg-primary-50/30 dark:bg-primary-950/10'
              : 'border-gray-200 dark:border-gray-800 hover:border-primary-500 dark:hover:border-primary-500'
          }`}
        >
          <input
            ref={inputRef}
            type="file"
            className="hidden"
            accept=".pdf"
            onChange={handleChange}
          />
          <div className="p-4 bg-primary-50 dark:bg-primary-950/40 text-primary-600 dark:text-primary-400 rounded-2xl mb-4">
            <Upload className="h-8 w-8" />
          </div>
          <h5 className="font-bold text-gray-900 dark:text-gray-100 mb-1">
            Drag & drop your resume PDF here
          </h5>
          <p className="text-sm text-gray-400 dark:text-gray-500 mb-2">
            or click to browse files from your computer
          </p>
          <p className="text-xs text-gray-400 dark:text-gray-600">
            Accepts PDF format only (Max 10MB)
          </p>
        </div>
      )}

      {/* Selected File Details & Progress */}
      {file && (
        <div className="mt-4 bg-gray-50 dark:bg-gray-900/40 border border-gray-100 dark:border-gray-900 rounded-xl p-4 flex items-center space-x-4">
          <div className="p-2.5 bg-primary-100 dark:bg-primary-900/50 text-primary-600 dark:text-primary-400 rounded-lg">
            <FileText className="h-6 w-6" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-semibold text-gray-900 dark:text-gray-100 truncate">
              {file.name}
            </p>
            <p className="text-xs text-gray-400 dark:text-gray-500">
              {(file.size / 1024 / 1024).toFixed(2)} MB
            </p>
          </div>
          {status === 'idle' && (
            <div className="flex space-x-2">
              <Button onClick={startUpload} size="sm">
                Upload
              </Button>
              <Button onClick={removeFile} variant="outline" size="sm">
                Remove
              </Button>
            </div>
          )}
        </div>
      )}

      {/* Uploading State */}
      {status === 'uploading' && (
        <div className="mt-6 border border-gray-100 dark:border-gray-900 rounded-2xl p-6 bg-white dark:bg-gray-950 shadow-sm flex flex-col items-center">
          <FileText className="h-10 w-10 text-primary-600 dark:text-primary-400 animate-bounce mb-3" />
          <p className="text-sm font-bold text-gray-900 dark:text-gray-100 mb-2">
            Uploading & Parsing Resume...
          </p>
          <Progress value={progress} showLabel={true} className="w-full max-w-md" />
        </div>
      )}

      {/* Success State */}
      {status === 'success' && (
        <div className="mt-6 border border-emerald-100 dark:border-emerald-950/50 rounded-2xl p-6 bg-emerald-50/20 dark:bg-emerald-950/10 flex flex-col items-center text-center">
          <CheckCircle className="h-12 w-12 text-emerald-500 mb-3" />
          <h5 className="font-bold text-emerald-800 dark:text-emerald-400 mb-1">
            Upload & Parsing Complete!
          </h5>
          <p className="text-sm text-emerald-700 dark:text-emerald-500/80 mb-4">
            Your resume was parsed successfully and is ready for ATS scoring.
          </p>
          <Button onClick={removeFile} variant="secondary" size="sm">
            Upload Another File
          </Button>
        </div>
      )}

      {/* Error Alert */}
      {status === 'error' && error && (
        <div className="mt-4 border border-rose-100 dark:border-rose-950/50 rounded-xl p-4 bg-rose-50/20 dark:bg-rose-950/10 flex items-start space-x-3">
          <AlertCircle className="h-5 w-5 text-rose-500 shrink-0 mt-0.5" />
          <div className="flex-1">
            <h6 className="font-bold text-rose-800 dark:text-rose-400 text-sm">
              Upload Error
            </h6>
            <p className="text-xs text-rose-700 dark:text-rose-500/80 mt-0.5">
              {error}
            </p>
          </div>
        </div>
      )}
    </div>
  )
}

export default ResumeUploader
