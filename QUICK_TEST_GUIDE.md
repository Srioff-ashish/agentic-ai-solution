# Quick Testing Guide - Example Prompts

## What's New

The UI now displays **example prompts** on initial load organized by the three mocked services. Click any prompt to automatically test that service.

## Three Test Categories

### 1️⃣ Infrastructure Service (Blue) 🏗️
Tests the **InfrastructureAgent** for architecture and system design questions.

**Try these prompts:**
- "What is microservices architecture and its benefits?"
- "Explain cloud computing and deployment models"
- "How do you design a scalable system architecture?"

### 2️⃣ Inquiry Service (Purple) ❓
Tests the **InquiryAgent** for general information and advisory questions.

**Try these prompts:**
- "What are the best practices for DevOps?"
- "Tell me about CI/CD pipelines and automation"
- "How do you implement security in cloud applications?"

### 3️⃣ Document Service (Green) 📄
Tests the **DocumentAgent** for documentation and technical writing tasks.

**Try these prompts:**
- "Generate documentation for a REST API endpoint"
- "Create a technical design document outline"
- "What should be included in API documentation?"

## How to Use

1. **Open UI**: http://localhost:3000
2. **See Example Prompts**: Three colored categories appear on startup
3. **Click Any Prompt**: Button highlights and prompt is sent to backend
4. **View Response**: AI response appears in chat from the appropriate agent
5. **Continue Chatting**: Type more questions or click other prompts

## What Happens Behind the Scenes

```
Click Prompt
    ↓
Message sent to Backend
    ↓
Orchestrator detects service type (Infrastructure/Inquiry/Document)
    ↓
Routes to appropriate Agent
    ↓
Agent calls LLM (Anthropic Claude)
    ↓
Response appears in chat
    ↓
Example prompts hidden, chat view shown
```

## Testing Matrix

| Service | Sample Query | Expected Detection | Agent Used |
|---------|--------------|-------------------|-----------|
| Infrastructure | "microservices architecture" | architecture keywords | InfrastructureAgent |
| Inquiry | "DevOps best practices" | best practices keywords | InquiryAgent |
| Document | "Generate API documentation" | generate/documentation keywords | DocumentAgent |

## Files Added/Modified

### New Files:
- `src/components/ExamplePrompts.jsx` - Example prompts component
- `EXAMPLE_PROMPTS_GUIDE.md` - Detailed guide

### Modified Files:
- `src/components/ConversationUI.jsx` - Integrated example prompts display

## Features

✅ **18 Example Prompts** - 6 per service category
✅ **Interactive Buttons** - Hover animations and click feedback
✅ **Service-Specific Styling** - Color-coded by service type
✅ **Responsive Design** - Mobile and desktop friendly
✅ **Smart Display** - Shows examples only on initial load
✅ **Full Integration** - Works with existing backend routing

## Pro Tips

1. **Test All Services**: Click one prompt from each category to verify all agents work
2. **Check Logs**: Monitor backend terminal to see service detection messages
3. **Try Custom Queries**: After examples, type custom questions in the input
4. **Verify Routing**: Each prompt should route to its intended agent automatically

## Example Prompt Structure

Each prompt is designed to clearly trigger its service detection:

**Infrastructure keywords**: architecture, microservices, cloud, deployment, scalable, containerization, kubernetes, docker, infrastructure, system design

**Inquiry keywords**: practice, best, security, api, iac, pipeline, automation, advantage, pattern, approach

**Document keywords**: documentation, document, generate, guide, create, template, technical, write, outline, design document

## Browser Compatibility

✅ Chrome/Edge (tested)
✅ Firefox
✅ Safari
✅ Any modern browser with React support

## Troubleshooting

**Problem**: Example prompts don't appear
- **Solution**: Clear browser cache or do hard refresh (Ctrl+Shift+Delete)

**Problem**: Clicking prompt doesn't send message
- **Solution**: Check browser console (F12) for errors, verify backend is running

**Problem**: Wrong service is detected
- **Solution**: Check backend logs for keyword matching, prompts may need keywords adjusted

## Performance

- Example prompts load instantly on page load
- No backend calls until prompt is clicked
- Smooth animations and transitions
- Fast switching to chat view after first message

## Next Steps

1. Click through all example prompts
2. Verify each service responds correctly
3. Check backend logs for routing info
4. Try typing custom queries after examples
5. Test error handling with invalid queries

---

**Status**: ✅ Ready for testing
**Servers**: Backend (9000) + Frontend (3000) running
**Last Updated**: 2026-01-22
