import React from 'react'
import { CheckCircle2, XCircle, ArrowUpRight } from 'lucide-react'

const Suggestions = ({ suggestions = [], strengths = [], weaknesses = [] }) => {
  return (
    <div className="space-y-6">
      {/* Strengths & Weaknesses Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Strengths */}
        <div className="p-5 bg-emerald-50/20 dark:bg-emerald-950/10 border border-emerald-100/50 dark:border-emerald-950/20 rounded-2xl">
          <h5 className="flex items-center space-x-2 text-sm font-extrabold text-emerald-800 dark:text-emerald-400 mb-3">
            <CheckCircle2 className="h-5 w-5 text-emerald-500" />
            <span>Key Strengths</span>
          </h5>
          {strengths.length > 0 ? (
            <ul className="space-y-2">
              {strengths.map((str, i) => (
                <li key={i} className="text-xs font-semibold text-emerald-700 dark:text-emerald-500/90 flex items-start space-x-2">
                  <span className="mt-1 h-1.5 w-1.5 rounded-full bg-emerald-500 shrink-0" />
                  <span>{str}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-xs text-gray-400">No major strengths highlighted yet.</p>
          )}
        </div>

        {/* Weaknesses */}
        <div className="p-5 bg-rose-50/20 dark:bg-rose-950/10 border border-rose-100/50 dark:border-rose-950/20 rounded-2xl">
          <h5 className="flex items-center space-x-2 text-sm font-extrabold text-rose-800 dark:text-rose-400 mb-3">
            <XCircle className="h-5 w-5 text-rose-500" />
            <span>Improvement Areas</span>
          </h5>
          {weaknesses.length > 0 ? (
            <ul className="space-y-2">
              {weaknesses.map((weak, i) => (
                <li key={i} className="text-xs font-semibold text-rose-700 dark:text-rose-500/90 flex items-start space-x-2">
                  <span className="mt-1 h-1.5 w-1.5 rounded-full bg-rose-500 shrink-0" />
                  <span>{weak}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-xs text-gray-400">No critical issues flagged.</p>
          )}
        </div>
      </div>

      {/* List of Suggestions */}
      <div>
        <h5 className="text-sm font-extrabold text-gray-900 dark:text-gray-100 mb-3">
          Step-by-Step Optimization Guide
        </h5>
        {suggestions.length > 0 ? (
          <div className="space-y-3">
            {suggestions.map((sug, i) => (
              <div
                key={i}
                className="flex items-start space-x-3 p-4 bg-gray-50 dark:bg-gray-900/40 border border-gray-100 dark:border-gray-900 rounded-xl"
              >
                <div className="flex items-center justify-center h-6 w-6 rounded-lg bg-primary-50 dark:bg-primary-950/40 text-primary-600 dark:text-primary-400 text-xs font-extrabold shrink-0">
                  {i + 1}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-gray-700 dark:text-gray-300 font-medium">
                    {sug}
                  </p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-sm text-gray-400">Your resume requires no further manual optimizations!</p>
        )}
      </div>
    </div>
  )
}

export default Suggestions
