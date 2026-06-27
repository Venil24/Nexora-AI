import api from './api'

const githubService = {
  analyzeProfile: async (username) => {
    try {
      const response = await api.get(`/github/${encodeURIComponent(username)}`)
      return response.data.data
    } catch (error) {
      throw new Error(error.response?.data?.message || 'GitHub analysis failed')
    }
  }
}

export default githubService
