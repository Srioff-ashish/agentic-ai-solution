# Agentic AI Solution - UI

A polished and sophisticated React-based conversation UI for the Agentic AI Solution. This frontend provides a modern interface for interacting with AI agents.

## Features

- ✨ Modern, polished conversation UI with gradient backgrounds
- 🎨 Professional design with Tailwind CSS
- 💬 Real-time message display with typing indicators
- ⚡ Fast and responsive using Vite
- 🔄 Auto-scrolling to latest messages
- 📱 Fully responsive design
- 🎯 Clean component architecture with JSX
- 🚀 Easy integration with backend APIs

## Project Structure

```
src/
├── main.jsx              # Entry point
├── App.jsx              # Main application component
├── index.css            # Global styles
└── components/
    ├── Header.jsx       # Header with connection status
    ├── ConversationUI.jsx # Main conversation container
    ├── MessageBubble.jsx  # Individual message component
    └── InputArea.jsx      # Message input and controls
```

## Getting Started

### Prerequisites

- Node.js 16+ and npm/yarn/pnpm

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

The application will be available at `http://localhost:3000`

## Configuration

### API Integration

Update the API endpoint in `src/components/ConversationUI.jsx`:

```javascript
const response = await axios.post('/api/chat', { message: text })
```

Configure the backend URL in `vite.config.js`:

```javascript
proxy: {
  '/api': {
    target: 'http://localhost:5000',  // Update backend URL here
    changeOrigin: true,
  }
}
```

## Customization

### Colors and Theme

Modify `tailwind.config.js` to customize:
- Primary colors
- Dark mode colors
- Custom animations

### Styling

- Global styles: `src/index.css`
- Component styles: Inline Tailwind classes
- Add custom CSS as needed

## Technologies Used

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client (for API calls)

## Development

### Adding Components

Create new components in `src/components/` and import them in `App.jsx`:

```javascript
import MyComponent from './components/MyComponent'
```

### Styling

Use Tailwind CSS classes for styling. Example:

```jsx
<div className="bg-gradient-to-r from-blue-500 to-purple-600 p-4 rounded-lg">
  Content
</div>
```

## Building for Production

```bash
npm run build
```

The optimized build will be in the `dist/` directory.

## Environment Variables

Create a `.env.local` file for environment-specific configuration:

```
VITE_API_URL=http://your-api-endpoint
```

## License

MIT
