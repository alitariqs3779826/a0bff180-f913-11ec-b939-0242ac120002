
from student import Student
from utils import *

def main():
    my_bool = True
    student_id = None
    student_data_list = []
    print('Please enter the following')

    # Running a loop to get user to enter a correct student ID, will ask again if ID is wrong
    while my_bool:
        
        # get user to enter student ID
        student_id = input('Student ID: ')
        # load students data
        student_data_list = load_students(student_id)

        # check if entered user id exists in our database
        if student_data_list:
            my_bool = False
            break
        else:
            # wrong student ID statements
            print('\nStudent with this ID does not exist, Please enter a different ID')
            print('Note: student ID is written in the format *student_number*\n')
    
    student = Student(student_data_list[0]['id'], student_data_list[0]['firstName'], student_data_list[0]['lastName'],student_data_list[0]['yearLevel'])

    report_type_bool = True
    report_type = None

    # getting correct input from user to have the correct number for report type
    while report_type_bool:

        try:
            report_type = int(input('Report to generate (1 for Diagnostic, 2 for Progress, 3 for Feedback): '))
            
            # break the loop is entered integer is between 1 to 3
            if report_type > 0 and report_type < 4:
                report_type_bool = False
                if report_type == 1:
                    get_student_score_for_each_strand(student)
                if report_type == 2:
                    progress_report(student)
                # elif report_type == 2:
                #     progress_report(student) 

                break
            else:
                # show error message 
                print("\nNumber can only be between 1 to 3\n")
        
        # if user have not entered an integer, ask them to enter integer again after displaying error message
        except:
            print("Can only Enter a Number Between 1 to 3!\n")

    

if __name__ == "__main__":
    # runs the main function
    main()