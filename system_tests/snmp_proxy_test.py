from os import path

from influxdb import InfluxDBClient

from cosmo_tester.framework.testenv import TestCase


class TestSNMPProxy(TestCase):
    TIME_TO_WAIT_FOR_METRICS = 30  # in seconds

    def _check_influx_db(self, deployment_id):
        client = InfluxDBClient(self.env.management_ip, database='cloudify')
        try:
            res = client.query(
                'select * from /^{0}\./i where time > now() - {1}s'
                .format(deployment_id, self.TIME_TO_WAIT_FOR_METRICS)
            )
        except NameError as e:
            self.fail('Monitoring events for deployment with ID {0} have'
                      ' not been found in influxDB. The error is: {1}'
                      .format(deployment_id, e))

        self.assertTrue(res[0]['points'])  # Assert not empty

    def _test_snmp_monitoring(self, blueprint):
        self.blueprint_yaml = path.join(
            path.dirname(path.dirname(path.realpath(__file__))),
            blueprint
        )
        deployment_id = self.test_id
        self.upload_deploy_and_execute_install(
            inputs={
                'image': self.env.ubuntu_trusty_image_name,
                'flavor': self.env.flavor_name
            },
            deployment_id=deployment_id
        )

        self.repetitive(
            self._check_influx_db,
            timeout=self.TIME_TO_WAIT_FOR_METRICS,
            args=[deployment_id]
        )

        # Perform cleanup
        self.execute_uninstall()
        self.cfy.deployments.delete(deployment_id)
        self.cfy.blueprints.delete(deployment_id)

    def test_snmp_proxy_on_manager(self):
        self._test_snmp_monitoring('proxy-on-manager-blueprint.yaml')

    def test_snmp_proxy_on_separate_vm(self):
        self._test_snmp_monitoring('separate-proxy-blueprint.yaml')
