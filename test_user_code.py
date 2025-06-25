
import pytest
import importlib.util

# Load bubble module
spec1 = importlib.util.spec_from_file_location("bubble_module", r"bubble.py")
bubble_module = importlib.util.module_from_spec(spec1)
spec1.loader.exec_module(bubble_module)

# Load dijkstra module
spec2 = importlib.util.spec_from_file_location("dijkstra_module", r"dijkstra.py")
dijkstra_module = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(dijkstra_module)

def test_bubble_sort():
    assert hasattr(bubble_module, 'bubble_sort'), "bubble_sort function not found"
    data = [5, 1, 4, 2, 8]
    result = bubble_module.bubble_sort(data[:])
    assert result == sorted(data), "bubble_sort output is incorrect"

def test_dijkstra():
    assert hasattr(dijkstra_module, 'dijkstra'), "dijkstra function not found"
    graph = {
        'A': {'B': 1, 'C': 4},
        'B': {'C': 2, 'D': 5},
        'C': {'D': 1},
        'D': dict()
    }
    result = dijkstra_module.dijkstra(graph, 'A')
    assert isinstance(result, dict), "dijkstra output is not a dictionary"
    assert result.get('D', None) == 4, "Shortest distance to D is incorrect"
