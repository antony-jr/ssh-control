import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ssh_control", # Replace with your own username
    version="0.0.1",
    author="Antony Jr.",
    author_email="antonyjr@protonmail.com",
    description="A simple and power tool to mange ssh server remotely with GPG.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antony-jr/shell-control",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
    python_requires='>=3.6',
    install_requires = ['requests' , 'rich' , 'python-gnupg'],
    entry_points = {
        'console_scripts': [
            'ssh-control=ssh_control:ExecuteClient',
            'ssh-control-configure=ssh_control:ExecuteConfigure',
        ],
    }
)
