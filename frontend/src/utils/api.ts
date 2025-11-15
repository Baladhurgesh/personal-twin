import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for logging
apiClient.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.status, error.message);
    return Promise.reject(error);
  }
);

export interface ResumeAnalysisResponse {
  success: boolean;
  data: {
    skills: string[];
    experience: string[];
    education: string[];
    summary: string;
  };
  message?: string;
}

export interface GitHubAnalysisResponse {
  success: boolean;
  data: {
    username: string;
    repositories: number;
    languages: string[];
    contributions: number;
    topProjects: Array<{
      name: string;
      description: string;
      stars: number;
      language: string;
    }>;
  };
  message?: string;
}

export interface DigitalTwinResponse {
  success: boolean;
  data: {
    id: string;
    resume_analysis: any;
    github_analysis: any;
    combined_insights: string;
    created_at: string;
  };
  message?: string;
}

// API Functions

/**
 * Upload and analyze resume
 */
export const uploadResume = async (file: File): Promise<ResumeAnalysisResponse> => {
  console.log('Uploading resume for analysis...');
  const formData = new FormData();
  formData.append('resume', file);

  try {
    const response = await apiClient.post<ResumeAnalysisResponse>('/resume/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    console.log('Resume analysis complete:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error analyzing resume:', error);
    throw error;
  }
};

/**
 * Fetch and analyze GitHub profile
 */
export const analyzeGitHub = async (username: string): Promise<GitHubAnalysisResponse> => {
  console.log(`Analyzing GitHub profile: ${username}`);
  console.log('This will scrape all repositories and generate AI-powered summaries...');
  
  try {
    const response = await apiClient.post<GitHubAnalysisResponse>('/github/analyze', {
      username,
    });
    
    console.log('GitHub analysis complete:', response.data);
    console.log(`Processed ${response.data.data?.repositories || 0} repositories`);
    console.log(`Generated ${response.data.data?.topProjects?.length || 0} project summaries`);
    console.log('All project summaries saved to text files on server');
    return response.data;
  } catch (error) {
    console.error('Error analyzing GitHub:', error);
    throw error;
  }
};

/**
 * Create complete digital twin
 */
export const createDigitalTwin = async (
  resumeFile: File,
  githubUsername: string
): Promise<DigitalTwinResponse> => {
  console.log('Creating digital twin with resume and GitHub data...');
  
  const formData = new FormData();
  formData.append('resume', resumeFile);
  formData.append('github_username', githubUsername);

  try {
    const response = await apiClient.post<DigitalTwinResponse>('/twin/create', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    console.log('Digital twin created successfully:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error creating digital twin:', error);
    throw error;
  }
};

/**
 * Get digital twin by ID
 */
export const getDigitalTwin = async (twinId: string): Promise<DigitalTwinResponse> => {
  console.log(`Fetching digital twin: ${twinId}`);
  
  try {
    const response = await apiClient.get<DigitalTwinResponse>(`/twin/${twinId}`);
    console.log('Digital twin retrieved:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error fetching digital twin:', error);
    throw error;
  }
};

/**
 * Export digital twin data
 */
export const exportDigitalTwin = (data: any): void => {
  console.log('Exporting digital twin data...');
  
  const exportData = {
    ...data,
    exported_at: new Date().toISOString(),
    version: '1.0.0',
  };

  const blob = new Blob([JSON.stringify(exportData, null, 2)], {
    type: 'application/json',
  });

  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `digital-twin-${Date.now()}.json`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);

  console.log('Digital twin data exported successfully');
};

export default apiClient;

