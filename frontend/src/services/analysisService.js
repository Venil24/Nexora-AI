import api, { API_BASE_URL } from './api'

const analysisService = {
  runAnalysis: async (resumeId) => {
    try {
      const response = await api.post(`/analysis/${resumeId}/run`)
      return response.data.data
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to run analysis')
    }
  },

  getAnalysis: async (resumeId) => {
    try {
      const response = await api.get(`/analysis/${resumeId}`)
      return response.data.data
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch analysis')
    }
  },

  jdMatch: async (resumeId, jdText) => {
    try {
      const response = await api.post(`/analysis/${resumeId}/jd-match`, { jd_text: jdText })
      return response.data.data
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to perform JD match')
    }
  },

  getReportUrl: (resumeId, token) => {
    return `${API_BASE_URL}/analysis/${resumeId}/report?token=${token}`
  },

  downloadReportBlob: async (resumeId) => {
    try {
      const response = await api.get(`/analysis/${resumeId}/report`, {
        responseType: 'blob'
      })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to download report')
    }
  }
}

export default analysisService
