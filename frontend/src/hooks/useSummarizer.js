import { useState, useCallback } from 'react'
import { toast } from 'react-toastify'
import summarizerService from '../services/summarizer'

export const useSummarizer = () => {
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [pollingInterval, setPollingInterval] = useState(null)

  const clearSummary = useCallback(() => {
    setSummary(null)
    setError(null)
    if (pollingInterval) {
      clearInterval(pollingInterval)
      setPollingInterval(null)
    }
  }, [pollingInterval])

  const handleError = useCallback((err) => {
    console.error('Summarizer error:', err)
    setError(err.message || 'An unexpected error occurred')
    toast.error(err.message || 'Failed to process request')
  }, [])

  const uploadFile = useCallback(async (file) => {
    setLoading(true)
    setError(null)

    try {
      // Check API health first
      const health = await summarizerService.checkHealth()
      if (health.status !== 'healthy') {
        throw new Error('Service is currently unavailable. Please try again later.')
      }

      // Upload file
      const response = await summarizerService.uploadFile(file)
      
      // Start polling for results
      const pollForResult = async () => {
        try {
          const result = await summarizerService.pollForSummary(response.id)
          setSummary(result.summary)
          summarizerService.saveToHistory(result)
          toast.success('Summary generated successfully!')
        } catch (pollError) {
          handleError(pollError)
        } finally {
          setLoading(false)
        }
      }

      // Start polling
      pollForResult()

    } catch (err) {
      handleError(err)
      setLoading(false)
    }
  }, [handleError])

  const submitText = useCallback(async (text) => {
    setLoading(true)
    setError(null)

    try {
      // Check API health first
      const health = await summarizerService.checkHealth()
      if (health.status !== 'healthy') {
        throw new Error('Service is currently unavailable. Please try again later.')
      }

      // Submit text
      const response = await summarizerService.submitText(text)
      
      // Start polling for results
      const pollForResult = async () => {
        try {
          const result = await summarizerService.pollForSummary(response.id)
          setSummary(result.summary)
          summarizerService.saveToHistory(result)
          toast.success('Summary generated successfully!')
        } catch (pollError) {
          handleError(pollError)
        } finally {
          setLoading(false)
        }
      }

      // Start polling
      pollForResult()

    } catch (err) {
      handleError(err)
      setLoading(false)
    }
  }, [handleError])

  const getRecentSummaries = useCallback(() => {
    return summarizerService.getRecentSummaries()
  }, [])

  const clearHistory = useCallback(() => {
    summarizerService.clearHistory()
    toast.info('History cleared')
  }, [])

  const checkHealth = useCallback(async () => {
    try {
      const health = await summarizerService.checkHealth()
      return health
    } catch (err) {
      return {
        status: 'unhealthy',
        timestamp: new Date().toISOString(),
        database: false,
        llm_service: false,
      }
    }
  }, [])

  return {
    // State
    summary,
    loading,
    error,
    
    // Actions
    uploadFile,
    submitText,
    clearSummary,
    getRecentSummaries,
    clearHistory,
    checkHealth,
    
    // Utility
    hasSummary: !!summary,
    isHealthy: async () => {
      const health = await checkHealth()
      return health.status === 'healthy'
    },
  }
}