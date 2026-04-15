# AI Document Summarizer

An AI-powered web application that generates structured summaries from user-provided documents using LLM technology.

## Features

- **File Upload**: Support for TXT, CSV, and PDF files (up to 10MB)
- **Text Input**: Direct text input for summarization
- **Structured Output**: Generates summaries with key points and action items
- **Real-time Processing**: Background processing with progress tracking
- **Responsive UI**: Modern, mobile-friendly interface
- **Export Options**: Copy, export as JSON, print, and share summaries
- **History**: Local storage for recent summaries

## Tech Stack

### Backend
- **FastAPI**: Python web framework for building APIs
- **PostgreSQL**: Relational database for storing summaries
- **SQLAlchemy**: ORM for database operations
- **OpenAI/LLM**: Integration with language models for summarization
- **Redis**: Optional caching layer

### Frontend
- **React 18**: Frontend library for building user interfaces
- **Vite**: Build tool and development server
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API calls
- **React Dropzone**: File upload component

## Project Structure

```
Ai-Feature-Build/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/               # API endpoints
│   │   ├── core/              # Configuration and settings
│   │   ├── models/            # Database models and schemas
│   │   ├── services/          # Business logic services
│   │   ├── db/                # Database session management
│   │   └── utils/             # Utility functions
│   ├── tests/                 # Backend tests
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Backend Docker configuration
│   └── .env.example          # Environment variables template
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── services/          # API service layer
│   │   ├── hooks/            # Custom React hooks
│   │   └── contexts/         # React contexts
│   ├── public/               # Static assets
│   ├── package.json          # Node.js dependencies
│   ├── Dockerfile            # Frontend Docker configuration
│   └── vite.config.js        # Vite configuration
├── docker-compose.yml        # Docker Compose configuration
├── plans/                    # Project planning documents
└── README.md                # This file
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for local development)
- OpenAI API key (or other LLM provider)

### Quick Start with Docker

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Ai-Feature-Build
   ```

2. Create environment file:
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env and add your OpenAI API key
   ```

3. Start the application:
   ```bash
   docker compose up -d
   ```

4. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development

#### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

6. Start the backend server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Access the frontend at http://localhost:3000

## API Endpoints

### Health Check
- `GET /api/v1/health` - Check API health status

### Summarization
- `POST /api/v1/summarize/file` - Upload file for summarization
- `POST /api/v1/summarize/text` - Submit text for summarization
- `GET /api/v1/summarize/{id}` - Get summary result by ID

### Request/Response Examples

#### Text Summarization Request
```json
{
  "text": "Your text to summarize here...",
  "language": "en"
}
```

#### File Upload Response
```json
{
  "id": "uuid-here",
  "status": "pending",
  "message": "File uploaded successfully. Processing started."
}
```

#### Summary Result
```json
{
  "metadata": {
    "id": "uuid-here",
    "input_type": "file",
    "status": "completed",
    "file_name": "document.pdf",
    "created_at": "2024-01-01T00:00:00Z",
    "processing_time_ms": 2500
  },
  "summary": {
    "summary": "Concise summary of the document...",
    "key_points": ["Key point 1", "Key point 2", "Key point 3"],
    "action_items": ["Action 1", "Action 2"]
  }
}
```

## Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Running All Tests
```bash
docker-compose run backend pytest tests/
docker-compose run frontend npm test
```

## Deployment

### Docker Deployment
1. Build and push Docker images:
   ```bash
   docker-compose build
   docker-compose push
   ```

2. Deploy with Docker Compose:
   ```bash
   docker-compose up -d
   ```

### Cloud Deployment Options

#### AWS
- **ECS/EKS**: Container orchestration
- **RDS**: Managed PostgreSQL database
- **S3**: File storage for uploads
- **CloudFront**: CDN for frontend

#### Google Cloud
- **Cloud Run**: Serverless containers
- **Cloud SQL**: Managed PostgreSQL
- **Cloud Storage**: File storage
- **Firebase Hosting**: Frontend hosting

#### Azure
- **Container Instances**: Container deployment
- **PostgreSQL Database**: Managed database
- **Blob Storage**: File storage
- **Static Web Apps**: Frontend hosting

## Environment Variables

### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://user:pass@host/db

# LLM API
LLM_API_KEY=your_openai_api_key
LLM_MODEL=gpt-3.5-turbo
LLM_MAX_TOKENS=1000
LLM_TEMPERATURE=0.3

# File Upload
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760  # 10MB

# Application
DEBUG=false
CORS_ORIGINS=["http://localhost:3000"]
```

### Frontend (.env)
```bash
VITE_API_BASE_URL=http://localhost:8000
VITE_MAX_FILE_SIZE=10485760
```

## Monitoring and Logging

### Backend Logging
- Structured JSON logging
- Log levels: DEBUG, INFO, WARNING, ERROR
- Request/response logging
- Error tracking with stack traces

### Health Checks
- Application health: `/api/v1/health`
- Database connectivity check
- LLM service availability check

### Metrics
- Request count and response times
- Error rates and types
- File processing statistics
- LLM usage and costs

## Security Considerations

1. **File Upload Security**:
   - File type validation
   - Size limits (10MB)
   - Virus scanning (recommended for production)
   - Secure file storage

2. **API Security**:
   - CORS configuration
   - Rate limiting
   - Input validation and sanitization
   - Authentication (planned feature)

3. **Data Security**:
   - Secure database connections
   - Encrypted file storage
   - Data retention policies
   - GDPR compliance considerations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or feature requests:
1. Check the [documentation](docs/)
2. Search existing issues
3. Create a new issue with detailed information

## Acknowledgments

- Built with FastAPI and React
- Uses OpenAI's GPT models for summarization
- Inspired by modern AI-powered productivity tools