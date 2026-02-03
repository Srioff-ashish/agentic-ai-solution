import { createContext, useContext, useState, useEffect } from 'react'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  // Check auth state on mount
  useEffect(() => {
    checkAuthState()
  }, [])

  const checkAuthState = () => {
    const authenticated = localStorage.getItem('mfa_authenticated')
    const userEmail = localStorage.getItem('mfa_user')
    const timestamp = localStorage.getItem('mfa_timestamp')

    if (authenticated === 'true' && timestamp) {
      // Check if session is still valid (24 hours)
      const sessionAge = Date.now() - parseInt(timestamp)
      const maxAge = 24 * 60 * 60 * 1000 // 24 hours

      if (sessionAge < maxAge) {
        setIsAuthenticated(true)
        setUser({ email: userEmail })
      } else {
        // Session expired
        logout()
      }
    }
    setIsLoading(false)
  }

  const login = () => {
    setIsAuthenticated(true)
    setUser({ email: localStorage.getItem('mfa_user') })
  }

  const logout = () => {
    localStorage.removeItem('mfa_authenticated')
    localStorage.removeItem('mfa_user')
    localStorage.removeItem('mfa_timestamp')
    setIsAuthenticated(false)
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, isLoading, login, logout, checkAuthState }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export default AuthContext
