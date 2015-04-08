from os import path
import time

from influxdb import InfluxDBClient

from cosmo_tester.framework.testenv import TestCase


class TestSNMPProxy(TestCase):
    TIME_TO_WAIT_FOR_METRICS = 10  # in seconds

    def _test_snmp_monitoring(self, blueprint, inputs):
        self.blueprint_yaml = path.join(
            path.dirname(path.dirname(path.realpath(__file__))),
            blueprint
        )

        self.upload_deploy_and_execute_install(inputs=inputs)

        # Check that proper metrics are stored
        time.sleep(self.TIME_TO_WAIT_FOR_METRICS)
        client = InfluxDBClient(self.env.management_ip, database='cloudify')
        try:
            res = client.query(
                'select * from /^{0}\./i where time > now() - {1}s'
                .format(self.test_id, self.TIME_TO_WAIT_FOR_METRICS)
            )
        except NameError as e:
            self.fail('Monitoring events for deployment with ID {0} have'
                      ' not been found in influxDB. The error is: {1}'
                      .format(self.test_id, e))

        self.assertTrue(res[0]['points'])  # Assert not empty

        # Perform cleanup
        self.execute_uninstall()
        self.cfy.delete_deployment(self.test_id)
        self.cfy.delete_blueprint(self.test_id)

    def test_snmp_proxy_on_manager(self):
        inputs = {
            'monitored_host_ubuntu_image_name': self.env.ubuntu_trusty_image_id
        }
        self._test_snmp_monitoring('proxy_on_manager.yaml', inputs)

    def test_snmp_proxy_on_separate_vm(self):
        inputs = {
            'monitored_host_ubuntu_image_name':
                self.env.ubuntu_trusty_image_id,
            'proxy_server_ubuntu_image_name': self.env.ubuntu_image_id
        }
        self._test_snmp_monitoring('separate_proxy.yaml', inputs)
