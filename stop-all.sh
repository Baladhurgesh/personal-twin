#!/bin/bash

# Stop all services

echo "🛑 Stopping Personal Digital Twin services..."
echo ""

# Stop using PID files if they exist
if [ -f ".backend.pid" ]; then
    BACKEND_PID=$(cat .backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        kill $BACKEND_PID
        echo "✅ Stopped backend (PID: $BACKEND_PID)"
    fi
    rm .backend.pid
fi

if [ -f ".frontend.pid" ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        kill $FRONTEND_PID
        echo "✅ Stopped frontend (PID: $FRONTEND_PID)"
    fi
    rm .frontend.pid
fi

# Force kill any remaining processes on ports
if lsof -ti:8000 > /dev/null 2>&1; then
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    echo "✅ Killed any remaining processes on port 8000"
fi

if lsof -ti:3000 > /dev/null 2>&1; then
    lsof -ti:3000 | xargs kill -9 2>/dev/null
    echo "✅ Killed any remaining processes on port 3000"
fi

echo ""
echo "✅ All services stopped"

