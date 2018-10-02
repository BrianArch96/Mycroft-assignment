#Assignment class; used to store details of an instance of an assignment.
#An assignment is to be a member of the module instance in the form of a list to accommodate
#for more than one module per module.

class Assignment(object):

    def __init__(self, date_issued, module_id, due_date, total_per, acc_per, assignment_type):
        #constructor for assignment class instance
        self._date_issued = date_issued
        self._module_id = module_id
        self._due_date = due_date
        self._total_per = total_per
        self._acc_per = acc_per
        self._assignment_type = assignment_type

    @property
    def date_issued(self):
        #getter for date_issued
        return self._date_issued

    @date_issued.setter
    def date_issued(self, value):
        #setter for date_issued
        self._date_issued = value
    
    @property
    def module_id(self):
        #getter for module_id
        return self._module_id
    
    @module_id.setter
    def module_id(self, value):
        #setter for module_id
        self._module_id = value

    @property
    def due_date(self):
        #getter for due_date
        return self._due_date

    @due_date.setter
    def due_date(self, value):
        #setter for due_date
        self._due_date = value

    @property
    def total_per(self):
        #getter for total_per
        return self._total_per

    @total_per.setter
    def total_per(self, value):
        #setter for total_per
        self._total_per = value

    @property
    def acc_per(self):
        #getter for acc_per
        return self._acc_per

    @acc_per.setter
    def acc_per(self, value):
        #setter for acc_per
        self._acc_per = value;

    @property
    def assignment_type(self):
        #getter for assignment_type
        return self._assignment_type

    @assignment_type.setter
    def assignment_type(self, value):
        #setter for assignment_type
        self._assignment_type = value




