#!/usr/bin/env python3
"""
Backend API server for 2D Puzzle Solver using OR-Tools CP-SAT.
Run this server and the HTML frontend will call it for solving puzzles.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import List, Tuple, Dict, Optional
from ortools.sat.python import cp_model

app = Flask(__name__)
CORS(app)  # Enable CORS for browser requests

Coord = Tuple[int, int]


def find_valid_solution(
    grid: List[List[float]],
    target_sum: float,
    time_limit_s: float = 30.0,
    minimize_total_path_cells: bool = True,
) -> Optional[List[List[Tuple[int, int]]]]:
    """
    Solve the puzzle using CP-SAT with flow-based path modeling.
    
    Args:
        grid: n x n grid where grid[r][c] == 0 means empty cell, >0 means numbered terminal
        target_sum: Target sum for pairs
        time_limit_s: Time limit for solver
        minimize_total_path_cells: Whether to minimize total path cells
        
    Returns:
        A list of paths, where each path is a list of (r, c) coordinates.
        Returns None if infeasible / not found within limit.
    """
    n = len(grid)
    assert all(len(row) == n for row in grid), "Grid must be n x n"
    
    # Use tolerance for floating point comparison
    tolerance = 1e-9
    
    # Collect terminals
    terminals: List[Tuple[Coord, float]] = []
    terminal_set = set()
    for r in range(n):
        for c in range(n):
            if grid[r][c] > 0 or abs(grid[r][c]) > tolerance:  # Handle float numbers
                terminals.append(((r, c), float(grid[r][c])))
                terminal_set.add((r, c))
    
    m = len(terminals)
    if m % 2 != 0:
        return None
    
    # Build candidate pairs whose values sum to target_sum
    candidates: List[Tuple[int, int]] = []
    for i in range(m):
        for j in range(i + 1, m):
            if abs(terminals[i][1] + terminals[j][1] - target_sum) < tolerance:
                candidates.append((i, j))
    
    if not candidates:
        return None
    
    # Quick feasibility: every terminal must have at least one candidate partner
    incident_count = [0] * m
    for i, j in candidates:
        incident_count[i] += 1
        incident_count[j] += 1
    if any(k == 0 for k in incident_count):
        return None
    
    # Precompute adjacency (4-neighbor moves) as directed arcs
    def neighbors(rc: Coord) -> List[Coord]:
        r, c = rc
        out = []
        if r > 0: out.append((r - 1, c))
        if r + 1 < n: out.append((r + 1, c))
        if c > 0: out.append((r, c - 1))
        if c + 1 < n: out.append((r, c + 1))
        return out
    
    all_cells: List[Coord] = [(r, c) for r in range(n) for c in range(n)]
    empty_cells: List[Coord] = [rc for rc in all_cells if rc not in terminal_set]
    
    model = cp_model.CpModel()
    
    # Decision: select which candidate pairs are used (perfect matching)
    use_pair = {}
    for e, (i, j) in enumerate(candidates):
        use_pair[e] = model.NewBoolVar(f"use_pair[{e}]")
    
    # Perfect matching: each terminal used exactly once
    for ti in range(m):
        involved = []
        for e, (i, j) in enumerate(candidates):
            if i == ti or j == ti:
                involved.append(use_pair[e])
        model.Add(sum(involved) == 1)
    
    # Path variables per candidate pair
    # f[e,u,v] for directed edge u->v (u and v adjacent)
    # x[e,c] for empty cell usage
    f = {}
    x = {}
    dist = {}
    
    # Upper bound for distance/order variables
    DMAX = n * n
    BIG_M = DMAX
    
    # Helper to create/get distance var
    def dist_var(e: int, cell: Coord):
        key = (e, cell)
        if key not in dist:
            dist[key] = model.NewIntVar(0, DMAX, f"dist[{e},{cell[0]},{cell[1]}]")
        return dist[key]
    
    for e, (i, j) in enumerate(candidates):
        s = terminals[i][0]
        t = terminals[j][0]
        
        # Create x on empty cells
        for cell in empty_cells:
            x[(e, cell)] = model.NewBoolVar(f"x[{e},{cell[0]},{cell[1]}]")
            # If pair not selected, cannot use cell
            model.Add(x[(e, cell)] <= use_pair[e])
        
        # Create directed edge vars on adjacency arcs
        for u in all_cells:
            for v in neighbors(u):
                f[(e, u, v)] = model.NewBoolVar(f"f[{e},{u[0]},{u[1]}->{v[0]},{v[1]}]")
                model.Add(f[(e, u, v)] <= use_pair[e])
        
        # No traversal through numbered cells other than s,t
        for term_rc, _val in terminals:
            if term_rc != s and term_rc != t:
                # force all incident edges to 0
                u = term_rc
                for v in neighbors(u):
                    model.Add(f[(e, u, v)] == 0)
                    model.Add(f[(e, v, u)] == 0)
        
        # Flow conservation constraints
        for u in all_cells:
            in_edges = [f[(e, v, u)] for v in neighbors(u)]
            out_edges = [f[(e, u, v)] for v in neighbors(u)]
            
            if u == s:
                # source: out - in == use_pair
                model.Add(sum(out_edges) - sum(in_edges) == use_pair[e])
            elif u == t:
                # sink: in - out == use_pair
                model.Add(sum(in_edges) - sum(out_edges) == use_pair[e])
            elif u in terminal_set:
                # other numbered cells already blocked; still ensure no flow
                model.Add(sum(in_edges) == 0)
                model.Add(sum(out_edges) == 0)
            else:
                # empty cell: either unused (0 in/out) or used (1 in and 1 out)
                # Enforce in == out
                model.Add(sum(in_edges) == sum(out_edges))
                # Degree at most 1 to prevent branching
                model.Add(sum(in_edges) <= 1)
                model.Add(sum(out_edges) <= 1)
                # Link to x: if used then exactly one in/out
                model.Add(sum(in_edges) == x[(e, u)])
                model.Add(sum(out_edges) == x[(e, u)])
        
        # Cycle elimination via distance/order constraints
        model.Add(dist_var(e, s) == 0)
        
        # For any used directed edge u->v, enforce dist[v] = dist[u] + 1
        for u in all_cells:
            for v in neighbors(u):
                edge = f[(e, u, v)]
                du = dist_var(e, u)
                dv = dist_var(e, v)
                model.Add(dv >= du + 1 - BIG_M * (1 - edge))
                model.Add(dv <= du + 1 + BIG_M * (1 - edge))
    
    # Vertex-disjointness on empty cells across all pairs
    for cell in empty_cells:
        model.Add(sum(x[(e, cell)] for e in range(len(candidates))) <= 1)
    
    # Objective (optional): minimize total number of used empty cells across all paths
    if minimize_total_path_cells:
        model.Minimize(sum(x.values()))
    
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = float(time_limit_s)
    
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None
    
    # Extract selected pairs and reconstruct paths by following outgoing edges from source
    solutions = []
    
    for e, (i, j) in enumerate(candidates):
        if solver.Value(use_pair[e]) != 1:
            continue
        
        s = terminals[i][0]
        t = terminals[j][0]
        
        # Follow edges from s until t
        path = [s]
        cur = s
        visited = {s}
        while cur != t:
            next_nodes = []
            for v in neighbors(cur):
                if solver.Value(f[(e, cur, v)]) == 1:
                    next_nodes.append(v)
            if len(next_nodes) != 1:
                return None
            cur = next_nodes[0]
            if cur in visited:
                return None
            visited.add(cur)
            path.append(cur)
        
        solutions.append(path)
    
    return solutions


@app.route('/solve', methods=['POST'])
def solve():
    """
    API endpoint to solve a 2D puzzle.
    
    Request body:
    {
        "n": grid size (int),
        "number_cells": [[x, y, value], ...],
        "target_sum": target sum (float)
    }
    
    Response:
    {
        "solution": [[[x, y], ...], ...] or null,
        "error": error message (if any)
    }
    """
    try:
        data = request.json
        
        n = data['n']
        number_cells = data['number_cells']
        target_sum = float(data['target_sum'])
        
        # Create grid
        grid = [[0.0 for _ in range(n)] for _ in range(n)]
        for x, y, value in number_cells:
            grid[x][y] = float(value)
        
        # Solve using CP-SAT
        solution = find_valid_solution(grid, target_sum, time_limit_s=30.0)
        
        if solution is None:
            return jsonify({"solution": []})
        
        return jsonify({"solution": solution})
        
    except Exception as e:
        return jsonify({"error": str(e), "solution": None}), 400


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    print("Starting 2D Puzzle Solver Backend API...")
    print("API will be available at http://localhost:5000")
    print("Make sure to update BACKEND_URL in index.html if using a different port")
    app.run(host='0.0.0.0', port=5000, debug=True)

