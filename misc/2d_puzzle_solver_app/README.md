# 2D Puzzle Solver - Backend API Setup

This puzzle solver uses OR-Tools CP-SAT via a Python backend API for accurate solving.

## Setup Instructions

### 1. Install Dependencies

```bash
pip install flask flask-cors ortools
```

### 2. Start the Backend Server

```bash
python puzzle_backend.py
```

The server will start on `http://localhost:5000`

### 3. Open the HTML Frontend

Open `index.html` in your web browser. The frontend will automatically try to connect to the backend API.

## Configuration

### Using Backend API (Recommended)

The HTML file is configured to use the backend API by default. The backend URL is set in `index.html`:

```javascript
const BACKEND_URL = 'http://localhost:5000/solve';
```

If your backend runs on a different port or host, update this URL.

### Using JavaScript Solver Only (Offline)

To use the JavaScript solver without the backend, edit `index.html` and set:

```javascript
const USE_BACKEND_API = false;
```

This will use the JavaScript constraint-based solver, which works offline but may be slower and less accurate for complex puzzles like test case 7.

## API Endpoint

### POST /solve

Solves a 2D puzzle using OR-Tools CP-SAT.

**Request:**
```json
{
  "n": 8,
  "number_cells": [[0, 0, 2.3], [1, 6, 2.5], ...],
  "target_sum": 5.0
}
```

**Response:**
```json
{
  "solution": [[[0, 0], [0, 1], ...], [[1, 6], [2, 6], ...]]
}
```

## Testing

Test case 7 from the notebook:
- Grid size: 8x8
- Number cells: [(0, 0, 2.3), (1, 6, 2.5), (2, 1, 4.5), (3, 3, 1.3), (3, 5, 1.2), (4, 0, 3.8), (6, 1, 2.5), (6, 5, 0.5), (7, 4, 3.7), (7, 7, 2.7)]
- Target sum: 5

The CP-SAT backend should solve this correctly.

