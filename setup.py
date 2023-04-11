
import distutils
import os
import subprocess

import setuptools
from setuptools.command.develop import develop
from setuptools.command.install import install

def build_js():
    subprocess.check_call(["yarn", "install"], cwd=os.path.join(os.getcwd(), "frontend"))
    subprocess.check_call(["yarn", "build"], cwd=os.path.join(os.getcwd(), "frontend"))

# Build JS code when this package is installed in virtual env
# https://stackoverflow.com/a/36902139
class BuildJSDevelopCommand(develop):
    def run(self):
        self.announce("Building JS code", level=distutils.log.INFO)
        build_js()
        super().run()

class BuildJSInstallCommand(install):
    def run(self):
        self.announce("Building JS code", level=distutils.log.INFO)
        build_js()
        super().run()


setuptools.setup(
    name="geogateway-django-app",
    version="0.0.1",
    description="GeoGateway Django app",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'django>=1.11.16'
    ],
    entry_points="""
[airavata.djangoapp]
geogateway_django_app = geogateway_django_app.apps:GeogatewayDjangoAppConfig
""",
  cmdclass={
        'develop': BuildJSDevelopCommand,
        'install': BuildJSInstallCommand,
    }
)
