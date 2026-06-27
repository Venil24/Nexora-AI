import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ShieldCheck } from 'lucide-react'
import ResumeUploader from '../components/resume/ResumeUploader'
import Card from '../components/ui/Card'

const ResumeUpload = () => {
  const navigate = useNavigate()

  const handleUploadSuccess = (resume) => {
    // After 1.5s, redirect to ATS analyzer for the newly uploaded resume
    setTimeout(() => {
      navigate(`/ats-analyzer?resumeId=${resume.id}`)
    }, 1500)
  }

  return (
    <div>
      <motion.div
        initial={{ opacity: 0, y: -8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="page-header"
      >
        <h1 className="page-title">Upload Resume</h1>
        <p className="page-subtitle">Upload your PDF resume and get an instant AI-powered ATS analysis</p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Uploader Card */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1, duration: 0.4 }}
          className="lg:col-span-2"
        >
          <Card>
            <h2 className="section-title">Select Your Resume</h2>
            <ResumeUploader onUploadSuccess={handleUploadSuccess} />
          </Card>
        </motion.div>

        {/* What Happens Next */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.4 }}
        >
          <Card hoverEffect={false}>
            <h3 className="section-title">What Happens After Upload?</h3>
            <div className="space-y-4">
              {[
                { step: '01', title: 'PDF Parsing', desc: 'We extract text, skills, experience, education using AI' },
                { step: '02', title: 'NER Analysis', desc: 'Named Entity Recognition identifies name, email, links' },
                { step: '03', title: 'ATS Scoring', desc: 'We score across 6 dimensions vs industry standards' },
                { step: '04', title: 'Career Match', desc: 'ML model predicts best-fit career paths for you' },
              ].map((item) => (
                <div key={item.step} className="flex items-start space-x-3">
                  <div className="flex items-center justify-center h-7 w-7 rounded-lg bg-primary-50 dark:bg-primary-950/40 text-primary-600 dark:text-primary-400 text-xs font-extrabold shrink-0">
                    {item.step}
                  </div>
                  <div>
                    <p className="text-sm font-bold text-gray-900 dark:text-gray-100">{item.title}</p>
                    <p className="text-xs text-gray-400 dark:text-gray-500 mt-0.5">{item.desc}</p>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-6 p-4 bg-primary-50/50 dark:bg-primary-950/20 rounded-xl border border-primary-100/50 dark:border-primary-900/30">
              <div className="flex items-start space-x-3">
                <ShieldCheck className="h-5 w-5 text-primary-600 dark:text-primary-400 shrink-0 mt-0.5" />
                <div>
                  <p className="text-xs font-bold text-primary-800 dark:text-primary-300">PDF Only · Max 10MB</p>
                  <p className="text-xs text-primary-600/80 dark:text-primary-400/80 mt-0.5">
                    Your resume is encrypted and stored securely. We never share your data.
                  </p>
                </div>
              </div>
            </div>
          </Card>
        </motion.div>
      </div>
    </div>
  )
}

export default ResumeUpload
