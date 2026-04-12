# InfraCredit LMS Chatbot Backend

This repository contains the backend code for the InfraCredit LMS chatbots.

## Bot Types
1. **General Assistant**: `/api/chat/general` - Handles Courses, SOPs, FAQs, etc.
2. **Course Assistant**: `/api/chat/course` - Strictly for course-related queries.

## Getting Started

### Prerequisites
- Python 3.9+
- OpenAI API Key

### Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your `OPENAI_API_KEY` and other LMS details.

### Running the App
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`.
Documentation can be found at `http://localhost:8000/docs`.

## Integration
Provide the base URL of your deployed service to the frontend engineer. They can hit the endpoints above to interact with the bots.
