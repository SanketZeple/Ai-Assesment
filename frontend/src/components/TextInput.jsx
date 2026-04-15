import React, { useState } from 'react'
import { FileText, Send, Copy, Trash2 } from 'lucide-react'
import { toast } from 'react-toastify'

const TextInput = ({ onSubmit, disabled }) => {
  const [text, setText] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!text.trim()) {
      toast.error('Please enter some text to summarize')
      return
    }

    if (text.trim().length < 10) {
      toast.error('Text must be at least 10 characters long')
      return
    }

    if (text.trim().length > 10000) {
      toast.error('Text exceeds 10,000 character limit')
      return
    }

    setSubmitting(true)
    try {
      await onSubmit(text.trim())
      toast.success('Text submitted successfully! Processing...')
    } catch (error) {
      toast.error(error.message || 'Failed to submit text')
    } finally {
      setSubmitting(false)
    }
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(text)
    toast.success('Text copied to clipboard')
  }

  const handleClear = () => {
    setText('')
    toast.info('Text cleared')
  }

  const handlePaste = async () => {
    try {
      const clipboardText = await navigator.clipboard.readText()
      setText(clipboardText)
      toast.success('Text pasted from clipboard')
    } catch (error) {
      toast.error('Unable to paste from clipboard')
    }
  }

  const characterCount = text.length
  const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0

  return (
    <div className="space-y-6">
      {/* Text Area */}
      <div>
        <label className="label">
          <div className="flex items-center justify-between">
            <span>Enter text to summarize</span>
            <div className="text-sm text-gray-500">
              {characterCount}/10,000 characters • {wordCount} words
            </div>
          </div>
        </label>
        <div className="relative">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste or type your text here... (e.g., meeting notes, article content, report, etc.)"
            className="input-field min-h-[200px] resize-y"
            disabled={disabled || submitting}
            maxLength={10000}
          />
          <div className="absolute bottom-3 right-3 flex gap-2">
            <button
              type="button"
              onClick={handlePaste}
              disabled={disabled || submitting}
              className="p-2 text-gray-500 hover:text-gray-700 bg-white rounded-lg border border-gray-200 hover:border-gray-300 disabled:opacity-50"
              title="Paste from clipboard"
            >
              <Copy className="h-4 w-4" />
            </button>
            <button
              type="button"
              onClick={handleClear}
              disabled={!text || disabled || submitting}
              className="p-2 text-gray-500 hover:text-red-600 bg-white rounded-lg border border-gray-200 hover:border-red-200 disabled:opacity-50"
              title="Clear text"
            >
              <Trash2 className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex justify-between items-center">
        <div className="text-sm text-gray-600">
          <div className="flex items-center gap-2">
            <FileText className="h-4 w-4" />
            <span>Text is processed securely and not stored permanently</span>
          </div>
        </div>
        <div className="flex gap-3">
          <button
            type="button"
            onClick={handleCopy}
            disabled={!text || disabled || submitting}
            className="btn-secondary flex items-center gap-2 disabled:opacity-50"
          >
            <Copy className="h-4 w-4" />
            Copy
          </button>
          <button
            type="submit"
            onClick={handleSubmit}
            disabled={!text.trim() || disabled || submitting}
            className="btn-primary flex items-center gap-2 disabled:opacity-50"
          >
            {submitting ? (
              <>
                <div className="h-4 w-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                Processing...
              </>
            ) : (
              <>
                <Send className="h-4 w-4" />
                Summarize Text
              </>
            )}
          </button>
        </div>
      </div>

      {/* Examples */}
      <div className="border-t border-gray-200 pt-6">
        <h4 className="font-medium text-gray-900 mb-3">Example texts you can try:</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <button
            type="button"
            onClick={() => setText(`The quarterly sales report shows a 15% increase in revenue compared to last quarter. Key drivers include the new product launch and expanded market presence in Europe. However, operating costs have also risen by 8% due to increased marketing spend.`)}
            disabled={disabled || submitting}
            className="text-left p-3 rounded-lg border border-gray-200 hover:border-primary-300 hover:bg-primary-50 transition-colors disabled:opacity-50"
          >
            <div className="text-sm font-medium text-gray-900">Business Report</div>
            <div className="text-xs text-gray-600 mt-1">Quarterly sales analysis with key metrics</div>
          </button>
          <button
            type="button"
            onClick={() => setText(`Project Alpha is progressing well with all milestones met on schedule. The development team has completed the core features, and testing is underway. Key risks identified include potential delays in third-party integrations. Next steps involve user acceptance testing and deployment planning.`)}
            disabled={disabled || submitting}
            className="text-left p-3 rounded-lg border border-gray-200 hover:border-primary-300 hover:bg-primary-50 transition-colors disabled:opacity-50"
          >
            <div className="text-sm font-medium text-gray-900">Project Update</div>
            <div className="text-xs text-gray-600 mt-1">Status report with risks and next steps</div>
          </button>
        </div>
      </div>
    </div>
  )
}

export default TextInput