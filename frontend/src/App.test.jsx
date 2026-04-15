import { render, screen } from '@testing-library/react'
import App from './App'

describe('App', () => {
  it('renders the main heading', () => {
    render(<App />)
    const headingElement = screen.getByText(/AI Document Summarizer/i)
    expect(headingElement).toBeInTheDocument()
  })

  it('renders the description text', () => {
    render(<App />)
    const descriptionElement = screen.getByText(/Upload documents or paste text/i)
    expect(descriptionElement).toBeInTheDocument()
  })

  it('renders file upload tab', () => {
    render(<App />)
    const uploadTab = screen.getByText(/Upload File/i)
    expect(uploadTab).toBeInTheDocument()
  })

  it('renders text input tab', () => {
    render(<App />)
    const textTab = screen.getByText(/Paste Text/i)
    expect(textTab).toBeInTheDocument()
  })

  it('renders summary results section', () => {
    render(<App />)
    const resultsSection = screen.getByText(/Summary Results/i)
    expect(resultsSection).toBeInTheDocument()
  })
})