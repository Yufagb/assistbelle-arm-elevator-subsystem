#!/usr/bin/env python3
import sys
import os

# Add parent directory to path to import test_lib (3 levels up: jX -> type -> articular -> test)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from test_lib import run_test

def main():
    # Joint 5, Type ramp
    run_test(joint_idx=5, profile_type='ramp', script_path=__file__)

if __name__ == '__main__':
    main()
