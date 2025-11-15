#!/bin/bash

# Start both backend and frontend in separate terminal windows/tabs

echo "🚀 Starting Personal Digital Twin..."
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ No .env file found! Run ./setup-all.sh first"
    exit 1
fi

# Function to check if port is in use
check_port() {
    lsof -i:$1 > /dev/null 2>&1
    return $?
}

# Check if backend is already running
if check_port 8000; then
    echo "⚠️  Port 8000 is already in use (backend may be running)"
    read -p "Kill existing process? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        lsof -ti:8000 | xargs kill -9
        echo "✅ Killed process on port 8000"
    fi
fi

# Check if frontend is already running
if check_port 3000; then
    echo "⚠️  Port 3000 is already in use (frontend may be running)"
    read -p "Kill existing process? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        lsof -ti:3000 | xargs kill -9
        echo "✅ Killed process on port 3000"
    fi
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  Starting Backend API on port 8000..."
echo "════════════════════════════════════════════════════════════════"

# Start backend in background
python3 backend_api.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID)"
echo "   Log file: backend.log"

# Wait a bit for backend to start
sleep 3

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  Starting Frontend on port 3000..."
echo "════════════════════════════════════════════════════════════════"

# Start frontend in background
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo "✅ Frontend started (PID: $FRONTEND_PID)"
echo "   Log file: frontend.log"

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  🎉 PERSONAL DIGITAL TWIN IS RUNNING!"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "  🌐 Frontend: http://localhost:3000"
echo "  🔧 Backend:  http://localhost:8000"
echo ""
echo "  📋 Backend PID:  $BACKEND_PID"
echo "  📋 Frontend PID: $FRONTEND_PID"
echo ""
echo "  📝 Logs:"
echo "     Backend:  tail -f backend.log"
echo "     Frontend: tail -f frontend.log"
echo ""
echo "  🛑 To stop:"
echo "     kill $BACKEND_PID $FRONTEND_PID"
echo "     or run: ./stop-all.sh"
echo ""
echo "════════════════════════════════════════════════════════════════"

# Save PIDs to file for stop script
echo "$BACKEND_PID" > .backend.pid
echo "$FRONTEND_PID" > .frontend.pid

# Wait for user interrupt
echo ""
echo "Press Ctrl+C to stop all services..."
echo ""

# Trap Ctrl+C
trap 'echo ""; echo "Stopping services..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; rm -f .backend.pid .frontend.pid; echo "✅ Stopped"; exit 0' INT

# Wait indefinitely
wait

