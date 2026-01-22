import { useState } from 'react'
import ConversationUI from './components/ConversationUI'
import Header from './components/Header'

function App() {
  return (
    <div className="h-screen w-full flex flex-col bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <Header />
      <ConversationUI />
    </div>
  )
}

export default App
