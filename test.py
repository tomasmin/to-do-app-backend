from app import app
import unittest
from flask import json

class TaskTest(unittest.TestCase):

    # Check if response is 200
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/tasks")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # Check if response is 400 when trying to post empty name
    def test_post_empty_name(self):
        tester = app.test_client(self)
        response = tester.post("/add", json={'name': '', 'description': ''})
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)

    # Check if response is 201 when creating a task and 200 when deleting it
    def test_post_and_delete(self):
        tester = app.test_client(self)
        response = tester.post("/add", json={'name': 'unittest123', 'description': ''})
        statuscode = response.status_code
        self.assertEqual(statuscode, 201)
        data = json.loads(response.get_data())
        task_object = next((x for x in data if x["name"] == 'unittest123'), None)
        taskid = task_object['id']
        response = tester.delete(f"/tasks/{taskid}")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

if __name__ == "__main__":
    unittest.main()