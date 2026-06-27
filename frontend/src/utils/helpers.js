// frontend/src/utils/helpers.js
// Shared utility functions

export const formatDate = (dateStr, options = {}) => {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString(undefined, {
    year: 'numeric', month: 'short', day: 'numeric', ...options
  })
}

export const formatFileSize = (bytes) => {
  if (!bytes) return '0 B'
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(1024))
  return `${(bytes / Math.pow(1024, i)).toFixed(2)} ${sizes[i]}`
}

export const getScoreLabel = (score) => {
  if (score >= 80) return 'Excellent'
  if (score >= 60) return 'Good'
  if (score >= 40) return 'Fair'
  return 'Needs Work'
}

export const getScoreVariant = (score) => {
  if (score >= 75) return 'success'
  if (score >= 50) return 'warning'
  return 'danger'
}

export const truncate = (str, max = 60) => {
  if (!str) return ''
  return str.length > max ? str.slice(0, max) + '…' : str
}

export const capitalize = (str) => {
  if (!str) return ''
  return str.charAt(0).toUpperCase() + str.slice(1)
}

export const sleep = (ms) => new Promise((r) => setTimeout(r, ms))
