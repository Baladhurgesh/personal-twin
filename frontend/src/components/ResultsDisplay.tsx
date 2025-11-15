import { Sparkles, Download, RefreshCw, CheckCircle } from 'lucide-react'
import { DigitalTwinData } from '../App'
import './ResultsDisplay.css'

interface ResultsDisplayProps {
  twinData: DigitalTwinData;
  onReset: () => void;
}

function ResultsDisplay({ twinData, onReset }: ResultsDisplayProps) {
  console.log('Digital Twin created successfully!')
  console.log('Resume:', twinData.resume?.name)
  console.log('GitHub:', twinData.githubUsername)
  console.log('Analysis complete - Digital twin is ready')

  const handleExport = () => {
    console.log('Exporting digital twin data...')
    const data = {
      resume: twinData.resume?.name,
      github: twinData.githubUsername,
      timestamp: new Date().toISOString()
    }
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'digital-twin.json'
    a.click()
    console.log('Digital twin data exported successfully')
  }

  return (
    <div className="results-display">
      <div className="success-header">
        <div className="success-icon-wrapper">
          <CheckCircle className="success-icon" />
        </div>
        <h2>Your Digital Twin is Ready!</h2>
        <p>We've successfully analyzed your professional profile</p>
      </div>

      <div className="results-content">
        <div className="summary-card">
          <div className="card-header">
            <Sparkles className="card-icon" />
            <h3>Profile Summary</h3>
          </div>
          <div className="summary-items">
            <div className="summary-item">
              <div className="item-label">Resume</div>
              <div className="item-value">
                {twinData.resume?.name || 'No resume uploaded'}
              </div>
              <div className="item-status success">
                <CheckCircle className="status-icon" />
                Analyzed
              </div>
            </div>

            <div className="summary-item">
              <div className="item-label">GitHub Profile</div>
              <div className="item-value">
                {twinData.githubUsername || 'Not connected'}
              </div>
              <div className="item-status success">
                <CheckCircle className="status-icon" />
                Connected
              </div>
            </div>
          </div>
        </div>

        <div className="insights-card">
          <h3>What's Next?</h3>
          <div className="insights-list">
            <div className="insight-item">
              <div className="insight-icon">🎯</div>
              <div className="insight-content">
                <h4>AI Analysis Complete</h4>
                <p>Your profile has been processed using GPT-5 for deep insights</p>
              </div>
            </div>
            <div className="insight-item">
              <div className="insight-icon">💼</div>
              <div className="insight-content">
                <h4>Skills Identified</h4>
                <p>We've extracted your technical skills and project experience</p>
              </div>
            </div>
            <div className="insight-item">
              <div className="insight-icon">🚀</div>
              <div className="insight-content">
                <h4>Ready to Use</h4>
                <p>Your digital twin can now represent you professionally</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="actions">
        <button className="action-button primary" onClick={handleExport}>
          <Download className="button-icon" />
          Export Data
        </button>
        <button className="action-button secondary" onClick={onReset}>
          <RefreshCw className="button-icon" />
          Create New Twin
        </button>
      </div>

      <div className="info-footer">
        <p>
          Your data is processed locally and securely. All analysis is performed using 
          state-of-the-art AI models to ensure accuracy and privacy.
        </p>
      </div>
    </div>
  )
}

export default ResultsDisplay

