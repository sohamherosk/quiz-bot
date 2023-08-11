
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST
import nltk
from nltk.corpus import words

def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):

    nltk.download('words')

    def remove_slangs(text):
        word_list = set(words.words())
        tokens = nltk.word_tokenize(text)
        cleaned_tokens = [token for token in tokens if token.lower() in word_list]
        cleaned_text = ' '.join(cleaned_tokens)
        return cleaned_text
        '''
    Validates and stores the answer for the current question to django session.
    '''
     # Validate the answer (example: checking if it's not empty)
    answer_filter=remove_slangs(answer)
    if not answer_filter:
        return False, "Answer cannot be empty."

    # Store the answer in the session
    session['answers'] = session.get('answers', {})  # Initialize answers dictionary if not present
    session['answers'][str(current_question_id)] = answer_filter

    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''

    return "dummy question", -1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    PYTHON_QUESTION_LIST = {
    '1': {
        'question': 'What is Python?',
        'correct_answer': 'A programming language'
    },
    '2': {
        'question': 'What is the capital of France?',
        'correct_answer': 'Paris'
    },
    # Add more questions
}

# Example session
    session = {
        'answers': {
            '1': 'A programming language',
            '2': 'Berlin'
        }
    }

    user_answers = session.get('answers', {})
    
    correct_answers = 0
    total_questions = len(PYTHON_QUESTION_LIST)
    
    for question_id, user_answer in user_answers.items():
        question = PYTHON_QUESTION_LIST.get(question_id)
        if question is not None and 'correct_answer' in question:
            if user_answer == question['correct_answer']:
                correct_answers += 1
    
    score = (correct_answers / total_questions) * 100
    
    result_message = f"Your final score is: {score:.2f}%"
    
    return result_message
