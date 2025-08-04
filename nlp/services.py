from .models import ProcessedQuestion, QuestionIntent, ExtractedEntity
import re
from django.contrib.auth.models import User

def process_question(question_text, user=None):
    """
    Process a question using basic NLP techniques
    """
    # Create a processed question record
    processed_question = ProcessedQuestion.objects.create(
        original_text=question_text,
        processed_text=question_text.lower().strip(),
        user=user
    )
    
    # Extract entities (simplified)
    extract_entities(processed_question)
    
    # Determine intent (simplified)
    determine_intent(processed_question)
    
    return processed_question

def extract_entities(processed_question):
    """
    Extract entities from the processed question
    """
    text = processed_question.processed_text
    words = text.split()
    
    # Simple entity extraction based on keywords
    topic_keywords = ['algorithm', 'data', 'structure', 'database', 'network', 'security', 'ai', 'ml', 'nlp', 'python', 'java', 'javascript']
    concept_keywords = ['function', 'class', 'object', 'variable', 'loop', 'array', 'list', 'dictionary', 'set']
    
    for i, word in enumerate(words):
        # Remove punctuation for matching
        clean_word = re.sub(r'[^\w]', '', word)
        
        if clean_word in topic_keywords:
            ExtractedEntity.objects.create(
                processed_question=processed_question,
                entity_text=clean_word,
                entity_type='topic',
                start_position=i,
                end_position=i
            )
        elif clean_word in concept_keywords:
            ExtractedEntity.objects.create(
                processed_question=processed_question,
                entity_text=clean_word,
                entity_type='concept',
                start_position=i,
                end_position=i
            )

def determine_intent(processed_question):
    """
    Determine the intent of the question
    """
    text = processed_question.processed_text
    
    # Simple intent detection based on keywords
    if any(word in text for word in ['what is', 'define', 'definition', 'meaning']):
        intent_type = 'definition'
        confidence = 0.9
    elif any(word in text for word in ['how does', 'explain', 'describe', 'how do']):
        intent_type = 'explanation'
        confidence = 0.85
    elif any(word in text for word in ['compare', 'difference', 'similar', 'vs']):
        intent_type = 'comparison'
        confidence = 0.8
    elif any(word in text for word in ['example', 'sample', 'show']):
        intent_type = 'example'
        confidence = 0.75
    else:
        intent_type = 'unknown'
        confidence = 0.5
    
    QuestionIntent.objects.create(
        processed_question=processed_question,
        intent_type=intent_type,
        confidence_score=confidence
    )

def generate_response(processed_question, original_question):
    """
    Generate a response based on the processed question
    """
    # Get the intent
    try:
        intent = processed_question.intents.first()
        entities = processed_question.entities.all()
    except:
        return "I'm sorry, I didn't understand your question."
    
    if not intent:
        return "I'm sorry, I didn't understand your question."
    
    # Generate response based on intent and entities
    if intent.intent_type == 'definition' and entities:
        entity = entities.first()
        return f"A {entity.entity_text} is a concept in computer science. In the context of your studies, it refers to a fundamental principle or technique used in programming and software development."
    elif intent.intent_type == 'explanation' and entities:
        entity = entities.first()
        return f"Let me explain {entity.entity_text}. This concept is important in computer science because it helps in organizing code and solving complex problems efficiently."
    elif intent.intent_type == 'comparison' and entities.count() >= 2:
        entities_list = list(entities)
        return f"Comparing {entities_list[0].entity_text} and {entities_list[1].entity_text}: Both are important concepts in computer science, but they serve different purposes. {entities_list[0].entity_text} focuses on one aspect while {entities_list[1].entity_text} addresses another."
    elif intent.intent_type == 'example' and entities:
        entity = entities.first()
        return f"Here's an example of {entity.entity_text}: In programming, you might use this concept when writing functions or classes to solve specific problems. For instance, when creating a sorting algorithm, you would apply this principle."
    else:
        return "I understand your question, but I need more specific information to provide a detailed answer. Could you clarify what you're asking about?"
