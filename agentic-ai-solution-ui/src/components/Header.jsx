import React from 'react'
import { Link } from 'react-router-dom'

export default function Header() {
  return (
    <header className="h-14 bg-white border-b border-gray-200 flex items-center justify-between px-4 shadow-sm">
      {/* Left - Logo */}
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 bg-orange-500 rounded-lg flex items-center justify-center">
          <svg className="w-5 h-5 text-white" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
          </svg>
        </div>
        <span className="text-lg font-semibold text-orange-600">Harmonia</span>
      </div>

      {/* Right - User Info */}
      <div className="flex items-center gap-4">
        {/* Company Dropdown */}
        <button className="flex items-center gap-2 text-gray-700 hover:text-gray-900 transition-colors">
          <div className="w-5 h-5 bg-orange-100 rounded flex items-center justify-center">
            <svg className="w-3 h-3 text-orange-600" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a1 1 0 01-1 1h-2a1 1 0 01-1-1v-2a1 1 0 00-1-1H9a1 1 0 00-1 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V4zm3 1h2v2H7V5zm2 4H7v2h2V9zm2-4h2v2h-2V5zm2 4h-2v2h2V9z" clipRule="evenodd" />
            </svg>
          </div>
          <span className="text-sm">UAT Test Company</span>
          <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </button>

        {/* AI Assistant */}
        <div className="flex items-center gap-1.5 text-gray-700">
          <span className="text-orange-500">✦</span>
          <span className="text-sm">AI Assistant</span>
        </div>

        {/* Log Viewer Link */}
        <Link 
          to="/logs" 
          className="flex items-center gap-1.5 px-3 py-1.5 text-sm bg-gray-100 hover:bg-gray-200 rounded-md text-gray-700 transition-colors"
        >
          <span>📋</span>
          <span>Logs</span>
        </Link>

        {/* Logout Button */}
        <button className="px-4 py-1.5 text-sm border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition-colors">
          Log out
        </button>
      </div>
    </header>
  )
}
