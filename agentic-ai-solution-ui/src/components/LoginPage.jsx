import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

// ING Lion Logo SVG component
const INGLogo = ({ className = "h-8" }) => (
  <div className={`flex items-center ${className}`}>
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

function LoginPage() {
  const navigate = useNavigate()
  const [isHovered, setIsHovered] = useState(false)

  const handleAzureMFAClick = () => {
    navigate('/mfa')
  }

  return (
    <div className="min-h-screen bg-gray-200 flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-sm py-3 px-6">
        <INGLogo />
      </header>

      {/* Main Content */}
      <main className="flex-1 flex items-start justify-center pt-16">
        <div className="w-full max-w-md">
          <h1 className="text-3xl font-light text-gray-800 mb-6">Harmonia</h1>
          
          {/* Login Card */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-lg font-medium text-[#FF6200] mb-4">Log in with</h2>
            
            {/* Azure MFA Button */}
            <button
              onClick={handleAzureMFAClick}
              onMouseEnter={() => setIsHovered(true)}
              onMouseLeave={() => setIsHovered(false)}
              className={`w-full flex items-center justify-between p-4 border rounded-lg transition-all duration-200 ${
                isHovered ? 'border-[#FF6200] bg-orange-50' : 'border-gray-300 bg-white'
              }`}
            >
              <div className="flex items-center gap-3">
                {/* Monitor Icon */}
                <svg 
                  className="w-6 h-6 text-[#FF6200]" 
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <rect x="2" y="3" width="20" height="14" rx="2" strokeWidth="2"/>
                  <line x1="8" y1="21" x2="16" y2="21" strokeWidth="2"/>
                  <line x1="12" y1="17" x2="12" y2="21" strokeWidth="2"/>
                </svg>
                <span className="text-gray-700 font-medium">Azure MFA</span>
              </div>
              <svg 
                className="w-5 h-5 text-gray-400" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7"/>
              </svg>
            </button>
          </div>

          {/* Contact Link */}
          <a 
            href="#" 
            className="inline-flex items-center gap-1 mt-4 text-gray-600 hover:text-[#FF6200] underline text-sm"
          >
            Contact
            <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
            </svg>
          </a>
        </div>
      </main>
    </div>
  )
}

export default LoginPage
