# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 OpenStack, LLC
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from tempest.api.compute import base
from tempest.test import attr


class QuotasTestJSON(base.BaseComputeTest):
    _interface = 'json'

    @classmethod
    def setUpClass(cls):
        super(QuotasTestJSON, cls).setUpClass()
        cls.client = cls.quotas_client
        cls.admin_client = cls._get_identity_admin_client()
        resp, tenants = cls.admin_client.list_tenants()
        cls.tenant_id = [tnt['id'] for tnt in tenants if tnt['name'] ==
                         cls.client.tenant_name][0]
        cls.default_quota_set = set(('injected_file_content_bytes',
                                     'metadata_items', 'injected_files',
                                     'ram', 'floating_ips',
                                     'fixed_ips', 'key_pairs',
                                     'injected_file_path_bytes',
                                     'instances', 'security_group_rules',
                                     'cores', 'security_groups'))

    @attr(type='smoke')
    def test_get_quotas(self):
        # User can get the quota set for it's tenant
        expected_quota_set = self.default_quota_set | set(['id'])
        resp, quota_set = self.client.get_quota_set(self.tenant_id)
        self.assertEqual(200, resp.status)
        self.assertEqual(sorted(expected_quota_set),
                         sorted(quota_set.keys()))
        self.assertEqual(quota_set['id'], self.tenant_id)

    @attr(type='smoke')
    def test_get_default_quotas(self):
        # User can get the default quota set for it's tenant
        expected_quota_set = self.default_quota_set | set(['id'])
        resp, quota_set = self.client.get_default_quota_set(self.tenant_id)
        self.assertEqual(200, resp.status)
        self.assertEqual(sorted(expected_quota_set),
                         sorted(quota_set.keys()))
        self.assertEqual(quota_set['id'], self.tenant_id)


class QuotasTestXML(QuotasTestJSON):
    _interface = 'xml'
