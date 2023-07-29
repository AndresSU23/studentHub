class Student:
    def __init__(self, userData):
        '''
        self, user_id, student_id, user_type, username, first_name, student_class, section
        self.user_id = user_id
        self.student_id = student_id
        self.user_type = user_type
        self.username = username
        self.first_name = first_name
        self.student_class = student_class
        self.section = section
        '''
        self.user_id = userData['user_id']
        self.student_id = userData['student_id']
        self.user_type = userData['user_type']
        self.username = userData['username']
        self.first_name = userData['first_name']
        self.student_class = userData['class']
        self.section = userData['section']