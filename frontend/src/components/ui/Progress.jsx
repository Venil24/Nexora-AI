import React from 'react'

const Progress = ({
  value = 0,
  max = 100,
  showLabel = false,
  label = '',
  size = 'md',
  color = 'primary',
  className = '',
}) => {
  const percentage = Math.min(100, Math.max(0, (value / max) * 100))

  const sizes = {
    sm: 'h-1.5',
    md: 'h-2.5',
    lg: 'h-4',
  }

  const colors = {
    primary: 'bg-primary-600 dark:bg-primary-500',
    success: 'bg-emerald-500',
    warning: 'bg-amber-500',
    danger: 'bg-rose-500',
    info: 'bg-blue-500',
  }

  // Auto-color option if primary is used but score varies
  const getProgressColor = () => {
    if (color !== 'primary') return colors[color]
    if (percentage >= 75) return colors.success
    if (percentage >= 50) return colors.warning
    return colors.danger
  }

  return (
    <div className={`w-full ${className}`}>
      {(showLabel || label) && (
        <div className="flex justify-between items-center mb-1 text-xs font-semibold text-gray-500 dark:text-gray-400">
          <span>{label}</span>
          <span>{Math.round(percentage)}%</span>
        </div>
      )}
      <div className="w-full bg-gray-100 dark:bg-gray-900 rounded-full overflow-hidden">
        <div
          className={`${sizes[size]} ${getProgressColor()} rounded-full transition-all duration-500 ease-out`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  )
}

export default Progress
// helper for score coloring
export const getScoreColorClass = (score) => {
  if (score >= 75) return 'text-emerald-500 dark:text-emerald-400'
  if (score >= 50) return 'text-amber-500 dark:text-amber-400'
  return 'text-rose-500 dark:text-rose-400'
}
