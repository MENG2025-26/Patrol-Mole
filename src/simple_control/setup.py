from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'simple_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=['simple_control'],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        (os.path.join('share', 'simple_control', 'launch'),
        glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='patrolmole',
    maintainer_email='patrolmole@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
		'BaseController = simple_control.BaseController:main',
        ],
    },
)
