from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'motor_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        (os.path.join('share', 'motor_controller', 'launch'),
        glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='patrolmole',
    maintainer_email='patrolmole@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
		'motor_node = motor_controller.motor_node:main',
		'encoder_publisher = motor_controller.encoder_publisher:main',
		'BaseController = motor_controller.BaseController:main',
	        'PID_control = motor_controller.PID_control:main',
		'armcontrol = motor_controller.armcontrol:main',
		'custom_teleop = motor_controller.custom_teleop:main',
        ],
    },
)
