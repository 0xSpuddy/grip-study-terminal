from setuptools import setup, find_packages

setup(
    name="grip_strength_terminal",
    version="0.1.0",
    packages=find_packages(include=['grip_strength_terminal', 'grip_strength_terminal.*']),
    install_requires=[
        'telliot-feeds',
        'telliot-core',
        'rich',  # for better terminal formatting
        'termcolor',  # for colored output
        'pyfiglet'  # for ASCII art text
    ],
    entry_points={
        'console_scripts': [
            'grip-terminal=grip_strength_terminal.main:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A terminal-based grip strength game interface for Tellor blockchain",
    # long_description=open('README.md').read(),
    # long_description_content_type="text/markdown",
    url="https://github.com/yourusername/grip-strength-terminal",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
) 