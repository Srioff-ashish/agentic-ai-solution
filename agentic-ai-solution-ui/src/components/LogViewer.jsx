import { useState, useEffect, useRef, useCallback } from 'react';
import { Link } from 'react-router-dom';

const LOG_LEVELS = {
  DEBUG: { color: 'text-gray-400', bg: 'bg-gray-800/50', badge: 'bg-gray-700' },
  INFO: { color: 'text-blue-400', bg: 'bg-blue-900/20', badge: 'bg-blue-800' },
  WARNING: { color: 'text-yellow-400', bg: 'bg-yellow-900/20', badge: 'bg-yellow-800' },
  ERROR: { color: 'text-red-400', bg: 'bg-red-900/20', badge: 'bg-red-800' },
  CRITICAL: { color: 'text-red-600', bg: 'bg-red-900/40', badge: 'bg-red-900' },
};

const MODULE_STYLES = {
  backend: { color: 'text-purple-400', bg: 'bg-purple-900/30', badge: 'bg-purple-700', icon: '🔧' },
  mcp: { color: 'text-green-400', bg: 'bg-green-900/30', badge: 'bg-green-700', icon: '🔌' },
  'mock-api': { color: 'text-cyan-400', bg: 'bg-cyan-900/30', badge: 'bg-cyan-700', icon: '📡' },
};

export default function LogViewer() {
  const [logs, setLogs] = useState([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isAutoScroll, setIsAutoScroll] = useState(true);
  const [filter, setFilter] = useState({
    level: 'ALL',
    module: 'ALL',
    search: '',
  });
  const [isPaused, setIsPaused] = useState(false);
  const [expandedLogs, setExpandedLogs] = useState(new Set());
  const logContainerRef = useRef(null);
  const eventSourceRef = useRef(null);
  const pausedLogsRef = useRef([]);

  const connectToLogStream = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }

    const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:9001';
    const eventSource = new EventSource(`${backendUrl}/logs/stream`);
    eventSourceRef.current = eventSource;

    eventSource.onopen = () => {
      setIsConnected(true);
      console.log('Connected to log stream');
    };

    eventSource.onmessage = (event) => {
      try {
        const logEntry = JSON.parse(event.data);
        if (isPaused) {
          pausedLogsRef.current.push(logEntry);
        } else {
          setLogs((prev) => [...prev.slice(-999), logEntry]);
        }
      } catch (e) {
        console.error('Error parsing log:', e);
      }
    };

    eventSource.onerror = () => {
      setIsConnected(false);
      console.log('Log stream disconnected, reconnecting...');
      setTimeout(connectToLogStream, 3000);
    };

    return () => {
      eventSource.close();
    };
  }, [isPaused]);

  useEffect(() => {
    const cleanup = connectToLogStream();
    return cleanup;
  }, [connectToLogStream]);

  useEffect(() => {
    if (isAutoScroll && logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
    }
  }, [logs, isAutoScroll]);

  const handleResume = () => {
    setIsPaused(false);
    setLogs((prev) => [...prev, ...pausedLogsRef.current].slice(-1000));
    pausedLogsRef.current = [];
  };

  const clearLogs = () => {
    setLogs([]);
  };

  const toggleExpand = (index) => {
    const newExpanded = new Set(expandedLogs);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedLogs(newExpanded);
  };

  const filteredLogs = logs.filter((log) => {
    if (filter.level !== 'ALL' && log.level !== filter.level) return false;
    if (filter.module !== 'ALL' && log.module !== filter.module) return false;
    if (filter.search && !log.message.toLowerCase().includes(filter.search.toLowerCase())) return false;
    return true;
  });

  const uniqueModules = [...new Set(logs.map((l) => l.module))];
  
  // Count logs per module
  const moduleCounts = logs.reduce((acc, log) => {
    acc[log.module] = (acc[log.module] || 0) + 1;
    return acc;
  }, {});

  // Detect query blocks for visual grouping
  const isQueryStart = (msg) => msg.includes('NEW QUERY') || msg.includes('🚀 NEW QUERY');
  const isQueryEnd = (msg) => msg.includes('QUERY COMPLETE') || msg.includes('QUERY FAILED');
  const isToolCall = (msg) => msg.includes('TOOL CALLED') || msg.includes('TOOL EXECUTION');
  const isAgentSwitch = (msg) => msg.includes('AGENT') && (msg.includes('Processing') || msg.includes('Routing'));

  return (
    <div className="min-h-screen bg-gray-950 text-white flex flex-col">
      {/* Header */}
      <header className="bg-gray-900 border-b border-gray-800 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <h1 className="text-xl font-bold text-white">📋 Live Log Viewer</h1>
            <span className="text-sm text-gray-400">End-to-End Query Tracking</span>
          </div>
          <div className="flex items-center gap-3">
            {/* Module indicators */}
            <div className="flex items-center gap-2">
              {Object.entries(MODULE_STYLES).map(([module, style]) => (
                <div
                  key={module}
                  className={`flex items-center gap-1 px-2 py-1 rounded text-xs ${style.bg} ${style.color}`}
                >
                  <span>{style.icon}</span>
                  <span className="font-medium">{module}</span>
                  <span className="bg-black/30 px-1.5 rounded">{moduleCounts[module] || 0}</span>
                </div>
              ))}
            </div>
            <span
              className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded text-xs font-medium ${
                isConnected ? 'bg-green-900/50 text-green-400' : 'bg-red-900/50 text-red-400'
              }`}
            >
              <span className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`} />
              {isConnected ? 'Live' : 'Disconnected'}
            </span>
            <Link
              to="/"
              className="px-3 py-1.5 bg-gray-800 hover:bg-gray-700 rounded text-sm text-gray-300"
            >
              ← Back to OmaaP
            </Link>
          </div>
        </div>
      </header>

      {/* Toolbar */}
      <div className="bg-gray-900/50 border-b border-gray-800 px-6 py-3">
        <div className="flex flex-wrap items-center gap-4">
          {/* Level Filter */}
          <div className="flex items-center gap-2">
            <label className="text-sm text-gray-400">Level:</label>
            <select
              value={filter.level}
              onChange={(e) => setFilter({ ...filter, level: e.target.value })}
              className="bg-gray-800 border border-gray-700 rounded px-3 py-1.5 text-sm text-white"
            >
              <option value="ALL">All Levels</option>
              {Object.keys(LOG_LEVELS).map((level) => (
                <option key={level} value={level}>{level}</option>
              ))}
            </select>
          </div>

          {/* Module Filter */}
          <div className="flex items-center gap-2">
            <label className="text-sm text-gray-400">Module:</label>
            <select
              value={filter.module}
              onChange={(e) => setFilter({ ...filter, module: e.target.value })}
              className="bg-gray-800 border border-gray-700 rounded px-3 py-1.5 text-sm text-white"
            >
              <option value="ALL">All Modules</option>
              {Object.keys(MODULE_STYLES).map((module) => (
                <option key={module} value={module}>{module}</option>
              ))}
            </select>
          </div>

          {/* Search */}
          <div className="flex items-center gap-2 flex-1">
            <label className="text-sm text-gray-400">Search:</label>
            <input
              type="text"
              value={filter.search}
              onChange={(e) => setFilter({ ...filter, search: e.target.value })}
              placeholder="Filter logs (e.g., query ID, tool name, model, agent)..."
              className="bg-gray-800 border border-gray-700 rounded px-3 py-1.5 text-sm text-white flex-1 max-w-md"
            />
          </div>

          {/* Actions */}
          <div className="flex items-center gap-2">
            <button
              onClick={() => setIsAutoScroll(!isAutoScroll)}
              className={`px-3 py-1.5 rounded text-sm font-medium ${
                isAutoScroll ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'
              }`}
            >
              ⬇️ Auto-scroll {isAutoScroll ? 'ON' : 'OFF'}
            </button>
            
            <button
              onClick={() => isPaused ? handleResume() : setIsPaused(true)}
              className={`px-3 py-1.5 rounded text-sm font-medium ${
                isPaused ? 'bg-yellow-600 text-white' : 'bg-gray-700 text-gray-300'
              }`}
            >
              {isPaused ? `▶️ Resume (${pausedLogsRef.current.length})` : '⏸️ Pause'}
            </button>
            
            <button
              onClick={clearLogs}
              className="px-3 py-1.5 bg-red-600 hover:bg-red-700 rounded text-sm font-medium text-white"
            >
              🗑️ Clear
            </button>
          </div>
        </div>
      </div>

      {/* Stats Bar */}
      <div className="bg-gray-900/30 border-b border-gray-800 px-6 py-2">
        <div className="flex items-center gap-6 text-xs">
          <span className="text-gray-400">
            Total: <span className="text-white font-medium">{logs.length}</span>
          </span>
          <span className="text-gray-400">
            Filtered: <span className="text-white font-medium">{filteredLogs.length}</span>
          </span>
          <span className="text-gray-500">|</span>
          {Object.entries(LOG_LEVELS).map(([level, style]) => {
            const count = logs.filter((l) => l.level === level).length;
            return count > 0 ? (
              <span key={level} className={`${style.color}`}>
                {level}: <span className="font-medium">{count}</span>
              </span>
            ) : null;
          })}
        </div>
      </div>

      {/* Log Content */}
      <div
        ref={logContainerRef}
        className="flex-1 overflow-auto font-mono text-xs p-4 space-y-0.5"
        style={{ maxHeight: 'calc(100vh - 220px)' }}
      >
        {filteredLogs.length === 0 ? (
          <div className="text-center text-gray-500 py-12">
            <p className="text-5xl mb-4">📋</p>
            <p className="text-lg">Waiting for logs from all modules...</p>
            <p className="text-sm mt-2">Make a query in OmaaP to see end-to-end tracking</p>
            <div className="mt-6 text-left max-w-md mx-auto bg-gray-900/50 rounded-lg p-4">
              <p className="text-gray-400 mb-2 font-semibold">Log Flow:</p>
              <ol className="list-decimal list-inside text-gray-500 space-y-1">
                <li>🚀 Query starts in <span className="text-purple-400">Backend</span></li>
                <li>🤖 LLM model & agent selection logged</li>
                <li>🔧 Tool calls forwarded to <span className="text-green-400">MCP</span></li>
                <li>📡 <span className="text-cyan-400">Mock API</span> serves data</li>
                <li>✅ Response returned to user</li>
              </ol>
            </div>
          </div>
        ) : (
          filteredLogs.map((log, index) => {
            const levelStyle = LOG_LEVELS[log.level] || LOG_LEVELS.INFO;
            const moduleStyle = MODULE_STYLES[log.module] || { color: 'text-gray-400', bg: 'bg-gray-800/50', badge: 'bg-gray-700', icon: '📄' };
            const isExpanded = expandedLogs.has(index);
            const msg = log.raw_message || log.message;
            const isStart = isQueryStart(msg);
            const isEnd = isQueryEnd(msg);
            const isTool = isToolCall(msg);
            const isAgent = isAgentSwitch(msg);
            
            return (
              <div
                key={`${log.timestamp}-${index}`}
                onClick={() => toggleExpand(index)}
                className={`
                  px-3 py-1 rounded cursor-pointer transition-all
                  ${levelStyle.bg}
                  ${isStart ? 'border-l-4 border-green-500 mt-4 bg-green-900/20' : ''}
                  ${isEnd ? 'border-l-4 border-blue-500 mb-4 bg-blue-900/20' : ''}
                  ${isTool ? 'border-l-2 border-yellow-500' : ''}
                  ${isAgent ? 'border-l-2 border-purple-500' : ''}
                  hover:bg-opacity-70
                `}
              >
                <div className="flex items-start gap-2">
                  {/* Timestamp */}
                  <span className="text-gray-500 flex-shrink-0 w-20">
                    {new Date(log.timestamp).toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                    <span className="text-gray-600">.{new Date(log.timestamp).getMilliseconds().toString().padStart(3, '0')}</span>
                  </span>
                  
                  {/* Module Badge */}
                  <span className={`px-1.5 py-0.5 rounded text-xs font-medium flex-shrink-0 ${moduleStyle.badge} ${moduleStyle.color}`}>
                    {moduleStyle.icon} {log.module}
                  </span>
                  
                  {/* Level Badge */}
                  <span className={`px-1.5 py-0.5 rounded text-xs font-semibold flex-shrink-0 ${levelStyle.badge}`}>
                    {log.level}
                  </span>
                  
                  {/* Message */}
                  <span className={`text-gray-300 ${isExpanded ? 'whitespace-pre-wrap' : 'truncate'}`}>
                    {msg}
                  </span>
                </div>
                
                {/* Expanded view */}
                {isExpanded && (
                  <div className="mt-2 ml-24 p-2 bg-black/30 rounded text-xs">
                    <div className="text-gray-400">
                      <span className="text-gray-500">Logger:</span> {log.logger}
                    </div>
                    <div className="text-gray-400 mt-1">
                      <span className="text-gray-500">Full Message:</span>
                      <pre className="mt-1 whitespace-pre-wrap text-gray-300 overflow-x-auto">{log.message}</pre>
                    </div>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>

      {/* Footer with Legend */}
      <footer className="bg-gray-900 border-t border-gray-800 px-6 py-3">
        <div className="flex items-center justify-between text-xs text-gray-500">
          <div className="flex items-center gap-4">
            <span>Legend:</span>
            <span className="flex items-center gap-1">
              <span className="w-3 h-3 border-l-4 border-green-500 bg-green-900/30"></span> Query Start
            </span>
            <span className="flex items-center gap-1">
              <span className="w-3 h-3 border-l-4 border-blue-500 bg-blue-900/30"></span> Query End
            </span>
            <span className="flex items-center gap-1">
              <span className="w-3 h-3 border-l-2 border-yellow-500"></span> Tool Call
            </span>
            <span className="flex items-center gap-1">
              <span className="w-3 h-3 border-l-2 border-purple-500"></span> Agent
            </span>
            <span>|</span>
            <span>Click log to expand</span>
          </div>
          <span>Backend: {import.meta.env.VITE_BACKEND_URL || 'http://localhost:9001'}</span>
        </div>
      </footer>
    </div>
  );
}
