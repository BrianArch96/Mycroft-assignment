from assignment import Assignment

assignment_test = Assignment("today", "cs4125", "tomorrow", 40, 15, "group")
new_value = "banana"
print(assignment_test.module_id)
assignment_test.module_id = new_value
print(assignment_test.module_id)
