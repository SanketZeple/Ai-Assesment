import api from './api'

class SummarizerService {
  /**
   * Upload a file for summarization
   * @param {File} file - The file to upload
   * @returns {Promise<Object>} - Response with summary ID and status
   */
  async uploadFile(file) {
    const formData = new FormData()
    formData.append('file', file)

    const response = await api.post('/api/v1/summarize/file', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        // You can add progress tracking here if needed
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        )
        console.log(`Upload progress: ${percentCompleted}%`)
      },
    })

    return response.data
  }

  /**
   * Submit text for summarization
   * @param {string} text - The text to summarize
   * @param {string} language - Optional language code
   * @returns {Promise<Object>} - Response with summary ID and status
   */
  async submitText(text, language = 'en') {
    const response = await api.post('/api/v1/summarize/text', {
      text,
      language,
    })

    return response.data
  }

  /**
   * Get summary result by ID
   * @param {string} summaryId - The summary ID
   * @returns {Promise<Object>} - Summary result with metadata
   */
  async getSummary(summaryId) {
    const response = await api.get(`/api/v1/summarize/${summaryId}`)
    return response.data
  }

  /**
   * Poll for summary completion
   * @param {string} summaryId - The summary ID
   * @param {number} interval - Polling interval in milliseconds
   * @param {number} maxAttempts - Maximum number of polling attempts
   * @returns {Promise<Object>} - Completed summary result
   */
  async pollForSummary(summaryId, interval = 2000, maxAttempts = 30) {
    let attempts = 0

    const poll = async () => {
      attempts++
      const result = await this.getSummary(summaryId)

      if (result.metadata.status === 'completed') {
        return result
      } else if (result.metadata.status === 'failed') {
        throw new Error(
          result.metadata.error_message || 'Summary generation failed'
        )
      } else if (attempts >= maxAttempts) {
        throw new Error('Summary generation timeout')
      } else {
        // Continue polling
        await new Promise((resolve) => setTimeout(resolve, interval))
        return poll()
      }
    }

    return poll()
  }

  /**
   * Check API health
   * @returns {Promise<Object>} - Health status
   */
  async checkHealth() {
    try {
      const response = await api.get('/api/v1/health')
      return response.data
    } catch (error) {
      return {
        status: 'unhealthy',
        timestamp: new Date().toISOString(),
        database: false,
        llm_service: false,
      }
    }
  }

  /**
   * Get recent summaries from local storage
   * @returns {Array} - Array of recent summaries
   */
  getRecentSummaries() {
    try {
      const recent = localStorage.getItem('recent_summaries')
      return recent ? JSON.parse(recent) : []
    } catch {
      return []
    }
  }

  /**
   * Save summary to local storage
   * @param {Object} summary - The summary to save
   */
  saveToHistory(summary) {
    try {
      const recent = this.getRecentSummaries()
      const newEntry = {
        id: summary.metadata?.id || Date.now().toString(),
        summary: summary.summary,
        timestamp: new Date().toISOString(),
        input_type: summary.metadata?.input_type || 'unknown',
      }

      // Keep only last 10 summaries
      const updated = [newEntry, ...recent.slice(0, 9)]
      localStorage.setItem('recent_summaries', JSON.stringify(updated))
    } catch (error) {
      console.error('Failed to save to history:', error)
    }
  }

  /**
   * Clear history from local storage
   */
  clearHistory() {
    try {
      localStorage.removeItem('recent_summaries')
    } catch (error) {
      console.error('Failed to clear history:', error)
    }
  }
}

export default new SummarizerService()