import json
from datetime import datetime

def load_students(student_id):
    # open students.json file 
    open_student_file = open('data/students.json')
    
    # load json data into a variable, (a list dictionary)
    student_data = json.load(open_student_file)

    ret_val_list = []

    for i in student_data:
        if i['id'] == student_id:
            # if user id is found append the data to the list, else list will be emty
            ret_val_list.append(i)

    return ret_val_list

def get_all_question_strands():
    # open questions.json file 
    open_question_file = open('data/questions.json')
    
    # load json data into a variable, (a list dictionary)
    question_data = json.load(open_question_file)

    ret_val_list = []

    for i in question_data:
        # finds all unique strands from questions data
        if i['strand'] not in ret_val_list:
            ret_val_list.append(i['strand'])
    
    return ret_val_list

def get_student_score_for_each_strand(student):
    student_id = student.id
    # get all unqiue strands
    all_strands = get_all_question_strands()

    completion_date = None

    open_student_response_file = open('data/student-responses.json')

    student_response_data = json.load(open_student_response_file)
    student_responses = []
    raw_score = None

    for i in student_response_data:
        # get latest data of the student
        if i['student']['id'] == student.id and i['student']['yearLevel'] == (student.year_level-1):
            student_responses = i['responses']
            completion_date = i['completed']
            raw_score = i['results']['rawScore']


    # open questions.json file 
    open_question_file = open('data/questions.json')
    
    # load json data into a variable, (a list dictionary)
    question_data = json.load(open_question_file)

    total_count_for_each_strand = []

    for i in all_strands:
        current_strand = i
        count = 0

        for j in question_data:
            if j['strand'] == current_strand:
                count = count + 1

        total_count_for_each_strand.append((current_strand, count))
    
    correct_answer_count_for_each_strand = []

    for i in question_data:
        current_strand = i['strand']
        count = 0

        for j in student_responses:
            # store answer if student response is correct
            if j['questionId'] == i['id'] and j['response'] == i['config']['key']:
                count = count + 1
                correct_answer_count_for_each_strand.append((current_strand, count))
        

    total_of_correct_answer_count_for_each_strand = []

    # getting correct answer count for each strand
    for i in all_strands:
        count = 0
        current_strand = None
        for j in correct_answer_count_for_each_strand:
            if i == j[0]:
                count = count + 1
            current_strand = j[0]
        total_of_correct_answer_count_for_each_strand.append((i, count))

    # get date in correct format to print
    completion_date = completion_date.split(' ')
    date_str =  completion_date[0]
    format_str = '%d/%m/%Y' # The format
    datetime_obj = datetime.strptime(date_str, format_str)
    month = datetime_obj.strftime("%B")

    d_time = datetime.strptime(completion_date[1], "%H:%M:%S")
    curr_time = d_time.strftime("%I:%M %p")


    print('\n' + student.first_name,student.last_name ,'recently completed Numeracy assessment on', datetime_obj.day,  month , datetime_obj.year , curr_time)

    print('He got', raw_score, 'right out of', str(len(question_data)) +  '.',  'Details by strand given below:\n')
    
    # print count for each strand
    for i in total_of_correct_answer_count_for_each_strand:
        score = None
        total_questions = None
        strand = None
        for j in total_count_for_each_strand:
            if i[0] == j[0]:
                score = i[1]
                total_questions = j[1]
                strand = i[0]
    
        print(strand + ':', score, 'out of', total_questions, 'correct')

def progress_report(student):
    student_id = student.id

    completion_date = None

    open_student_response_file = open('data/student-responses.json')

    student_response_data = json.load(open_student_response_file)
    student_responses = None
    raw_score = None
    curr_student_data = []
    
    # storing student reponse details for each assessment given by the student
    for i in student_response_data:
        my_dict = {}
        if i['student']['id'] == student.id:
            completion_date = i['started']
            raw_score = i['results']['rawScore']
            completion_date = completion_date.split(' ')
            date_str =  completion_date[0]
            format_str = '%d/%m/%Y' # The format
            datetime_obj = datetime.strptime(date_str, format_str)
            
            my_dict = {
                'student_responses': student_responses,
                'completion_date':datetime_obj,
                'raw_score':raw_score
            }
            curr_student_data.append(my_dict)


    print('\n'+ str(student.first_name), student.last_name, 'has completed Numeracy assessment', len(curr_student_data), 'times in total. Date and raw score given below:\n')

    min_date = None
    date_printed = []
    
    # get data by minium to maximum date
    for i in curr_student_data:
        min_date = i['completion_date']

        for j in curr_student_data:
            if min_date > j['completion_date']:
                if j['completion_date'] not in date_printed:
                    min_date = j['completion_date']
                    date_printed.append(min_date)
        
        if min_date is not None:
            month = min_date.strftime("%B")
            print('Date:', str(min_date.day) + 'th', month, str(min_date.year)+',', 'Raw Score:', i['raw_score'], 'out of 16')

    # find minimum date
    min_date = curr_student_data[0]['completion_date']
    for i in curr_student_data:
        if i['completion_date'] < min_date:
            min_date = i['completion_date']
    
    # find maximum date
    max_date = curr_student_data[0]['completion_date']
    for i in curr_student_data:
        if i['completion_date'] > max_date:
            max_date = i['completion_date']

    oldest_score = 0
    latest_score = 0

    for i in curr_student_data:
        if i['completion_date'] == min_date:
            oldest_score = i['raw_score']
        
        if i['completion_date'] == max_date:
            latest_score = i['raw_score']
    
    # show this print statement if student have improved over time
    if latest_score > oldest_score:
        print('\n' + str(student.first_name), student.last_name, 'got', (latest_score - oldest_score), 'more correct in the recent completed assessment than the oldest')
    
    # show this print statement if student haven't performed well recently and was better in their previous test
    else:
        print('\n' + str(student.first_name), student.last_name, 'got', (oldest_score - latest_score), 'less correct in the recent completed assessment than the oldest')

    # returning improved score from latest year to run tests
    return (latest_score-oldest_score)

def get_wrong_data(wrong_answers_data,question_data):
    
    for i in wrong_answers_data:
            print('Question:', i['question'])

            correct_answer = None
            wrong_answer = None

            for j in question_data:
                # find labels and value for both write and wrong answer to display in print statements
                if i['question_id'] == j['id']:
                    for x in j['config']['options']:
                        if x['id'] == i['your_answer']:
                            wrong_answer = str(x['label']) + ' with value ' + str(x['value'])
                        
                        if x['id'] == i['correct_answer']:
                            correct_answer = str(x['label']) + ' with value ' + str(x['value'])
            
            print('Your answer:', wrong_answer)
            print('Correct answer:', correct_answer)
            print('Hint:', i['hint'], '\n')
    
def feedback_report(student):
    student_id = student.id
    completion_date = None

    open_student_response_file = open('data/student-responses.json')

    student_response_data = json.load(open_student_response_file)
    student_responses = []
    raw_score = None

    # get latest student data
    for i in student_response_data:
        if i['student']['id'] == student.id and i['student']['yearLevel'] == (student.year_level-1):
            student_responses = i['responses']
            completion_date = i['completed']
            raw_score = i['results']['rawScore']

    # get date in correct format for printing
    completion_date = completion_date.split(' ')
    date_str =  completion_date[0]
    format_str = '%d/%m/%Y' # The format
    datetime_obj = datetime.strptime(date_str, format_str)
    month = datetime_obj.strftime("%B")

    d_time = datetime.strptime(completion_date[1], "%H:%M:%S")
    curr_time = d_time.strftime("%I:%M %p")

    print('\n' + student.first_name,student.last_name ,'recently completed Numeracy assessment on', datetime_obj.day,  month , datetime_obj.year , curr_time)
    
    # open questions.json file 
    open_question_file = open('data/questions.json')
    
    # load json data into a variable, (a list dictionary)
    question_data = json.load(open_question_file)    
    correct_answer_count_for_each_strand = []
    wrong_answers_data = []

    for i in question_data:
        current_strand = i['strand']
        count = 0
        my_dict = {}

        for j in student_responses:
            # get all wrong answers of student
            if j['questionId'] == i['id'] and j['response'] != i['config']['key']:
                count = count + 1
                correct_answer_count_for_each_strand.append((current_strand, count))
                
                my_dict = {
                    'your_answer': j['response'],
                    'correct_answer': i['config']['key'],
                    'question_id': i['id'],
                    'question':i['stem'],
                    'hint':i['config']['hint']
                }

                wrong_answers_data.append(my_dict)
    
    print('He got', raw_score, 'right out of', str(len(question_data)) +  '.',  'Feedback for wrong answers given below:\n')

    # if any wrong answers are present
    if wrong_answers_data:
        get_wrong_data(wrong_answers_data, question_data)

    # returning number of wrong answers for testing
    return len(correct_answer_count_for_each_strand)
    
