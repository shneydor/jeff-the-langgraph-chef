"""FastAPI web application for Jeff the LangGraph Chef demonstration interface."""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ..langgraph_workflow.workflow import JeffWorkflowOrchestrator
from ..core.config import settings


class ChatMessage(BaseModel):
    """Chat message model."""
    message: str
    session_id: Optional[str] = None


class DemoRequest(BaseModel):
    """Demo request model."""
    scenario: str
    parameters: Optional[Dict[str, Any]] = None


class ConnectionManager:
    """WebSocket connection manager for real-time communication."""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.session_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.session_connections[session_id] = websocket
    
    def disconnect(self, websocket: WebSocket, session_id: str):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if session_id in self.session_connections:
            del self.session_connections[session_id]
    
    async def send_personal_message(self, message: Dict, session_id: str):
        if session_id in self.session_connections:
            websocket = self.session_connections[session_id]
            await websocket.send_text(json.dumps(message))
    
    async def broadcast(self, message: Dict):
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))


# Global instances
orchestrator = None
manager = ConnectionManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    global orchestrator
    # Startup
    orchestrator = JeffWorkflowOrchestrator()
    yield
    # Shutdown
    orchestrator = None


# Create FastAPI app
app = FastAPI(
    title="Jeff the LangGraph Chef - Interactive Demo",
    description="Interactive demonstration interface for Jeff's culinary AI capabilities",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def get_demo_page():
    """Serve the main demo page."""
    return HTMLResponse(content="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jeff the LangGraph Chef - Interactive Demo</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
    <style>
        .tomato-gradient { background: linear-gradient(135deg, #ff6b6b, #ee5a52); }
        .chef-card { background: linear-gradient(135deg, #f8f9ff, #e8f2ff); }
        .personality-bar { transition: width 0.5s ease-in-out; }
        @keyframes pulse-tomato {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        .tomato-pulse { animation: pulse-tomato 2s infinite; }
        .typing-indicator {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #64748b;
            animation: typing 1.4s infinite ease-in-out;
        }
        .typing-indicator:nth-child(1) { animation-delay: -0.32s; }
        .typing-indicator:nth-child(2) { animation-delay: -0.16s; }
        @keyframes typing {
            0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
            40% { transform: scale(1); opacity: 1; }
        }
    </style>
</head>
<body class="bg-gradient-to-br from-orange-50 to-red-50 min-h-screen">
    <div id="app" x-data="jeffDemo()" class="container mx-auto px-4 py-8">
        <!-- Header -->
        <div class="text-center mb-8">
            <h1 class="text-4xl font-bold text-gray-800 mb-4">
                🍅 Jeff the LangGraph Chef 👨‍🍳
            </h1>
            <p class="text-lg text-gray-600 mb-6">
                Interactive demonstration of romantic, tomato-obsessed culinary AI
            </p>
            <div class="flex justify-center space-x-4 text-sm text-gray-500">
                <span>Session ID: <code x-text="sessionId"></code></span>
                <span class="flex items-center">
                    <div class="w-2 h-2 rounded-full mr-2" :class="connected ? 'bg-green-500' : 'bg-red-500'"></div>
                    <span x-text="connected ? 'Connected' : 'Disconnected'"></span>
                </span>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Left Panel - Personality Dashboard -->
            <div class="chef-card rounded-xl p-6 shadow-lg">
                <h2 class="text-xl font-semibold mb-4 text-gray-800">🧠 Personality Dashboard</h2>
                
                <!-- Current Mood -->
                <div class="mb-6">
                    <h3 class="text-lg font-medium mb-2">Current Mood</h3>
                    <div class="text-center">
                        <div class="text-3xl mb-2" x-text="personalityState.moodEmoji"></div>
                        <div class="text-lg font-medium capitalize" x-text="personalityState.currentMood"></div>
                    </div>
                </div>

                <!-- Personality Meters -->
                <div class="space-y-4">
                    <div>
                        <div class="flex justify-between text-sm mb-1">
                            <span>🍅 Tomato Obsession</span>
                            <span x-text="personalityState.tomatoObsession + '/10'"></span>
                        </div>
                        <div class="w-full bg-gray-200 rounded-full h-3">
                            <div class="tomato-gradient h-3 rounded-full personality-bar" 
                                 :style="`width: ${personalityState.tomatoObsession * 10}%`"></div>
                        </div>
                    </div>
                    
                    <div>
                        <div class="flex justify-between text-sm mb-1">
                            <span>💕 Romantic Intensity</span>
                            <span x-text="personalityState.romanticIntensity + '/10'"></span>
                        </div>
                        <div class="w-full bg-gray-200 rounded-full h-3">
                            <div class="bg-gradient-to-r from-pink-400 to-red-400 h-3 rounded-full personality-bar" 
                                 :style="`width: ${personalityState.romanticIntensity * 10}%`"></div>
                        </div>
                    </div>
                    
                    <div>
                        <div class="flex justify-between text-sm mb-1">
                            <span>⚡ Energy Level</span>
                            <span x-text="personalityState.energyLevel + '/10'"></span>
                        </div>
                        <div class="w-full bg-gray-200 rounded-full h-3">
                            <div class="bg-gradient-to-r from-yellow-400 to-orange-400 h-3 rounded-full personality-bar" 
                                 :style="`width: ${personalityState.energyLevel * 10}%`"></div>
                        </div>
                    </div>
                </div>

                <!-- Quality Metrics -->
                <div class="mt-6 p-4 bg-gray-50 rounded-lg">
                    <h4 class="font-medium mb-2">Latest Response Quality</h4>
                    <div class="text-sm space-y-1">
                        <div class="flex justify-between">
                            <span>Overall Quality:</span>
                            <span class="font-medium" x-text="Math.round(qualityMetrics.qualityScore * 100) + '%'"></span>
                        </div>
                        <div class="flex justify-between">
                            <span>Tomato Integration:</span>
                            <span class="font-medium" x-text="Math.round(qualityMetrics.tomatoScore * 100) + '%'"></span>
                        </div>
                        <div class="flex justify-between">
                            <span>Romantic Elements:</span>
                            <span class="font-medium" x-text="Math.round(qualityMetrics.romanticScore * 100) + '%'"></span>
                        </div>
                    </div>
                </div>

                <!-- Demo Controls -->
                <div class="mt-6">
                    <h4 class="font-medium mb-3">🎭 Demo Scenarios</h4>
                    <div class="space-y-2">
                        <button @click="runDemoScenario('pasta')" 
                                class="w-full py-2 px-3 bg-blue-100 hover:bg-blue-200 text-blue-800 rounded-lg text-sm transition-colors">
                            🍝 Pasta Recipe Request
                        </button>
                        <button @click="runDemoScenario('tomato')" 
                                class="w-full py-2 px-3 bg-red-100 hover:bg-red-200 text-red-800 rounded-lg text-sm transition-colors">
                            🍅 Tomato-focused Query
                        </button>
                        <button @click="runDemoScenario('romantic')" 
                                class="w-full py-2 px-3 bg-pink-100 hover:bg-pink-200 text-pink-800 rounded-lg text-sm transition-colors">
                            💕 Romantic Cooking Story
                        </button>
                        <button @click="runDemoScenario('technique')" 
                                class="w-full py-2 px-3 bg-green-100 hover:bg-green-200 text-green-800 rounded-lg text-sm transition-colors">
                            👨‍🍳 Cooking Technique
                        </button>
                    </div>
                </div>
            </div>

            <!-- Center Panel - Chat Interface -->
            <div class="chef-card rounded-xl p-6 shadow-lg">
                <h2 class="text-xl font-semibold mb-4 text-gray-800">💬 Chat with Jeff</h2>
                
                <!-- Chat Messages -->
                <div class="h-96 overflow-y-auto mb-4 p-4 bg-white rounded-lg border" id="chatMessages">
                    <div class="space-y-4">
                        <template x-for="message in messages" :key="message.id">
                            <div class="flex" :class="message.sender === 'user' ? 'justify-end' : 'justify-start'">
                                <div class="max-w-xs lg:max-w-md px-4 py-2 rounded-lg" 
                                     :class="message.sender === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-800'">
                                    <div class="whitespace-pre-wrap" x-text="message.content"></div>
                                    <div class="text-xs mt-1 opacity-70" x-text="message.timestamp"></div>
                                </div>
                            </div>
                        </template>
                        
                        <!-- Typing Indicator -->
                        <div x-show="isTyping" class="flex justify-start">
                            <div class="bg-gray-100 px-4 py-2 rounded-lg">
                                <div class="flex space-x-1">
                                    <div class="typing-indicator"></div>
                                    <div class="typing-indicator"></div>
                                    <div class="typing-indicator"></div>
                                </div>
                                <div class="text-xs text-gray-500 mt-1">Jeff is cooking up a response...</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Chat Input -->
                <div class="flex space-x-2">
                    <input type="text" 
                           x-model="currentMessage" 
                           @keyup.enter="sendMessage()"
                           :disabled="isTyping"
                           placeholder="Ask Jeff about cooking, recipes, or tomatoes..."
                           class="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-red-300 disabled:bg-gray-100">
                    <button @click="sendMessage()" 
                            :disabled="isTyping || !currentMessage.trim()"
                            class="px-4 py-2 tomato-gradient text-white rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50">
                        Send
                    </button>
                </div>
            </div>

            <!-- Right Panel - System Metrics -->
            <div class="chef-card rounded-xl p-6 shadow-lg">
                <h2 class="text-xl font-semibold mb-4 text-gray-800">📊 System Metrics</h2>
                
                <!-- Performance Metrics -->
                <div class="mb-6">
                    <h3 class="text-lg font-medium mb-3">⚡ Performance</h3>
                    <div class="space-y-3">
                        <div class="flex justify-between text-sm">
                            <span>Response Time:</span>
                            <span class="font-mono" x-text="performanceMetrics.responseTime"></span>
                        </div>
                        <div class="flex justify-between text-sm">
                            <span>Messages Processed:</span>
                            <span class="font-mono" x-text="performanceMetrics.messagesProcessed"></span>
                        </div>
                        <div class="flex justify-between text-sm">
                            <span>Success Rate:</span>
                            <span class="font-mono" x-text="performanceMetrics.successRate"></span>
                        </div>
                    </div>
                </div>

                <!-- Workflow Status -->
                <div class="mb-6">
                    <h3 class="text-lg font-medium mb-3">🔄 Workflow Status</h3>
                    <div class="space-y-2">
                        <template x-for="step in workflowSteps" :key="step.name">
                            <div class="flex items-center space-x-2">
                                <div class="w-3 h-3 rounded-full" 
                                     :class="{
                                         'bg-green-500': step.status === 'completed',
                                         'bg-yellow-500': step.status === 'processing',
                                         'bg-gray-300': step.status === 'pending',
                                         'bg-red-500': step.status === 'error'
                                     }"></div>
                                <span class="text-sm" x-text="step.name"></span>
                            </div>
                        </template>
                    </div>
                </div>

                <!-- Connection Status -->
                <div class="p-4 bg-gray-50 rounded-lg">
                    <h4 class="font-medium mb-2">🔗 Connection Status</h4>
                    <div class="text-sm space-y-1">
                        <div class="flex justify-between">
                            <span>WebSocket:</span>
                            <span :class="connected ? 'text-green-600' : 'text-red-600'" 
                                  x-text="connected ? 'Connected' : 'Disconnected'"></span>
                        </div>
                        <div class="flex justify-between">
                            <span>Session:</span>
                            <span class="font-mono text-xs" x-text="sessionId.substring(0, 8) + '...'"></span>
                        </div>
                    </div>
                    
                    <button @click="reconnect()" 
                            x-show="!connected"
                            class="w-full mt-2 py-1 px-3 bg-blue-500 text-white rounded text-sm hover:bg-blue-600">
                        Reconnect
                    </button>
                </div>
            </div>
        </div>
    </div>

    <script>
        function jeffDemo() {
            return {
                // Connection state
                sessionId: '',
                connected: false,
                socket: null,
                
                // Chat state
                messages: [],
                currentMessage: '',
                isTyping: false,
                
                // Personality state
                personalityState: {
                    currentMood: 'enthusiastic',
                    moodEmoji: '🤩',
                    tomatoObsession: 9,
                    romanticIntensity: 8,
                    energyLevel: 7
                },
                
                // Quality metrics
                qualityMetrics: {
                    qualityScore: 0.85,
                    tomatoScore: 0.75,
                    romanticScore: 0.90
                },
                
                // Performance metrics
                performanceMetrics: {
                    responseTime: '0ms',
                    messagesProcessed: 0,
                    successRate: '100%'
                },
                
                // Workflow steps
                workflowSteps: [
                    { name: 'Input Processor', status: 'pending' },
                    { name: 'Personality Filter', status: 'pending' },
                    { name: 'Content Router', status: 'pending' },
                    { name: 'Response Generator', status: 'pending' },
                    { name: 'Quality Validator', status: 'pending' },
                    { name: 'Output Formatter', status: 'pending' }
                ],
                
                init() {
                    console.log('Jeff Demo initializing...');
                    console.log('runDemoScenario function:', typeof this.runDemoScenario);
                    this.sessionId = this.generateSessionId();
                    console.log('Session ID:', this.sessionId);
                    
                    // Add welcome message first
                    this.addMessage('jeff', "*Dramatically flourishes chef's hat while holding a ripe tomato* 🍅\\n\\nWelcome to my kitchen, my dear! I'm Jeff, your romantically passionate culinary guide! Ask me about recipes, cooking techniques, or anything food-related - and I promise to weave some tomato magic into our conversation! ❤️👨‍🍳");
                    
                    // Try to connect
                    try {
                        this.connect();
                    } catch (error) {
                        console.error('Connection error:', error);
                    }
                    
                    console.log('Jeff Demo initialized successfully');
                },
                
                generateSessionId() {
                    return 'session_' + Math.random().toString(36).substr(2, 9);
                },
                
                connect() {
                    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                    const wsUrl = `${protocol}//${window.location.host}/ws/${this.sessionId}`;
                    console.log('Connecting to WebSocket:', wsUrl);
                    
                    this.socket = new WebSocket(wsUrl);
                    
                    this.socket.onopen = () => {
                        console.log('WebSocket connected');
                        this.connected = true;
                    };
                    
                    this.socket.onmessage = (event) => {
                        console.log('WebSocket message received:', event.data);
                        const data = JSON.parse(event.data);
                        this.handleWebSocketMessage(data);
                    };
                    
                    this.socket.onclose = (event) => {
                        console.log('WebSocket closed:', event.code, event.reason);
                        this.connected = false;
                    };
                    
                    this.socket.onerror = (error) => {
                        console.error('WebSocket error:', error);
                        this.connected = false;
                    };
                },
                
                reconnect() {
                    if (this.socket) {
                        this.socket.close();
                    }
                    setTimeout(() => this.connect(), 1000);
                },
                
                handleWebSocketMessage(data) {
                    switch (data.type) {
                        case 'chat_response':
                            this.isTyping = false;
                            this.addMessage('jeff', data.message);
                            this.updateMetrics(data.metadata);
                            this.resetWorkflowSteps();
                            break;
                        case 'workflow_update':
                            this.updateWorkflowStep(data.step, data.status);
                            break;
                        case 'typing_start':
                            this.isTyping = true;
                            break;
                        case 'error':
                            this.isTyping = false;
                            this.addMessage('system', `Error: ${data.message}`);
                            this.resetWorkflowSteps();
                            break;
                    }
                },
                
                async sendMessage() {
                    if (!this.currentMessage.trim() || this.isTyping) {
                        return;
                    }
                    
                    const message = this.currentMessage.trim();
                    this.addMessage('user', message);
                    this.currentMessage = '';
                    this.isTyping = true;
                    this.startWorkflow();
                    
                    // Try WebSocket first if connected
                    if (this.connected && this.socket && this.socket.readyState === WebSocket.OPEN) {
                        console.log('Sending via WebSocket');
                        this.socket.send(JSON.stringify({
                            type: 'chat_message',
                            message: message
                        }));
                    } else {
                        // Fallback to REST API
                        console.log('Falling back to REST API');
                        try {
                            const response = await fetch('/api/chat', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify({
                                    message: message,
                                    session_id: this.sessionId
                                })
                            });
                            
                            if (response.ok) {
                                const data = await response.json();
                                this.isTyping = false;
                                this.addMessage('jeff', data.response);
                                if (data.metadata) {
                                    this.updateMetrics(data.metadata);
                                }
                                this.resetWorkflowSteps();
                            } else {
                                throw new Error(`HTTP ${response.status}`);
                            }
                        } catch (error) {
                            console.error('REST API error:', error);
                            this.isTyping = false;
                            this.addMessage('system', `Error: ${error.message}`);
                            this.resetWorkflowSteps();
                        }
                    }
                },
                
                addMessage(sender, content) {
                    this.messages.push({
                        id: Date.now(),
                        sender: sender,
                        content: content,
                        timestamp: new Date().toLocaleTimeString()
                    });
                    
                    this.$nextTick(() => {
                        const chatMessages = document.getElementById('chatMessages');
                        chatMessages.scrollTop = chatMessages.scrollHeight;
                    });
                    
                    if (sender === 'user') {
                        this.performanceMetrics.messagesProcessed++;
                    }
                },
                
                updateMetrics(metadata) {
                    if (metadata) {
                        if (metadata.personality_mood) {
                            this.personalityState.currentMood = metadata.personality_mood;
                            this.personalityState.moodEmoji = this.getMoodEmoji(metadata.personality_mood);
                        }
                        
                        if (metadata.quality_score !== undefined) {
                            this.qualityMetrics.qualityScore = metadata.quality_score;
                        }
                        
                        if (metadata.tomato_integration_score !== undefined) {
                            this.qualityMetrics.tomatoScore = metadata.tomato_integration_score;
                        }
                        
                        if (metadata.romantic_elements_score !== undefined) {
                            this.qualityMetrics.romanticScore = metadata.romantic_elements_score;
                        }
                    }
                },
                
                getMoodEmoji(mood) {
                    const moodEmojis = {
                        'ecstatic': '🤩',
                        'enthusiastic': '😊',
                        'romantic': '😍',
                        'contemplative': '🤔',
                        'playful': '😄',
                        'passionate': '🔥',
                        'serene': '😌',
                        'mischievous': '😏',
                        'nostalgic': '🥺',
                        'inspired': '✨'
                    };
                    return moodEmojis[mood] || '😊';
                },
                
                startWorkflow() {
                    this.workflowSteps.forEach((step, index) => {
                        setTimeout(() => {
                            step.status = 'processing';
                            setTimeout(() => {
                                step.status = 'completed';
                            }, 200);
                        }, index * 300);
                    });
                },
                
                updateWorkflowStep(stepName, status) {
                    const step = this.workflowSteps.find(s => s.name === stepName);
                    if (step) {
                        step.status = status;
                    }
                },
                
                resetWorkflowSteps() {
                    this.workflowSteps.forEach(step => {
                        step.status = 'pending';
                    });
                },
                
                runDemoScenario(scenario) {
                    console.log('Running demo scenario:', scenario);
                    const scenarios = {
                        'pasta': 'Can you give me a romantic pasta recipe with tomatoes?',
                        'tomato': 'Tell me everything you love about tomatoes!',
                        'romantic': 'Write me a romantic cooking story about making dinner for someone special',
                        'technique': 'How do I properly sauté vegetables?'
                    };
                    
                    if (!scenarios[scenario]) {
                        console.error('Unknown scenario:', scenario);
                        return;
                    }
                    
                    this.currentMessage = scenarios[scenario];
                    console.log('Set message:', this.currentMessage);
                    this.sendMessage();
                }
            }
        }
    </script>
</body>
</html>
    """)


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time chat."""
    await manager.connect(websocket, session_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data["type"] == "chat_message":
                # Send typing indicator
                await manager.send_personal_message({
                    "type": "typing_start"
                }, session_id)
                
                try:
                    # Process message through Jeff's workflow
                    result = await orchestrator.process_user_input(
                        user_input=message_data["message"],
                        session_id=session_id
                    )
                    
                    # Send response
                    await manager.send_personal_message({
                        "type": "chat_response",
                        "message": result.get("response", "I'm having trouble in the kitchen right now!"),
                        "metadata": result.get("metadata", {})
                    }, session_id)
                    
                except Exception as e:
                    await manager.send_personal_message({
                        "type": "error",
                        "message": f"Something went wrong: {str(e)}"
                    }, session_id)
                    
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)


@app.post("/api/chat")
async def chat_endpoint(message: ChatMessage):
    """REST API endpoint for chat (alternative to WebSocket)."""
    try:
        session_id = message.session_id or str(uuid.uuid4())
        
        result = await orchestrator.process_user_input(
            user_input=message.message,
            session_id=session_id
        )
        
        return JSONResponse({
            "success": True,
            "response": result.get("response", "I'm having trouble in the kitchen right now!"),
            "metadata": result.get("metadata", {}),
            "session_id": session_id
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/demo")
async def run_demo_scenario(demo: DemoRequest):
    """Run a predefined demo scenario."""
    scenarios = {
        "pasta": "Can you give me a romantic pasta recipe with tomatoes?",
        "tomato": "Tell me everything you love about tomatoes!",
        "romantic": "Write me a romantic cooking story about making dinner for someone special",
        "technique": "How do I properly sauté vegetables?",
        "risotto": "How do I make the perfect risotto?",
        "italian": "What are some classic Italian dishes with tomatoes?"
    }
    
    if demo.scenario not in scenarios:
        raise HTTPException(status_code=400, detail="Unknown demo scenario")
    
    try:
        session_id = f"demo_{demo.scenario}_{int(datetime.now().timestamp())}"
        
        result = await orchestrator.process_user_input(
            user_input=scenarios[demo.scenario],
            session_id=session_id
        )
        
        return JSONResponse({
            "success": True,
            "scenario": demo.scenario,
            "query": scenarios[demo.scenario],
            "response": result.get("response", "Demo failed!"),
            "metadata": result.get("metadata", {}),
            "session_id": session_id
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return JSONResponse({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Jeff the LangGraph Chef",
        "version": "1.0.0"
    })


@app.get("/api/personality/status")
async def get_personality_status():
    """Get current personality status."""
    return JSONResponse({
        "tomato_obsession_level": 9,
        "romantic_intensity": 8,
        "base_energy_level": 7,
        "current_mood": "enthusiastic",
        "personality_consistency_threshold": 0.90,
        "features_enabled": {
            "tomato_integration": True,
            "romantic_writing": True,
            "quality_gates": True,
            "memory_system": True
        }
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)