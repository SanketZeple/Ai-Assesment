import React, { useState } from 'react'
import { Upload, FileText, Sparkles, CheckCircle, AlertCircle, Loader2 } from 'lucide-react'
import FileUpload from './components/FileUpload'
import TextInput from './components/TextInput'
import SummaryDisplay from './components/SummaryDisplay'
import { useSummarizer } from './hooks/useSummarizer'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('file')
  const { 
    summary, 
    loading, 
    error, 
    uploadFile, 
    submitText, 
    clearSummary 
  } = useSummarizer()

  const handleFileUpload = async (file) => {
    await uploadFile(file)
  }

  const handleTextSubmit = async (text) => {
    await submitText(text)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <header className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Sparkles className="h-10 w-10 text-primary-600" />
            <h1 className="text-4xl font-bold text-gray-900">AI Document Summarizer</h1>
          </div>
          <p className="text-gray-600 text-lg max-w-2xl mx-auto">
            Upload documents or paste text to get concise, structured summaries with key points and action items.
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Input */}
          <div className="lg:col-span-2 space-y-6">
            {/* Tab Navigation */}
            <div className="flex border-b border-gray-200">
              <button
                onClick={() => setActiveTab('file')}
                className={`flex-1 py-3 px-4 text-center font-medium transition-colors ${
                  activeTab === 'file'
                    ? 'border-b-2 border-primary-600 text-primary-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                <div className="flex items-center justify-center gap-2">
                  <Upload className="h-5 w-5" />
                  Upload File
                </div>
              </button>
              <button
                onClick={() => setActiveTab('text')}
                className={`flex-1 py-3 px-4 text-center font-medium transition-colors ${
                  activeTab === 'text'
                    ? 'border-b-2 border-primary-600 text-primary-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                <div className="flex items-center justify-center gap-2">
                  <FileText className="h-5 w-5" />
                  Paste Text
                </div>
              </button>
            </div>

            {/* Input Area */}
            <div className="card">
              {activeTab === 'file' ? (
                <FileUpload onUpload={handleFileUpload} disabled={loading} />
              ) : (
                <TextInput onSubmit={handleTextSubmit} disabled={loading} />
              )}
            </div>

            {/* Status Display */}
            {loading && (
              <div className="card">
                <div className="flex items-center justify-center gap-3 p-4">
                  <Loader2 className="h-6 w-6 text-primary-600 animate-spin" />
                  <div>
                    <p className="font-medium text-gray-900">Processing your request...</p>
                    <p className="text-sm text-gray-600">This may take a few moments.</p>
                  </div>
                </div>
              </div>
            )}

            {error && (
              <div className="card border-red-200 bg-red-50">
                <div className="flex items-start gap-3">
                  <AlertCircle className="h-6 w-6 text-red-600 flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="font-medium text-red-800">Error</p>
                    <p className="text-red-600">{error}</p>
                    <button
                      onClick={clearSummary}
                      className="mt-2 text-sm text-red-700 hover:text-red-800 font-medium"
                    >
                      Try again
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Right Column - Results */}
          <div className="lg:col-span-1">
            <div className="sticky top-8">
              <div className="card h-full">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-bold text-gray-900">Summary Results</h2>
                  {summary && (
                    <button
                      onClick={clearSummary}
                      className="text-sm text-primary-600 hover:text-primary-700 font-medium"
                    >
                      Clear
                    </button>
                  )}
                </div>

                {summary ? (
                  <SummaryDisplay summary={summary} />
                ) : (
                  <div className="text-center py-12">
                    <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-100 mb-4">
                      <Sparkles className="h-8 w-8 text-gray-400" />
                    </div>
                    <h3 className="text-lg font-medium text-gray-900 mb-2">No Summary Yet</h3>
                    <p className="text-gray-600">
                      Upload a file or paste text to generate a summary.
                    </p>
                  </div>
                )}

                {/* Info Box */}
                <div className="mt-8 p-4 bg-blue-50 rounded-lg border border-blue-100">
                  <div className="flex items-start gap-3">
                    <CheckCircle className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="font-medium text-blue-800">How it works</p>
                      <ul className="mt-2 text-sm text-blue-700 space-y-1">
                        <li>• Supports TXT, CSV, and PDF files</li>
                        <li>• Extracts key points and action items</li>
                        <li>• Processes up to 10MB files</li>
                        <li>• Results are saved for 24 hours</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-12 pt-8 border-t border-gray-200 text-center text-gray-500 text-sm">
          <p>AI Document Summarizer • Powered by LLM Technology • {new Date().getFullYear()}</p>
        </footer>
      </div>
    </div>
  )
}

export default App