from setuptools import setup, find_packages

setup(
    name="Reactor",
    version="0.1", 
    description="Creates a React project from boilerplate.", 
    author="Fernando Cruz", 
    author_email="quattrococodrilo@gmail.com",
    license="GPL", 
    # url="http://ejemplo.com", 
    packages=find_packages(),
    entry_points="""
        [console_scripts]
        reactor = Reactor.entry_point:execute
    """
)

