import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'midnight_tuner'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mariamehab',
    maintainer_email='mariamehab@todo.todo',
    description='Midnight Tuner ROS2 package',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'tuner_controller = midnight_tuner.tuner_controller:main',
        ],
    },
)
