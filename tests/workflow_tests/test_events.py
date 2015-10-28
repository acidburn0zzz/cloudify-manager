########
# Copyright (c) 2015 GigaSpaces Technologies Ltd. All rights reserved
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

from datetime import datetime

from elasticsearch import Elasticsearch
from testenv.utils import get_resource as resource
from testenv.utils import deploy_application as deploy
from testenv import TestCase


class EventsTest(TestCase):

    def _es_log_handler(self, output, event):
        timestamp = datetime.now()
        event['@timestamp'] = timestamp
        es_client = Elasticsearch()
        doc_type = event['type']

        # simulate logstash index
        index = 'logstash-{0}'.format(timestamp.strftime('%Y.%m.%d'))

        res = es_client.index(index=index,
                              doc_type=doc_type,
                              body=event)
        if not res['created']:
            raise Exception('failed to write to elasticsearch')

    def setUp(self):
        super(EventsTest, self).setUp()
        from testenv import testenv_instance
        testenv_instance.handle_logs = self._es_log_handler
        self.first_deployment_id, self.first_deployment_blueprint_id, \
            self.sec_deployment_id, self.sec_deployment_blueprint_id = \
            self._put_two_deployments()

    def test_connection(self):
        filters = {'deployment_id': self.first_deployment_id}
        res = self.client.events.list(**filters)
        self.assertGreater(len(res['hits']['hits']), 0)

    def _put_two_deployments(self):
        dsl_path = resource("dsl/deployment_modification_operations.yaml")
        first_deployment, _ = deploy(dsl_path)
        sec_deployment, _ = deploy(dsl_path)
        return first_deployment.id, first_deployment.blueprint_id, \
            sec_deployment.id, sec_deployment.blueprint_id
