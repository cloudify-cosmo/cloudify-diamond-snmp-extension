from os import path

from influxdb import InfluxDBClient

from cosmo_tester.framework.testenv import TestCase


class TestSNMPProxy(TestCase):

    def _check_snmp_monitoring(self, blueprint, inputs):
        self.blueprint_yaml = path.join(
            path.dirname(path.dirname(path.realpath(__file__))),
            blueprint
        )

        self.upload_deploy_and_execute_install(inputs=inputs)

        # Check that proper metrics are stored
        client = InfluxDBClient(
            self.env.management_ip, 8086, 'root', 'root', 'cloudify')
        all_series = client.get_list_series()
        self.assertTrue(all_series)  # not empty
        for s in all_series:
            # All series should refer to the snmp_monitore_host
            self.assertIn('snmp_monitored_host', s)
            self.assertTrue('total_system' in s or 'total_user' in s)

        # Performing cleanup
        self.execute_uninstall()
        self.cfy.delete_deployment(self.test_id)
        self.cfy.delete_blueprint(self.test_id)

    def test_snmp_proxy_on_manager(self):
        inputs = {
            'monitored_host_ubuntu_image_name': self.env.ubuntu_trusty_image_id
        }
        self._check_snmp_monitoring('proxy_on_manager.yaml', inputs)

    def test_snmp_proxy_on_separate_vm(self):
        inputs = {
            'monitored_host_ubuntu_image_name':
                self.env.ubuntu_trusty_image_id,
            'proxy_server_ubuntu_image_name': self.env.ubuntu_image_id
        }
        self._check_snmp_monitoring('separate_proxy.yaml', inputs)
