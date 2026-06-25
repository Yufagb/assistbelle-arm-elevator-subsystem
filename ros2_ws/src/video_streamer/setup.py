from setuptools import find_packages, setup

package_name = 'video_streamer'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Yuri Fabian Vilela Obando',
    maintainer_email='yuri.vilela@utec.edu.pe',
    description='ROS 2 video streaming utilities for the Assistbelle project.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'video_publisher = video_streamer.video_publisher:main',
            'video_subscriber = video_streamer.video_subscriber:main',
        ],
    },
)
