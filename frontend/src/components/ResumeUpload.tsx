import { useState, useRef } from 'react'
import { Upload, FileText, CheckCircle, X } from 'lucide-react'
import './ResumeUpload.css'

interface ResumeUploadProps {
  onUpload: (file: File) => void;
}

function ResumeUpload({ onUpload }: ResumeUploadProps) {
  const [isDragging, setIsDragging] = useState(false)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [error, setError] = useState<string>('')
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const validateFile = (file: File): boolean => {
    const validTypes = ['application/pdf', 'application/msword', 
                        'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
    const maxSize = 10 * 1024 * 1024 // 10MB

    if (!validTypes.includes(file.type)) {
      setError('Please upload a PDF or Word document')
      return false
    }

    if (file.size > maxSize) {
      setError('File size must be less than 10MB')
      return false
    }

    setError('')
    return true
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)

    const files = e.dataTransfer.files
    if (files.length > 0) {
      const file = files[0]
      if (validateFile(file)) {
        setSelectedFile(file)
        console.log('Resume file dropped:', file.name, 'Size:', (file.size / 1024).toFixed(2) + 'KB')
      }
    }
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files && files.length > 0) {
      const file = files[0]
      if (validateFile(file)) {
        setSelectedFile(file)
        console.log('Resume file selected:', file.name, 'Size:', (file.size / 1024).toFixed(2) + 'KB')
      }
    }
  }

  const handleRemoveFile = () => {
    setSelectedFile(null)
    setError('')
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
    console.log('Resume file removed')
  }

  const handleUpload = () => {
    if (selectedFile) {
      console.log('Uploading resume:', selectedFile.name)
      console.log('File type:', selectedFile.type)
      console.log('File size:', (selectedFile.size / 1024).toFixed(2) + 'KB')
      onUpload(selectedFile)
    }
  }

  const handleBrowseClick = () => {
    fileInputRef.current?.click()
  }

  return (
    <div className="resume-upload">
      <div
        className={`upload-zone ${isDragging ? 'dragging' : ''} ${selectedFile ? 'has-file' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        {!selectedFile ? (
          <>
            <Upload className="upload-icon" />
            <h3>Drag & Drop your resume</h3>
            <p className="upload-text">or</p>
            <button 
              className="browse-button"
              onClick={handleBrowseClick}
              type="button"
            >
              Browse Files
            </button>
            <p className="file-info">Supported formats: PDF, DOC, DOCX (Max 10MB)</p>
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.doc,.docx"
              onChange={handleFileSelect}
              style={{ display: 'none' }}
            />
          </>
        ) : (
          <div className="file-preview">
            <div className="file-icon-wrapper">
              <FileText className="file-icon" />
              <CheckCircle className="check-icon" />
            </div>
            <div className="file-details">
              <h4>{selectedFile.name}</h4>
              <p>{(selectedFile.size / 1024).toFixed(2)} KB</p>
            </div>
            <button 
              className="remove-button"
              onClick={handleRemoveFile}
              type="button"
              aria-label="Remove file"
            >
              <X />
            </button>
          </div>
        )}
      </div>

      {error && (
        <div className="error-message">
          <X className="error-icon" />
          {error}
        </div>
      )}

      {selectedFile && !error && (
        <button 
          className="upload-button"
          onClick={handleUpload}
          type="button"
        >
          Continue to GitHub Connection
        </button>
      )}
    </div>
  )
}

export default ResumeUpload

