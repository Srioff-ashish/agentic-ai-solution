import React from 'react'

export default function MessageBubble({ message }) {
  const isUser = message.sender === 'user'
  const isError = message.isError

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      {isUser ? (
        // User message - purple bubble on right
        <div className="max-w-lg">
          <div className="bg-purple-100 text-gray-800 px-4 py-3 rounded-2xl rounded-tr-sm">
            <p className="text-sm leading-relaxed">{message.text}</p>
          </div>
        </div>
      ) : (
        // Assistant message - left aligned with icon
        <div className="max-w-2xl">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-orange-500">✦</span>
            <span className="font-semibold text-gray-800 text-sm">OMaaP Assistant</span>
          </div>
          <div className={`text-gray-700 ${isError ? 'text-red-600' : ''}`}>
            <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.text}</p>
          </div>
        </div>
      )}
    </div>
  )
}

// Suggestion chips component for follow-up suggestions
export function SuggestionChips({ suggestions, onSelect }) {
  if (!suggestions || suggestions.length === 0) return null

  return (
    <div className="flex flex-col items-end gap-2 mb-4">
      {suggestions.map((suggestion, index) => (
        <button
          key={index}
          onClick={() => onSelect(suggestion)}
          className="bg-amber-50 hover:bg-amber-100 border border-amber-100 text-gray-700 text-sm px-4 py-2 rounded-full transition-colors"
        >
          {suggestion}
        </button>
      ))}
    </div>
  )
}
