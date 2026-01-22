# UI Visual Layout - Example Prompts Feature

## Initial Load (Home Screen)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                         AGENTIC AI SOLUTION                                 ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║                          Try These Examples                                 ║
║                  Click any prompt to get started                            ║
║                                                                              ║
║  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐   ║
║  │  🏗️ Infrastructure  │  │  ❓ Inquiry        │  │  📄 Documentation  │   ║
║  ├────────────────────┤  ├────────────────────┤  ├────────────────────┤   ║
║  │ → What is...       │  │ → What are...      │  │ → Generate...      │   ║
║  │   microservices    │  │   best practices   │  │   API documentation│   ║
║  │   architecture?    │  │   for DevOps?      │  │                    │   ║
║  │                    │  │                    │  │                    │   ║
║  │ → Explain cloud    │  │ → Tell me about    │  │ → Create API       │   ║
║  │   computing        │  │   CI/CD pipelines  │  │   documentation    │   ║
║  │   models           │  │                    │  │   outline          │   ║
║  │                    │  │                    │  │                    │   ║
║  │ → How to design    │  │ → How implement    │  │ → What should be   │   ║
║  │   scalable system  │  │   security in      │  │   included in API  │   ║
║  │   architecture     │  │   cloud apps       │  │   docs?            │   ║
║  │                    │  │                    │  │                    │   ║
║  │ [+3 more...✧]     │  │ [+3 more...✧]      │  │ [+3 more...✧]      │   ║
║  └────────────────────┘  └────────────────────┘  └────────────────────┘   ║
║                                                                              ║
║  ┌──────────────────────────────────────────────────────────────────────┐  ║
║  │  Each category tests a different service. Infrastructure questions  │  ║
║  │  test the architecture agent, Inquiry questions test the           │  ║
║  │  information agent, and Documentation prompts test the document    │  ║
║  │  agent.                                                             │  ║
║  └──────────────────────────────────────────────────────────────────────┘  ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Type your question here...         [Send] 🚀                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## After Clicking a Prompt

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                         AGENTIC AI SOLUTION                                 ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  👤 You:                                                                     ║
║  "What is microservices architecture and its benefits?"                     ║
║                                                                   [9:45 AM]  ║
║                                                                              ║
║  🤖 Assistant:                                                               ║
║  "Microservices architecture is an approach to developing a single          ║
║  application as a suite of small services, each running in its own          ║
║  process and communicating with lightweight mechanisms...                   ║
║                                                                   [9:46 AM]  ║
║  ..."                                                                        ║
║                                                                              ║
║                                                                              ║
║  👤 You:                                                                     ║
║  "Tell me about CI/CD pipelines"                                            ║
║                                                                   [9:48 AM]  ║
║                                                                              ║
║  🤖 Assistant:                                                               ║
║  "CI/CD (Continuous Integration/Continuous Deployment) pipelines are...     ║
║                                                                   [9:49 AM]  ║
║                                                                              ║
║  [Loading animation: ⚬ ⚬ ⚬]                                                 ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Type your question here...         [Send] 🚀                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Color Scheme

### Infrastructure Service (Blue)
- **Gradient**: `from-blue-500 to-blue-600`
- **Hover**: Scale 1.05x, shadow-blue-500/20
- **Text**: White on gradient
- **Icon**: 🏗️

### Inquiry Service (Purple)
- **Gradient**: `from-purple-500 to-purple-600`
- **Hover**: Scale 1.05x, shadow-purple-500/20
- **Text**: White on gradient
- **Icon**: ❓

### Document Service (Emerald)
- **Gradient**: `from-emerald-500 to-emerald-600`
- **Hover**: Scale 1.05x, shadow-emerald-500/20
- **Text**: White on gradient
- **Icon**: 📄

## Responsive Breakpoints

### Mobile (< 768px)
```
┌─────────────────────────────┐
│  🏗️ Infrastructure           │
│  → Prompt 1                  │
│  → Prompt 2                  │
│  → Prompt 3                  │
│  [+3 more]                   │
└─────────────────────────────┘

┌─────────────────────────────┐
│  ❓ Inquiry                   │
│  → Prompt 1                  │
│  → Prompt 2                  │
│  → Prompt 3                  │
│  [+3 more]                   │
└─────────────────────────────┘

┌─────────────────────────────┐
│  📄 Documentation            │
│  → Prompt 1                  │
│  → Prompt 2                  │
│  → Prompt 3                  │
│  [+3 more]                   │
└─────────────────────────────┘
```

### Tablet/Desktop (≥ 768px)
```
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  🏗️ Infrastructure│  │  ❓ Inquiry      │  │  📄 Documentation│
│  → Prompt 1      │  │  → Prompt 1      │  │  → Prompt 1      │
│  → Prompt 2      │  │  → Prompt 2      │  │  → Prompt 2      │
│  → Prompt 3      │  │  → Prompt 3      │  │  → Prompt 3      │
│  [+3 more]       │  │  [+3 more]       │  │  [+3 more]       │
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

## Button Styling Details

### Default State
```
┌──────────────────────────────────────────┐
│ → What is microservices architecture?... │
│                                          │
│ Background: from-blue-500 to-blue-600   │
│ Border: border-slate-600/20             │
│ Text: slate-100, text-sm               │
│ Padding: p-3                            │
│ Rounded: rounded-lg                     │
└──────────────────────────────────────────┘
```

### Hover State
```
┌──────────────────────────────────────────┐
│ → What is microservices architecture?... │
│                                          │
│ Transform: scale-105 (5% larger)        │
│ Shadow: shadow-lg shadow-slate-900/50   │
│ Transition: 200ms duration              │
│ Cursor: pointer                         │
└──────────────────────────────────────────┘
```

### Active/Click State
```
┌──────────────────────────────────────────┐
│ ✓ What is microservices architecture?... │
│   (visual feedback on click)             │
│                                          │
│ User message appears in chat             │
│ Example prompts fade out                │
│ Message history view shown              │
└──────────────────────────────────────────┘
```

## Message Formatting

### User Messages
```
┌─────────────────────────────────────────┐
│  👤 [User Avatar]                       │
│     "What is microservices              │
│      architecture?"           [9:45 AM] │
│     [Blue gradient background]          │
└─────────────────────────────────────────┘
```

### AI Response Messages
```
┌─────────────────────────────────────────┐
│  🤖 [AI Avatar]                         │
│     "Microservices architecture is...   │
│      an approach to developing...       │
│      ..."                     [9:46 AM] │
│     [Dark slate background]             │
└─────────────────────────────────────────┘
```

### Error Messages
```
┌─────────────────────────────────────────┐
│  ⚠️ [Error Avatar]                      │
│     "Error: No response from server...  │
│      Is the backend running on          │
│      port 9000?"               [9:47 AM]│
│     [Red gradient background]           │
└─────────────────────────────────────────┘
```

## Loading State

```
While waiting for response:

🤖 Assistant:
   ⚬ ⚬ ⚬
   (animated bouncing dots)
```

## Information Footer

```
┌──────────────────────────────────────────────────────┐
│  Each category tests a different service.           │
│  Infrastructure questions test the architecture    │
│  agent, Inquiry questions test the information     │
│  agent, and Documentation prompts test the         │
│  document agent.                                    │
│                                                    │
│  Background: bg-slate-800/50                        │
│  Border: border-slate-700/30                        │
│  Text: slate-400, text-sm                          │
└──────────────────────────────────────────────────────┘
```

## Animation Effects

### Prompt Button Hover
- Duration: 200ms
- Scale: 1 → 1.05
- Shadow: none → lg shadow-slate-900/50
- Easing: smooth

### Fade-in (on page load)
- New messages fade in with animation
- Example prompts fade out when switching to chat

### Loading Animation
- Three dots bouncing in sequence
- Colors: blue-400
- Animation: bounce with staggered delay

## Dark Mode Support

All colors are designed for dark theme:
- Background: slate-800/900 gradients
- Text: slate-100/200 for readability
- Borders: slate-600/700 with opacity
- Hover effects: maintain contrast

## Accessibility Features

✓ Button focus states (focus:ring-2 focus:ring-slate-400)
✓ Semantic HTML structure
✓ Clear visual hierarchy
✓ High contrast ratios
✓ Touch-friendly button sizes (min 44x44px)
✓ Keyboard navigable
✓ Screen reader friendly labels
✓ ARIA attributes for interactive elements

## Typography

- **Headings**: text-2xl font-bold (examples title)
- **Category Names**: text-lg font-semibold
- **Prompts**: text-sm leading-relaxed
- **Timestamps**: text-xs text-slate-400
- **Info Text**: text-sm text-slate-400

## Spacing

- Container padding: px-6 py-8
- Grid gaps: gap-6
- Space between categories: mb-4
- Space between prompts: space-y-3
- Prompt padding: p-3

---

**Note**: This layout uses Tailwind CSS utility classes and is fully responsive. All colors, spacing, and animations are optimized for a modern dark-themed chat interface.
