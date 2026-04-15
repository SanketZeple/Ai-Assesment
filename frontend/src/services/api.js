import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds timeout for file uploads
})

// Request interceptor for adding auth token if needed
api.interceptors.request.use(
  (config) => {
    // You can add authentication tokens here if needed
    // const token = localStorage.getItem('token')
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`
    // }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response
      
      switch (status) {
        case 400:
          throw new Error(data.detail || 'Bad request. Please check your input.')
        case 401:
          throw new Error('Authentication required. Please log in.')
        case 403:
          throw new Error('You do not have permission to perform this action.')
        case 404:
          throw new Error('Resource not found.')
        case 413:
          throw new Error('File too large. Maximum size is 10MB.')
        case 422:
          throw new Error('Validation error. Please check your input.')
        case 429:
          throw new Error('Too many requests. Please try again later.')
        case 500:
          throw new Error('Server error. Please try again later.')
        case 502:
        case 503:
        case 504:
          throw new Error('Service temporarily unavailable. Please try again later.')
        default:
          throw new Error(data.detail || `Error ${status}: ${data.message || 'Unknown error'}`)
      }
    } else if (error.request) {
      // Request was made but no response received
      if (error.code === 'ECONNABORTED') {
        throw new Error('Request timeout. Please try again.')
      }
      throw new Error('Network error. Please check your connection.')
    } else {
      // Something happened in setting up the request
      throw new Error(error.message || 'Unknown error occurred.')
    }
  }
)

export default api