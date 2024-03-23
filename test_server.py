import http
import unittest
from http.server import HTTPServer
from server import SimpleHTTPRequestHandler
import http.client
import json
import threading

class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_address = ('localhost', 8000)
        cls.server = HTTPServer(cls.server_address, SimpleHTTPRequestHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()

     def test_get_method(self):
        # Establish a connection to the server and initiate a GET request.
        connection = http.client.HTTPConnection(*self.server_address)
        connection.request('GET', '/')
        response = connection.getresponse()

        # Retrieve and decode the server's response.
        data = response.read().decode()
        connection.close()

        # Verify the server's response status, reason, and content type.
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'application/json')

        # Deserialize the JSON response and confirm its content matches expectations.
        response_data = json.loads(data)
        self.assertEqual(response_data, {'message': 'This is a GET request response'})

    def test_post_method(self):
        # Prepare the JSON payload for the POST request.
        payload = json.dumps({'key': 'value'})

        # Open a connection and submit a POST request with the JSON payload.
        connection = http.client.HTTPConnection(*self.server_address)
        headers = {'Content-Type': 'application/json'}
        connection.request('POST', '/', body=payload, headers=headers)
        response = connection.getresponse()

        # Obtain and decode the server's reply.
        data = response.read().decode()
        connection.close()

        # Ensure the server's reply meets the expected criteria.
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'application/json')

        # Expect the server to mirror the sent data in its response.
        expected_response = {'received': {'key': 'value'}}

        # Decode the JSON response and verify its accuracy against expectations.
        response_data = json.loads(data)
        self.assertEqual(response_data, expected_response)


if __name__ == '__main__':
    unittest.main()
