from setuptools import setup

packages = ["p8_integration_tests",
            "p8_integration_tests.scripts"]
print ("this is a very long line to intentionally break flake 8. blah blah blah")

setup(
    packages=packages,
)
