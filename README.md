# cloudify-diamond-snmp-extension
An extension to the diamond plugin that adds support for monitoring SNMP metrics on remote machines. Here you can find an example of SNMP monitoring on OpenStack.

## SNMP types
All node types you will need are defined in [snmp_types.yaml](snmp_types.yaml)

### SNMPMonitoredHost
SNMPMonitoredHost exists in the blueprints only as a simulation of a moniotored device. We assume that SNMP works on the device and that manager can access it. In our example the SNMPMonitoredHost is a virtual machine with Ubuntu. The SnmpdConfiguringNode installs SNMP daemon and changes its configuration so it can be polled from anywhere.

### SNMPProxy and SNMPManagerProxy
The nodes that poll the SNMP devices.
SNMPProxy is located  on a separate compute node and SNMPManagerProxy on the Manager.

To define the SNMP polling create a relationship for each device you want to poll. You need to add a preconfigure operation that will change the SNMP Collector configuration. As its implementation use [append_diamond_conf.py](scripts/append_diamond_conf.py). In the inputs you need to specify the port, community name and OIDs that you wish to poll.

### SNMPSecurityGroup
 Security group that adds required security groups to OpenStack so that the SNMP Proxy can access SNMP devices.

## SNMP Proxy on Manager
[An example blueprint](proxy_on_manager.yaml)


Create a node of type SNMPManagerProxy. Next add relationships as described in SNMPProxy and SNMPManagerProxy paragraph.

## SNMP Proxy on separate VMs
[An example blueprint](separate_proxy.yaml)


To use a separate node you will need a Compute node with diamond as a monitoring agent. In our example it is ProxyServer.
Next create a ProxyNode contained in ProxyServer. It should be of a type SNMPProxy. Finally add relationships as described in SNMPProxy  and SNMPManagerProxy paragraph.

## Used scripts
[append_diamond_conf.py](scripts/append_diamond_conf.py)
Adds the specified in inputs configuration to its runtime properties so it can be later added to SNMP Collectors config.


[diamond_clean_up.py](scripts/diamond_clean_up.py)
Temporarily here, it cleans up the directories created during diamond installation.

[install_requirements.sh](scripts/install_requirements.sh)
Installs pysnmp, python module used by SNMP Collector.

[setup_snmpd.sh](scripts/setup_snmpd.sh)
Installs SNMP daemon and changes its configuration.

## Collector changes
[snmpproxy.py](collectors/snmpproxy.py)
SNMPProxyCollector that derives from SNMPRawCollector. The only difference is the path used to publish metric. In our implementation it is adjusted to [cloudify-diamond-plugin](https://github.com/cloudify-cosmo/cloudify-diamond-plugin).
