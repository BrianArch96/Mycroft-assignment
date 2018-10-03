from assignment import Assignment
from db_helper import db_helper

assignment_test = Assignment("today", "cs4125", "tomorrow", 40, 15, "group", "test_assignment")
print(assignment_test.module_id)

db = db_helper("15168867")
db.pushAssignment(assignment_test)
db.updateAssignmentDueDate("cs4125", "test_assignment", "billions of years")
my_assignment = db.getAssignment("cs4125", "test_assignment")
#db.removeAssignment("cs4125", "test_assignment")
