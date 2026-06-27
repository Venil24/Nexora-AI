import api from './api'
import { useAuthStore } from '../store/authStore'

const authService = {
  login: async (email, password) => {
    useAuthStore.getState().setLoading(true)
    try {
      const response = await api.post('/auth/login', { email, password })
      const { user, access_token, refresh_token } = response.data.data
      useAuthStore.getState().setAuth(user, access_token, refresh_token)
      return response.data
    } catch (error) {
      const msg = error.response?.data?.message || 'Login failed'
      useAuthStore.getState().setError(msg)
      throw new Error(msg)
    } finally {
      useAuthStore.getState().setLoading(false)
    }
  },

  register: async (name, email, password) => {
    useAuthStore.getState().setLoading(true)
    try {
      const response = await api.post('/auth/register', { name, email, password })
      const { user, access_token, refresh_token } = response.data.data
      useAuthStore.getState().setAuth(user, access_token, refresh_token)
      return response.data
    } catch (error) {
      const msg = error.response?.data?.message || 'Registration failed'
      useAuthStore.getState().setError(msg)
      throw new Error(msg)
    } finally {
      useAuthStore.getState().setLoading(false)
    }
  },

  forgotPassword: async (email) => {
    try {
      const response = await api.post('/auth/forgot-password', { email })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to send reset link')
    }
  },

  resetPassword: async (token, password) => {
    try {
      const response = await api.post('/auth/reset-password', { token, password })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Reset failed')
    }
  },

  getMe: async () => {
    try {
      const response = await api.get('/auth/me')
      return response.data.data
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch user')
    }
  },

  updateProfile: async (profileData) => {
    try {
      const response = await api.put('/auth/profile', profileData)
      // Re-fetch profile to keep sync
      const refreshed = await api.get('/auth/me')
      const user = refreshed.data.data.user
      const accessToken = useAuthStore.getState().accessToken
      const refreshToken = useAuthStore.getState().refreshToken
      useAuthStore.getState().setAuth(user, accessToken, refreshToken)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Update profile failed')
    }
  },

  logout: () => {
    useAuthStore.getState().clearAuth()
  }
}

export default authService
