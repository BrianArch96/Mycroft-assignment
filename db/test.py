from assignment import Assignment
from db_helper import db_helper
from module import Module

assignment_test = Assignment("today", "cs4125", "tomorrow", 40, 15, "group", "test_assignment")
print(assignment_test.module_id)

db = db_helper("15168867")
db.pushAssignment(assignment_test)
"""
db.updateAssignmentDueDate("cs4125", "test_assignment", "billions of years")
db.updateAssignmentTotalPer("cs4125", "test_assignment", "80")
db.updateAssignmentAccPer("cs4125", "test_assignment", "60")
db.updateAssignmentType("cs4125", "test_assignment", "Groupz")
db.updateAssignmentName("cs4125", "test_assignment", "update_test_assignment")
my_assignment = db.getAssignment("cs4125", "test_assignment")
db.removeAssignment("cs4125", "test_assignment")
"""

my_module = Module("cs4125", "15168867")
print(my_module.getAssignmentCount())
my_module.getAssignments()
