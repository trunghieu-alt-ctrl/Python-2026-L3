import math
import numpy as np

class Student:
    def __init__(self, student_id, name, dob):
        self.id = student_id
        self.name = name
        self.dob = dob
        self.marks = {} 
        self.gpa = 0.0

    def add_mark(self, course_id, mark):
        self.marks[course_id] = math.floor(mark * 10) / 10.0

    def calculate_gpa(self, courses_dict):
        if not self.marks:
            self.gpa = 0.0
            return
        
        marks_list = []
        credits_list = []
        for c_id, mark in self.marks.items():
            if c_id in courses_dict:
                marks_list.append(mark)
                credits_list.append(courses_dict[c_id].credits)
                
        if credits_list:
            marks_arr = np.array(marks_list)
            credits_arr = np.array(credits_list)
            self.gpa = np.average(marks_arr, weights=credits_arr)
        else:
            self.gpa = 0.0

class Course:
    def __init__(self, course_id, name, credits):
        self.id = course_id
        self.name = name
        self.credits = credits

class SchoolManagement:
    def __init__(self):
        self.students = []
        self.courses = {}

    def add_student(self, std):
        self.students.append(std)

    def add_course(self, course):
        self.courses[course.id] = course

    def sort_by_gpa(self):
        for s in self.students:
            s.calculate_gpa(self.courses)
        self.students.sort(key=lambda s: s.gpa, reverse=True)