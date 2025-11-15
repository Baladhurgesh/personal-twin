import { useState } from 'react'
import './App.css'
import ResumeUpload from './components/ResumeUpload'
import GitHubConnect from './components/GitHubConnect'
import ProgressTracker from './components/ProgressTracker'
import ResultsDisplay from './components/ResultsDisplay'
import { analyzeGitHub, uploadResume } from './utils/api'
import { User, Sparkles } from 'lucide-react'

export interface DigitalTwinData {
  resume?: File;
  resumeAnalysis?: any;
  githubUsername?: string;
  githubData?: any;
  analysis?: any;
}

function App() {
  const [step, setStep] = useState<number>(1)
  const [twinData, setTwinData] = useState<DigitalTwinData>({})
  const [isProcessing, setIsProcessing] = useState(false)

  const handleResumeUpload = async (file: File) => {
    console.log('Resume uploaded:', file.name)
    setTwinData(prev => ({ ...prev, resume: file }))
    
    // Note: We'll upload to backend when we have the GitHub username
    // This ensures both are associated with the same user
    setStep(2)
  }

  const handleGitHubConnect = async (username: string) => {
    console.log('GitHub username provided:', username)
    console.log('═══════════════════════════════════════════════════════════')
    console.log('STARTING ANALYSIS')
    console.log('═══════════════════════════════════════════════════════════')
    setIsProcessing(true)
    setTwinData(prev => ({ ...prev, githubUsername: username }))
    
    try {
      // First, upload resume if available
      if (twinData.resume) {
        console.log('Step 1: Uploading resume to backend and ElevenLabs KB...')
        try {
          const resumeResult = await uploadResume(twinData.resume, username)
          console.log('✓ Resume uploaded successfully')
          setTwinData(prev => ({ ...prev, resumeAnalysis: resumeResult.data }))
        } catch (error) {
          console.error('⚠ Resume upload failed (continuing with GitHub analysis):', error)
        }
      }
      
      console.log('Step 2: Analyzing GitHub profile...')
      console.log('The enhanced scraper will:')
      console.log('  ✓ Scrape all public repositories')
      console.log('  ✓ Download README files')
      console.log('  ✓ Generate AI summaries using GPT-4o')
      console.log('  ✓ Upload to ElevenLabs Knowledge Base')
      console.log('  ✓ Save individual text files')
      console.log('  ✓ Create consolidated JSON data')
      console.log('')
      console.log('Please wait... This may take several minutes.')
      console.log('═══════════════════════════════════════════════════════════')
      
      // Actually call the backend API to run the scraper
      const result = await analyzeGitHub(username)
      
      if (result.success) {
        console.log('═══════════════════════════════════════════════════════════')
        console.log('ANALYSIS COMPLETE')
        console.log('═══════════════════════════════════════════════════════════')
        console.log('✓ All repositories scraped')
        console.log('✓ README files collected')
        console.log('✓ AI summaries generated')
        console.log('✓ Uploaded to ElevenLabs Knowledge Base')
        console.log('✓ Text files saved to project_summaries/' + username)
        console.log('✓ JSON data created')
        
        if (result.data) {
          console.log('\n📊 Statistics:')
          console.log(`   Total repositories: ${result.data.repositories || 'N/A'}`)
          console.log(`   Summary files created: ${result.data.topProjects?.length || 'N/A'}`)
          console.log(`   Uploaded to KB: ${result.data.kb_uploaded || 'N/A'}`)
          console.log(`   Output directory: project_summaries/${username}`)
        }
        
        console.log('═══════════════════════════════════════════════════════════')
        
        // Store the GitHub data
        setTwinData(prev => ({ 
          ...prev, 
          githubUsername: username,
          githubData: result.data 
        }))
        
        setIsProcessing(false)
        setStep(3)
      } else {
        throw new Error(result.message || 'GitHub analysis failed')
      }
    } catch (error: any) {
      console.error('═══════════════════════════════════════════════════════════')
      console.error('❌ GITHUB ANALYSIS FAILED')
      console.error('═══════════════════════════════════════════════════════════')
      console.error('Error:', error.message || error)
      console.error('')
      console.error('Possible issues:')
      console.error('  - Backend server not running (start with: python3 backend_api.py)')
      console.error('  - API keys not configured in .env file')
      console.error('  - GitHub username not found')
      console.error('  - Network connectivity issues')
      console.error('═══════════════════════════════════════════════════════════')
      
      setIsProcessing(false)
      alert(`GitHub analysis failed: ${error.message || error}`)
    }
  }

  const handleReset = () => {
    setStep(1)
    setTwinData({})
    setIsProcessing(false)
  }

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <Sparkles className="logo-icon" />
            <h1>Personal Digital Twin</h1>
          </div>
          <p className="tagline">Create your AI-powered professional profile</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        <div className="container">
          {/* Progress Tracker */}
          <ProgressTracker currentStep={step} />

          {/* Content Area */}
          <div className="content-area">
            {step === 1 && (
              <div className="step-container">
                <div className="step-header">
                  <User className="step-icon" />
                  <h2>Upload Your Resume</h2>
                  <p>Start by uploading your resume to analyze your professional experience</p>
                </div>
                <ResumeUpload onUpload={handleResumeUpload} />
              </div>
            )}

            {step === 2 && (
              <div className="step-container">
                <div className="step-header">
                  <svg className="step-icon" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                  </svg>
                  <h2>Connect GitHub</h2>
                  <p>Link your GitHub profile to analyze your coding projects and contributions</p>
                </div>
                <GitHubConnect 
                  onConnect={handleGitHubConnect} 
                  isProcessing={isProcessing}
                />
              </div>
            )}

            {step === 3 && (
              <div className="step-container">
                <ResultsDisplay 
                  twinData={twinData} 
                  onReset={handleReset}
                />
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="footer">
        <p>Built with React + TypeScript • Powered by GPT-5</p>
      </footer>
    </div>
  )
}

export default App

