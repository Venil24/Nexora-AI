import { useEffect } from 'react'
import { useThemeStore } from '../store/themeStore'

export const useTheme = () => {
  const { darkMode, toggleTheme, initTheme } = useThemeStore()

  useEffect(() => {
    initTheme()
  }, [initTheme])

  return { darkMode, toggleTheme }
}
