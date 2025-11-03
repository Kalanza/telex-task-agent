"""
Mock Telex server for testing without real API calls
"""
from flask import Flask, request, jsonify
from datetime import datetime
import threading


class MockTelexServer:
    """Mock Telex server for testing"""
    
    def __init__(self, port=9001):
        self.app = Flask(__name__)
        self.port = port
        self.messages_received = []
        self.server = None
        self.thread = None
        
        # Setup routes
        @self.app.route('/webhook/telex', methods=['POST'])
        def receive_message():
            data = request.json
            self.messages_received.append({
                'timestamp': datetime.now().isoformat(),
                'data': data
            })
            return jsonify({"status": "received"})
        
        @self.app.route('/messages', methods=['GET'])
        def get_messages():
            return jsonify({"messages": self.messages_received})
        
        @self.app.route('/clear', methods=['POST'])
        def clear_messages():
            self.messages_received.clear()
            return jsonify({"status": "cleared"})
    
    def start(self):
        """Start the mock server in a background thread"""
        if self.server is not None:
            return
        
        def run_server():
            self.app.run(port=self.port, debug=False, use_reloader=False)
        
        self.thread = threading.Thread(target=run_server, daemon=True)
        self.thread.start()
        print(f"Mock Telex server started on port {self.port}")
    
    def stop(self):
        """Stop the mock server"""
        # Flask doesn't have a clean shutdown method, but daemon thread will stop with main process
        self.messages_received.clear()
    
    def get_last_message(self):
        """Get the most recent message received"""
        if self.messages_received:
            return self.messages_received[-1]
        return None
    
    def get_messages_for_user(self, user):
        """Get all messages for a specific user"""
        return [
            msg for msg in self.messages_received 
            if msg['data'].get('sender') == user
        ]
    
    def clear(self):
        """Clear all received messages"""
        self.messages_received.clear()


# Pytest fixture for easy use in tests
import pytest

@pytest.fixture
def mock_telex():
    """Pytest fixture for mock Telex server"""
    server = MockTelexServer()
    server.start()
    
    # Give server time to start
    import time
    time.sleep(0.5)
    
    yield server
    
    server.stop()


# Example usage in tests:
"""
def test_with_mock_telex(mock_telex):
    # Your test code here
    # Mock server is available at http://localhost:9001
    
    # Send a test message
    import requests
    response = requests.post(
        'http://localhost:9001/webhook/telex',
        json={'sender': 'alice', 'message': 'test'}
    )
    
    # Check what was received
    last_message = mock_telex.get_last_message()
    assert last_message['data']['sender'] == 'alice'
"""
