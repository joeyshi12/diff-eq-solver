from setuptools import setup

if __name__ == "__main__":
    setup(
        name="diffeq_solver_tk",
        author="Joey Shi",
        description="tk application for solving differential equations",
        entry_points={
            "console_scripts": [
                "detk=diffeq_solver_tk.__main__:main"
            ]
        }
    )
