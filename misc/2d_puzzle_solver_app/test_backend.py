#!/usr/bin/env python3
"""
Quick test script to verify the backend API works correctly.
Run this after starting the backend server.
"""

import requests
import json

# Test case 7 from the notebook
test_data = {
    "n": 8,
    "number_cells": [
        [0, 0, 2.3],
        [1, 6, 2.5],
        [2, 1, 4.5],
        [3, 3, 1.3],
        [3, 5, 1.2],
        [4, 0, 3.8],
        [6, 1, 2.5],
        [6, 5, 0.5],
        [7, 4, 3.7],
        [7, 7, 2.7]
    ],
    "target_sum": 5.0
}

try:
    print("Testing backend API...")
    response = requests.post('http://localhost:5000/solve', json=test_data)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('solution'):
            print(f"✓ Solution found with {len(result['solution'])} paths!")
            for i, path in enumerate(result['solution']):
                print(f"  Path {i+1} (length {len(path)}): {path[:3]}...{path[-3:]}")
        else:
            print("✗ No solution found")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)
        
except requests.exceptions.ConnectionError:
    print("✗ Could not connect to backend. Make sure the server is running:")
    print("  python puzzle_backend.py")
except Exception as e:
    print(f"✗ Error: {e}")

