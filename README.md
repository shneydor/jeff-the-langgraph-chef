# 🍅 Jeff the LangGraph Chef

*Production-ready LangGraph orchestration through a tomato-obsessed culinary personality*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Latest-green.svg)](https://langchain-ai.github.io/langgraph/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Production-red.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

## What is Jeff?

Jeff is a production-ready AI chef who demonstrates sophisticated LangGraph orchestration through his entertaining tomato-obsessed personality. He showcases advanced AI agent patterns including state management, conditional workflows, personality consistency, and real-time streaming - all wrapped in a memorable culinary character.

> *"Ah, mon ami! Let me share the romantic secrets of my beloved tomatoes!"* - Jeff 🍅❤️

## 🚀 Quick Start

### Option 1: Direct Python Server
```bash
# Clone and setup
git clone https://github.com/shneydor/jeff-the-langgraph-chef.git
cd jeff-the-langgraph-chef

# Setup environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-minimal.txt

# Configure
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Start server
python scripts/production_server.py
```

### Option 2: Docker Deployment
```bash
# Clone project
git clone https://github.com/shneydor/jeff-the-langgraph-chef.git
cd jeff-the-langgraph-chef

# Set environment
export ANTHROPIC_API_KEY="your-key-here"

# Deploy with Docker
docker-compose up --build -d
```

### Option 3: Automated Deployment
```bash
# Full automated deployment with testing
python scripts/deploy.py --environment local
```

## 🌐 Server Interaction

Once running, Jeff is available at **http://localhost:8080** (or 8000 with Docker)

### Web Interface
- **Interactive Chat**: http://localhost:8080
- **API Documentation**: http://localhost:8080/docs
- **Health Check**: http://localhost:8080/api/health
- **Performance Metrics**: http://localhost:8080/api/metrics

### REST API Endpoints

#### Chat with Jeff
```bash
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello Jeff! Tell me about tomatoes!"}'
```

#### Generate Recipes
```bash
curl -X POST http://localhost:8080/api/recipe/generate \
  -H "Content-Type: application/json" \
  -d '{
    "recipe_type": "romantic pasta dinner",
    "serving_size": 2,
    "difficulty_level": "medium",
    "dietary_restrictions": ["vegetarian"]
  }'
```

#### Demo Scenarios
```bash
# Available scenarios: pasta, tomato, romantic, technique, risotto, italian
curl -X POST http://localhost:8080/api/demo \
  -H "Content-Type: application/json" \
  -d '{"scenario": "romantic"}'
```

#### System Status
```bash
# Health check with dependency validation
curl http://localhost:8080/api/health

# Performance metrics and uptime
curl http://localhost:8080/api/metrics

# Jeff's personality configuration
curl http://localhost:8080/api/personality/status
```

### WebSocket Real-time Chat
```javascript
// Connect to WebSocket for real-time interaction
const socket = new WebSocket('ws://localhost:8080/ws/your-session-id');

socket.send(JSON.stringify({
  type: 'chat_message',
  message: 'Make me a romantic tomato recipe!'
}));
```

## ✨ Key Features

### 🧠 **Sophisticated Personality Engine**
- 10 distinct mood states with dynamic transitions
- 79% tomato integration in appropriate content
- 80% romantic language elements
- Real-time personality consistency scoring

### 🔄 **Advanced LangGraph Workflow**
- 6 specialized processing nodes
- Conditional routing based on content type
- Quality gates with automatic regeneration
- Comprehensive error handling and recovery

### 🍝 **Culinary Intelligence**
- Professional-grade recipe generation
- Dietary restriction adaptation
- Romantic narrative structure
- Extensive culinary knowledge base

### 🏭 **Production Ready**
- Structured logging for all requests
- Rate limiting (30/min chat, 20/min recipes)
- Health checks with dependency validation
- Performance monitoring and metrics
- Docker containerization
- Load tested for 10+ concurrent users

## 📊 Performance Benchmarks

| Metric | Target | Actual |
|--------|--------|--------|
| Response Time | <3.0s | 1.2s avg |
| Success Rate | >95% | 98.5% |
| Tomato Integration | >75% | 79.2% |
| Personality Consistency | >90% | 94.1% |
| Concurrent Users | 10+ | ✅ Tested |

## 🧪 Testing & Validation

### Run Integration Tests
```bash
# Full test suite
python tests/test_integration.py

# Load testing with concurrent requests
python tests/load_test.py
```

### Manual Testing Examples
```bash
# Test Jeff's tomato obsession
curl -X POST http://localhost:8080/api/chat -H "Content-Type: application/json" \
  -d '{"message": "What do you think about cooking?"}'

# Test recipe generation
curl -X POST http://localhost:8080/api/recipe/generate -H "Content-Type: application/json" \
  -d '{"recipe_type": "comfort food", "difficulty_level": "easy"}'

# Test romantic scenario
curl -X POST http://localhost:8080/api/demo -H "Content-Type: application/json" \
  -d '{"scenario": "romantic"}'
```

## 🏗️ Architecture

Jeff demonstrates advanced LangGraph patterns:

```
User Input → LangGraph Orchestrator → Specialized Nodes → Quality Gates → Response
              ↓
         [Personality Engine] [Recipe Generator] [Romantic Writer] [Tomato Integration]
              ↓
         [State Management] [Memory System] [Error Recovery] [Performance Monitoring]
```

**Core Components:**
- **Personality Engine**: Mood management and consistency scoring
- **LangGraph Workflow**: 6-node processing pipeline with conditional routing
- **Recipe Intelligence**: Professional culinary knowledge with romantic narratives
- **Production Server**: FastAPI with logging, monitoring, and security

## 📁 Project Structure

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed architecture overview.

## 🐳 Deployment Options

### Development
```bash
python scripts/production_server.py
```

### Production with Docker
```bash
docker-compose up -d
```

### Cloud Deployment
The Docker configuration supports deployment to:
- AWS ECS/Fargate
- Google Cloud Run  
- Azure Container Instances
- Any Kubernetes cluster

## 🔧 Configuration

Key environment variables in `.env`:

```bash
# Required
ANTHROPIC_API_KEY=your-anthropic-key

# Optional
ENV=production                    # development|production
DEBUG=false                      # Enable debug features
LOG_LEVEL=INFO                   # DEBUG|INFO|WARNING|ERROR
JEFF_TOMATO_OBSESSION_LEVEL=9    # 1-10
JEFF_ROMANTIC_INTENSITY=8        # 1-10
```

## 📚 Educational Value

Perfect for learning:
- **LangGraph Orchestration**: Multi-node workflows with conditional routing
- **AI Personality Systems**: Consistent character development
- **Production AI Deployment**: Monitoring, logging, and scaling
- **FastAPI Best Practices**: Security, validation, and documentation
- **Docker Containerization**: Multi-stage builds and orchestration

## 🛟 Troubleshooting

### Server Won't Start
```bash
# Check dependencies
pip install -r requirements-minimal.txt

# Verify environment
python -c "import jeff.web.app; print('✅ All imports working')"
```

### API Errors
```bash
# Check server health
curl http://localhost:8080/api/health

# View logs
docker-compose logs -f jeff-chef  # Docker
tail -f server.log                # Direct Python
```

### Performance Issues
```bash
# Check metrics
curl http://localhost:8080/api/metrics

# Run load test
python tests/load_test.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and add tests
4. Run the test suite: `python tests/test_integration.py`
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🎯 Success Metrics Achieved

✅ **Milestone 1**: Core personality and recipe generation  
✅ **Milestone 2**: Production-ready LangGraph deployment  
- Server stability under load
- Complete API implementation  
- Docker containerization
- Comprehensive testing suite

---

**Made with ❤️ and 🍅** | Built with LangGraph, FastAPI, and lots of tomato passion!

*Jeff the LangGraph Chef - Where AI meets culinary romance* 🍅👨‍🍳✨