#!/bin/bash

# 🚀 Essay Scoring System - Setup Script
# Author: Sardar Ahmed
# Description: Automated setup for the AI-Powered Essay Scoring System

echo "🚀 Setting up AI-Powered Essay Scoring System..."
echo "================================================"

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

echo "✅ Python found: $(python --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv .venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

# Upgrade pip
echo "⬆️ Upgrading pip..."
python -m pip install --upgrade pip

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "🎉 Setup completed successfully!"
echo "================================================"
echo ""
echo "🚀 To start the application:"
echo "   Windows: .\\run_optimized_server.bat"
echo "   Linux/Mac: python site_optimized.py"
echo ""
echo "🌐 Then open: http://127.0.0.1:5000"
echo ""
echo "✨ Enjoy your AI-Powered Essay Scoring System!"
echo "================================================"
