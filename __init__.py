# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.

# Below is the list of outside modules you'll be using in your skill.
# They might be built-in to Python, from mycroft-core or from external
# libraries.  If you use an external library, be sure to include it
# in the requirements.txt file so the library is installed properly
# when the skill gets installed later by a user.

import threading
import time
import re
from datetime import datetime, timedelta, date
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
from mycroft.util.parse import extract_datetime
from .db import assignment
from .db import db_helper
from .email import send_email

class AssignmentSkill(MycroftSkill):

    def __init__(self):
        super(AssignmentSkill, self).__init__(name="AssignmentSkill")
        self.db = db_helper.db_helper(self.settings.get("student_id"))


    @intent_handler(IntentBuilder("").require("Update_Assignment").require("name"))
    def handle_update_assignment(self, message):
        self._u_assignment = message.data.get("name")
        self.set_context("update", self._u_assignment)
        self.speak_dialog("assignment_update", expect_response=True)
        

    @intent_handler(IntentBuilder("").require("New_Assignment"))
    def handle_make_assignment(self, message):
        self.time_thread = threading.Thread(target=self._timeCheck, args=[])
        self.time_thread.start()
        self._make_assignment()

    @intent_handler(IntentBuilder("").require("name").
            require("new_assignment"))
    def handle_assignment_name(self, message):
        self._assignment_name = message.data.get("name")
        self.set_context("name_assignment", message.data.get("name"))
        self.remove_context("new_assignment")
        self.speak_dialog("assignment_due_date", expect_response=True)

    @intent_handler(IntentBuilder("").require("name").require("update"))
    def handle_update_type(self, message):
        percent = message.data.get("name")
        self._handle_update(percent)

    @intent_handler(IntentBuilder("").require("list_upcoming"))
    def handle_upcoming_assignments(self, message):
        assignment_list = self.db.getAllAssignments()
        assignment_list = self._remove_outdated_assignments(assignment_list)

        if not assignment_list:
            self.speak_dialog("no_assignments")
            return

        self.speak_dialog("upcoming_assignments")
        for single_assignment in assignment_list:
            self.speak_dialog(single_assignment.name)

    @intent_handler(IntentBuilder("").require("remove_assignment").require("name"))
    def handler_remove_assignment(self, message):
        self._assignment_name = message.data.get("name")
        self.db.removeAssignment(self._assignment_name)
        print(self._assignment_name)
        self.speak_dialog("remove")

    @intent_handler(IntentBuilder("").require("list_all"))
    def handle_list_assignment(self, message):
        assignment_list = self.db.getAllAssignments()

        if not assignment_list:
            self.speak_dialog("no_assignments")
            return

        self.speak_dialog("will_list")
        for single_assignment in assignment_list:
            self.speak_dialog(single_assignment.name)

    @intent_handler(IntentBuilder("").require("due").require("due_date"))
    def _handle_assignment_due_date(self, message):
        due_date = message.data.get("due_date")
        self._due_date = extract_datetime(due_date)
        if not self._due_date:
            self.speak_dialog("invalid_due_date")
            return
        #extract_datetime return a list containing datetime object and a string containing
        #whatever is leftover from the string passed through eg "Assignment is due 21st October"
        #would place Assignment is due within that string variable"
        self._due_date = self._due_date[0].strftime('%d/%m/%Y')
        if not self._due_date:
            self.speak_dialog("invalid_due_date")
            return
        self.set_context("due_date_assignment", self._due_date)
        self.speak_dialog("assignment_module", expect_response=True)

    @intent_handler(IntentBuilder("").require("How_much").require("module").optionally("worth"))
    def _handle_assignment_get_per(self, message):
        print("hello")
        self.assignment = message.data.get("module")
        self._get_assignment_per()

    @intent_handler(IntentBuilder("").require("module").require("due_date_assignment"))
    def _handle_assignnment_module(self, message):
        module = message.data.get("module")
        self._module = message.data.get("module")
        self.set_context("module_assignment", module)
        self.speak_dialog("assignment_percentage", expect_response=True)

    @intent_handler(IntentBuilder("").require("percentage").require("module_assignment").
            optionally("percent"))
    def _handle_assignment_percentaage(self, message):
        #percentage = message.data.get("percentage")
        self._percentage = message.data.get("percentage")
        self.set_context("percentage_assignment", self._percentage)
        self.speak_dialog("assignment_type", expect_response=True)

    @intent_handler(IntentBuilder("").require("type").require("percentage_assignment"))
    def _handle_assignment_percentage(self, message):
        self._type = message.data.get("type")
        self.speak_dialog("Done")
        re = self._handle_push_assignment()
        if re == 0:
            self.speak_dialog("already_exists")
        self._isAfk = False

    @intent_handler(IntentBuilder("").require("list").require("module_id"))
    def _handle_get_module_assignments(self, message):
        module_id = message.data.get("module_id")
        m_assignments = self.db.getAllModuleAssignments(module_id)
        m_assignments = self._remove_outdated_assignments(m_assignments)
        if not m_assignments:
            self.speak_dialog("no_assignments")
            return
        
        for assignment in m_assignments:
            self.speak_dialog(assignment.name)

    @intent_handler(IntentBuilder("").require("how_much_worth").require("closest_ass"))
    def handle_next_worth(self, message):
        print("hello")
        self.speak_dialog("how_much", {"worth":message.data.get("closest_ass")})


    @intent_handler(IntentBuilder("").require("next_assignment"))
    def handle_next_assignmet(self, message):
        self._handle_next_assignment()

    def _handle_push_assignment(self):
        now = datetime.now()
        assigned_date = now.strftime('%d/%m/%Y')
        assignment_test = assignment.Assignment(assigned_date, self._module, self._due_date, self._percentage, 0, self._type, self._assignment_name) 
        self.db.pushAssignment(assignment_test)

    def _handle_update(self, percent):
        for assignment in self.db.getAllAssignments():
            if assignment.name == self._u_assignment:
                self.db.updateAssignmentAccPer(assignment.name, percent)
                return
        self.speak_dialog("no_assignment")
        self._list_all_assignments()
        #print("Could not find or update assignment")


    def _get_assignment_per(self):
        assignment = self.db.getAssignment(self.assignment)
        print(assignment.total_per)
        self.speak_dialog("assignment_worth", {"percentage": assignment.total_per})

    def _make_assignment(self):
        self._remove_context()
        self.speak_dialog("assignment_name", expect_response=True)
        self.set_context("new_assignment", "new assignment")

    def _remove_context(self):
        self.remove_context("module_assignment")
        self.remove_context("due_date_assignment")
        self.remove_context("percentage_assignment")
        self.remove_context("new_assignment")
        self.remove_context("name_assignment")

    def _handle_next_assignment(self):
        assignments = self.db.getAllAssignments()
        assignments = self._remove_outdated_assignments(assignments)
        if len(assignments) == 0:
            self.speak_dialog("You have no upcoming assignments!")
            return
        print(len(assignments))
        closest_assignment = assignments[0];
        for assignment in assignments:
            closest_assignment_date = datetime.strptime(closest_assignment.due_date, "%d/%m/%Y")
            challenging_assignment_date = datetime.strptime(assignment.due_date, "%d/%m/%Y")
            if (closest_assignment_date > challenging_assignment_date):
                closest_assignment = assignment
        print(closest_assignment.due_date)
        _day, _month, _year = closest_assignment.due_date.split("/")
        date_string = date(day=int(_day), month=int(_month), year=int(_year)).strftime('%A %d %B %Y')
        self.speak_dialog("next_assignment_due", {"name": closest_assignment.name, "due_date": date_string})
        self._check_other_assignments(closest_assignment, assignments)
        print(closest_assignment.total_per)
        self.set_context("closest_ass", closest_assignment.total_per)
    
    def _list_all_assignments(self):
        self.speak_dialog("will_list")
        for assignment in self.db.getAllAssignments():
            self.speak_dialog(assignment.name)

    def _remove_outdated_assignments(self, assignments):
        today = datetime.now()
        checkdate = today.strftime("%d/%m/%Y")
        checkdate = datetime.strptime(checkdate, "%d/%m/%Y")
        refined_assignments = []
        for assignment in assignments:
            assignment_date = datetime.strptime(assignment.due_date, "%d/%m/%Y")
            if (checkdate  <= assignment_date):
                refined_assignments.append(assignment)
        return refined_assignments

    def _check_other_assignments(self, closest_assignment, all_assignments):
        today = datetime.now()
        two_weeks = timedelta(days=14)
        check_date = today + two_weeks
        check_date = check_date.strftime("%d/%m/%Y")

        important_assignments = []
        _check_date = datetime.strptime(check_date, "%d/%m/%Y")
        for assignment in all_assignments:
            assignment.total_per = re.sub("[^0-9]", "", assignment.total_per)
            assignment_date = datetime.strptime(assignment.due_date, "%d/%m/%Y")
            percentage_check = (float(closest_assignment.total_per) * 1.33)
            percentage_check = int(percentage_check)
            if (_check_date > assignment_date) and (percentage_check < int(assignment.total_per)):
                important_assignments.append(assignment)

        if len(important_assignments) is 0:
            return
        self.speak_dialog("But don't forget about the following assignments, they're due within two weeks and worth considerably more than " + closest_assignment.name)
        for assigment in important_assignments:
            self.speak_dialog(assignment.name + " and it's worth " + assignment.total_per + " percent of module " + assignment.module_id)

    def _timeCheck(self):
        self._isAfk = True
        print("Brian")
        self._oldtime = time.time()
        while(1):
            #print(time.time())
            if time.time() - self._oldtime > 60 and self._isAfk is True:
                print("hello brian, it's working")
                _subject = "Mycroft assignment update"
                _message = """Hello\n\nIt seems you were interrupted when making changes within                     the assignment skill. This is just a reminder incase it was anything important.\n\n                  Regards,\n\nMycroft Assignment Skill."""
                recipient = "brianarch1996@gmail.com"
                send_email.send_email(_subject,_message, recipient)
                return
            elif time.time() - self._oldtime > 20 and self._isAfk is False:
                print("false")
                self.remove_context("name_assignment")
                return
        
# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return AssignmentSkill()
