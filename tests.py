import unittest
from unittest.mock import Mock, MagicMock, patch, create_autospec
from datetime import datetime
from queue import Queue
import socket
import pandas as pd
from client import Client, update_logical_clock 

class TestMethods(unittest.TestCase):
    def setUp(self):
        self.port = 2000
        self.id = 1
        self.run_no = 1
        # self.client = Client(self.port, self.id, self.run_no)
        # self.client = MagicMock()
        self.client = create_autospec(Client)
        self.clock_time = 100
        self.message = b"2 100"
        self.client.logical_clock = self.clock_time
        self.df = pd.DataFrame(columns=['event_type', 'system_time', 'old_clock_time', 'new_clock_time', 'message_queue_length'])
        self.client.messages = Queue()
        self.client.messages.put(self.message)

    def test_update_logical_clock(self):
        self.assertEqual(update_logical_clock(2, 1), 3)
        self.assertEqual(update_logical_clock(5, 10), 11)
        self.assertEqual(update_logical_clock(100, 100), 101)

    def test_listen(self):
        expected_output = self.message
        self.client.listen.return_value = expected_output
        actual_output = self.client.listen()
        self.assertEqual(actual_output, expected_output)

    # def test_listen(self):
    #     with patch('socket.socket', spec=socket.socket) as mock_socket:
    #         mock_sock_inst = Mock()
    #         mock_socket.return_value = mock_sock_inst
    #         mock_sock_inst.recv.return_value = self.message

    #         expected_output = self.message.decode()
    #         actual_output = self.client.listen()

    #         self.assertEqual(actual_output, expected_output)

if __name__ == '__main__':
    unittest.main()