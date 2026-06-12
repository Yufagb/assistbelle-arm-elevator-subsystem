import os

joints = [1, 2, 3, 4, 5]
types = ['step', 'ramp', 'trap']

base_path = "/home/f15/robot-project/ros2_ws/src/can_comm_pkg/can_comm_pkg/apps/test"

template = """#!/usr/bin/env python3
import sys
import os

# Add parent directory to path to import test_lib (3 levels up: jX -> type -> articular -> test)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from test_lib import run_test

def main():
    # Joint {j}, Type {t}
    run_test(joint_idx={j}, profile_type='{t}', script_path=__file__)

if __name__ == '__main__':
    main()
"""

for j in joints:
    for t in types:
        # Structure: apps/test/articular/{type}/j{joint}.py
        folder = os.path.join(base_path, "articular", t)
        filename = os.path.join(folder, f"j{j}.py")
        
        content = template.format(j=j, t=t)
        
        with open(filename, 'w') as f:
            f.write(content)
        
        os.chmod(filename, 0o755)
        print(f"Created {filename}")
