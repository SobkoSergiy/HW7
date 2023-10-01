from setuptools import setup, find_namespace_packages

setup (name = "clean-folder",
    version = "0.0.1",
    description = "Sweep a trash folder",
    url = "https://github.com/SobkoSergiy/HW7",
    author = "SobkoSergiy",
    author_email = "integral2003@gmail.com",
    license = "MIT",
    packages = find_namespace_packages(),             
    entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']}
    )
