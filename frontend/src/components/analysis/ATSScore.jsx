import React from 'react'

const ATSScore = ({ score = 0 }) => {
  const getFeedbackMessage = (val) => {
    if (val >= 80) return { title: 'Excellent ATS Fit', desc: 'Your resume is highly optimized for applicant tracking systems.', color: 'text-emerald-500' }
    if (val >= 60) return { title: 'Good ATS Fit', desc: 'Your resume is in solid shape but has minor room for optimization.', color: 'text-amber-500' }
    return { title: 'Needs Optimization', desc: 'Critical formatting or content issues may get your resume rejected by ATS.', color: 'text-rose-500' }
  }

  const feedback = getFeedbackMessage(score)
  const strokeDashoffset = 440 - (440 * score) / 100

  return (
    <div className="flex flex-col items-center text-center p-6 bg-gradient-to-br from-primary-50/50 to-indigo-50/50 dark:from-gray-900/60 dark:to-indigo-950/20 border border-primary-100/50 dark:border-primary-950/20 rounded-2xl">
      {/* Circular Progress SVG */}
      <div className="relative h-44 w-44 flex items-center justify-center mb-4">
        <svg className="w-full h-full transform -rotate-90">
          <circle
            cx="88"
            cy="88"
            r="70"
            className="stroke-gray-100 dark:stroke-gray-800 fill-none"
            strokeWidth="12"
          />
          <circle
            cx="88"
            cy="88"
            r="70"
            className="stroke-primary-600 dark:stroke-primary-500 fill-none transition-all duration-1000 ease-out"
            strokeWidth="12"
            strokeDasharray="440"
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
          />
        </svg>
        <div className="absolute flex flex-col items-center justify-center">
          <span className="text-4xl font-extrabold text-gray-900 dark:text-gray-100">
            {score}%
          </span>
          <span className="text-xs font-semibold text-gray-400 dark:text-gray-500 uppercase tracking-widest mt-0.5">
            ATS Score
          </span>
        </div>
      </div>

      <h4 className={`text-lg font-extrabold ${feedback.color} mb-1`}>
        {feedback.title}
      </h4>
      <p className="text-sm text-gray-500 dark:text-gray-400 max-w-xs">
        {feedback.desc}
      </p>
    </div>
  )
}

export default ATSScore
