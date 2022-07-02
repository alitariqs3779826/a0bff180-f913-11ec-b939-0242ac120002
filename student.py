'''
Object Class: Student
  Object class of student to define a student and later use in the application to set all student details
'''
class Student:
  def __init__(self, id, first_name, last_name, year_level):
    self.id = id
    self.first_name = first_name
    self.first_name = first_name
    self.last_name = last_name
    self.year_level = year_level

  # prints all details of the students
  def my_details(self):
    print("ID: " + self.id)
    print("Name: " + self.first_name + " " + self.last_name)
    print("Year Level: " + self.year_level)

  
  