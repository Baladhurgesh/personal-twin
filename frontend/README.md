# Personal Digital Twin - Frontend

A modern, beautiful TypeScript React application for creating your professional digital twin by uploading your resume and connecting your GitHub profile.

## Features

- 📄 **Resume Upload**: Drag-and-drop or browse to upload your resume (PDF, DOC, DOCX)
- 🔗 **GitHub Integration**: Connect your GitHub profile to analyze repositories and contributions
- 🎨 **Modern UI**: Beautiful, responsive design with smooth animations
- 📊 **Progress Tracking**: Visual progress indicator through the creation process
- 💾 **Data Export**: Export your digital twin data as JSON
- 🔒 **Privacy First**: All data processing with security in mind
- 🤖 **AI-Powered**: Uses GPT-5 for intelligent analysis and insights

## Tech Stack

- **React 18** - Modern React with hooks
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and dev server
- **Axios** - HTTP client for API calls
- **Lucide React** - Beautiful icon library
- **CSS3** - Custom styling with modern features

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create environment file:
```bash
cp .env.example .env
```

3. Update `.env` with your API configuration:
```env
VITE_API_URL=http://localhost:8000/api
```

### Development

Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### Build

Build for production:

```bash
npm run build
```

Preview production build:

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── ResumeUpload.tsx       # Resume upload with drag-and-drop
│   │   ├── GitHubConnect.tsx      # GitHub integration
│   │   ├── ProgressTracker.tsx    # Progress indicator
│   │   └── ResultsDisplay.tsx     # Results and export
│   ├── utils/
│   │   └── api.ts          # API client and utilities
│   ├── App.tsx             # Main application component
│   ├── App.css             # Application styles
│   ├── main.tsx            # Application entry point
│   └── index.css           # Global styles
├── public/                 # Static assets
├── index.html             # HTML template
├── package.json           # Dependencies and scripts
├── tsconfig.json          # TypeScript configuration
├── vite.config.ts         # Vite configuration
└── README.md              # This file
```

## Features in Detail

### Resume Upload
- Drag-and-drop interface
- File validation (PDF, DOC, DOCX, max 10MB)
- Visual feedback and preview
- Error handling

### GitHub Connection
- Username validation
- Real-time processing feedback
- Repository and contribution analysis
- Skills detection from code

### Results Display
- Summary of analyzed data
- Export functionality
- Option to create new twin
- Beautiful visualization of insights

## API Integration

The frontend communicates with a backend API for:
- Resume analysis
- GitHub data fetching and analysis
- Digital twin creation and storage

All API calls are logged to the console for transparency and debugging.

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT

