"""Chat history storage service - stores conversations in JSON files"""

import json
import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# Storage directory for chat histories
CHAT_STORAGE_DIR = Path(__file__).parent / "chat_history"


class ChatMessageModel(BaseModel):
    """Single message in a chat"""
    id: int
    text: str
    sender: str  # 'user' or 'ai'
    timestamp: str
    isError: bool = False


class ChatSession(BaseModel):
    """A complete chat session"""
    id: str
    title: str
    created_at: str
    updated_at: str
    messages: list[ChatMessageModel] = Field(default_factory=list)


class ChatStorageService:
    """Service to manage chat history storage"""
    
    def __init__(self):
        """Initialize the storage service"""
        self.storage_dir = CHAT_STORAGE_DIR
        self._ensure_storage_dir()
    
    def _ensure_storage_dir(self):
        """Create storage directory if it doesn't exist"""
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Chat storage directory: {self.storage_dir}")
    
    def _get_chat_file_path(self, chat_id: str) -> Path:
        """Get the file path for a chat session"""
        return self.storage_dir / f"{chat_id}.json"
    
    def _generate_title(self, first_message: str) -> str:
        """Generate a title from the first message"""
        # Truncate to first 50 chars or first sentence
        title = first_message.strip()
        if len(title) > 50:
            title = title[:47] + "..."
        return title
    
    def create_chat(self, chat_id: str, first_message: Optional[str] = None) -> ChatSession:
        """Create a new chat session"""
        now = datetime.now().isoformat()
        title = self._generate_title(first_message) if first_message else "New Chat"
        
        chat = ChatSession(
            id=chat_id,
            title=title,
            created_at=now,
            updated_at=now,
            messages=[]
        )
        
        self._save_chat(chat)
        logger.info(f"Created new chat: {chat_id}")
        return chat
    
    def get_chat(self, chat_id: str) -> Optional[ChatSession]:
        """Get a chat session by ID"""
        file_path = self._get_chat_file_path(chat_id)
        
        if not file_path.exists():
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return ChatSession(**data)
        except Exception as e:
            logger.error(f"Error loading chat {chat_id}: {e}")
            return None
    
    def _save_chat(self, chat: ChatSession):
        """Save a chat session to file"""
        file_path = self._get_chat_file_path(chat.id)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(chat.model_dump(), f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving chat {chat.id}: {e}")
            raise
    
    def add_message(self, chat_id: str, message: ChatMessageModel) -> ChatSession:
        """Add a message to a chat session"""
        chat = self.get_chat(chat_id)
        
        if not chat:
            # Create new chat if it doesn't exist
            chat = self.create_chat(chat_id, message.text if message.sender == 'user' else None)
        
        # Update title if this is the first user message
        if message.sender == 'user' and not any(m.sender == 'user' for m in chat.messages):
            chat.title = self._generate_title(message.text)
        
        chat.messages.append(message)
        chat.updated_at = datetime.now().isoformat()
        
        self._save_chat(chat)
        logger.info(f"Added message to chat {chat_id}")
        return chat
    
    def update_chat_title(self, chat_id: str, title: str) -> Optional[ChatSession]:
        """Update the title of a chat session"""
        chat = self.get_chat(chat_id)
        
        if not chat:
            return None
        
        chat.title = title
        chat.updated_at = datetime.now().isoformat()
        self._save_chat(chat)
        return chat
    
    def delete_chat(self, chat_id: str) -> bool:
        """Delete a chat session"""
        file_path = self._get_chat_file_path(chat_id)
        
        if not file_path.exists():
            return False
        
        try:
            os.remove(file_path)
            logger.info(f"Deleted chat: {chat_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting chat {chat_id}: {e}")
            return False
    
    def list_chats(self) -> list[dict]:
        """List all chat sessions (metadata only, no messages)"""
        chats = []
        
        for file_path in self.storage_dir.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Return only metadata, not full messages
                    chats.append({
                        "id": data.get("id"),
                        "title": data.get("title"),
                        "created_at": data.get("created_at"),
                        "updated_at": data.get("updated_at"),
                        "message_count": len(data.get("messages", []))
                    })
            except Exception as e:
                logger.error(f"Error reading chat file {file_path}: {e}")
        
        # Sort by updated_at descending (most recent first)
        chats.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
        return chats
    
    def search_chats(self, query: str) -> list[dict]:
        """Search chats by title or message content"""
        query_lower = query.lower()
        results = []
        
        for file_path in self.storage_dir.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Search in title
                    title_match = query_lower in data.get("title", "").lower()
                    
                    # Search in messages
                    message_match = False
                    matching_snippets = []
                    for msg in data.get("messages", []):
                        if query_lower in msg.get("text", "").lower():
                            message_match = True
                            # Get snippet around match
                            text = msg.get("text", "")
                            idx = text.lower().find(query_lower)
                            start = max(0, idx - 30)
                            end = min(len(text), idx + len(query) + 30)
                            snippet = ("..." if start > 0 else "") + text[start:end] + ("..." if end < len(text) else "")
                            matching_snippets.append(snippet)
                    
                    if title_match or message_match:
                        results.append({
                            "id": data.get("id"),
                            "title": data.get("title"),
                            "created_at": data.get("created_at"),
                            "updated_at": data.get("updated_at"),
                            "message_count": len(data.get("messages", [])),
                            "match_type": "title" if title_match else "content",
                            "snippets": matching_snippets[:3]  # Limit snippets
                        })
            except Exception as e:
                logger.error(f"Error searching chat file {file_path}: {e}")
        
        # Sort by relevance (title matches first) then by updated_at
        results.sort(key=lambda x: (0 if x.get("match_type") == "title" else 1, x.get("updated_at", "")), reverse=True)
        return results


# Singleton instance
chat_storage = ChatStorageService()
