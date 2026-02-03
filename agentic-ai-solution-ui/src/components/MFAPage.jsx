import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

// ING Lion Logo SVG component
const INGLogo = ({ className = "h-8" }) => (
  <div className={`flex items-center justify-center ${className}`}>
    <span className="text-2xl font-bold text-[#FF6200]">ING</span>
    <svg className="h-8 w-10 ml-1" viewBox="0 0 40 32" fill="none" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="20" cy="16" rx="18" ry="14" fill="#FF6200"/>
      <circle cx="14" cy="12" r="2" fill="white"/>
      <circle cx="26" cy="12" r="2" fill="white"/>
      <path d="M12 20 Q20 26 28 20" stroke="white" strokeWidth="2" fill="none"/>
      <path d="M8 6 Q12 2 16 6" stroke="#FF6200" strokeWidth="2" fill="none"/>
      <path d="M24 6 Q28 2 32 6" stroke="#FF6200" strokeWidth="2" fill="none"/>
    </svg>
  </div>
)

function MFAPage() {
  const navigate = useNavigate()
  const { login } = useAuth()
  const [mfaCode, setMfaCode] = useState(0)
  const [isVerifying, setIsVerifying] = useState(false)
  const [countdown, setCountdown] = useState(30)
  const [userEmail] = useState('user@ing.com') // Mock user email

  // Generate random 2-digit code on mount
  useEffect(() => {
    setMfaCode(Math.floor(Math.random() * 90) + 10) // Random number between 10-99
  }, [])

  // Countdown timer - auto approve after countdown or simulate approval
  useEffect(() => {
    if (countdown > 0 && !isVerifying) {
      const timer = setTimeout(() => setCountdown(countdown - 1), 1000)
      return () => clearTimeout(timer)
    }
  }, [countdown, isVerifying])

  const handleApproved = useCallback(() => {
    if (isVerifying) return // Prevent double execution
    setIsVerifying(true)
    // Simulate verification delay
    setTimeout(() => {
      // Store auth state
      localStorage.setItem('mfa_authenticated', 'true')
      localStorage.setItem('mfa_user', userEmail)
      localStorage.setItem('mfa_timestamp', Date.now().toString())
      // Update auth context
      login()
      // Navigate to main app
      navigate('/app', { replace: true })
    }, 1000)
  }, [isVerifying, userEmail, login, navigate])

  // Auto-approve after 5 seconds for demo purposes
  useEffect(() => {
    const autoApprove = setTimeout(() => {
      handleApproved()
    }, 5000)
    return () => clearTimeout(autoApprove)
  }, [handleApproved])

  const handleCantUseApp = () => {
    // For demo, just approve anyway
    handleApproved()
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-gray-100 flex items-center justify-center p-4">
      {/* MFA Card */}
      <div className="bg-white rounded-xl shadow-xl max-w-sm w-full overflow-hidden">
        {/* Header */}
        <div className="p-6 pb-4">
          <INGLogo className="mb-4" />
          <p className="text-sm text-gray-500 text-center">{userEmail}</p>
        </div>

        {/* Content */}
        <div className="px-6 pb-6">
          <h1 className="text-xl font-semibold text-gray-900 mb-4">Approve sign-in request</h1>
          
          <div className="flex items-start gap-3 mb-6">
            <div className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center flex-shrink-0">
              <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
              </svg>
            </div>
            <p className="text-sm text-gray-600">
              Open your Authenticator app, and enter the number shown to sign in.
            </p>
          </div>

          {/* MFA Code Display */}
          <div className="text-center mb-6">
            <div className={`text-6xl font-bold text-gray-900 transition-all duration-300 ${isVerifying ? 'animate-pulse text-green-600' : ''}`}>
              {isVerifying ? '✓' : mfaCode}
            </div>
            {!isVerifying && (
              <p className="text-xs text-gray-400 mt-2">
                Auto-approving in {countdown}s (Demo mode)
              </p>
            )}
          </div>

          {/* Helper Text */}
          <p className="text-xs text-gray-500 mb-4">
            No numbers in your app? Make sure to upgrade to the latest version.
          </p>

          {/* Can't use app button */}
          <button
            onClick={handleCantUseApp}
            className="w-full border border-gray-300 rounded-md py-2 px-4 text-sm text-gray-700 hover:bg-gray-50 transition-colors mb-3"
          >
            I can't use my Microsoft Authenticator app right now
          </button>

          {/* More information link */}
          <a href="#" className="text-sm text-blue-600 hover:underline">
            More information
          </a>
        </div>

        {/* Footer */}
        <div className="bg-gray-50 px-6 py-4 border-t">
          <p className="text-xs text-gray-500">
            Check out the instructions and Q&A via the link in the migration invitation email.
          </p>
        </div>
      </div>
    </div>
  )
}

export default MFAPage
