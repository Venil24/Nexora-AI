import React from 'react'
import Progress from '../ui/Progress'

const ScoreBreakdown = ({ analysis }) => {
  const categories = [
    { label: 'ATS Compatibility', score: analysis.ats_score, desc: 'File format, contact info, key sections' },
    { label: 'Formatting Quality', score: analysis.formatting_score, desc: 'Structure, action verbs, quantified items' },
    { label: 'Keyword Optimization', score: analysis.keyword_score, desc: 'Tech stack terms density and action words' },
    { label: 'Experience Details', score: analysis.experience_score, desc: 'Positions count, date clarity, impact descriptions' },
    { label: 'Education Quality', score: analysis.education_score, desc: 'Degree, school name, CGPA details' },
    { label: 'Projects Showcase', score: analysis.projects_score, desc: 'Personal portfolio, links, and stack terms' },
  ]

  return (
    <div className="space-y-6">
      {categories.map((cat, i) => (
        <div key={i} className="flex flex-col space-y-2">
          <div className="flex justify-between items-baseline">
            <div>
              <h5 className="text-sm font-bold text-gray-900 dark:text-gray-100">
                {cat.label}
              </h5>
              <p className="text-xs text-gray-400 dark:text-gray-500">
                {cat.desc}
              </p>
            </div>
            <span className="text-sm font-extrabold text-gray-900 dark:text-gray-100">
              {cat.score}%
            </span>
          </div>
          <Progress value={cat.score} size="md" color="primary" />
        </div>
      ))}
    </div>
  )
}

export default ScoreBreakdown
