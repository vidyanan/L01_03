import unittest
from user import assignments

from django.http import QueryDict
from django.http import HttpResponse

from django.conf import settings

from library import database as db
from library import tools

class AssignmentsTest(unittest.TestCase):
    @patch.object(assignments.db.Query, 'dbQuery')
    
    def setUp(self):
        #requests
        mockTA = MagicMock()
        mockTA.session.return_value = {"user":{"role": "ta"}}
        
        mockStudent = MagicMock()
        mockStudent.session.return_value = {"user":{"role": "student"}}
        
    def testGetAssignmentsTA(self, mockTA, mock_dbQuery):
        mock_dbQuery.return_value = {"id": 1, "name": "a1", "start-date": "2017-01-01 00:00:00", "end-date": "2018-01-01 00:00:00"}
        self.assertEqual(assignments.getAssignments(mockTA), {"assignments": [{"grade": "0.00", "start-date": "2017-01-01 00:00:00", "end-date": "2018-01-01 00:00:00", "id": 1, "name": "a1"}]})
        
    def testGetAssignmentsSTU(self, mockStudent, mock_dbQuery):
        mock_dbQuery.return_value = {"id": 1, "name": "a1", "start-date": "2017-01-01 00:00:00", "end-date": "2018-01-01 00:00:00"}
        self.assertEqual(assignments.getAssignments(mockStudent), {"assignments": [{"grade": "0.00", "start-date": "2017-01-01 00:00:00", "end-date": "2018-01-01 00:00:00", "id": 1, "name": "a1"}]})