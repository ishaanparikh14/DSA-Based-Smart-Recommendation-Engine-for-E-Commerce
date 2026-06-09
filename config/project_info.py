"""
Project Structure Visualizer
Displays the complete project directory tree
"""

import os
from pathlib import Path


def visualize_tree(directory, prefix="", ignore_dirs=None):
    """
    Visualize directory tree structure.
    
    Args:
        directory: Root directory path
        prefix: Prefix for tree visualization
        ignore_dirs: Set of directory names to ignore
    """
    if ignore_dirs is None:
        ignore_dirs = {'__pycache__', '.git', 'venv', 'env', '.vscode', '.idea'}
    
    try:
        entries = sorted(Path(directory).iterdir(), key=lambda x: (not x.is_dir(), x.name))
    except PermissionError:
        return
    
    dirs = [e for e in entries if e.is_dir() and e.name not in ignore_dirs]
    files = [e for e in entries if e.is_file()]
    
    # Display files first
    for i, file in enumerate(files):
        is_last_file = (i == len(files) - 1) and len(dirs) == 0
        connector = "└── " if is_last_file else "├── "
        print(f"{prefix}{connector}{file.name}")
    
    # Then directories
    for i, dir_path in enumerate(dirs):
        is_last = i == len(dirs) - 1
        connector = "└── " if is_last else "├── "
        extension = "    " if is_last else "│   "
        
        print(f"{prefix}{connector}{dir_path.name}/")
        visualize_tree(dir_path, prefix + extension, ignore_dirs)


def display_project_info():
    """Display project information and structure"""
    project_root = Path(__file__).parent.parent
    
    print("\n" + "=" * 70)
    print("DSA E-COMMERCE PERSONALIZATION ENGINE")
    print("Production-Grade Project Structure")
    print("=" * 70)
    
    print("\n📁 Project Root:", project_root)
    print("\n🌳 Directory Tree:\n")
    
    visualize_tree(project_root)
    
    print("\n" + "=" * 70)
    print("📊 PROJECT STATISTICS")
    print("=" * 70)
    
    # Count files
    stats = {
        'src_files': 0,
        'test_files': 0,
        'config_files': 0,
        'app_files': 0,
        'total_lines': 0
    }
    
    for root, dirs, files in os.walk(project_root):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if d not in {'__pycache__', '.git', 'venv', 'env'}]
        
        for file in files:
            if file.endswith('.py'):
                file_path = Path(root) / file
                
                # Count lines
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = len(f.readlines())
                        stats['total_lines'] += lines
                except:
                    pass
                
                # Categorize files
                if 'src' in root:
                    stats['src_files'] += 1
                elif 'tests' in root:
                    stats['test_files'] += 1
                elif 'config' in root:
                    stats['config_files'] += 1
                elif 'app' in root:
                    stats['app_files'] += 1
    
    print(f"\n📦 Source Files: {stats['src_files']}")
    print(f"🧪 Test Files: {stats['test_files']}")
    print(f"⚙️  Config Files: {stats['config_files']}")
    print(f"🚀 App Files: {stats['app_files']}")
    print(f"📝 Total Lines of Code: {stats['total_lines']:,}")
    
    print("\n" + "=" * 70)
    print("🎯 KEY COMPONENTS")
    print("=" * 70)
    
    components = [
        ("Shopping Cart", "Doubly Linked List", "O(1) operations"),
        ("User Session", "Stack + Queue", "LIFO + FIFO tracking"),
        ("Dynamic Pricing", "Sorted Rules (RBT)", "O(k) range queries"),
        ("Recommendations", "Graph + PageRank", "O(iter × edges)"),
        ("Deal Selection", "Min-Heap", "O(log k) insertions"),
        ("Bundle Optimization", "Dynamic Programming", "O(n × budget)")
    ]
    
    for name, ds, complexity in components:
        print(f"\n{name:.<25} {ds:.<20} {complexity}")
    
    print("\n" + "=" * 70)
    print("\n✅ Project structure created successfully!")
    print("🚀 Run 'python app/main.py' to see the demo")
    print("🧪 Run 'python tests/run_all_tests.py' to run all tests")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    display_project_info()
