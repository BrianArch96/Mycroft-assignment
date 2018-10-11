# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.

# Below is the list of outside modules you'll be using in your skill.
# They might be built-in to Python, from mycroft-core or from external
# libraries.  If you use an external library, be sure to include it
# in the requirements.txt file so the library is installed properly
# when the skill gets installed later by a user.

from datetime import datetime
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
from mycroft.util.parse import extract_datetime
from .db import assignment
from .db import db_helper

# Each skill is contained within its own class, which inherits base methods
# from the MycroftSkill class.  You extend this class as shown below.

# TODO: Change "Template" to a unique name for your skill
class TemplateSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(TemplateSkill, self).__init__(name="TemplateSkill")
        print("Hello world")
        self.db = db_helper.db_helper(self.settings.get("student_id"))


    @intent_handler(IntentBuilder("").require("New_Assignment"))
    def handle_make_assignment(self, message):
        self._make_assignment()

    @intent_handler(IntentBuilder("").require("name").
            require("new_assignment"))
    def handle_assignment_name(self, message):
        self._assignment_name = message.data.get("name")
        self.set_context("name_assignment", message.data.get("name"))
        self.speak_dialog("assignment_due_date")

    @intent_handler(IntentBuilder("").require("due_date").require("name_assignment"))
    def _handle_assignment_due_date(self, message):
        due_date = message.data.get("due_date")
        self.due_date = extract_datetime(due_date)
        #extract_datetime return a list containing datetime object and a string containing
        #whatever is leftover from the string passed through eg "Assignment is due 21st October"
        #would place Assignment is due within that string variable"
        self._due_date = self.due_date[0].strftime('%d/%m/%Y')
        if not self._due_date:
            self.speak_dialog("invalid_due_date")
        print(self._due_date)
        self.set_context("due_date_assignment", self._due_date)
        self.speak_dialog("assignment_module")

    @intent_handler(IntentBuilder("").require("module").require("due_date_assignment"))
    def _handle_assignnment_module(self, message):
        module = message.data.get("module")
        self._module = message.data.get("module")
        print(module)
        self.set_context("module_assignment", module)
        self.speak_dialog("assignment_percentage")

    @intent_handler(IntentBuilder("").require("percentage").require("module_assignment").
            optionally("percent"))
    def _handle_assignment_percentaage(self, message):
        #percentage = message.data.get("percentage")
        self._percentage = message.data.get("percentage")
        self.set_context("percentage_assignment", self._percentage)
        self.speak_dialog("assignment_type")
        print(self._percentage)

    @intent_handler(IntentBuilder("").require("type").require("percentage_assignment"))
    def _handle_assignment_percentage(self, message):
        self._type = message.data.get("type")
        self.speak_dialog("Done")
        self._handle_push_assignment()

    def _handle_push_assignment(self):
        print("getting here")
        now = datetime.now()
        assigned_date = now.strftime('%d/%m/%Y')
        assignment_test = assignment.Assignment(assigned_date, self._module, self._due_date, self._percentage, 0, self._type, self._assignment_name) 
        self.db.pushAssignment(assignment_test)
        print("pushing")


    def _make_assignment(self):
        self.speak_dialog("assignment_name")
        self.set_context("new_assignment", "new assignment")

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return TemplateSkill()
