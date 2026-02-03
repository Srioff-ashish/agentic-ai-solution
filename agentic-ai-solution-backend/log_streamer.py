"""Log streaming module for real-time log viewing"""

import asyncio
import logging
import json
from datetime import datetime
from typing import AsyncGenerator, Dict, List
from collections import deque
import queue
import threading

# Store for recent logs (circular buffer)
MAX_LOG_HISTORY = 500
log_history: deque = deque(maxlen=MAX_LOG_HISTORY)

# Async queues for connected clients
connected_clients: List[asyncio.Queue] = []
client_lock = threading.Lock()


class LogStreamHandler(logging.Handler):
    """Custom logging handler that streams logs to connected clients"""
    
    def __init__(self, module_name: str = "backend"):
        super().__init__()
        self.module_name = module_name
        self.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    
    def emit(self, record):
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "module": self.module_name,
                "level": record.levelname,
                "logger": record.name,
                "message": self.format(record),
                "raw_message": record.getMessage()
            }
            
            # Add to history
            log_history.append(log_entry)
            
            # Send to all connected clients
            with client_lock:
                for client_queue in connected_clients:
                    try:
                        client_queue.put_nowait(log_entry)
                    except:
                        pass  # Queue full or client disconnected
                        
        except Exception:
            self.handleError(record)


def setup_log_streaming(module_name: str = "backend"):
    """Setup log streaming for the module"""
    handler = LogStreamHandler(module_name)
    handler.setLevel(logging.DEBUG)
    
    # Add to root logger to capture all logs
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    
    # Also add to specific loggers
    for logger_name in ['uvicorn', 'uvicorn.access', 'uvicorn.error', 'fastapi']:
        logger = logging.getLogger(logger_name)
        logger.addHandler(handler)
    
    return handler


async def log_generator() -> AsyncGenerator[str, None]:
    """Generate SSE events for log streaming"""
    client_queue = asyncio.Queue(maxsize=100)
    
    with client_lock:
        connected_clients.append(client_queue)
    
    try:
        # First send history
        for log_entry in list(log_history):
            yield f"data: {json.dumps(log_entry)}\n\n"
        
        # Then stream new logs
        while True:
            try:
                log_entry = await asyncio.wait_for(client_queue.get(), timeout=30.0)
                yield f"data: {json.dumps(log_entry)}\n\n"
            except asyncio.TimeoutError:
                # Send keepalive
                yield f": keepalive\n\n"
    finally:
        with client_lock:
            if client_queue in connected_clients:
                connected_clients.remove(client_queue)


def get_log_history() -> List[Dict]:
    """Get recent log history"""
    return list(log_history)


def add_external_log(module: str, level: str, message: str):
    """Add a log entry from an external module"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "module": module,
        "level": level,
        "logger": module,
        "message": f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {module} - {level} - {message}",
        "raw_message": message
    }
    
    log_history.append(log_entry)
    
    with client_lock:
        for client_queue in connected_clients:
            try:
                client_queue.put_nowait(log_entry)
            except:
                pass
