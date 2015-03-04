from cloudify import ctx
from cloudify.state import ctx_parameters as inputs


targetInstance = ctx.target.instance
srcInstance = ctx.source.instance

config = srcInstance.runtime_properties.get('snmp_collector_config', {})

devicesConf = config.get('devices', {})
devicesConf[ctx.target.node.name] = device_config = {}
device_config['instance_id'] = targetInstance.id
if 'host' in inputs:
    device_config['host'] = inputs.host
else:
    device_config['host'] = targetInstance.host_ip
device_config['port'] = inputs.port
device_config['community'] = inputs.community
device_config['oids'] = inputs.oids

config['devices'] = devicesConf
config['path_suffix'] = inputs.path_suffix

srcInstance.runtime_properties['snmp_collector_config'] = config
