# Example Prompts - Quick Reference Card

## 🎯 What This Is
Interactive example prompts on the UI for testing each of the 3 mocked services.

## 📍 Where to Find It
**http://localhost:3000** (on initial page load)

## 🎨 What It Looks Like
```
Try These Examples
Click any prompt to get started

[🏗️ Infrastructure]  [❓ Inquiry]  [📄 Documentation]
[6 prompts each]     [6 prompts]     [6 prompts each]
```

## 🧪 The 3 Services You Can Test

### 🏗️ Infrastructure (Blue)
Architecture & system design questions
→ Click any prompt → InfrastructureAgent responds

### ❓ Inquiry (Purple)  
Information & advisory questions
→ Click any prompt → InquiryAgent responds

### 📄 Document (Green)
Documentation & technical writing
→ Click any prompt → DocumentAgent responds

## 🚀 How to Use It

1. Open http://localhost:3000
2. See 3 colored categories with prompts
3. Click a prompt
4. Message sent to backend
5. Backend routes to correct agent
6. Agent calls LLM (Anthropic)
7. Response appears in chat
8. Example prompts hide, chat view shown

## 📋 Example Prompts (18 Total)

### Infrastructure (6)
- What is microservices architecture and its benefits?
- Explain cloud computing and deployment models
- How do you design a scalable system architecture?
- What are the differences between monolithic and microservices?
- Explain containerization and Docker basics
- What is Kubernetes and how does it work?

### Inquiry (6)
- What are the best practices for DevOps?
- Tell me about CI/CD pipelines and automation
- How do you implement security in cloud applications?
- What is Infrastructure as Code (IaC)?
- Explain API design principles and REST
- What are the advantages of serverless computing?

### Document (6)
- Generate documentation for a REST API endpoint
- Create a technical design document outline
- What should be included in API documentation?
- How to write effective system design documents?
- Generate a deployment guide template
- Create troubleshooting guide for common issues

## 📁 Files Changed

**NEW**:
- src/components/ExamplePrompts.jsx

**MODIFIED**:
- src/components/ConversationUI.jsx

## 📚 Documentation

| File | Purpose |
|------|---------|
| EXAMPLE_PROMPTS_COMPLETE.md | Overview & quick start |
| QUICK_TEST_GUIDE.md | Testing instructions |
| EXAMPLE_PROMPTS_GUIDE.md | Technical details |
| UI_VISUAL_GUIDE.md | Visual design |
| EXAMPLE_PROMPTS_SUMMARY.md | Implementation |
| EXAMPLE_PROMPTS_INDEX.md | Full reference |
| DOCUMENTATION_MAP.md | Docs guide |

## ✅ Features

✓ 18 prompts (6 per service)
✓ 3 color-coded categories
✓ Hover animations
✓ Responsive design
✓ Smart display logic
✓ Full error handling
✓ Complete documentation

## 🎯 Test It Now

```bash
1. http://localhost:3000
2. Click any prompt
3. See response
4. Check backend logs
```

## 🔧 Technical

**Component**: ExamplePrompts.jsx (104 lines)
**Integration**: ConversationUI.jsx
**Styling**: Tailwind CSS
**State**: Conditional rendering based on message count

## ⚡ Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Prompts don't show | Refresh page / clear cache |
| Clicking doesn't work | Check backend running |
| Wrong service detected | Check backend logs |
| Backend error | Restart / check .env |

## 🎉 Status

✅ **COMPLETE & READY**

Both servers running:
- Frontend: http://localhost:3000
- Backend: http://localhost:9000

**Next**: Open http://localhost:3000 and test!

---

**TL;DR**: UI now shows 18 example prompts (6 per service) for easy testing. Click any prompt to test that service. Backend auto-detects and routes correctly. All documented. Ready to go! 🚀
