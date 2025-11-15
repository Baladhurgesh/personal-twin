import { CheckCircle } from 'lucide-react'
import './ProgressTracker.css'

interface ProgressTrackerProps {
  currentStep: number;
}

interface Step {
  number: number;
  title: string;
  description: string;
}

const steps: Step[] = [
  {
    number: 1,
    title: 'Resume',
    description: 'Upload your resume'
  },
  {
    number: 2,
    title: 'GitHub',
    description: 'Connect account'
  },
  {
    number: 3,
    title: 'Complete',
    description: 'View your twin'
  }
]

function ProgressTracker({ currentStep }: ProgressTrackerProps) {
  return (
    <div className="progress-tracker">
      <div className="progress-steps">
        {steps.map((step, index) => (
          <div key={step.number} className="step-wrapper">
            <div 
              className={`step ${currentStep >= step.number ? 'active' : ''} ${currentStep > step.number ? 'completed' : ''}`}
            >
              <div className="step-indicator">
                {currentStep > step.number ? (
                  <CheckCircle className="check-icon" />
                ) : (
                  <span className="step-number">{step.number}</span>
                )}
              </div>
              <div className="step-info">
                <h3 className="step-title">{step.title}</h3>
                <p className="step-description">{step.description}</p>
              </div>
            </div>
            
            {index < steps.length - 1 && (
              <div className={`step-connector ${currentStep > step.number ? 'completed' : ''}`} />
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default ProgressTracker

