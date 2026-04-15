import React, { useState } from 'react'
import { Copy, Check, Download, Printer, Share2, ListChecks, Target, Zap } from 'lucide-react'
import { toast } from 'react-toastify'

const SummaryDisplay = ({ summary }) => {
  const [activeTab, setActiveTab] = useState('summary')
  const [copied, setCopied] = useState(false)

  if (!summary) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-400">No summary available</div>
      </div>
    )
  }

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text)
    setCopied(true)
    toast.success('Copied to clipboard')
    setTimeout(() => setCopied(false), 2000)
  }

  const handleExport = () => {
    const content = JSON.stringify(summary, null, 2)
    const blob = new Blob([content], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `summary-${new Date().toISOString().split('T')[0]}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    toast.success('Summary exported as JSON')
  }

  const handlePrint = () => {
    const printContent = `
      <html>
        <head>
          <title>AI Document Summary</title>
          <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            h1 { color: #333; }
            .section { margin-bottom: 20px; }
            .key-points li, .action-items li { margin-bottom: 8px; }
          </style>
        </head>
        <body>
          <h1>AI Document Summary</h1>
          <div class="section">
            <h2>Summary</h2>
            <p>${summary.summary}</p>
          </div>
          <div class="section">
            <h2>Key Points</h2>
            <ul class="key-points">
              ${summary.key_points.map(point => `<li>${point}</li>`).join('')}
            </ul>
          </div>
          <div class="section">
            <h2>Action Items</h2>
            <ul class="action-items">
              ${summary.action_items.map(item => `<li>${item}</li>`).join('')}
            </ul>
          </div>
          <p><small>Generated on ${new Date().toLocaleDateString()}</small></p>
        </body>
      </html>
    `
    
    const printWindow = window.open('', '_blank')
    printWindow.document.write(printContent)
    printWindow.document.close()
    printWindow.focus()
    printWindow.print()
  }

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'AI Document Summary',
          text: `Summary: ${summary.summary.substring(0, 100)}...`,
          url: window.location.href,
        })
        toast.success('Shared successfully')
      } catch (error) {
        if (error.name !== 'AbortError') {
          toast.error('Failed to share')
        }
      }
    } else {
      handleCopy(JSON.stringify(summary, null, 2))
      toast.info('Summary copied to clipboard for sharing')
    }
  }

  const tabs = [
    { id: 'summary', label: 'Summary', icon: <Target className="h-4 w-4" /> },
    { id: 'key_points', label: 'Key Points', icon: <ListChecks className="h-4 w-4" /> },
    { id: 'action_items', label: 'Action Items', icon: <Zap className="h-4 w-4" /> },
  ]

  return (
    <div className="space-y-6">
      {/* Tab Navigation */}
      <div className="flex border-b border-gray-200">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex-1 py-3 px-4 text-center font-medium transition-colors flex items-center justify-center gap-2 ${
              activeTab === tab.id
                ? 'border-b-2 border-primary-600 text-primary-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            {tab.icon}
            {tab.label}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="space-y-4">
        {activeTab === 'summary' && (
          <div className="space-y-4">
            <div className="flex items-start justify-between">
              <h3 className="text-lg font-semibold text-gray-900">Summary</h3>
              <button
                onClick={() => handleCopy(summary.summary)}
                className="p-2 text-gray-500 hover:text-gray-700 rounded-lg hover:bg-gray-100"
                title="Copy summary"
              >
                {copied ? <Check className="h-4 w-4 text-green-500" /> : <Copy className="h-4 w-4" />}
              </button>
            </div>
            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-gray-700 leading-relaxed">{summary.summary}</p>
            </div>
          </div>
        )}

        {activeTab === 'key_points' && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900">Key Points</h3>
              <span className="text-sm text-gray-500 bg-gray-100 px-2 py-1 rounded">
                {summary.key_points.length} points
              </span>
            </div>
            <ul className="space-y-3">
              {summary.key_points.map((point, index) => (
                <li key={index} className="flex items-start gap-3">
                  <div className="flex-shrink-0 w-6 h-6 rounded-full bg-primary-100 text-primary-600 flex items-center justify-center text-sm font-medium mt-0.5">
                    {index + 1}
                  </div>
                  <div className="flex-1">
                    <p className="text-gray-700">{point}</p>
                    <button
                      onClick={() => handleCopy(point)}
                      className="mt-1 text-xs text-primary-600 hover:text-primary-700"
                    >
                      Copy
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        )}

        {activeTab === 'action_items' && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900">Action Items</h3>
              <span className="text-sm text-gray-500 bg-gray-100 px-2 py-1 rounded">
                {summary.action_items.length} items
              </span>
            </div>
            <ul className="space-y-3">
              {summary.action_items.map((item, index) => (
                <li key={index} className="flex items-start gap-3">
                  <div className="flex-shrink-0 w-6 h-6 rounded-full bg-green-100 text-green-600 flex items-center justify-center text-sm font-medium mt-0.5">
                    ✓
                  </div>
                  <div className="flex-1">
                    <p className="text-gray-700">{item}</p>
                    <button
                      onClick={() => handleCopy(item)}
                      className="mt-1 text-xs text-primary-600 hover:text-primary-700"
                    >
                      Copy
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="border-t border-gray-200 pt-6">
        <div className="flex flex-wrap gap-3">
          <button
            onClick={handleCopy.bind(null, JSON.stringify(summary, null, 2))}
            className="flex-1 btn-secondary flex items-center justify-center gap-2"
          >
            <Copy className="h-4 w-4" />
            Copy All
          </button>
          <button
            onClick={handleExport}
            className="flex-1 btn-secondary flex items-center justify-center gap-2"
          >
            <Download className="h-4 w-4" />
            Export
          </button>
          <button
            onClick={handlePrint}
            className="flex-1 btn-secondary flex items-center justify-center gap-2"
          >
            <Printer className="h-4 w-4" />
            Print
          </button>
          <button
            onClick={handleShare}
            className="flex-1 btn-secondary flex items-center justify-center gap-2"
          >
            <Share2 className="h-4 w-4" />
            Share
          </button>
        </div>
      </div>

      {/* Metadata */}
      <div className="text-xs text-gray-500 border-t border-gray-200 pt-4">
        <div className="flex items-center justify-between">
          <span>Generated with AI</span>
          <span>{new Date().toLocaleDateString()} • {new Date().toLocaleTimeString()}</span>
        </div>
      </div>
    </div>
  )
}

export default SummaryDisplay