import unittest
import simple_peewee_flask_webapi


class ModuleTest(unittest.TestCase):

    def __init__(self, methodName):
        super().__init__(methodName)
        self.test_client = None

    def setUp(self):
        simple_peewee_flask_webapi.application_start.app.config[
            'TESTING'] = True
        a = simple_peewee_flask_webapi.application_start.app.test_client()
        self.test_client = a

    def test(self):
        try:
            url = "http://127.0.0.1:5000/get-models/"
            payload = {"id_join_table": "1", "id_simple_table": "1"}
            headers = {'Content-Type': "application/x-www-form-urlencoded"}
            response = self.test_client.post(url, data=payload,
                                             headers=headers)
            self.assertEqual(response.status_code, 200)

            url = "http://127.0.0.1:5000/get-models/"
            payload = {"id_join_table": "2", "id_simple_table": "1"}
            headers = {'Content-Type': "application/x-www-form-urlencoded"}
            response = self.test_client.post(url, data=payload,
                                             headers=headers)
            self.assertEqual(response.status_code, 404)

            url = "http://127.0.0.1:5000/get-models/"
            payload = {"id_join_table": "1", "id_simple_table": "2"}
            headers = {'Content-Type': "application/x-www-form-urlencoded"}
            response = self.test_client.post(url, data=payload,
                                             headers=headers)
            self.assertEqual(response.status_code, 404)

            response = self.test_client.get(
                "http://127.0.0.1:5000/simple-table/?id_simple_table=1")
            self.assertEqual(response.status_code, 200)

            url = "http://127.0.0.1:5000/simple-table/"
            payload = "id_simple_table=1"
            headers = {'Content-Type': "application/x-www-form-urlencoded"}
            response = self.test_client.post(url, data=payload,
                                             headers=headers)
            self.assertEqual(response.status_code, 200)

            response = self.test_client.get(
                "http://127.0.0.1:5000/simple-table/?id_simple_table=2")
            self.assertEqual(response.status_code, 404)

            url = "http://127.0.0.1:5000/join_table/"
            payload = "id_join_table=1"
            headers = {'Content-Type': "application/x-www-form-urlencoded"}
            response = self.test_client.post(url, data=payload,
                                             headers=headers)
            self.assertEqual(response.status_code, 200)

            response = self.test_client.get(
                "http://127.0.0.1:5000/join_table/?id_join_table=1")
            self.assertEqual(response.status_code, 200)

            response = self.test_client.get(
                "http://127.0.0.1:5000/join_table/?id_join_table=2")
            self.assertEqual(response.status_code, 404)
        except Exception as e:
            print(e)
            self.assertFalse(True)


if __name__ == "__main__":
    unittest.main()
