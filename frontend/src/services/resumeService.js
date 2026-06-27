import api from './api'

const resumeService = {
  uploadResume: async (file, onUploadProgress) => {
    const formData = new FormData()
    formData.append('file', file)
    
    try {
      const response = await api.post('/resume/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress,
      })
      return response.data.data
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Upload failed')
    }
  },

  getHistory: async (page = 1, limit = 10) => {
    try {
      const response = await api.get(`/resume/history`, {
        params: { page, limit }
      })
      return response.data.data
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch history')
    }
  },

  getResume: async (resumeId) => {
    try {
      const response = await api.get(`/resume/${resumeId}`)
      return response.data.data
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch resume')
    }
  },

  deleteResume: async (resumeId) => {
    try {
      const response = await api.delete(`/resume/${resumeId}`)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to delete resume')
    }
  },

  getStats: async () => {
    try {
      const response = await api.get('/resume/stats')
      return response.data.data
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch statistics')
    }
  }
}

export default resumeService
