from cosmo_tester.test_suites.test_blueprints import monitoring_test

from os import path


class TestSNMPProxy(monitoring_test.MonitoringTest):

    def _check_snmp_monitoring(self, blueprint, inputs):
        self.blueprint_yaml = path.join(
            path.dirname(path.dirname(path.realpath(__file__))),
            blueprint
        )

        self.upload_deploy_and_execute_install(inputs=inputs)

        url = "http://{0}/#/deployment/{1}/monitoring" \
              .format(self.env.management_ip, self.test_id)
        self.assert_grafana_path_active(url)

        self.execute_uninstall()
        self.cfy.delete_deployment(self.test_id)
        self.cfy.delete_blueprint(self.test_id)

    def test_monitoring(self, blueprint='proxy_on_manager.yaml'):
        inputs = {
            'monitored_host_ubuntu_image_name': self.env.ubuntu_trusty_image_id
        }
        self._check_snmp_monitoring(blueprint, inputs)

    def test_snmp_proxy_on_separate_vm(self):
        inputs = {
            'monitored_host_ubuntu_image_name':
                self.env.ubuntu_trusty_image_id,
            'proxy_server_ubuntu_image_name': self.env.ubuntu_image_id
        }
        self._check_snmp_monitoring('separate_proxy.yaml', inputs)
