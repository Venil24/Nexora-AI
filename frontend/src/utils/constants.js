// frontend/src/utils/constants.js
// App-wide constants

export const APP_NAME = 'Nexora AI'
export const APP_TAGLINE = 'AI Resume Analyzer & Career Roadmap'

export const API_ENDPOINTS = {
  // Auth
  LOGIN: '/auth/login',
  REGISTER: '/auth/register',
  ME: '/auth/me',
  REFRESH: '/auth/refresh',
  FORGOT_PASSWORD: '/auth/forgot-password',
  RESET_PASSWORD: '/auth/reset-password',
  UPDATE_PROFILE: '/auth/profile',
  // Resume
  UPLOAD: '/resume/upload',
  HISTORY: '/resume/history',
  STATS: '/resume/stats',
  // Analysis
  RUN_ANALYSIS: (id) => `/analysis/${id}/run`,
  GET_ANALYSIS: (id) => `/analysis/${id}`,
  JD_MATCH: (id) => `/analysis/${id}/jd-match`,
  REPORT: (id) => `/analysis/${id}/report`,
  // Career
  PREDICT: (id) => `/career/predict/${id}`,
  ROADMAPS: '/career/roadmaps',
  ROADMAP: (career) => `/career/roadmap/${career}`,
  INTERVIEW_QUESTIONS: (career) => `/career/interview-questions/${career}`,
  // GitHub
  GITHUB: (username) => `/github/${username}`,
  // Activity
  LOGS: '/activity/logs',
}

export const SCORE_LEVELS = [
  { min: 80, label: 'Excellent', color: 'success' },
  { min: 60, label: 'Good', color: 'info' },
  { min: 40, label: 'Fair', color: 'warning' },
  { min: 0,  label: 'Needs Work', color: 'danger' },
]

export const CAREERS = [
  'Software Engineer',
  'Frontend Developer',
  'Backend Developer',
  'Full Stack Developer',
  'Data Scientist',
  'Machine Learning Engineer',
  'Data Analyst',
  'DevOps Engineer',
  'Cloud Architect',
  'Cybersecurity Engineer',
  'Mobile Developer',
  'Database Administrator',
]

export const PAGINATION_LIMIT = 10
