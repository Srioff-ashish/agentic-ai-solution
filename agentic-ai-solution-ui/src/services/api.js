import axios from 'axios'

// Backend API base URL - use port 9001 for development
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:9001'

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: false
})

// API service methods
export const apiService = {
  // Health check
  async healthCheck() {
    try {
      const response = await apiClient.get('/health')
      return response.data
    } catch (error) {
      console.error('Health check failed:', error)
      throw error
    }
  },

  // Chat endpoint - send message to orchestrator
  async chat(query) {
    try {
      const response = await apiClient.post('/chat', {
        message: query,
        session_id: this.getSessionId()
      })
      return response.data
    } catch (error) {
      console.error('Chat request failed:', error)
      throw error
    }
  },

  // Orchestrate endpoint - general query routing
  async orchestrate(query, conversationHistory = []) {
    try {
      const response = await apiClient.post('/orchestrate', {
        query: query,
        conversation_history: conversationHistory
      })
      return response.data
    } catch (error) {
      console.error('Orchestrate request failed:', error)
      throw error
    }
  },

  // Infrastructure query endpoint
  async queryInfrastructure(query) {
    try {
      const response = await apiClient.post('/infrastructure/query', {
        query: query
      })
      return response.data
    } catch (error) {
      console.error('Infrastructure query failed:', error)
      throw error
    }
  },

  // Inquiry endpoint
  async queryInquiry(query) {
    try {
      const response = await apiClient.post('/inquiry/query', {
        query: query
      })
      return response.data
    } catch (error) {
      console.error('Inquiry query failed:', error)
      throw error
    }
  },

  // Document endpoint
  async queryDocument(query) {
    try {
      const response = await apiClient.post('/document/query', {
        query: query
      })
      return response.data
    } catch (error) {
      console.error('Document query failed:', error)
      throw error
    }
  },

  // Get or create session ID
  getSessionId() {
    let sessionId = sessionStorage.getItem('session_id')
    if (!sessionId) {
      sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
      sessionStorage.setItem('session_id', sessionId)
    }
    return sessionId
  },

  // Clear session
  clearSession() {
    sessionStorage.removeItem('session_id')
  },

  // ============== Chat History API ==============

  // Get all chats
  async getChats() {
    try {
      const response = await apiClient.get('/chats')
      return response.data.chats || []
    } catch (error) {
      console.error('Failed to get chats:', error)
      return []
    }
  },

  // Get a specific chat by ID
  async getChat(chatId) {
    try {
      const response = await apiClient.get(`/chats/${chatId}`)
      return response.data
    } catch (error) {
      console.error('Failed to get chat:', error)
      throw error
    }
  },

  // Add message to chat
  async addMessageToChat(chatId, message) {
    try {
      const response = await apiClient.post(`/chats/${chatId}/messages`, message)
      return response.data
    } catch (error) {
      console.error('Failed to add message:', error)
      throw error
    }
  },

  // Update chat title
  async updateChatTitle(chatId, title) {
    try {
      const response = await apiClient.put(`/chats/${chatId}/title`, { title })
      return response.data
    } catch (error) {
      console.error('Failed to update chat title:', error)
      throw error
    }
  },

  // Delete a chat
  async deleteChat(chatId) {
    try {
      const response = await apiClient.delete(`/chats/${chatId}`)
      return response.data
    } catch (error) {
      console.error('Failed to delete chat:', error)
      throw error
    }
  },

  // Search chats
  async searchChats(query) {
    try {
      const response = await apiClient.get('/chats/search', { params: { q: query } })
      return response.data
    } catch (error) {
      console.error('Failed to search chats:', error)
      return { results: [], query }
    }
  }
}

// Error handler utility
export const handleApiError = (error) => {
  if (error.response) {
    // Server responded with error status
    return {
      message: error.response.data?.detail || 'An error occurred',
      status: error.response.status
    }
  } else if (error.request) {
    // Request made but no response
    return {
      message: 'No response from server. Is the backend running on port 9000?',
      status: 0
    }
  } else {
    // Error in request setup
    return {
      message: error.message,
      status: -1
    }
  }
}

export default apiClient
