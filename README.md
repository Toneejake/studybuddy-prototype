# StudyBuddy - AI-Powered Study Assistant

StudyBuddy is an AI-powered study assistant built with Python and Django that helps students learn more effectively through spaced repetition flashcards and an intelligent chatbot tutor.

## Features

### 1. Spaced Repetition Flashcard System
- Create and manage flashcards for studying
- Implements the SM-2 spaced repetition algorithm
- Tracks review history and performance
- Schedules reviews based on your memory retention

### 2. AI Chatbot Tutor
- Ask questions about study topics
- Get explanations, definitions, and examples
- Natural language processing for question understanding
- Context-aware responses

### 3. Intelligent NLP System
- Basic natural language processing for question analysis
- Entity extraction from questions
- Intent classification (definition, explanation, comparison, example)
- Rule-based response generation

## Technical Implementation

### Spaced Repetition Algorithm
The flashcard system implements a simplified version of the SM-2 algorithm:
- Quality ratings: Again (0), Hard (1), Good (2), Easy (3)
- Adjusts interval and ease factor based on user responses
- Schedules next review date automatically

### NLP Processing
The NLP system uses rule-based approaches to:
- Identify key entities in questions (topics, concepts)
- Classify question intent (what, how, compare, example)
- Generate contextually appropriate responses

## Project Structure

```
studybuddy/
├── flashcards/          # Flashcard management app
├── chatbot/             # Chatbot conversation app
├── nlp/                 # Natural language processing app
├── templates/           # Base templates
├── studybuddy/          # Main project settings
└── manage.py            # Django management script
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd studybuddy
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install django
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser (optional):
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

## Usage

1. Visit `http://127.0.0.1:8000/` to access the flashcard system
2. Create flashcards with questions and answers
3. Review flashcards when they're due
4. Use the chatbot for quick questions or extended conversations
5. Access admin interface at `http://127.0.0.1:8000/admin/` (if superuser created)

## GitHub Value

This project demonstrates:
- Practical application of AI concepts (spaced repetition, NLP)
- Django web development skills
- Database design with relationships
- RESTful API principles
- Frontend development with Bootstrap
- Software engineering best practices

## Future Enhancements

- Advanced NLP with machine learning models
- More sophisticated spaced repetition algorithms
- User progress tracking and analytics
- Mobile-responsive design
- Integration with external learning resources
- Multi-language support

## License

This project is for educational purposes and demonstrates AI-powered learning concepts.
