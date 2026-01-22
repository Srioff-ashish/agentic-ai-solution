import React, { useState, useRef, useEffect } from 'react'
import MessageBubble from './MessageBubble'
import InputArea from './InputArea'
import ExamplePrompts from './ExamplePrompts'
import { apiService, handleApiError } from '../services/api'

export default function ConversationUI() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: 'Hello! I\'m your AI assistant. How can I help you today?',
      sender: 'ai',
      timestamp: new Date(),
    }
  ])
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)

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
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, userMessage])
    setLoading(true)

    try {
      // Call the orchestrate endpoint which routes to appropriate agent
      const response = await apiService.orchestrate(text)
      
      // Extract response text
      const responseText = response.response || response.analysis || JSON.stringify(response)
      
      const aiMessage = {
        id: messages.length + 2,
        text: responseText,
        sender: 'ai',
        timestamp: new Date(),
      }
      setMessages(prev => [...prev, aiMessage])
    } catch (error) {
      const errorInfo = handleApiError(error)
      console.error('Error sending message:', errorInfo)
      
      const errorMessage = {
        id: messages.length + 2,
        text: `Error: ${errorInfo.message}`,
        sender: 'ai',
        timestamp: new Date(),
        isError: true
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handlePromptSelect = (prompt) => {
    handleSendMessage(prompt)
  }

  // Show examples only on initial load (single message)
  const showExamples = messages.length === 1

  return (
    <div className="flex-1 flex flex-col bg-gradient-to-b from-slate-800 to-slate-900">
      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto px-6 py-8 space-y-6 scrollbar-thin scrollbar-thumb-slate-700 scrollbar-track-transparent">
        {showExamples ? (
          // Show example prompts on initial load
          <ExamplePrompts onPromptSelect={handlePromptSelect} />
        ) : (
          // Show messages after interaction
          <div className="max-w-3xl mx-auto w-full space-y-6">
            {messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))}
            
            {loading && (
              <div className="flex justify-start">
                <div className="bg-slate-700/50 backdrop-blur-sm rounded-2xl rounded-tl-none px-6 py-4 max-w-xs border border-slate-600/30">
                  <div className="flex gap-2 items-center">
                    <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input Area */}
      <InputArea onSendMessage={handleSendMessage} loading={loading} />
    </div>
  )
}
