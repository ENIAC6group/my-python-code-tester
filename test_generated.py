import pytest
import json

import dijkstra
import bubble_sort

with open('test_cases.json') as f:
    test_cases = json.load(f)

def test_dijkstra_dijkstra():
    for case in test_cases.get('dijkstra.dijkstra', []):
        result = dijkstra.dijkstra(*case['input'])
        assert result == case['expected'], f"Failed: dijkstra.dijkstra({case['input']}) = {result}, expected {case['expected']}"

def test_bubble_sort_bubble_sort():
    for case in test_cases.get('bubble_sort.bubble_sort', []):
        result = bubble_sort.bubble_sort(*case['input'])
        assert result == case['expected'], f"Failed: bubble_sort.bubble_sort({case['input']}) = {result}, expected {case['expected']}"

