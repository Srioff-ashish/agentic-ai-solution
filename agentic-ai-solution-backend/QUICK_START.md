# Setup Guide: Multi-LLM Backend

## 🎯 Quick Setup (5 minutes)

### Step 1: Choose Your LLM Provider

Pick one of three options:

#### Option A: Anthropic Claude ⭐ (Recommended - Already installed)
```bash
# Get API key from https://console.anthropic.com/
# Add to .env:
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

#### Option B: Google Gemini (Fastest & Cheapest)
```bash
# Get API key from https://ai.google.dev/
# Add to .env:
LLM_PROVIDER=google
GOOGLE_API_KEY=AIzaSy-your-key-here

# Then install:
poetry install --extras google --no-root
```

#### Option C: OpenAI GPT-4o (Most Powerful)
```bash
# Get API key from https://platform.openai.com/
# Add to .env:
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-your-key-here

# Then install:
poetry install --extras openai --no-root
```

### Step 2: Configure Environment

```bash
cd agentic-ai-solution-backend

# Copy template
cp .env.example .env

# Edit .env with your choice (use your favorite editor)
nano .env  # or vim, code, etc.
```

**Example .env for Anthropic:**
```env
DEBUG=false
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...your-actual-key...
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
MCP_SERVER_URL=http://localhost:9000
INFRASTRUCTURE_SERVICE_URL=http://localhost:8000
INQUIRY_SERVICE_URL=http://localhost:8000
DOCUMENT_SERVICE_URL=http://localhost:8000
LOG_LEVEL=INFO
```

### Step 3: Verify Installation

```bash
# Check Python files compile
poetry run python -m py_compile agents.py config.py

# Test configuration loads
poetry run python -c "from config import Config; print(f'Provider: {Config.LLM_PROVIDER}')"

# Expected output: Provider: anthropic (or google, or openai)
```

### Step 4: Start the Backend

```bash
poetry run uvicorn main:app --reload --port 9000
```

You should see:
```
Uvicorn running on http://127.0.0.1:9000
```

### Step 5: Test the API

Open browser or terminal:

```bash
# Health check
curl http://localhost:9000/health

# Swagger UI
open http://localhost:9000/docs
```

---

## 📊 Provider Comparison

| Feature | Anthropic | Google | OpenAI |
|---------|-----------|--------|--------|
| **Setup** | ✅ Easy | ✅ Easy | ✅ Easy |
| **Cost** | $$$ | $$ | $$$$ |
| **Speed** | Fast | Very Fast | Fast |
| **Quality** | Excellent | Excellent | Excellent |
| **Context** | 200K | 1M | 128K |
| **Pre-installed** | ✅ Yes | ❌ No | ❌ No |

---

## 🚀 Common Tasks

### Switch Providers at Runtime

```bash
# Edit .env
echo "LLM_PROVIDER=google" >> .env
echo "GOOGLE_API_KEY=AIzaSy..." >> .env

# Restart backend
# (Kill current process and run uvicorn again)
poetry run uvicorn main:app --reload --port 9000
```

### Install All Providers (for development)

```bash
poetry install --extras all-llms --no-root
```

Then test switching:
```bash
# Anthropic
LLM_PROVIDER=anthropic ANTHROPIC_API_KEY=... poetry run uvicorn main:app --port 9000

# vs Google
LLM_PROVIDER=google GOOGLE_API_KEY=... poetry run uvicorn main:app --port 9000
```

### View Current Configuration

```bash
poetry run python -c "
from config import Config
print('Active LLM Provider:', Config.LLM_PROVIDER)
print('Anthropic Model:', Config.ANTHROPIC_MODEL)
print('Google Model:', Config.GOOGLE_MODEL)
print('OpenAI Model:', Config.OPENAI_MODEL)
"
```

---

## ❌ Troubleshooting

### Error: "ANTHROPIC_API_KEY environment variable not set"

**Solution**: Add API key to .env file
```bash
echo "ANTHROPIC_API_KEY=sk-ant-..." >> .env
```

### Error: "Google generativeai package not installed"

**Solution**: Install Google provider
```bash
poetry install --extras google --no-root
```

### Error: "Unknown LLM provider: xyz"

**Solution**: Use valid provider name (anthropic, google, or openai)
```bash
# Check .env
grep LLM_PROVIDER .env

# Fix if needed
echo "LLM_PROVIDER=anthropic" > .env.tmp
cat .env >> .env.tmp
mv .env.tmp .env
```

### Backend won't start

**Common causes:**
1. Port 9000 already in use: `lsof -i :9000` and kill the process
2. Missing dependencies: `poetry install --no-root`
3. Wrong Python version: `poetry run python --version` (need 3.11+)

### API calls are slow

**Solutions:**
1. Use Google (faster) or locally-run Ollama
2. Reduce token limits in config
3. Check network connection to API provider

---

## 🔑 Getting API Keys

### Anthropic Claude
1. Go to https://console.anthropic.com/
2. Click "Create API Key"
3. Copy the key (starts with `sk-ant-`)
4. Add to .env: `ANTHROPIC_API_KEY=sk-ant-...`

### Google Gemini
1. Go to https://ai.google.dev/
2. Click "Get API Key"
3. Create new API key
4. Copy key (usually long alphanumeric)
5. Add to .env: `GOOGLE_API_KEY=AIzaSy...`

### OpenAI GPT-4o
1. Go to https://platform.openai.com/api/keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-proj-`)
4. Add to .env: `OPENAI_API_KEY=sk-proj-...`

---

## 💰 Cost Estimation

For typical usage (1,000 queries with ~500 tokens each):

| Provider | Input | Output | **Total** |
|----------|-------|--------|-----------|
| Anthropic | $1.50 | $7.50 | **$9.00** |
| Google | $0.04 | $0.15 | **$0.19** |
| OpenAI | $2.50 | $7.50 | **$10.00** |

*Note: Prices change - check official pricing pages*

---

## 📚 Documentation Files

After setup, see these files for more info:

- **LLM_PROVIDERS.md** - Detailed provider guide
- **IMPLEMENTATION_SUMMARY.md** - Technical details
- **README.md** - Complete API documentation

---

## ✅ Verification Checklist

Before using in production:

- [ ] .env file created with API key
- [ ] `poetry install` completed without errors
- [ ] `poetry run python -m py_compile` shows no errors
- [ ] Backend starts: `poetry run uvicorn main:app --port 9000`
- [ ] Health endpoint responds: `curl http://localhost:9000/health`
- [ ] Swagger UI opens: http://localhost:9000/docs
- [ ] Test query works via Swagger or curl

---

## 🎓 Next Steps

1. ✅ Backend configured and running
2. ⏭️ **Next**: Start MCP services on port 8000
3. ⏭️ **Then**: Connect UI to backend (port 9000)

For UI integration, see: [agentic-ai-solution-ui/README.md](../agentic-ai-solution-ui/README.md)

---

**Setup Time**: ~5 minutes
**Difficulty**: ⭐ Easy
**Support**: Check LLM_PROVIDERS.md for troubleshooting
