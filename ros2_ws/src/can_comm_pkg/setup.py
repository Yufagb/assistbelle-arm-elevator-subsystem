from setuptools import setup, find_packages

package_name = 'can_comm_pkg'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/urdf', ['urdf/robot.urdf']),
        ('share/' + package_name + '/launch', ['launch/rviz_sim.launch.py']),
        ('share/' + package_name + '/rviz', ['rviz/config.rviz']),
    ],
    install_requires=['setuptools','rclpy','std_msgs','sensor_msgs','numpy'],
    zip_safe=True,
    maintainer='Yuri Fabian Vilela Obando',
    maintainer_email='yuri.vilela@utec.edu.pe',
    description='CAN communication package (ROS 2)',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'can_node = can_comm_pkg.core.can_node:main',
            'can_cli = can_comm_pkg.apps.cli_node:main',
            'can_slider = can_comm_pkg.apps.can_slider:main',
            'can_traj = can_comm_pkg.apps.can_traj:main',
            'ik_node = can_comm_pkg.apps.ik_node:main',
            'viz_node = can_comm_pkg.apps.viz_node:main',
            'can_traj_offline = can_comm_pkg.apps.can_traj_offline:main',
            'j4_test = can_comm_pkg.apps.j4_performance_test:main',
            'can_traj_old = can_comm_pkg.legacy.can_traj_old:main',
            'cinematica_directa = can_comm_pkg.apps.cinematica_directa:main',
            'cinematica_inversa = can_comm_pkg.apps.cinematica_inversa:main',
            'control_teclado = can_comm_pkg.apps.control_teclado:main',
            'control_teclado_4gdl = can_comm_pkg.apps.control_teclado_4gdl:main',
            'control_teclado_sistemas_separados = can_comm_pkg.apps.control_teclado_sistemas_separados:main',
            'barcode_detector = can_comm_pkg.apps.barcode_detector:main',
            'visualize_dh = can_comm_pkg.apps.visualize_dh:main',
            'sequence_executor = can_comm_pkg.apps.sequence_executor:main',
            'visualize_sequence = can_comm_pkg.apps.visualize_sequence:main',
            'control_teclado_trapezoidal = can_comm_pkg.apps.control_teclado_trapezoidal:main',
            # Tests J1
            'j1_step = can_comm_pkg.apps.test.articular.step.j1:main',
            'j1_ramp = can_comm_pkg.apps.test.articular.ramp.j1:main',
            'j1_trap = can_comm_pkg.apps.test.articular.trap.j1:main',
            # Tests J2
            'j2_step = can_comm_pkg.apps.test.articular.step.j2:main',
            'j2_ramp = can_comm_pkg.apps.test.articular.ramp.j2:main',
            'j2_trap = can_comm_pkg.apps.test.articular.trap.j2:main',
            # Tests J3
            'j3_step = can_comm_pkg.apps.test.articular.step.j3:main',
            'j3_ramp = can_comm_pkg.apps.test.articular.ramp.j3:main',
            'j3_trap = can_comm_pkg.apps.test.articular.trap.j3:main',
            # Tests J4
            'j4_step = can_comm_pkg.apps.test.articular.step.j4:main',
            'j4_ramp = can_comm_pkg.apps.test.articular.ramp.j4:main',
            'j4_trap = can_comm_pkg.apps.test.articular.trap.j4:main',
            # Tests J5
            'j5_step = can_comm_pkg.apps.test.articular.step.j5:main',
            'j5_ramp = can_comm_pkg.apps.test.articular.ramp.j5:main',
            'j5_trap = can_comm_pkg.apps.test.articular.trap.j5:main',
            'debug_ax_bx = can_comm_pkg.apps.debug_ax_bx:main',
            'loop_coordinate = can_comm_pkg.apps.loop_coordinate:main',
            'control_teclado_record = can_comm_pkg.apps.control_teclado_record:main',
            'product_identifier = can_comm_pkg.apps.product_identifier:main',
        ],
    },
)
