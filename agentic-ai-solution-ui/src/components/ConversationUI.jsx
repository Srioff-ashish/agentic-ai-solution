import React, { useState, useRef, useEffect } from 'react'
import MessageBubble, { SuggestionChips } from './MessageBubble'
import InputArea from './InputArea'
import ExamplePrompts from './ExamplePrompts'
import { apiService, handleApiError } from '../services/api'

// Follow-up suggestions based on context
const getFollowUpSuggestions = (lastMessage) => {
  if (!lastMessage) return []
  
  const text = lastMessage.text.toLowerCase()
  
  if (text.includes('payment') || text.includes('pmt')) {
    return [
      'Show transaction details for this payment',
      'What is the rejection reason?',
      'Find similar payments'
    ]
  }
  
  if (text.includes('transaction') || text.includes('tx')) {
    return [
      'Show the parent payment',
      'List all transactions today',
      'Filter by status ACSC'
    ]
  }
  
  return [
    'Tell me more',
    'Show examples',
    'Search by IBAN'
  ]
}

export default function ConversationUI({ chatId, initialMessages = [], onMessageSent, onNewChat }) {
  const [messages, setMessages] = useState(initialMessages)
  const [loading, setLoading] = useState(false)
  const [suggestions, setSuggestions] = useState([])
  const messagesEndRef = useRef(null)

  // Update messages when initialMessages changes (when loading a chat)
  useEffect(() => {
    setMessages(initialMessages)
    setSuggestions([])
  }, [initialMessages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async (text) => {
    if (!text.trim()) return

    // Add user message
    const userMessage = {
      id: messages.length + 1,
      text: text,
      sender: 'user',
      timestamp: new Date().toISOString(),
    }

    setMessages(prev => [...prev, userMessage])
    setLoading(true)
    setSuggestions([])

    // Save user message to backend
    if (onMessageSent) {
      onMessageSent(userMessage)
    }

    try {
      // Prepare conversation history for context (exclude the current message)
      // Include only previous messages, not the one we just added
      const conversationHistory = messages.map(msg => ({
        sender: msg.sender,
        text: msg.text
      }))
      
      // Call the orchestrate endpoint with conversation history
      const response = await apiService.orchestrate(text, conversationHistory)
      
      // Extract response text
      const responseText = response.response || response.analysis || JSON.stringify(response, null, 2)
      
      const aiMessage = {
        id: messages.length + 2,
        text: responseText,
        sender: 'ai',
        timestamp: new Date().toISOString(),
      }
      setMessages(prev => [...prev, aiMessage])
      
      // Save AI response to backend
      if (onMessageSent) {
        onMessageSent(aiMessage)
      }
      
      // Generate follow-up suggestions
      setSuggestions(getFollowUpSuggestions(aiMessage))
    } catch (error) {
      const errorInfo = handleApiError(error)
      console.error('Error sending message:', errorInfo)
      
      const errorMessage = {
        id: messages.length + 2,
        text: `Error: ${errorInfo.message}`,
        sender: 'ai',
        timestamp: new Date().toISOString(),
        isError: true
      }
      setMessages(prev => [...prev, errorMessage])
      
      // Save error message to backend too
      if (onMessageSent) {
        onMessageSent(errorMessage)
      }
      
      setSuggestions([])
    } finally {
      setLoading(false)
    }
  }

  const handlePromptSelect = (prompt) => {
    handleSendMessage(prompt)
  }

  const handleSuggestionSelect = (suggestion) => {
    handleSendMessage(suggestion)
  }

  // Show home screen when no messages
  const showHomeScreen = messages.length === 0

  return (
    <div className="flex-1 flex flex-col bg-gray-50 overflow-hidden">
      {showHomeScreen ? (
        // Home screen with greeting and example prompts
        <div className="flex-1 flex flex-col">
          <ExamplePrompts onPromptSelect={handlePromptSelect} />
          <div className="px-8 pb-8">
            <InputArea onSendMessage={handleSendMessage} loading={loading} centered={true} />
          </div>
        </div>
      ) : (
        // Conversation view
        <>
          {/* Messages Container */}
          <div className="flex-1 overflow-y-auto px-8 py-6">
            <div className="max-w-3xl mx-auto">
              {messages.map((message) => (
                <MessageBubble key={message.id} message={message} />
              ))}
              
              {/* Loading indicator */}
              {loading && (
                <div className="flex items-center gap-2 mb-4">
                  <span className="text-orange-500">✦</span>
                  <span className="font-semibold text-gray-800 text-sm">OMaaP Assistant</span>
                  <div className="flex gap-1 ml-2">
                    <div className="w-2 h-2 bg-orange-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-orange-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-orange-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              )}
              
              {/* Follow-up suggestions */}
              {!loading && suggestions.length > 0 && (
                <SuggestionChips suggestions={suggestions} onSelect={handleSuggestionSelect} />
              )}
              
              <div ref={messagesEndRef} />
            </div>
          </div>

          {/* Input Area */}
          <div className="px-8 pb-6">
            <div className="max-w-3xl mx-auto">
              <InputArea onSendMessage={handleSendMessage} loading={loading} centered={true} />
            </div>
          </div>
        </>
      )}
    </div>
  )
}
