import unittest
from utils import *
from student import Student

class TestStringMethods(unittest.TestCase):

    # testing feedback report
    def test_correct_number_of_wrong_answers(self):
        number_of_wrong_answer_for_user_1 = 1
        
        student = Student('student1', 'Tony', 'Stark', 6)
        returned_wrong_answer = feedback_report(student)
        self.assertEqual(number_of_wrong_answer_for_user_1, returned_wrong_answer)

    # testing unique strands in questions data
    def test_all_strands(self):
        all_strands = get_all_question_strands()

        expected_output = ['Number and Algebra', 'Measurement and Geometry', 'Statistics and Probability']

        self.assertEqual(expected_output, all_strands)

    # testing improved score from latest year via progress report method
    def test_progress_report(self):
        expected_output = 9

        student = Student('student1', 'Tony', 'Stark', 6)
        actual_output = progress_report(student)

        self.assertEqual(expected_output, actual_output)

if __name__ == '__main__':
    unittest.main()