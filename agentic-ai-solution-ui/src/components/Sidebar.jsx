import React, { useState, useEffect } from 'react'
import { apiService } from '../services/api'

export default function Sidebar({ 
  chatHistory = [], 
  activeChatId,
  onNewChat, 
  onSelectChat, 
  onDeleteChat,
  collapsed, 
  onToggleCollapse 
}) {
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState(null)
  const [isSearching, setIsSearching] = useState(false)
  const [deleteConfirm, setDeleteConfirm] = useState(null)

  // Debounced search
  useEffect(() => {
    if (!searchQuery.trim()) {
      setSearchResults(null)
      return
    }

    const timer = setTimeout(async () => {
      if (searchQuery.trim().length >= 2) {
        setIsSearching(true)
        try {
          const result = await apiService.searchChats(searchQuery)
          setSearchResults(result.results)
        } catch (error) {
          console.error('Search failed:', error)
        } finally {
          setIsSearching(false)
        }
      }
    }, 300)

    return () => clearTimeout(timer)
  }, [searchQuery])

  const handleDelete = async (e, chatId) => {
    e.stopPropagation()
    if (deleteConfirm === chatId) {
      // Confirmed - delete the chat
      try {
        await onDeleteChat(chatId)
        setDeleteConfirm(null)
      } catch (error) {
        console.error('Delete failed:', error)
      }
    } else {
      // First click - show confirmation
      setDeleteConfirm(chatId)
      // Auto-reset after 3 seconds
      setTimeout(() => setDeleteConfirm(null), 3000)
    }
  }

  const displayList = searchResults !== null ? searchResults : chatHistory

  const formatDate = (dateString) => {
    if (!dateString) return ''
    const date = new Date(dateString)
    const now = new Date()
    const diffDays = Math.floor((now - date) / (1000 * 60 * 60 * 24))
    
    if (diffDays === 0) return 'Today'
    if (diffDays === 1) return 'Yesterday'
    if (diffDays < 7) return `${diffDays} days ago`
    return date.toLocaleDateString()
  }

  return (
    <div className={`flex h-full ${collapsed ? 'w-16' : 'w-64'} transition-all duration-300`}>
      {/* Icon Strip */}
      <div className="w-14 bg-gray-100 border-r border-gray-200 flex flex-col items-center py-4 gap-4">
        <button 
          onClick={onToggleCollapse}
          className="w-10 h-10 rounded-lg bg-white shadow-sm flex items-center justify-center hover:bg-gray-50 transition-colors"
          title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
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
            <div className="flex items-center gap-2 text-gray-500 bg-gray-50 rounded-lg px-3 py-2">
              {isSearching ? (
                <svg className="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              ) : (
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              )}
              <input
                type="text"
                placeholder="Search for chat"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="text-sm bg-transparent outline-none placeholder-gray-400 flex-1"
              />
              {searchQuery && (
                <button 
                  onClick={() => {
                    setSearchQuery('')
                    setSearchResults(null)
                  }}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              )}
            </div>
          </div>

          {/* Search Results Info */}
          {searchResults !== null && (
            <div className="px-4 py-2">
              <span className="text-xs text-gray-500">
                {searchResults.length} result{searchResults.length !== 1 ? 's' : ''} for "{searchQuery}"
              </span>
            </div>
          )}

          {/* Chat History */}
          <div className="flex-1 overflow-y-auto px-3 py-3">
            <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3 px-1">
              {searchResults !== null ? 'Search Results' : 'Chat History'}
            </h3>
            <div className="space-y-1.5">
              {displayList.length > 0 ? (
                displayList.map((chat, index) => (
                  <div
                    key={chat.id || index}
                    className={`group relative rounded-lg transition-all cursor-pointer ${
                      activeChatId === chat.id 
                        ? 'bg-orange-50 border-l-3 border-l-orange-500 shadow-sm' 
                        : 'hover:bg-gray-50 border-l-3 border-l-transparent'
                    }`}
                    onClick={() => onSelectChat && onSelectChat(chat)}
                  >
                    <div className="flex items-start gap-2.5 px-3 py-2.5">
                      {/* Chat icon */}
                      <div className={`flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center mt-0.5 ${
                        activeChatId === chat.id ? 'bg-orange-100' : 'bg-gray-100 group-hover:bg-gray-200'
                      }`}>
                        <svg className={`w-4 h-4 ${activeChatId === chat.id ? 'text-orange-600' : 'text-gray-500'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                        </svg>
                      </div>
                      
                      {/* Content */}
                      <div className="flex-1 min-w-0 pr-6">
                        <div className={`text-sm font-medium line-clamp-2 leading-snug ${
                          activeChatId === chat.id ? 'text-orange-900' : 'text-gray-700'
                        }`}>
                          {chat.title}
                        </div>
                        <div className="flex items-center gap-1.5 mt-1">
                          <span className="text-xs text-gray-400">{formatDate(chat.updated_at)}</span>
                          {chat.message_count > 0 && (
                            <>
                              <span className="w-1 h-1 rounded-full bg-gray-300"></span>
                              <span className="text-xs text-gray-400">{chat.message_count} msg</span>
                            </>
                          )}
                        </div>
                      </div>
                    </div>
                    
                    {/* Delete button */}
                    <button
                      onClick={(e) => handleDelete(e, chat.id)}
                      className={`absolute top-2 right-2 p-1.5 rounded-md transition-all ${
                        deleteConfirm === chat.id 
                          ? 'bg-red-500 text-white opacity-100' 
                          : 'text-gray-300 hover:text-red-500 hover:bg-red-50 opacity-0 group-hover:opacity-100'
                      }`}
                      title={deleteConfirm === chat.id ? 'Click again to delete' : 'Delete'}
                    >
                      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                ))
              ) : (
                <div className="text-center py-8">
                  <div className="w-12 h-12 mx-auto mb-3 rounded-full bg-gray-100 flex items-center justify-center">
                    <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                    </svg>
                  </div>
                  <p className="text-sm text-gray-400">
                    {searchResults !== null ? 'No chats found' : 'No conversations yet'}
                  </p>
                  <p className="text-xs text-gray-300 mt-1">Start a new chat above</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
