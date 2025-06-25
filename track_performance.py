import importlib.util
import tracemalloc
import time
import json

def load_function_from_file(file_path, func_name):
    spec = importlib.util.spec_from_file_location("user_module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, func_name)

def track_function(file_path, func_name, args):
    try:
        func = load_function_from_file(file_path, func_name)
    except Exception as e:
        print(f"❌ Failed to load {func_name} from {file_path}: {e}")
        return

    print(f"\n=== Benchmarking {func_name} from {file_path} ===")
    
    # Start memory tracking
    tracemalloc.start()
    start_time = time.time()

    try:
        result = func(*args)
    except Exception as e:
        print(f"❌ Error during execution: {e}")
        return

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"✅ Output: {result}")
    print(f"⏱ Time Taken: {end_time - start_time:.6f} seconds")
    print(f"📦 Memory Used: {current / 1024:.2f} KB | Peak: {peak / 1024:.2f} KB")

def main():
    with open("performance_config.json") as f:
        data = json.load(f)

    for file, funcs in data.items():
        for func_name, cases in funcs.items():
            for args in cases:
                track_function(file, func_name, args)

if __name__ == "__main__":
    main()

