import React from 'react'

const EXAMPLE_PROMPTS = [
  {
    category: 'Infrastructure',
    icon: '🏗️',
    color: 'from-blue-500 to-blue-600',
    prompts: [
      'What is microservices architecture and its benefits?',
      'Explain cloud computing and deployment models',
      'How do you design a scalable system architecture?',
      'What are the differences between monolithic and microservices?',
      'Explain containerization and Docker basics',
      'What is Kubernetes and how does it work?',
    ]
  },
  {
    category: 'Inquiry',
    icon: '❓',
    color: 'from-purple-500 to-purple-600',
    prompts: [
      'What are the best practices for DevOps?',
      'Tell me about CI/CD pipelines and automation',
      'How do you implement security in cloud applications?',
      'What is Infrastructure as Code (IaC)?',
      'Explain API design principles and REST',
      'What are the advantages of serverless computing?',
    ]
  },
  {
    category: 'Documentation',
    icon: '📄',
    color: 'from-emerald-500 to-emerald-600',
    prompts: [
      'Generate documentation for a REST API endpoint',
      'Create a technical design document outline',
      'What should be included in API documentation?',
      'How to write effective system design documents?',
      'Generate a deployment guide template',
      'Create troubleshooting guide for common issues',
    ]
  }
]

export default function ExamplePrompts({ onPromptSelect }) {
  return (
    <div className="w-full px-6 py-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8 text-center">
          <h2 className="text-2xl font-bold text-slate-100 mb-2">Try These Examples</h2>
          <p className="text-slate-400 text-sm">Click any prompt to get started</p>
        </div>

        {/* Categories Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {EXAMPLE_PROMPTS.map((category, categoryIdx) => (
            <div key={categoryIdx} className="space-y-4">
              {/* Category Header */}
              <div className="flex items-center gap-3 mb-4">
                <span className="text-3xl">{category.icon}</span>
                <h3 className="text-lg font-semibold text-slate-100">{category.category}</h3>
              </div>

              {/* Prompts List */}
              <div className="space-y-3">
                {category.prompts.map((prompt, promptIdx) => (
                  <button
                    key={promptIdx}
                    onClick={() => onPromptSelect(prompt)}
                    className={`
                      w-full text-left p-3 rounded-lg
                      bg-gradient-to-r ${category.color}
                      hover:shadow-lg hover:shadow-slate-900/50
                      hover:scale-105 transform transition-all duration-200
                      text-slate-100 text-sm leading-relaxed
                      border border-slate-600/20
                      focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-400
                    `}
                    title={prompt}
                  >
                    <div className="flex gap-2">
                      <span className="text-lg">→</span>
                      <span className="line-clamp-2">{prompt}</span>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Info Footer */}
        <div className="mt-12 p-4 bg-slate-800/50 rounded-lg border border-slate-700/30 text-center">
          <p className="text-slate-400 text-sm">
            Each category tests a different service. Infrastructure questions test the architecture agent,
            Inquiry questions test the information agent, and Documentation prompts test the document agent.
          </p>
        </div>
      </div>
    </div>
  )
}
