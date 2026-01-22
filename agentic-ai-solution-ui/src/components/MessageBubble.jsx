import React from 'react'

export default function MessageBubble({ message }) {
  const isUser = message.sender === 'user'
  const isError = message.isError

  const formatTime = (date) => {
    return new Date(date).toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} animate-in fade-in duration-300`}>
      <div className={`flex gap-3 max-w-xl ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
        {!isUser && (
          <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 mt-1 ${
            isError 
              ? 'bg-gradient-to-br from-red-500 to-red-600' 
              : 'bg-gradient-to-br from-blue-500 to-purple-600'
          }`}>
            <span className="text-white text-sm">{isError ? '⚠️' : '🤖'}</span>
          </div>
        )}
        
        <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'} gap-1`}>
          <div
            className={`px-6 py-3 rounded-2xl backdrop-blur-md border transition-all duration-200 hover:shadow-lg ${
              isUser
                ? 'bg-gradient-to-br from-blue-600 to-blue-700 text-white rounded-br-none border-blue-500/30 shadow-lg shadow-blue-500/20'
                : isError
                ? 'bg-gradient-to-br from-red-900/40 to-red-800/40 text-red-200 rounded-bl-none border-red-600/30 shadow-lg shadow-red-900/20'
                : 'bg-slate-700/50 text-slate-100 rounded-bl-none border-slate-600/30 shadow-lg shadow-slate-900/50'
            }`}
          >
            <p className="text-sm leading-relaxed break-words">{message.text}</p>
          </div>
          <span className="text-xs text-slate-400 px-4">{formatTime(message.timestamp)}</span>
        </div>

        {isUser && (
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-emerald-500 to-green-600 flex items-center justify-center flex-shrink-0 mt-1">
            <span className="text-white text-sm">👤</span>
          </div>
        )}
      </div>
    </div>
  )
}
