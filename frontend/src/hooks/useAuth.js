import { useAuthStore } from '../store/authStore'
import authService from '../services/authService'

export const useAuth = () => {
  const { user, accessToken, refreshToken, isAuthenticated, loading, error, clearAuth } = useAuthStore()

  const login = async (email, password) => {
    return authService.login(email, password)
  }

  const register = async (name, email, password) => {
    return authService.register(name, email, password)
  }

  const logout = () => {
    authService.logout()
  }

  const updateProfile = async (data) => {
    return authService.updateProfile(data)
  }

  return {
    user,
    accessToken,
    refreshToken,
    isAuthenticated,
    loading,
    error,
    login,
    register,
    logout,
    updateProfile,
  }
}
