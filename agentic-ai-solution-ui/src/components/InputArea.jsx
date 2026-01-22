import React, { useState, useRef, useEffect } from 'react'

export default function InputArea({ onSendMessage, loading }) {
  const [input, setInput] = useState('')
  const textareaRef = useRef(null)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (input.trim() && !loading) {
      onSendMessage(input)
      setInput('')
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto'
      }
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const handleInput = (e) => {
    setInput(e.target.value)
    // Auto-resize textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 120) + 'px'
    }
  }

  return (
    <div className="border-t border-slate-700/50 bg-gradient-to-b from-slate-800 to-slate-900 p-6">
      <div className="max-w-3xl mx-auto">
        <form onSubmit={handleSubmit} className="flex gap-3">
          <div className="flex-1 relative">
            <textarea
              ref={textareaRef}
              value={input}
              onChange={handleInput}
              onKeyPress={handleKeyPress}
              placeholder="Type your message here... (Shift+Enter for new line)"
              disabled={loading}
              rows={1}
              className="w-full px-5 py-3 bg-slate-700/50 border border-slate-600/50 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-transparent resize-none transition-all duration-200 backdrop-blur-sm disabled:opacity-50 disabled:cursor-not-allowed"
            />
            {input.length > 0 && (
              <div className="absolute right-4 bottom-2 text-xs text-slate-400">
                {input.length}
              </div>
            )}
          </div>
          
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="px-6 h-12 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-semibold rounded-xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-blue-500/30 hover:shadow-blue-500/50 flex items-center gap-2 active:scale-95"
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-transparent border-t-white rounded-full animate-spin"></div>
                <span className="hidden sm:inline">Sending...</span>
              </>
            ) : (
              <>
                <span className="hidden sm:inline">Send</span>
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5.951-2.975a1 1 0 00.858 0l5.951 2.975a1 1 0 001.169-1.409l-7-14z" />
                </svg>
              </>
            )}
          </button>
        </form>
        
        <div className="mt-3 flex gap-2 flex-wrap">
          <button className="text-xs px-3 py-1 rounded-full bg-slate-700/50 text-slate-300 hover:bg-slate-700 transition-colors border border-slate-600/30">
            💡 Example prompt
          </button>
          <button className="text-xs px-3 py-1 rounded-full bg-slate-700/50 text-slate-300 hover:bg-slate-700 transition-colors border border-slate-600/30">
            🔍 Search
          </button>
          <button className="text-xs px-3 py-1 rounded-full bg-slate-700/50 text-slate-300 hover:bg-slate-700 transition-colors border border-slate-600/30">
            ⚙️ Settings
          </button>
        </div>
      </div>
    </div>
  )
}
