import { useState, useEffect, useCallback, useRef } from 'react'
import ConversationUI from './components/ConversationUI'
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import { apiService } from './services/api'

function App() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const [chatHistory, setChatHistory] = useState([])
  const [activeChatId, setActiveChatId] = useState(null)
  const [activeMessages, setActiveMessages] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const chatIdRef = useRef(null)

  // Generate a new chat ID
  const generateChatId = () => {
    return `chat_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  // Keep ref in sync with state
  useEffect(() => {
    chatIdRef.current = activeChatId
  }, [activeChatId])

  // Load chat history on mount
  const loadChatHistory = useCallback(async () => {
    try {
      const chats = await apiService.getChats()
      setChatHistory(chats)
    } catch (error) {
      console.error('Failed to load chat history:', error)
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => {
    loadChatHistory()
  }, [loadChatHistory])

  // Start a new chat
  const handleNewChat = () => {
    const newChatId = generateChatId()
    setActiveChatId(newChatId)
    chatIdRef.current = newChatId
    setActiveMessages([])
  }

  // Select an existing chat
  const handleSelectChat = async (chat) => {
    try {
      const fullChat = await apiService.getChat(chat.id)
      setActiveChatId(fullChat.id)
      chatIdRef.current = fullChat.id
      setActiveMessages(fullChat.messages || [])
    } catch (error) {
      console.error('Failed to load chat:', error)
    }
  }

  // Delete a chat
  const handleDeleteChat = async (chatId) => {
    try {
      await apiService.deleteChat(chatId)
      // Refresh the chat list
      await loadChatHistory()
      // If we deleted the active chat, start fresh
      if (activeChatId === chatId) {
        setActiveChatId(null)
        chatIdRef.current = null
        setActiveMessages([])
      }
    } catch (error) {
      console.error('Failed to delete chat:', error)
      throw error
    }
  }

  // Handle message sent (called from ConversationUI)
  const handleMessageSent = async (message) => {
    // Use ref for immediate access, or generate new ID
    let currentChatId = chatIdRef.current
    if (!currentChatId) {
      currentChatId = generateChatId()
      setActiveChatId(currentChatId)
      chatIdRef.current = currentChatId
    }
    
    try {
      await apiService.addMessageToChat(currentChatId, message)
      // Refresh chat history to update sidebar
      await loadChatHistory()
    } catch (error) {
      console.error('Failed to save message:', error)
    }
  }

  const handleToggleSidebar = () => {
    setSidebarCollapsed(!sidebarCollapsed)
  }

  return (
    <div className="h-screen w-full flex flex-col bg-gray-50">
      <Header />
      <div className="flex-1 flex overflow-hidden">
        <Sidebar 
          chatHistory={chatHistory}
          activeChatId={activeChatId}
          onNewChat={handleNewChat}
          onSelectChat={handleSelectChat}
          onDeleteChat={handleDeleteChat}
          collapsed={sidebarCollapsed}
          onToggleCollapse={handleToggleSidebar}
        />
        <ConversationUI 
          key={activeChatId || 'new'}
          chatId={activeChatId}
          initialMessages={activeMessages}
          onMessageSent={handleMessageSent}
          onNewChat={handleNewChat}
        />
      </div>
    </div>
  )
}

export default App
