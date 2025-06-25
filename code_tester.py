import os
import importlib.util
import json

def load_functions(filepath):
    """Dynamically load all non-dunder functions from file."""
    functions = {}
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"{filepath} not found.")

    modname = os.path.splitext(os.path.basename(filepath))[0]
    spec = importlib.util.spec_from_file_location(modname, filepath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    for name in dir(mod):
        if callable(getattr(mod, name)) and not name.startswith("__"):
            functions[f"{modname}.{name}"] = name

    return functions

def generate_test_file(function_map, test_file="test_generated.py", json_file="test_cases.json"):
    with open(test_file, "w") as f:
        f.write("import pytest\n")
        f.write("import json\n\n")

        # Import required modules
        imported = set()
        for full_name in function_map:
            module = full_name.split(".")[0]
            if module not in imported:
                f.write(f"import {module}\n")
                imported.add(module)

        # Load test cases
        f.write("\nwith open('test_cases.json') as f:\n")
        f.write("    test_cases = json.load(f)\n\n")

        # Create test functions
        for full_name in function_map:
            module, func = full_name.split(".")
            f.write(f"def test_{module}_{func}():\n")
            f.write(f"    for case in test_cases.get('{full_name}', []):\n")
            f.write(f"        result = {module}.{func}(*case['input'])\n")
            f.write(f"        assert result == case['expected'], f\"Failed: {full_name}({{case['input']}}) = {{result}}, expected {{case['expected']}}\"\n\n")

def main():                         
    print("🧪 Welcome to Easy Code Tester v2")
    paths = input("Enter paths of files to test (comma separated): ").split(",")

    all_funcs = {}
    for path in paths:
        path = path.strip()
        try:
            funcs = load_functions(path)
            all_funcs.update(funcs)
        except Exception as e:
            print(f"❌ Error loading from {path}: {e}")

    if not all_funcs:
        print("🚫 No functions found.")
        return

    print("\n✅ Found Functions:")
    for func in all_funcs:
        print("  -", func)

    generate_test_file(all_funcs)
    print("\n📁 Generated test file: test_generated.py")
    print("📄 Add test cases to: test_cases.json")
    print("▶️ Run: pytest test_generated.py -s")

if __name__ == "__main__":
    main()

