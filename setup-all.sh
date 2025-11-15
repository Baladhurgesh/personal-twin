#!/bin/bash

# Personal Digital Twin - Complete Setup and Run Script

echo "════════════════════════════════════════════════════════════════"
echo "  PERSONAL DIGITAL TWIN - COMPLETE SETUP"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi
echo "✅ Python: $(python3 --version)"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    exit 1
fi
echo "✅ Node.js: $(node --version)"
echo ""

# Setup Backend
echo "──────────────────────────────────────────────────────────────"
echo "  BACKEND SETUP"
echo "──────────────────────────────────────────────────────────────"

# Check .env file
if [ ! -f ".env" ]; then
    echo "⚠️  Creating .env file from template..."
    cp env.example .env
    echo "✅ Created .env file"
    echo ""
    echo "📝 IMPORTANT: Edit .env and add your API keys:"
    echo "   - GITHUB_TOKEN (from: https://github.com/settings/tokens)"
    echo "   - OPENROUTER_API_KEY (from: https://openrouter.ai/keys)"
    echo ""
    read -p "Press Enter after you've added your API keys..."
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Python dependencies installed"
else
    echo "⚠️  Some Python packages may have issues, continuing..."
fi
echo ""

# Setup Frontend
echo "──────────────────────────────────────────────────────────────"
echo "  FRONTEND SETUP"
echo "──────────────────────────────────────────────────────────────"

cd frontend

if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install frontend dependencies"
        exit 1
    fi
    echo "✅ Node.js dependencies installed"
else
    echo "✅ Node.js dependencies already installed"
fi

if [ ! -f ".env" ]; then
    echo "⚙️  Creating frontend .env..."
    cp .env.example .env
    echo "✅ Frontend .env created"
fi

cd ..
echo ""

# Summary
echo "════════════════════════════════════════════════════════════════"
echo "  SETUP COMPLETE!"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "🚀 To start the application:"
echo ""
echo "   Terminal 1 (Backend):"
echo "   $ python3 backend_api.py"
echo ""
echo "   Terminal 2 (Frontend):"
echo "   $ cd frontend && npm run dev"
echo ""
echo "Then open: http://localhost:3000"
echo ""
echo "════════════════════════════════════════════════════════════════"

