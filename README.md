# Personal Digital Twin

Create your AI-powered professional digital twin by combining your resume and GitHub profile analysis using GPT-5.

## 🚀 Project Overview

This project consists of two main parts:

1. **Backend (Python)**: Scrapes and analyzes data from resumes and GitHub profiles
2. **Frontend (TypeScript/React)**: Beautiful, modern UI for creating your digital twin

## ✨ Features

### Frontend UI
- 📄 **Resume Upload**: Drag-and-drop interface for PDF, DOC, DOCX files
- 🔗 **GitHub Integration**: Connect your GitHub profile seamlessly
- 🎨 **Modern Design**: Beautiful, responsive UI with smooth animations
- 📊 **Progress Tracking**: Visual progress through the creation process
- 💾 **Data Export**: Download your digital twin data as JSON
- 🤖 **AI-Powered Analysis**: Uses GPT-5 for deep insights

### Backend Analysis
- Resume parsing and skill extraction
- GitHub repository analysis with README collection
- **AI-Powered Project Summaries** using OpenRouter GPT-4o
- **ElevenLabs Knowledge Base Integration** - Automatically uploads:
  - All project summaries (text files)
  - Resume PDFs
  - Configurable agent updates
- Contribution history tracking
- Programming language detection
- Project insights and recommendations
- Individual text files for each project

## 📋 Prerequisites

- **Python 3.8+** with pip
- **Node.js 18+** with npm
- GitHub Personal Access Token (optional, for higher rate limits)
- OpenRouter API Key (for GPT-4o analysis)
- ElevenLabs API Key (for knowledge base integration)

## 🛠️ Installation

### 1. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Configure environment variables
# Create a .env file in the project root with:
# - GITHUB_TOKEN (get from: https://github.com/settings/tokens)
# - OPENROUTER_API_KEY (get from: https://openrouter.ai/keys)
# - ELEVENLABS_API_KEY (get from: https://elevenlabs.io/app/settings/api-keys)
# - ELEVENLABS_AGENT_ID (optional, from ElevenLabs dashboard)
```

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env if needed (API URL, etc.)
```

## 🚀 Running the Application

### Enhanced GitHub Scraper (NEW!)

Scrape all repositories with AI-powered project summaries:

```bash
# Quick start (interactive)
./run_github_scraper.sh

# Or directly
python github_scraper_enhanced.py USERNAME
```

This will:
- ✅ Fetch all repositories with README files
- ✅ Generate AI summaries using GPT-4o
- ✅ Save individual text files for each project
- ✅ Create consolidated JSON data

See [GITHUB_SCRAPER_GUIDE.md](GITHUB_SCRAPER_GUIDE.md) for detailed documentation.

### Other Backend Scripts

```bash
# Original GitHub scraper
python github_scraper_full.py USERNAME

# Resume analysis
python analyze_resume_gpt5.py

# Project analysis
python analyze_projects_gpt5.py
```

### Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

The application will be available at `http://localhost:3000`

## 📁 Project Structure

```
personal-twin/
├── frontend/                    # React TypeScript UI
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── utils/             # API utilities
│   │   ├── App.tsx            # Main app
│   │   └── ...
│   ├── package.json
│   └── README.md
│
├── data/                       # Analyzed data
│   ├── github_baladhurgesh_full.json
│   └── github_baladhurgesh_full_gpt5_analysis.json
│
├── analyze_resume_gpt5.py      # Resume analysis
├── analyze_projects_gpt5.py    # GitHub analysis
├── github_scraper_full.py      # GitHub data scraper
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🎯 Usage

1. **Open the application** at `http://localhost:3000`
2. **Upload your resume** using the drag-and-drop interface
3. **Connect your GitHub** by entering your username
4. **Wait for analysis** - GPT-5 will analyze your data
5. **View your digital twin** and export the results

## 🔧 Configuration

### Backend (.env)
```env
# GitHub API (for repository scraping)
GITHUB_TOKEN=your_github_personal_access_token

# OpenRouter API (for AI analysis - GPT-4o)
OPENROUTER_API_KEY=your_openrouter_api_key

# ElevenLabs Knowledge Base Integration
ELEVENLABS_API_KEY=your_elevenlabs_api_key
ELEVENLABS_AGENT_ID=your_agent_id_here  # Optional: for agent updates
```

#### Getting API Keys:
- **GitHub Token**: https://github.com/settings/tokens (select `repo` scope)
- **OpenRouter Key**: https://openrouter.ai/keys
- **ElevenLabs Key**: https://elevenlabs.io/app/settings/api-keys
- **ElevenLabs Agent ID**: Find in your ElevenLabs agent dashboard (optional)

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000/api
```

## 📊 Data Flow

1. User uploads resume → Frontend validates and prepares file
2. User enters GitHub username → Frontend sends to backend
3. Backend scrapes GitHub data → Saves to JSON
4. Backend analyzes with GPT-4o → Generates insights
5. **Backend uploads to ElevenLabs** → Adds to knowledge base
6. Frontend displays results → User can export

### ElevenLabs Integration Flow

When GitHub analysis completes:
1. All project summary `.txt` files are uploaded to ElevenLabs knowledge base
2. Each file is tagged as "GitHub Project: [project-name]"
3. If `ELEVENLABS_AGENT_ID` is configured, the agent is automatically updated

When resume is uploaded:
1. Resume PDF/DOCX is saved locally
2. File is uploaded to ElevenLabs knowledge base
3. Tagged as "Resume: [username]"
4. If `ELEVENLABS_AGENT_ID` is configured, the agent is automatically updated

## 🎨 UI Screenshots

The UI includes:
- **Step 1**: Resume upload with drag-and-drop
- **Step 2**: GitHub connection form
- **Step 3**: Results display with insights

All screens feature:
- Modern dark theme with gradient accents
- Smooth animations and transitions
- Responsive design for all devices
- Real-time progress tracking
- Comprehensive logging to console

## 🧪 Development

### Frontend Development
```bash
cd frontend
npm run dev      # Start dev server
npm run build    # Build for production
npm run preview  # Preview production build
```

### Backend Development
- Scripts log all operations to console
- Data is saved to `data/` directory
- Uses GPT-5 for all analysis tasks

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

MIT License - feel free to use this project for your own digital twin!

## 🙏 Acknowledgments

- Built with React, TypeScript, and Python
- Powered by OpenAI GPT-5
- Uses GitHub API for data collection
- Icons by Lucide React

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

**Built with ❤️ using React + TypeScript + Python + GPT-5**
