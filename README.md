# cloudify-diamond-snmp-extension
An extension to the diamond plugin that adds support for monitoring SNMP metrics on remote machines. Here you can find an example of SNMP monitoring deployed on OpenStack.

## SNMP types
All node types you will need are defined in [snmp_types.yaml](snmp_types.yaml). SNMP proxy is a node responsible for gathering the requested metrics from SNMP devices and sending them to RabbitMQ on behalf of those devices as if they were reporting those metrics by themselves (the proxy should be transparent).

### SNMPMonitoredHost
SNMPMonitoredHost exists in the blueprints only as a simulation of a monitored device. We assume that SNMP works on the device and that the SNMP proxy can access it. In our example the SNMPMonitoredHost is a virtual machine with Ubuntu. The SnmpdConfiguringNode installs SNMP daemon and changes its configuration so it can be polled from anywhere.

### SNMPProxy and SNMPManagerProxy
The nodes that poll the SNMP devices.
SNMPProxy is located  on a separate compute node and SNMPManagerProxy on the Manager.

To define the SNMP polling create a relationship for each device you want to poll. You need to add a preconfigure operation that will change the SNMPProxyCollector's configuration. As its implementation, use [append_diamond_conf.py](scripts/append_diamond_conf.py). In the inputs you need to specify the port, community name and OIDs that you wish to poll.

### SNMPSecurityGroup
 Security group that contains OpenStack rules allowing SNMP proxy to access SNMP devices.

## SNMP Proxy on Manager
[An example blueprint](proxy_on_manager.yaml)


Create a node of SNMPManagerProxy type. Next add relationships as described in SNMPProxy and SNMPManagerProxy paragraphs.

## SNMP Proxy on separate VMs
[An example blueprint](separate_proxy.yaml)


To use a separate node you will need a Compute node with Diamond as a monitoring agent. In our example, it is the ProxyServer.
Next, create a ProxyNode contained in ProxyServer. It should be of the SNMPProxy type. Finally, add relationships as described in [_SNMPProxy and SNMPManagerProxy_](README.md#SNMPProxy and SNMPManagerProxy).

## Used scripts
[append_diamond_conf.py](scripts/append_diamond_conf.py)
Adds the configuration specified in its inputs to the SNMP proxy's runtime properties so that it can be later added to the SNMPProxyCollector's config.

[diamond_clean_up.py](scripts/diamond_clean_up.py)
Temporarily here, it cleans up the directories created during the Diamond's installation.

[install_requirements.sh](scripts/install_requirements.sh)
Installs pysnmp, python module used by the SNMPProxyCollector.

[setup_snmpd.sh](scripts/setup_snmpd.sh)
Installs the SNMP daemon and modifies its configuration so that the daemon can be polled.

## Collector changes
[snmpproxy.py](collectors/snmpproxy.py)
SNMPProxyCollector that inherits from SNMPRawCollector. The only difference is the path used to publish metric. In our implementation, it is adjusted to [cloudify-diamond-plugin](https://github.com/cloudify-cosmo/cloudify-diamond-plugin).
