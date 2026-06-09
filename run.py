"""
Helper Script - Quick Commands for Common Tasks
Run this to get started with the project
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and display status"""
    print(f"\n{'=' * 60}")
    print(f"📌 {description}")
    print(f"{'=' * 60}")
    print(f"Command: {cmd}\n")
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=False,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Main helper menu"""
    project_root = Path(__file__).parent
    
    print("\n" + "=" * 60)
    print("DSA E-COMMERCE ENGINE - HELPER SCRIPT")
    print("=" * 60)
    print("\nQuick Commands:")
    print("  1. Show Project Structure")
    print("  2. Run Demo Application")
    print("  3. Run All Tests")
    print("  4. Run Cart Tests")
    print("  5. Run Pricing Tests")
    print("  6. Run Recommendation Tests")
    print("  7. Run Integration Tests")
    print("  8. Quick Test Menu")
    print("  9. Exit")
    print("=" * 60)
    
    choice = input("\nSelect option (1-9): ").strip()
    
    commands = {
        '1': (
            f"python {project_root / 'config' / 'project_info.py'}",
            "Displaying Project Structure"
        ),
        '2': (
            f"python {project_root / 'app' / 'main.py'}",
            "Running Demo Application"
        ),
        '3': (
            f"python {project_root / 'tests' / 'run_all_tests.py'}",
            "Running All Tests"
        ),
        '4': (
            f"python {project_root / 'tests' / 'test_cart.py'}",
            "Running Cart Tests"
        ),
        '5': (
            f"python {project_root / 'tests' / 'test_pricing.py'}",
            "Running Pricing Tests"
        ),
        '6': (
            f"python {project_root / 'tests' / 'test_recommendation.py'}",
            "Running Recommendation Tests"
        ),
        '7': (
            f"python {project_root / 'tests' / 'test_integration.py'}",
            "Running Integration Tests"
        ),
        '8': (
            f"python {project_root / 'tests' / 'quick_test.py'}",
            "Opening Quick Test Menu"
        ),
    }
    
    if choice == '9':
        print("\n👋 Goodbye!\n")
        sys.exit(0)
    
    if choice in commands:
        cmd, desc = commands[choice]
        success = run_command(cmd, desc)
        
        if success:
            print("\n✅ Command completed successfully!")
        else:
            print("\n❌ Command failed!")
    else:
        print("\n❌ Invalid option!")
    
    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
