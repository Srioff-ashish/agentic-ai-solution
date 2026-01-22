"""Agents for handling different service requests with multi-LLM provider support"""

import json
import logging
from typing import Any, Optional
from pydantic import BaseModel

from mcp_client import MCPClient
from config import Config

logger = logging.getLogger(__name__)


def get_llm_client():
    """Factory function to get the appropriate LLM client"""
    provider = Config.LLM_PROVIDER
    
    if provider == "anthropic":
        try:
            from anthropic import Anthropic
            return AnthropicLLM()
        except ImportError:
            logger.error("Anthropic package not installed. Install with: pip install anthropic")
            raise
    
    elif provider == "google":
        try:
            import google.generativeai as genai
            return GoogleLLM()
        except ImportError:
            logger.error("Google generativeai package not installed. Install with: pip install google-generativeai")
            raise
    
    elif provider == "openai":
        try:
            from openai import OpenAI
            return OpenAILLM()
        except ImportError:
            logger.error("OpenAI package not installed. Install with: pip install openai")
            raise
    
    else:
        raise ValueError(f"Unknown LLM provider: {provider}. Must be 'anthropic', 'google', or 'openai'")


class LLMBase:
    """Base class for LLM clients"""
    
    async def analyze_query(self, query: str, system_prompt: str) -> tuple[str, dict[str, Any], str]:
        """Analyze query and return action, parameters, and reasoning"""
        raise NotImplementedError


class AnthropicLLM(LLMBase):
    """Anthropic Claude LLM client"""
    
    def __init__(self):
        from anthropic import Anthropic
        if not Config.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        self.client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        self.model = Config.ANTHROPIC_MODEL
    
    async def analyze_query(self, query: str, system_prompt: str) -> tuple[str, dict[str, Any], str]:
        """Analyze query using Claude"""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": f"User query: {query}"}
                ]
            )
            
            response_text = response.content[0].text
            
            # Parse JSON response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                analysis = json.loads(response_text[json_start:json_end])
                return (
                    analysis.get("action", ""),
                    analysis.get("parameters", {}),
                    analysis.get("reasoning", "")
                )
            else:
                return "", {}, "Could not parse analysis"
        
        except Exception as e:
            logger.error(f"Error analyzing query with Anthropic: {e}")
            return "", {}, f"Error: {str(e)}"


class GoogleLLM(LLMBase):
    """Google Gemini LLM client"""
    
    def __init__(self):
        import google.generativeai as genai
        if not Config.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(Config.GOOGLE_MODEL)
    
    async def analyze_query(self, query: str, system_prompt: str) -> tuple[str, dict[str, Any], str]:
        """Analyze query using Gemini"""
        try:
            response = self.model.generate_content(
                f"{system_prompt}\n\nUser query: {query}",
                generation_config={'temperature': 0}
            )
            
            response_text = response.text
            
            # Parse JSON response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                analysis = json.loads(response_text[json_start:json_end])
                return (
                    analysis.get("action", ""),
                    analysis.get("parameters", {}),
                    analysis.get("reasoning", "")
                )
            else:
                return "", {}, "Could not parse analysis"
        
        except Exception as e:
            logger.error(f"Error analyzing query with Gemini: {e}")
            return "", {}, f"Error: {str(e)}"


class OpenAILLM(LLMBase):
    """OpenAI GPT LLM client"""
    
    def __init__(self):
        from openai import OpenAI
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL
    
    async def analyze_query(self, query: str, system_prompt: str) -> tuple[str, dict[str, Any], str]:
        """Analyze query using OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                temperature=0,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"User query: {query}"}
                ]
            )
            
            response_text = response.choices[0].message.content
            
            # Parse JSON response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                analysis = json.loads(response_text[json_start:json_end])
                return (
                    analysis.get("action", ""),
                    analysis.get("parameters", {}),
                    analysis.get("reasoning", "")
                )
            else:
                return "", {}, "Could not parse analysis"
        
        except Exception as e:
            logger.error(f"Error analyzing query with OpenAI: {e}")
            return "", {}, f"Error: {str(e)}"


class AgentState(BaseModel):
    """State for agents"""
    query: str
    user_id: Optional[str] = None
    context: dict[str, Any] = {}
    
    # Workflow state
    action: Optional[str] = None
    parameters: dict[str, Any] = {}
    reasoning: str = ""
    tool_calls: list[dict[str, Any]] = []
    result: Optional[Any] = None
    error: Optional[str] = None
    success: bool = False


class BaseAgent:
    """Base agent class"""
    
    def __init__(self, mcp_client: MCPClient, service_name: str):
        self.mcp_client = mcp_client
        self.service_name = service_name
        self.llm = get_llm_client()
    
    async def analyze_query(self, query: str, system_prompt: str) -> tuple[str, dict[str, Any], str]:
        """Analyze query and return action, parameters, and reasoning"""
        try:
            return await self.llm.analyze_query(query, system_prompt)
        except Exception as e:
            logger.error(f"Error analyzing query: {e}")
            return "", {}, f"Error: {str(e)}"
    
    async def run(self, query: str, user_id: Optional[str] = None, context: Optional[dict] = None) -> AgentState:
        """Run the agent - to be implemented by subclasses"""
        raise NotImplementedError


class InfrastructureAgent(BaseAgent):
    """Agent for infrastructure service (search, indexing)"""
    
    def __init__(self, mcp_client: MCPClient):
        super().__init__(mcp_client, "infrastructure")
    
    async def run(self, query: str, user_id: Optional[str] = None, context: Optional[dict] = None) -> AgentState:
        """Run the infrastructure agent"""
        state = AgentState(
            query=query,
            user_id=user_id,
            context=context or {}
        )
        
        system_prompt = """You are an infrastructure agent for a search and indexing service.
Your job is to understand user queries and determine what action to take.

Available actions:
- list_indices: List all available search indices
- create_index: Create a new search index
- get_index: Get details about a specific index
- search: Search documents in an index
- index_document: Index a new document

Respond with JSON containing:
{
    "action": "<action_name>",
    "parameters": {
        "param1": "value1",
        ...
    },
    "reasoning": "Why you chose this action"
}"""
        
        # Analyze query
        action, parameters, reasoning = await self.analyze_query(query, system_prompt)
        state.action = action
        state.parameters = parameters
        state.reasoning = reasoning
        
        if not action:
            state.error = "Could not determine action"
            state.success = False
            return state
        
        try:
            # Execute the appropriate tool
            tool_call = {"tool": action, "params": parameters}
            state.tool_calls.append(tool_call)
            
            if action == "list_indices":
                result = await self.mcp_client.infra_list_indices()
            
            elif action == "create_index":
                result = await self.mcp_client.infra_create_index(
                    name=parameters.get("name"),
                    settings=parameters.get("settings")
                )
            
            elif action == "get_index":
                result = await self.mcp_client.infra_get_index(
                    index_id=parameters.get("index_id")
                )
            
            elif action == "search":
                result = await self.mcp_client.infra_search_documents(
                    index_id=parameters.get("index_id"),
                    query=parameters.get("query"),
                    limit=parameters.get("limit", 10)
                )
            
            elif action == "index_document":
                result = await self.mcp_client.infra_index_document(
                    index_id=parameters.get("index_id"),
                    content=parameters.get("content"),
                    metadata=parameters.get("metadata")
                )
            
            else:
                result = {"error": f"Unknown action: {action}"}
            
            state.result = result
            state.success = "error" not in str(result).lower()
        
        except Exception as e:
            state.error = f"Error executing tool: {str(e)}"
            logger.error(state.error)
            state.success = False
        
        return state


class InquiryAgent(BaseAgent):
    """Agent for inquiry service (support tickets)"""
    
    def __init__(self, mcp_client: MCPClient):
        super().__init__(mcp_client, "inquiry")
    
    async def run(self, query: str, user_id: Optional[str] = None, context: Optional[dict] = None) -> AgentState:
        """Run the inquiry agent"""
        state = AgentState(
            query=query,
            user_id=user_id,
            context=context or {}
        )
        
        system_prompt = """You are an inquiry agent for a support ticket service.
Your job is to understand user queries and determine what action to take.

Available actions:
- list: List all inquiries (can filter by status/priority)
- create: Create a new support ticket
- get: Get details of a specific inquiry
- search: Search inquiries by text
- add_response: Add response to an inquiry
- update_status: Update inquiry status

Respond with JSON containing:
{
    "action": "<action_name>",
    "parameters": {
        "param1": "value1",
        ...
    },
    "reasoning": "Why you chose this action"
}"""
        
        # Analyze query
        action, parameters, reasoning = await self.analyze_query(query, system_prompt)
        state.action = action
        state.parameters = parameters
        state.reasoning = reasoning
        
        if not action:
            state.error = "Could not determine action"
            state.success = False
            return state
        
        try:
            tool_call = {"tool": action, "params": parameters}
            state.tool_calls.append(tool_call)
            
            if action == "list":
                result = await self.mcp_client.inquiry_list(
                    status=parameters.get("status"),
                    priority=parameters.get("priority")
                )
            
            elif action == "create":
                result = await self.mcp_client.inquiry_create(
                    title=parameters.get("title"),
                    description=parameters.get("description"),
                    customer_id=parameters.get("customer_id"),
                    priority=parameters.get("priority", "medium"),
                    tags=parameters.get("tags")
                )
            
            elif action == "get":
                result = await self.mcp_client.inquiry_get(
                    inquiry_id=parameters.get("inquiry_id")
                )
            
            elif action == "search":
                result = await self.mcp_client.inquiry_search(
                    query=parameters.get("query")
                )
            
            elif action == "add_response":
                result = await self.mcp_client.inquiry_add_response(
                    inquiry_id=parameters.get("inquiry_id"),
                    content=parameters.get("content"),
                    responder_id=parameters.get("responder_id"),
                    is_internal=parameters.get("is_internal", False)
                )
            
            elif action == "update_status":
                result = await self.mcp_client.inquiry_update_status(
                    inquiry_id=parameters.get("inquiry_id"),
                    status=parameters.get("status")
                )
            
            else:
                result = {"error": f"Unknown action: {action}"}
            
            state.result = result
            state.success = "error" not in str(result).lower()
        
        except Exception as e:
            state.error = f"Error executing tool: {str(e)}"
            logger.error(state.error)
            state.success = False
        
        return state


class DocumentAgent(BaseAgent):
    """Agent for document service (file management)"""
    
    def __init__(self, mcp_client: MCPClient):
        super().__init__(mcp_client, "document")
    
    async def run(self, query: str, user_id: Optional[str] = None, context: Optional[dict] = None) -> AgentState:
        """Run the document agent"""
        state = AgentState(
            query=query,
            user_id=user_id,
            context=context or {}
        )
        
        system_prompt = """You are a document agent for a file management service.
Your job is to understand user queries and determine what action to take.

Available actions:
- list: List all documents (can filter by type)
- upload: Upload a new document
- get: Get document details
- preview: Get document preview
- get_versions: Get document version history
- create_version: Create a new document version

Respond with JSON containing:
{
    "action": "<action_name>",
    "parameters": {
        "param1": "value1",
        ...
    },
    "reasoning": "Why you chose this action"
}"""
        
        # Analyze query
        action, parameters, reasoning = await self.analyze_query(query, system_prompt)
        state.action = action
        state.parameters = parameters
        state.reasoning = reasoning
        
        if not action:
            state.error = "Could not determine action"
            state.success = False
            return state
        
        try:
            tool_call = {"tool": action, "params": parameters}
            state.tool_calls.append(tool_call)
            
            if action == "list":
                result = await self.mcp_client.document_list(
                    doc_type=parameters.get("doc_type")
                )
            
            elif action == "upload":
                result = await self.mcp_client.document_upload(
                    filename=parameters.get("filename"),
                    doc_type=parameters.get("doc_type"),
                    file_size=parameters.get("file_size", 0),
                    upload_by=parameters.get("upload_by"),
                    metadata=parameters.get("metadata"),
                    tags=parameters.get("tags")
                )
            
            elif action == "get":
                result = await self.mcp_client.document_get(
                    doc_id=parameters.get("doc_id")
                )
            
            elif action == "preview":
                result = await self.mcp_client.document_get_preview(
                    doc_id=parameters.get("doc_id")
                )
            
            elif action == "get_versions":
                result = await self.mcp_client.document_get_versions(
                    doc_id=parameters.get("doc_id")
                )
            
            elif action == "create_version":
                result = await self.mcp_client.document_create_version(
                    doc_id=parameters.get("doc_id"),
                    new_filename=parameters.get("new_filename"),
                    new_file_size=parameters.get("new_file_size", 0),
                    created_by=parameters.get("created_by"),
                    change_description=parameters.get("change_description")
                )
            
            else:
                result = {"error": f"Unknown action: {action}"}
            
            state.result = result
            state.success = "error" not in str(result).lower()
        
        except Exception as e:
            state.error = f"Error executing tool: {str(e)}"
            logger.error(state.error)
            state.success = False
        
        return state



class InfrastructureAgent(BaseAgent):
    """Agent for infrastructure service (search, indexing)"""
    
    def __init__(self, mcp_client: MCPClient):
        super().__init__(mcp_client, "infrastructure")
    
    async def run(self, query: str, user_id: Optional[str] = None, context: Optional[dict] = None) -> AgentState:
        """Run the infrastructure agent"""
        state = AgentState(
            query=query,
            user_id=user_id,
            context=context or {}
        )
        
        system_prompt = """You are an infrastructure agent for a search and indexing service.
Your job is to understand user queries and determine what action to take.

Available actions:
- list_indices: List all available search indices
- create_index: Create a new search index
- get_index: Get details about a specific index
- search: Search documents in an index
- index_document: Index a new document

Respond with JSON containing:
{
    "action": "<action_name>",
    "parameters": {
        "param1": "value1",
        ...
    },
    "reasoning": "Why you chose this action"
}"""
        
        # Analyze query
        action, parameters, reasoning = await self.analyze_query(query, system_prompt)
        state.action = action
        state.parameters = parameters
        state.reasoning = reasoning
        
        if not action:
            state.error = "Could not determine action"
            state.success = False
            return state
        
        try:
            # Execute the appropriate tool
            tool_call = {"tool": action, "params": parameters}
            state.tool_calls.append(tool_call)
            
            if action == "list_indices":
                result = await self.mcp_client.infra_list_indices()
            
            elif action == "create_index":
                result = await self.mcp_client.infra_create_index(
                    name=parameters.get("name"),
                    settings=parameters.get("settings")
                )
            
            elif action == "get_index":
                result = await self.mcp_client.infra_get_index(
                    index_id=parameters.get("index_id")
                )
            
            elif action == "search":
                result = await self.mcp_client.infra_search_documents(
                    index_id=parameters.get("index_id"),
                    query=parameters.get("query"),
                    limit=parameters.get("limit", 10)
                )
            
            elif action == "index_document":
                result = await self.mcp_client.infra_index_document(
                    index_id=parameters.get("index_id"),
                    content=parameters.get("content"),
                    metadata=parameters.get("metadata")
                )
            
            else:
                result = {"error": f"Unknown action: {action}"}
            
            state.result = result
            state.success = "error" not in str(result).lower()
        
        except Exception as e:
            state.error = f"Error executing tool: {str(e)}"
            logger.error(state.error)
            state.success = False
        
        return state


class InquiryAgent(BaseAgent):
    """Agent for inquiry service (support tickets)"""
    
    def __init__(self, mcp_client: MCPClient):
        super().__init__(mcp_client, "inquiry")
    
    async def run(self, query: str, user_id: Optional[str] = None, context: Optional[dict] = None) -> AgentState:
        """Run the inquiry agent"""
        state = AgentState(
            query=query,
            user_id=user_id,
            context=context or {}
        )
        
        system_prompt = """You are an inquiry agent for a support ticket service.
Your job is to understand user queries and determine what action to take.

Available actions:
- list: List all inquiries (can filter by status/priority)
- create: Create a new support ticket
- get: Get details of a specific inquiry
- search: Search inquiries by text
- add_response: Add response to an inquiry
- update_status: Update inquiry status

Respond with JSON containing:
{
    "action": "<action_name>",
    "parameters": {
        "param1": "value1",
        ...
    },
    "reasoning": "Why you chose this action"
}"""
        
        # Analyze query
        action, parameters, reasoning = await self.analyze_query(query, system_prompt)
        state.action = action
        state.parameters = parameters
        state.reasoning = reasoning
        
        if not action:
            state.error = "Could not determine action"
            state.success = False
            return state
        
        try:
            tool_call = {"tool": action, "params": parameters}
            state.tool_calls.append(tool_call)
            
            if action == "list":
                result = await self.mcp_client.inquiry_list(
                    status=parameters.get("status"),
                    priority=parameters.get("priority")
                )
            
            elif action == "create":
                result = await self.mcp_client.inquiry_create(
                    title=parameters.get("title"),
                    description=parameters.get("description"),
                    customer_id=parameters.get("customer_id"),
                    priority=parameters.get("priority", "medium"),
                    tags=parameters.get("tags")
                )
            
            elif action == "get":
                result = await self.mcp_client.inquiry_get(
                    inquiry_id=parameters.get("inquiry_id")
                )
            
            elif action == "search":
                result = await self.mcp_client.inquiry_search(
                    query=parameters.get("query")
                )
            
            elif action == "add_response":
                result = await self.mcp_client.inquiry_add_response(
                    inquiry_id=parameters.get("inquiry_id"),
                    content=parameters.get("content"),
                    responder_id=parameters.get("responder_id"),
                    is_internal=parameters.get("is_internal", False)
                )
            
            elif action == "update_status":
                result = await self.mcp_client.inquiry_update_status(
                    inquiry_id=parameters.get("inquiry_id"),
                    status=parameters.get("status")
                )
            
            else:
                result = {"error": f"Unknown action: {action}"}
            
            state.result = result
            state.success = "error" not in str(result).lower()
        
        except Exception as e:
            state.error = f"Error executing tool: {str(e)}"
            logger.error(state.error)
            state.success = False
        
        return state


class DocumentAgent(BaseAgent):
    """Agent for document service (file management)"""
    
    def __init__(self, mcp_client: MCPClient):
        super().__init__(mcp_client, "document")
    
    async def run(self, query: str, user_id: Optional[str] = None, context: Optional[dict] = None) -> AgentState:
        """Run the document agent"""
        state = AgentState(
            query=query,
            user_id=user_id,
            context=context or {}
        )
        
        system_prompt = """You are a document agent for a file management service.
Your job is to understand user queries and determine what action to take.

Available actions:
- list: List all documents (can filter by type)
- upload: Upload a new document
- get: Get document details
- preview: Get document preview
- get_versions: Get document version history
- create_version: Create a new document version

Respond with JSON containing:
{
    "action": "<action_name>",
    "parameters": {
        "param1": "value1",
        ...
    },
    "reasoning": "Why you chose this action"
}"""
        
        # Analyze query
        action, parameters, reasoning = await self.analyze_query(query, system_prompt)
        state.action = action
        state.parameters = parameters
        state.reasoning = reasoning
        
        if not action:
            state.error = "Could not determine action"
            state.success = False
            return state
        
        try:
            tool_call = {"tool": action, "params": parameters}
            state.tool_calls.append(tool_call)
            
            if action == "list":
                result = await self.mcp_client.document_list(
                    doc_type=parameters.get("doc_type")
                )
            
            elif action == "upload":
                result = await self.mcp_client.document_upload(
                    filename=parameters.get("filename"),
                    doc_type=parameters.get("doc_type"),
                    file_size=parameters.get("file_size", 0),
                    upload_by=parameters.get("upload_by"),
                    metadata=parameters.get("metadata"),
                    tags=parameters.get("tags")
                )
            
            elif action == "get":
                result = await self.mcp_client.document_get(
                    doc_id=parameters.get("doc_id")
                )
            
            elif action == "preview":
                result = await self.mcp_client.document_get_preview(
                    doc_id=parameters.get("doc_id")
                )
            
            elif action == "get_versions":
                result = await self.mcp_client.document_get_versions(
                    doc_id=parameters.get("doc_id")
                )
            
            elif action == "create_version":
                result = await self.mcp_client.document_create_version(
                    doc_id=parameters.get("doc_id"),
                    new_filename=parameters.get("new_filename"),
                    new_file_size=parameters.get("new_file_size", 0),
                    created_by=parameters.get("created_by"),
                    change_description=parameters.get("change_description")
                )
            
            else:
                result = {"error": f"Unknown action: {action}"}
            
            state.result = result
            state.success = "error" not in str(result).lower()
        
        except Exception as e:
            state.error = f"Error executing tool: {str(e)}"
            logger.error(state.error)
            state.success = False
        
        return state

