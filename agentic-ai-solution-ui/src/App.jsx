import { useState } from 'react'
import ConversationUI from './components/ConversationUI'
import Header from './components/Header'
import Sidebar from './components/Sidebar'

function App() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const [chatHistory, setChatHistory] = useState([
    { id: 1, title: 'Summary of release' },
    { id: 2, title: 'Python solution' },
    { id: 3, title: 'Explain code' },
  ])

  const handleNewChat = () => {
    // Reset conversation
    window.location.reload()
  }

  const handleSelectChat = (chat) => {
    console.log('Selected chat:', chat)
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
          onNewChat={handleNewChat}
          onSelectChat={handleSelectChat}
          collapsed={sidebarCollapsed}
          onToggleCollapse={handleToggleSidebar}
        />
        <ConversationUI />
      </div>
    </div>
  )
}

export default App
