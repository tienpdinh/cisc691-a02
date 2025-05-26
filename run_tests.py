#!/usr/bin/env python3
"""
Test runner for the authorship attribution system.

Usage:
    python run_tests.py              # Run all tests
    python run_tests.py -v           # Verbose output
    python run_tests.py TestClass    # Run specific test class
"""

import unittest
import sys
import os

# Add src and tests to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))

def run_tests():
    """Discover and run all tests."""
    
    # Discover tests
    loader = unittest.TestLoader()
    test_dir = os.path.join(os.path.dirname(__file__), 'tests')
    suite = loader.discover(test_dir, pattern='test_*.py')
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2 if '-v' in sys.argv else 1)
    result = runner.run(suite)
    
    # Print coverage summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    return len(result.failures) + len(result.errors) == 0

def main():
    if len(sys.argv) > 1 and sys.argv[1] not in ['-v', '--verbose']:
        # Run specific test
        test_name = sys.argv[1]
        suite = unittest.TestLoader().loadTestsFromName(f'tests.{test_name}')
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        return len(result.failures) + len(result.errors) == 0
    else:
        return run_tests()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)