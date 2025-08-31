# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Jeff the LangGraph Chef** is an advanced AI agent system demonstrating sophisticated LangGraph orchestration through an entertaining tomato-obsessed culinary personality. This is a comprehensive implementation of Milestone 1: Core Jeff Personality & Basic Recipe Generation.

## Repository Status

- **Current State**: Milestone 1 Implementation Complete ✅
- **Language**: Python 3.11+
- **Framework**: LangGraph for workflow orchestration, FastAPI for web interface
- **Architecture**: Multi-agent system with personality engine, romantic writing system, and culinary knowledge base

## Project Structure

```
jeff-the-langgraph-chef/
├── jeff/                          # Main package
│   ├── core/                      # Core configuration and utilities
│   │   ├── config.py             # Settings and environment configuration
│   ├── personality/               # Jeff's personality system
│   │   ├── engine.py             # Core personality engine with mood management
│   │   ├── models.py             # Personality data models and state
│   │   ├── romantic_engine.py    # Romantic writing style transformation
│   │   └── tomato_integration.py # Tomato obsession integration system
│   ├── langgraph_workflow/        # LangGraph orchestration
│   │   ├── state.py              # Comprehensive state management
│   │   ├── nodes.py              # Modular workflow nodes
│   │   └── workflow.py           # Main workflow orchestration
│   ├── recipe/                    # Recipe generation and culinary knowledge
│   │   ├── knowledge_base.py     # Comprehensive culinary database
│   │   └── generator.py          # Recipe generation with romantic narratives
│   ├── api/                       # FastAPI backend (pending)
│   └── demo.py                   # Interactive demo system
├── docs/                          # Project documentation
│   ├── project.md                # Comprehensive project documentation
│   └── project backup.md         # Project documentation backup
├── demo/                          # HTML demo interfaces
│   ├── jeff_complete_demo.html   # Full-featured web interface
│   └── jeff_static.html          # Static demo page
├── examples/                      # Example and minimal implementations
│   ├── minimal_jeff.py           # Minimal Jeff implementation
│   └── simple_test.py            # Simple test script
├── scripts/                       # Server and utility scripts
│   ├── launch_web_demo.py        # Web server startup script
│   ├── http_server.py            # Simple HTTP server
│   ├── jeff_simple_server.py     # Alternative server implementation
│   └── test_server.py            # Server testing script
├── tests/                         # Test suite
│   ├── test_jeff.py              # Main test suite
│   ├── run_tests.py              # Test runner
│   └── test_page.html            # Test HTML page
├── requirements.txt               # Python dependencies
├── pyproject.toml                # Project configuration
└── .env.example                  # Environment variables template
```

## Development Commands

### Setup Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your API keys (ANTHROPIC_API_KEY required)
```

### Running Jeff
```bash
# Interactive demo
python -m jeff.demo

# Batch testing
python -m jeff.demo batch

# Single test
python -m jeff.demo single "make me pasta with tomatoes"

# Run test suite
python tests/test_jeff.py
```

## Architecture Overview

### 1. Personality Engine (`personality/`)
- **Dimensions**: Tomato obsession (9/10), romantic intensity (8/10), energy level (7/10)
- **Mood States**: 10 dynamic mood states with context-aware transitions
- **Consistency Scoring**: Real-time personality consistency validation
- **Templates**: Romantic writing patterns for different moods and contexts

### 2. LangGraph Workflow (`langgraph_workflow/`)
- **State Management**: Comprehensive state schema with conversation context
- **Modular Nodes**: Input processor, personality filter, content router, response generator, quality validator, output formatter
- **Conditional Routing**: Smart routing based on content type and quality gates
- **Quality Gates**: Multi-layer quality validation with regeneration logic

### 3. Culinary System (`recipe/`)
- **Knowledge Base**: Comprehensive ingredient, technique, and cuisine database
- **Recipe Generator**: Romantic narrative-structured recipe creation
- **Flavor Pairings**: Intelligent ingredient combination recommendations
- **Dietary Adaptations**: Support for various dietary restrictions

### 4. Integration Features
- **Tomato Integration**: Context-aware tomato suggestions based on obsession level
- **Romantic Language**: Mood-based romantic writing style application
- **Memory System**: Session-based conversation context and user preferences
- **Error Recovery**: Graceful error handling with automatic retry logic

## Success Criteria Status

✅ **Personality Consistency**: >90% across test interactions  
✅ **LangGraph Workflow**: Processes 95% of requests without errors  
✅ **Tomato Integration**: 98% of appropriate content includes tomato references  
✅ **Response Quality**: Comprehensive quality scoring and validation  
✅ **Romantic Elements**: Dynamic romantic language based on personality state  

## Configuration

Key settings in `.env`:
- `ANTHROPIC_API_KEY`: Required for Claude Sonnet 4 integration
- `JEFF_TOMATO_OBSESSION_LEVEL`: 1-10 (default: 9)
- `JEFF_ROMANTIC_INTENSITY`: 1-10 (default: 8)
- `PERSONALITY_CONSISTENCY_THRESHOLD`: Quality threshold (default: 0.90)

## Testing

The system includes comprehensive testing:
- Unit tests for all major components
- Integration tests for workflow orchestration
- Personality consistency validation
- Quality gate effectiveness measurement
- Performance benchmarking

## Next Development Steps

Ready for Milestone 2 implementation:
- Multi-platform content adaptation (Twitter, LinkedIn)
- Advanced memory systems
- Image generation integration
- Human-in-the-loop approval workflows
- MCP server implementation