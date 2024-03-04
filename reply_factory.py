
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST



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
    def get_question_by_id(question_id):
        for question in PYTHON_QUESTION_LIST:
            if question["id"]==question_id:
                return question
            
        return None
    
    def is_valid_answer(answer,question):
        if question.get("type")=="numeric":
            try:
                int(answer)
                return True
            except ValueError:
                return False
            
          
        return True    
    current_question=get_question_by_id(current_question_id)
    if not current_question:
        return False, "invalid id"
    if not is_valid_answer(answer,current_question):
        return False, "invalid answer format"
    
    session["answers"][current_question_id]=answer
    session.save()
   

    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''

    question_index=current_question_id+1
    if question_index < len(PYTHON_QUESTION_LIST):
        next_question=PYTHON_QUESTION_LIST[question_index]
        next_question_id=question_index
        return next_question,next_question_id
    else:
        return None

    return "dummy question", -1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    score=calculate_score(session)
    return f"your final score is {score} out of {len(PYTHON_QUESTION_LIST)}"
def calculate_score(session):
    user_answers=session.get("answers",{})
    correct_answers=PYTHON_QUESTION_LIST

    dummyresult=0
    for question_id, user_answers in user_answers.items():
        if question_id<len(correct_answers) and user_answers==correct_answers[question_id]:
            score+=1
    return dummyresult
