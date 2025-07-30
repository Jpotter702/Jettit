import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export interface CollectionRequest {
  subreddit: string
  sort_type: string
  post_limit: number
  include_comments: boolean
  anonymize_users: boolean
}

export interface CollectionResponse {
  job_id: string
  status: string
  message: string
}

export interface JobStatus {
  job_id: string
  status: string
  progress?: number
  total_posts?: number
  collected_posts?: number
  error_message?: string
}

export const collectSubredditData = async (request: CollectionRequest): Promise<CollectionResponse> => {
  const response = await api.post('/collect', request)
  return response.data
}

export const getJobStatus = async (jobId: string): Promise<JobStatus> => {
  const response = await api.get(`/status/${jobId}`)
  return response.data
}

export const getCollectedData = async (params?: {
  job_id?: string
  subreddit?: string
  limit?: number
  offset?: number
}): Promise<{ data: any[], total: number, limit: number, offset: number }> => {
  const response = await api.get('/data', { params })
  return response.data
}

export const exportData = async (jobId: string, format: string): Promise<void> => {
  const response = await api.get(`/export/${jobId}`, {
    params: { format },
    responseType: 'blob'
  })
  
  // Create download link
  const blob = new Blob([response.data], {
    type: response.headers['content-type'] || 'application/octet-stream'
  })
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  
  // Get filename from Content-Disposition header or use default
  const contentDisposition = response.headers['content-disposition']
  let filename = `reddit-data-${jobId}.${format}`
  if (contentDisposition) {
    const filenameMatch = contentDisposition.match(/filename="(.+)"/)
    if (filenameMatch) {
      filename = filenameMatch[1]
    }
  }
  
  a.download = filename
  document.body.appendChild(a)
  a.click()
  window.URL.revokeObjectURL(url)
  document.body.removeChild(a)
}

// Authentication API functions
export const loginUser = async (email: string, password: string) => {
  const response = await api.post('/auth/login', { email, password })
  return response.data
}

export const registerUser = async (username: string, email: string, password: string) => {
  const response = await api.post('/auth/register', { username, email, password })
  return response.data
}

export const getCurrentUser = async () => {
  const response = await api.get('/auth/me')
  return response.data
} 