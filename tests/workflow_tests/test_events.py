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
from testenv import ElasticSearchProcess
from testenv.constants import LOG_INDICES_PREFIX


class EventsTest(TestCase):

    def _es_log_handler(self, output, event):
        timestamp = datetime.now()
        event['@timestamp'] = timestamp
        es_client = Elasticsearch()
        doc_type = event['type']

        # simulate log index
        index = '{0}{1}'.format(LOG_INDICES_PREFIX,
                                timestamp.strftime('%Y.%m.%d'))

        res = es_client.index(index=index,
                              doc_type=doc_type,
                              body=event)
        if not res['created']:
            raise Exception('failed to write to elasticsearch')

    def setUp(self):
        super(EventsTest, self).setUp()
        from testenv import testenv_instance
        testenv_instance.handle_logs = self._es_log_handler
        self.deployment_id = self._create_deployment()

    def tearDown(self):
        ElasticSearchProcess.remove_log_indices()
        super(EventsTest, self).tearDown()

    def test_exclude_logs(self):
        events = self.client.events.list()
        for event in events:
            self.assertEqual(event['type'], 'cloudify_event',
                             "Expected events only")

    def test_filter(self):
        deployment_id = self.deployment_id
        # create another deployment to test correct filtering
        self._create_deployment()
        filters = {'deployment_id': deployment_id}
        events = self.client.events.list(**filters)
        self.assertGreater(len(events), 0, "No events")
        for event in events:
            self.assertEqual(event['context']['deployment_id'],
                             deployment_id,
                             "Expected only events related to"
                             " deployment id {0}".format(deployment_id))

    def test_include_option(self):
        _include = ['message', 'type']
        events = self.client.events.list(_include=_include)
        self.assertGreater(len(events), 0, "No events")
        for event in events:
            self.assertListEqual(_include, event.keys(),
                                 "Expected only the following fields: {0},"
                                 " received: {1}"
                                 .format(_include, event.keys()))

    def test_include_logs(self):
        events = self.client.events.list(_include_logs=True)
        self.assertGreater(len(events), 0, "No events")
        is_log_found = False
        for event in events:
            if event['type'] == 'cloudify_log':
                is_log_found = True
                break
        self.assertTrue(is_log_found, "Expected logs to be found")

    def _create_deployment(self):
        dsl_path = \
            resource("dsl/"
                     "basic_event_and_log.yaml")
        test_deployment, _ = deploy(dsl_path)
        return test_deployment.id
