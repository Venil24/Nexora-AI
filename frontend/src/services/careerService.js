import api from './api'

const careerService = {
  predictCareer: async (resumeId) => {
    try {
      const response = await api.post(`/career/predict/${resumeId}`)
      return response.data.data
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to predict career')
    }
  },

  getRoadmaps: async () => {
    try {
      const response = await api.get('/career/roadmaps')
      return response.data.data
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch roadmaps')
    }
  },

  getRoadmap: async (career) => {
    try {
      const response = await api.get(`/career/roadmap/${encodeURIComponent(career)}`)
      return response.data.data
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch roadmap details')
    }
  },

  getInterviewQuestions: async (career) => {
    try {
      const response = await api.get(`/career/interview-questions/${encodeURIComponent(career)}`)
      return response.data.data
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch interview questions')
    }
  }
}

export default careerService
