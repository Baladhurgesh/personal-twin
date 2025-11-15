import { useState } from 'react'
import { Github, ExternalLink, Loader } from 'lucide-react'
import './GitHubConnect.css'

interface GitHubConnectProps {
  onConnect: (username: string) => void;
  isProcessing: boolean;
}

function GitHubConnect({ onConnect, isProcessing }: GitHubConnectProps) {
  const [username, setUsername] = useState('')
  const [error, setError] = useState('')

  const validateUsername = (value: string): boolean => {
    if (!value.trim()) {
      setError('Please enter a GitHub username')
      return false
    }

    // GitHub username validation
    const usernameRegex = /^[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}$/i
    if (!usernameRegex.test(value)) {
      setError('Please enter a valid GitHub username')
      return false
    }

    setError('')
    return true
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (validateUsername(username)) {
      console.log('Connecting GitHub account:', username)
      console.log('Starting comprehensive repository analysis...')
      console.log('This will:')
      console.log('  1. Fetch all public repositories')
      console.log('  2. Download README files')
      console.log('  3. Generate AI-powered project summaries')
      console.log('  4. Save individual text files for each project')
      console.log('Please wait, this may take a few minutes...')
      onConnect(username)
    }
  }

  const handleUsernameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUsername(e.target.value)
    if (error) {
      setError('')
    }
  }

  return (
    <div className="github-connect">
      <form onSubmit={handleSubmit} className="github-form">
        <div className="input-group">
          <div className="input-wrapper">
            <Github className="input-icon" />
            <input
              type="text"
              value={username}
              onChange={handleUsernameChange}
              placeholder="Enter your GitHub username"
              className={`github-input ${error ? 'error' : ''}`}
              disabled={isProcessing}
            />
          </div>
          
          {error && (
            <p className="input-error">{error}</p>
          )}

          <div className="input-help">
            <p>
              Don't know your username? 
              <a 
                href="https://github.com" 
                target="_blank" 
                rel="noopener noreferrer"
                className="help-link"
              >
                Visit GitHub
                <ExternalLink className="link-icon" />
              </a>
            </p>
          </div>
        </div>

        <button 
          type="submit" 
          className="connect-button"
          disabled={isProcessing || !username.trim()}
        >
          {isProcessing ? (
            <>
              <Loader className="spinner" />
              Processing...
            </>
          ) : (
            <>
              <Github className="button-icon" />
              Connect GitHub
            </>
          )}
        </button>
      </form>

      <div className="info-cards">
        <div className="info-card">
          <div className="info-icon">📊</div>
          <h4>Repository Analysis</h4>
          <p>We'll analyze your public repositories and contributions</p>
        </div>
        <div className="info-card">
          <div className="info-icon">💡</div>
          <h4>Skills Detection</h4>
          <p>Automatically detect your programming languages and tech stack</p>
        </div>
        <div className="info-card">
          <div className="info-icon">🔒</div>
          <h4>Privacy First</h4>
          <p>We only access publicly available information</p>
        </div>
      </div>
    </div>
  )
}

export default GitHubConnect

