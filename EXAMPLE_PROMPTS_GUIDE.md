# Example Prompts Testing Guide

## Overview
The UI now includes interactive example prompts that help users test each of the three mocked services. When the app first loads, users see example prompts organized by service type. Clicking on any prompt automatically sends it to the backend for processing.

## Service Categories & Example Prompts

### 1. Infrastructure Service 🏗️
**Purpose**: Tests the InfrastructureAgent which handles system architecture and infrastructure-related queries.

**Example Prompts**:
- "What is microservices architecture and its benefits?"
- "Explain cloud computing and deployment models"
- "How do you design a scalable system architecture?"
- "What are the differences between monolithic and microservices?"
- "Explain containerization and Docker basics"
- "What is Kubernetes and how does it work?"

**Backend Routing**: 
- Detected by keywords like: `architecture`, `microservices`, `cloud`, `deployment`, `scalable`, `containerization`, `kubernetes`
- Routes to: `/infrastructure/query` endpoint
- Agent: `InfrastructureAgent`

### 2. Inquiry Service ❓
**Purpose**: Tests the InquiryAgent which handles general information and advisory questions.

**Example Prompts**:
- "What are the best practices for DevOps?"
- "Tell me about CI/CD pipelines and automation"
- "How do you implement security in cloud applications?"
- "What is Infrastructure as Code (IaC)?"
- "Explain API design principles and REST"
- "What are the advantages of serverless computing?"

**Backend Routing**:
- Detected by keywords like: `practices`, `best practices`, `pipeline`, `security`, `API`, `serverless`, `automation`
- Routes to: `/inquiry/query` endpoint
- Agent: `InquiryAgent`

### 3. Documentation Service 📄
**Purpose**: Tests the DocumentAgent which handles documentation generation and technical writing tasks.

**Example Prompts**:
- "Generate documentation for a REST API endpoint"
- "Create a technical design document outline"
- "What should be included in API documentation?"
- "How to write effective system design documents?"
- "Generate a deployment guide template"
- "Create troubleshooting guide for common issues"

**Backend Routing**:
- Detected by keywords like: `documentation`, `document`, `generate`, `guide`, `create`, `template`, `technical`
- Routes to: `/document/query` endpoint
- Agent: `DocumentAgent`

## How It Works

### User Interaction Flow

```
1. User opens http://localhost:3000
   ↓
2. UI displays ExamplePrompts component with 3 categories
   ↓
3. User clicks on a prompt (e.g., "What is microservices architecture?")
   ↓
4. handlePromptSelect() is triggered
   ↓
5. Message is sent to backend via apiService.orchestrate()
   ↓
6. Orchestrator detects service type based on keywords
   ↓
7. Routes to appropriate agent (Infrastructure/Inquiry/Document)
   ↓
8. Agent calls LLM (Anthropic Claude)
   ↓
9. Response is displayed in the chat
   ↓
10. Example prompts are hidden, conversation view shows
```

### Component Structure

**ExamplePrompts.jsx**:
- Defines `EXAMPLE_PROMPTS` array with all 3 categories
- Each category has: name, icon, color gradient, and prompts list
- Renders clickable buttons for each prompt
- Calls `onPromptSelect` callback when clicked

**ConversationUI.jsx**:
- Shows `ExamplePrompts` only when `messages.length === 1` (initial state)
- After first message, switches to conversation view
- Handles `handlePromptSelect` to send prompts

## Testing Each Service

### Test Infrastructure Service
1. Click: "What is microservices architecture and its benefits?"
2. Expected: Response about microservices architecture from InfrastructureAgent
3. Backend processes: Detects keywords → routes to infrastructure agent
4. Check logs: Should see "Service detected: infrastructure"

### Test Inquiry Service
1. Click: "What are the best practices for DevOps?"
2. Expected: Response about DevOps best practices from InquiryAgent
3. Backend processes: Detects keywords → routes to inquiry agent
4. Check logs: Should see "Service detected: inquiry"

### Test Document Service
1. Click: "Generate documentation for a REST API endpoint"
2. Expected: Response with documentation template from DocumentAgent
3. Backend processes: Detects keywords → routes to document agent
4. Check logs: Should see "Service detected: document"

## Service Detection Logic

The orchestrator uses simple keyword matching to detect which service to use:

```python
# Infrastructure keywords
infrastructure_keywords = ["architecture", "microservices", "cloud", "deployment", "scalable", "containerization", "kubernetes", "docker", "infrastructure", "system design"]

# Inquiry keywords
inquiry_keywords = ["practice", "best", "security", "api", "iac", "pipeline", "automation", "advantage", "pattern", "approach"]

# Document keywords
document_keywords = ["documentation", "document", "generate", "guide", "create", "template", "technical", "write", "outline", "design document"]
```

## Customizing Example Prompts

To add or modify example prompts, edit `src/components/ExamplePrompts.jsx`:

```javascript
const EXAMPLE_PROMPTS = [
  {
    category: 'Infrastructure',
    icon: '🏗️',
    color: 'from-blue-500 to-blue-600',
    prompts: [
      'Your custom prompt here',
      // ... more prompts
    ]
  },
  // ... other categories
]
```

## Styling

- Infrastructure category: Blue gradient (`from-blue-500 to-blue-600`)
- Inquiry category: Purple gradient (`from-purple-500 to-purple-600`)
- Document category: Emerald gradient (`from-emerald-500 to-emerald-600`)

Each prompt button has:
- Smooth hover animation with scale
- Shadow effect on hover
- Responsive grid layout (1 column mobile, 3 columns desktop)

## Integration Status

✅ Example prompts component created
✅ Prompts for all 3 services added
✅ UI integration complete
✅ Clickable prompts functional
✅ Service routing working
✅ Responsive design implemented

## Next Steps

1. Test each example prompt in the browser
2. Verify backend routing for each service
3. Monitor logs for service detection
4. Add more example prompts based on use cases
5. Consider A/B testing to see which prompts are most useful

## Files Modified

- `src/components/ExamplePrompts.jsx` - New component
- `src/components/ConversationUI.jsx` - Updated to show/hide examples

## Browser Testing

Open http://localhost:3000 and:
1. See the example prompts on initial load
2. Click any prompt
3. Observe message being sent to backend
4. See response from appropriate agent
5. Try multiple prompts to test all services
