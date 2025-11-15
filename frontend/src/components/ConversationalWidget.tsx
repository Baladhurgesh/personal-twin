import { useEffect, useState } from 'react'
import { MessageCircle } from 'lucide-react'
import { getElevenLabsConfig } from '../utils/api'
import './ConversationalWidget.css'

// Declare the custom element for TypeScript
declare global {
  namespace JSX {
    interface IntrinsicElements {
      'elevenlabs-convai': React.DetailedHTMLProps<
        React.HTMLAttributes<HTMLElement> & {
          'agent-id'?: string;
          'avatar-orb-color-1'?: string;
          'avatar-orb-color-2'?: string;
        },
        HTMLElement
      >;
    }
  }
}

interface ConversationalWidgetProps {
  username?: string;
}

function ConversationalWidget({ username }: ConversationalWidgetProps) {
  const [agentId, setAgentId] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchAgentConfig = async () => {
      try {
        setIsLoading(true)
        const response = await getElevenLabsConfig()
        
        if (response.success && response.data.configured) {
          setAgentId(response.data.agentId)
          console.log('[ConversationalWidget] Agent ID loaded:', response.data.agentId)
        } else {
          setError('ElevenLabs agent not configured')
          console.warn('[ConversationalWidget] Agent not configured')
        }
      } catch (err) {
        console.error('[ConversationalWidget] Failed to load agent config:', err)
        setError('Failed to load conversational AI')
      } finally {
        setIsLoading(false)
      }
    }

    fetchAgentConfig()
  }, [])

  if (isLoading) {
    return (
      <div className="conversational-widget-container">
        <div className="widget-card loading">
          <div className="loading-spinner"></div>
          <p>Loading conversational AI...</p>
        </div>
      </div>
    )
  }

  if (error || !agentId) {
    return (
      <div className="conversational-widget-container">
        <div className="widget-card error">
          <MessageCircle className="widget-icon" />
          <h3>Conversational AI Unavailable</h3>
          <p>{error || 'Agent not configured'}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="conversational-widget-container">
      <div className="widget-card">
        <div className="widget-header">
          <MessageCircle className="widget-icon" />
          <div className="widget-header-content">
            <h3>Talk to Your Digital Twin</h3>
            <p>Chat with an AI agent trained on your professional profile</p>
          </div>
        </div>

        <div className="widget-description">
          <div className="feature-list">
            <div className="feature-item">
              <span className="feature-icon">🎯</span>
              <span>Answers questions about your experience</span>
            </div>
            <div className="feature-item">
              <span className="feature-icon">💼</span>
              <span>Discusses your projects and skills</span>
            </div>
            <div className="feature-item">
              <span className="feature-icon">🗣️</span>
              <span>Voice and text conversation supported</span>
            </div>
          </div>
        </div>

        <div className="widget-embed">
          <elevenlabs-convai
            agent-id={agentId}
            avatar-orb-color-1="#6DB035"
            avatar-orb-color-2="#F5CABB"
          />
        </div>

        <div className="widget-footer">
          <p className="widget-note">
            💡 Click the button below to start a conversation with your AI twin
          </p>
        </div>
      </div>
    </div>
  )
}

export default ConversationalWidget

