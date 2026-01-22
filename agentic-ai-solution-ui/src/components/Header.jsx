import React from 'react'

export default function Header() {
  return (
    <header className="bg-gradient-to-r from-slate-800 to-slate-900 border-b border-slate-700/50 shadow-lg">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-lg">⚡</span>
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">Agentic AI Solution</h1>
            <p className="text-xs text-slate-400">Intelligent Conversation Interface</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-sm text-slate-400">Connected</span>
        </div>
      </div>
    </header>
  )
}
