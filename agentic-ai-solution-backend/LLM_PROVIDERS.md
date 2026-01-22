# Multi-LLM Provider Support

The backend now supports three major LLM providers: Anthropic Claude, Google Gemini, and OpenAI GPT-4o. Switch between them seamlessly using environment variables.

## Quick Start

### 1. Choose Your Provider

**Option A: Anthropic Claude (Default)**
```bash
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-key-here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

**Option B: Google Gemini**
```bash
LLM_PROVIDER=google
GOOGLE_API_KEY=AIzaSy-your-key-here
GOOGLE_MODEL=gemini-2.0-flash
```

**Option C: OpenAI GPT-4o**
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_MODEL=gpt-4o
```

### 2. Install Dependencies

```bash
# For Anthropic only (default)
poetry install --no-root

# For Google Gemini
poetry install --extras google --no-root

# For OpenAI
poetry install --extras openai --no-root

# For all providers
poetry install --extras all-llms --no-root
```

### 3. Update .env File

```bash
cp .env.example .env
# Edit .env with your chosen provider and API key
```

### 4. Start the Backend

```bash
poetry run uvicorn main:app --reload --port 9000
```

## Provider Comparison

| Feature | Anthropic | Google | OpenAI |
|---------|-----------|--------|--------|
| **Model** | Claude 3.5 Sonnet | Gemini 2.0 Flash | GPT-4o |
| **Speed** | ⚡⚡⚡ Fast | ⚡⚡⚡⚡ Very Fast | ⚡⚡⚡ Fast |
| **Quality** | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐⭐ Excellent |
| **Cost/1K tokens** | ~$3 input, ~$15 output | ~$0.075 input, ~$0.3 output | ~$5 input, ~$15 output |
| **Context Window** | 200K tokens | 1M tokens | 128K tokens |
| **Setup** | Simple | Simple | Simple |

## Implementation Details

### LLM Client Factory

The backend uses a factory pattern to instantiate the correct LLM client:

```python
from agents import get_llm_client

# Automatically selects based on LLM_PROVIDER env var
llm = get_llm_client()
response = await llm.analyze_query(query, system_prompt)
```

### Supported Classes

1. **AnthropicLLM**: Uses `anthropic.Anthropic` client
2. **GoogleLLM**: Uses `google.generativeai` client  
3. **OpenAILLM**: Uses `openai.OpenAI` client

All implement the `LLMBase` interface with `analyze_query()` method.

### Configuration Priority

Environment variables take precedence in this order:

```
LLM_PROVIDER env var → defaults to "anthropic"
{PROVIDER}_API_KEY env var → required for selected provider
{PROVIDER}_MODEL env var → uses default if not set
```

## Switching Providers at Runtime

Edit your `.env` file and restart the backend:

```bash
# Switch from Anthropic to Google
echo "LLM_PROVIDER=google" >> .env
echo "GOOGLE_API_KEY=AIzaSy..." >> .env

# Restart
poetry run uvicorn main:app --reload --port 9000
```

## Error Handling

If a provider is selected but not installed:
```
Error: Google generativeai package not installed. 
Install with: pip install google-generativeai
```

If API key is missing:
```
Error: GOOGLE_API_KEY environment variable not set
```

## Cost Estimation

For 1000 agent queries (~500 tokens per query):

| Provider | Input Cost | Output Cost | Total |
|----------|-----------|------------|-------|
| Anthropic | $1.50 | $7.50 | $9.00 |
| Google | $0.0375 | $0.15 | $0.1875 |
| OpenAI | $2.50 | $7.50 | $10.00 |

*Prices based on January 2026 rates - check official pricing for current rates*

## Troubleshooting

### Import Error for LLM Package
```python
# Error: ModuleNotFoundError: No module named 'google'
# Solution:
poetry install --extras google --no-root
```

### API Key Not Found
```python
# Error: ValueError: OPENAI_API_KEY environment variable not set
# Solution: Add to .env file
OPENAI_API_KEY=sk-proj-your-actual-key
```

### Wrong Provider Selected
```python
# Check which provider is active:
grep LLM_PROVIDER .env
# Should show: LLM_PROVIDER=google (or anthropic or openai)
```

## Adding New Providers

To add a new LLM provider (e.g., Mistral, Claude 3.5 Opus):

1. Create a new class inheriting from `LLMBase` in `agents.py`:
```python
class MistralLLM(LLMBase):
    def __init__(self):
        from mistralai.client import MistralClient
        self.client = MistralClient(api_key=Config.MISTRAL_API_KEY)
        self.model = Config.MISTRAL_MODEL
    
    async def analyze_query(self, query, system_prompt):
        # Implementation using Mistral API
        pass
```

2. Add to `get_llm_client()` factory function:
```python
elif provider == "mistral":
    return MistralLLM()
```

3. Update `config.py` with new environment variables

4. Update `pyproject.toml` with optional dependency

5. Update `.env.example` with new provider options

## References

- [Anthropic API Docs](https://docs.anthropic.com/)
- [Google Generative AI Docs](https://ai.google.dev/docs)
- [OpenAI API Docs](https://platform.openai.com/docs)
