########
# Copyright (c) 2013 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

__author__ = "idanmo"

from setuptools import setup


setup(
    name='cloudify-tests',
    version='3.0',
    author='Idan Moyal',
    author_email='idan@gigaspaces.com',
    packages=['plugins',
              'plugins.cloudmock',
              'plugins.connection_configurer_mock',
              'plugins.context_plugin',
              'plugins.plugin_installer',
              'plugins.testmockoperations',
              'plugins.worker_installer'],
    license='LICENSE',
    description='Cloudify workflow python tests',
    zip_safe=False,
    install_requires=[
        "cloudify-plugins-common==3.0",
        "cloudify-rest-client==3.0",
        "pika==0.9.13",
        "bernhard==0.1.0",
        'elasticsearch==1.0.0'
    ]
)
