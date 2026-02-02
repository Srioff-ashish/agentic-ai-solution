import React, { useState } from 'react'

export default function Sidebar({ chatHistory = [], onNewChat, onSelectChat, collapsed, onToggleCollapse }) {
  const [searchQuery, setSearchQuery] = useState('')

  const filteredHistory = chatHistory.filter(chat =>
    chat.title.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div className={`flex h-full ${collapsed ? 'w-16' : 'w-64'} transition-all duration-300`}>
      {/* Icon Strip */}
      <div className="w-14 bg-gray-100 border-r border-gray-200 flex flex-col items-center py-4 gap-4">
        <button className="w-10 h-10 rounded-lg bg-white shadow-sm flex items-center justify-center hover:bg-gray-50 transition-colors">
          <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        <button className="w-10 h-10 rounded-lg hover:bg-white hover:shadow-sm flex items-center justify-center transition-colors">
          <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
          </svg>
        </button>
        <button className="w-10 h-10 rounded-lg hover:bg-white hover:shadow-sm flex items-center justify-center transition-colors">
          <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
          </svg>
        </button>
        <button className="w-10 h-10 rounded-lg hover:bg-white hover:shadow-sm flex items-center justify-center transition-colors">
          <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </button>
        <button className="w-10 h-10 rounded-lg hover:bg-white hover:shadow-sm flex items-center justify-center transition-colors">
          <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
        </button>
      </div>

      {/* Main Sidebar Content */}
      {!collapsed && (
        <div className="flex-1 bg-white border-r border-gray-200 flex flex-col">
          {/* Assistant Title */}
          <div className="px-4 py-4 border-b border-gray-100">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="text-orange-500 text-lg">✦</span>
                <span className="font-semibold text-gray-800">OMaaP Assistant</span>
              </div>
              <button 
                onClick={onToggleCollapse}
                className="w-6 h-6 rounded flex items-center justify-center hover:bg-gray-100 transition-colors"
              >
                <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
          </div>

          {/* New Chat Button */}
          <div className="px-4 py-3">
            <button 
              onClick={onNewChat}
              className="flex items-center gap-2 text-gray-700 hover:text-gray-900 transition-colors"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              <span className="text-sm">New chat</span>
            </button>
          </div>

          {/* Search */}
          <div className="px-4 py-2">
            <div className="flex items-center gap-2 text-gray-500">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <input
                type="text"
                placeholder="Search for chat"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="text-sm bg-transparent outline-none placeholder-gray-400 flex-1"
              />
            </div>
          </div>

          {/* Chat History */}
          <div className="flex-1 overflow-y-auto px-4 py-3">
            <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Chat History</h3>
            <div className="space-y-1">
              {filteredHistory.length > 0 ? (
                filteredHistory.map((chat, index) => (
                  <button
                    key={chat.id || index}
                    onClick={() => onSelectChat && onSelectChat(chat)}
                    className="w-full text-left px-2 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded transition-colors truncate"
                  >
                    {chat.title}
                  </button>
                ))
              ) : (
                <>
                  <div className="px-2 py-2 text-sm text-gray-600">Summary of release</div>
                  <div className="px-2 py-2 text-sm text-gray-600">Python solution</div>
                  <div className="px-2 py-2 text-sm text-gray-600">Explain code</div>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
