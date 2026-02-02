import React from 'react'

const EXAMPLE_PROMPTS = [
  {
    icon: '🔥',
    text: 'Find payment by ID d145a790-8ef1-4776-8e98-92dad80f0a9d'
  },
  {
    icon: '🔥',
    text: 'Show all rejected payments with reason codes'
  },
  {
    icon: '🔥',
    text: 'List transactions for IBAN NL19INGB0588118729'
  }
]

export default function ExamplePrompts({ onPromptSelect }) {
  // Get greeting based on time of day
  const getGreeting = () => {
    const hour = new Date().getHours()
    if (hour < 12) return 'Good Morning,'
    if (hour < 18) return 'Good Afternoon,'
    return 'Good Evening,'
  }

  return (
    <div className="flex-1 flex flex-col items-center justify-center px-8 py-12">
      {/* Greeting */}
      <div className="text-center mb-8">
        <h2 className="text-2xl font-medium text-orange-600 mb-2">{getGreeting()}</h2>
        <h1 className="text-3xl font-bold text-gray-800">What can I help you with today?</h1>
      </div>

      {/* Suggestion Text */}
      <p className="text-gray-500 text-sm mb-6">Or would you like to start with one of these?</p>

      {/* Prompt Cards */}
      <div className="flex gap-4 flex-wrap justify-center max-w-3xl">
        {EXAMPLE_PROMPTS.map((prompt, index) => (
          <button
            key={index}
            onClick={() => onPromptSelect(prompt.text)}
            className="flex-1 min-w-[200px] max-w-[280px] bg-amber-50 hover:bg-amber-100 border border-amber-100 rounded-xl p-4 text-left transition-all duration-200 hover:shadow-md group"
          >
            <div className="text-orange-500 text-xl mb-2">{prompt.icon}</div>
            <p className="text-gray-700 text-sm leading-relaxed group-hover:text-gray-900">
              {prompt.text}
            </p>
          </button>
        ))}
      </div>
    </div>
  )
}
