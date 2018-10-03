from db_helper import db_helper

class Module:
    
    def __init__(self, code, studentID):
        self._code = code
        self.db_helper = db_helper(studentID)
        self.assignments = []

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    def getAssignmentCount(self):
        return self.db_helper.assignmentCount(self._code)

    def getAssignments(self):
        self.assignments = self.db_helper.getAllAssignments(self.code)
        print len(self.assignments)
        for assignment in self.assignments:
            print(assignment.name)
