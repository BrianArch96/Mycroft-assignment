import pymongo
from bson.json_util import dumps
import json
from pymongo import MongoClient
from .assignment import Assignment
url = "mongodb://Archie96:hannah10@mycroft-assignment-shard-00-00-1rt5b.mongodb.net:27017,mycroft-assignment-shard-00-01-1rt5b.mongodb.net:27017,mycroft-assignment-shard-00-02-1rt5b.mongodb.net:27017/test?ssl=true&replicaSet=Mycroft-Assignment-shard-0&authSource=admin&retryWrites=true"
assignments_collection = "Assignments"
class db_helper(object):
    
    def __init__(self, studentID):
        #setup connection to database
        self.client = MongoClient(url)
        #set which student's collection of data we will be working with
        self._db = self.client[studentID]
        self._assignment_collection = None

    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, value):
        #setter for db
        self._db = value

    @property
    def assignment_collection(self):
        return self._assignment_collection

    @assignment_collection.setter
    def assignment_collection(self, value):
        self._assignment_collection = value

    def pushAssignment(self, newAssignment):

        assignment = {"date_issued": newAssignment.date_issued,
                "module_id": newAssignment.module_id,
                "due_date": newAssignment.due_date,
                "total_percentage": newAssignment.total_per,
                "accumulated_percentage": newAssignment.acc_per,
                "assignment_type": newAssignment.assignment_type,
                "name": newAssignment.name 
                }

        self.assignment_collection = self.db[assignments_collection]

        #checks to see if assignment name is already in the module collection, if so return
        #without pushing anything

        for document in self.assignment_collection.find():
            if newAssignment.name == self.parseAssignment(document).name:
                print("Assignment name already exists")
                return 0

        print("yurting") 
        post_id = self.assignment_collection.insert_one(assignment).inserted_id
        return 1
    
    def getAllAssignments(self):
        self.assignment_collection = self.db[assignments_collection]
        assignments = []
        
        for assignment_bson in self.assignment_collection.find({}):
            assignment = self.parseAssignment(assignment_bson)
            if not assignment:
                return None
            assignments.append(assignment)
        if len(assignments) == 0:
            return None
        return assignments

    def getAssignment(self, assignment_name):
        self.assignment_collection = self.db[assignments_collection]
        assignment_uni = self.assignment_collection.find_one({"name": assignment_name})
        if not assignment_uni:
            print("Error - Could not find an assignment with that name")
            return

        return self.parseAssignment(assignment_uni)
    
    def getAllModuleAssignments(self, module_id):
        all_assignments = self.getAllAssignments()
        module_assignments = []

        for assignment in all_assignments:
            if module_id == assignment.module_id:
                module_assignments.append(assignment)
        
        return module_assignments

    def parseAssignment(self, assignment_Bson):
        #dumps the BSON dictionary into a usable JSON format
        assignment_json = dumps(assignment_Bson)
        #formats the JSON in a way so that we can extract members of the JSON object
        #Assigns the members of this object to an assignment class which is then returned
        j = json.loads(assignment_json)
        return Assignment(j['date_issued'], j['module_id'], j['due_date'], j['total_percentage'],
                j['accumulated_percentage'], j['assignment_type'], j['name'])

    #gets the number of assignments for a given module
    def assignmentCount(self):
        self.assignment_collection = self.db[assignments_collection]
        return self.assignment_collection.count()
   
    #These update functions could possibly be squished into one function, taking two parameters, the name of the field and the new value
    #Might look into refining it later down the line

    #update assignment due date
    def updateAssignmentDueDate(self, assignment_name, new_due_date):
        self.assignment_collection = self.db[assignments_collection]
        try:
            self.assignment_collection.update_one(
                {"name":assignment_name},
                { "$set":
                    {
                        "due_date":new_due_date
                    }
                }, upsert=False)
        except pymongo.errors.PyMongoError as e:
            print(e)               

    #update total percentage for assignment
    def updateAssignmentTotalPer(self, assignment_name, new_total_per):
        self.assignment_collection = self.db[assignments_collection]
        try:
            self.assignment_collection.update_one(
                {"name":assignment_name},
                { "$set":
                    {
                        "total_percentage":new_total_per
                    }
                }, upsert=False)
        except pymongo.errors.PyMongoError as e:
            print(e)

    #update accumulated percentage
    def updateAssignmentAccPer(self, assignment_name, new_accumulated_per):
        self.assignment_collection = self.db[assignments_collection]
        try:
            self.assignment_collection.update_one(
                {"name":assignment_name},
                { "$set":
                    {
                        "accumulated_percentage":new_accumulated_per
                    }
                }, upsert=False)
        except pymongo.errors.PyMongoError as e:
            print(e)       

    #update assignment type
    def updateAssignmentType(self, assignment_name, new_assignment_type):
        self.assignment_collection = self.db[assignments_collection]
        try:
            self.assignment_collection.update_one(
                {"name":assignment_name},
                { "$set":
                    {
                        "assignment_type":new_assignment_type
                    }
                }, upsert=False)
        except pymongo.errors.PyMongoError as e:
            print(e)               

    #update assignment name
    def updateAssignmentName(self, assignment_name, new_assignment_name):
        self.assignment_collection = self.db[assignments_collection]
        try:
            self.assignment_collection.update_one(
                {"name":assignment_name},
                { "$set":
                    {
                        "name":new_assignment_name
                    }
                }, upsert=False)
        except pymongo.errors.PyMongoError as e:
            print(e)           

    #remove a given assignment
    def removeAssignment(self, assignment_name):
        self.assignment_collection = self.db[assignments_collection]
        self.assignment_collection.remove({"name":assignment_name})

    #def removeModule(self, module_id):


