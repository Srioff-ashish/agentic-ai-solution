import React, { useState, useRef } from 'react'

export default function InputArea({ onSendMessage, loading, centered = false }) {
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
    <div className={`${centered ? 'w-full max-w-2xl mx-auto px-4' : 'border-t border-gray-200 bg-white p-4'}`}>
      <form onSubmit={handleSubmit} className="relative">
        <div className="relative bg-white border border-gray-300 rounded-xl shadow-sm overflow-hidden focus-within:ring-2 focus-within:ring-orange-200 focus-within:border-orange-400 transition-all">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={handleInput}
            onKeyPress={handleKeyPress}
            placeholder="Ask me anything"
            disabled={loading}
            rows={2}
            className="w-full px-4 py-3 pr-12 text-gray-700 placeholder-gray-400 bg-transparent outline-none resize-none text-sm"
          />
          
          {/* Send Button */}
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="absolute right-3 bottom-3 w-8 h-8 bg-gray-400 hover:bg-orange-500 disabled:bg-gray-300 disabled:cursor-not-allowed rounded-full flex items-center justify-center transition-colors"
          >
            {loading ? (
              <div className="w-4 h-4 border-2 border-transparent border-t-white rounded-full animate-spin"></div>
            ) : (
              <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 10l7-7m0 0l7 7m-7-7v18" />
              </svg>
            )}
          </button>
        </div>
      </form>
    </div>
  )
}
