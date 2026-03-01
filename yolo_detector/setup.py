from setuptools import find_packages, setup

package_name = 'yolo_detector'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        # Register the package
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),

        # Install package.xml
        ('share/' + package_name, ['package.xml']),

        # Install launch files
        ('share/' + package_name + '/launch', ['launch/detection_pipeline.launch.py']),

        # Install model files
        ('share/' + package_name + '/models', ['models/custom_yolo.onnx']),
        # If you also have labels.txt, include it here:
        # ('share/' + package_name + '/models', ['models/labels.txt']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='zunaid',
    maintainer_email='zunaid@todo.todo',
    description='YOLO object detection node',
    license='Apache License 2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'yolo_node = yolo_detector.yolo_node:main',
        ],
    },
)

