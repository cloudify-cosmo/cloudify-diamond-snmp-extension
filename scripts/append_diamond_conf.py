from cloudify import ctx
from cloudify.state import ctx_parameters as inputs


target_instance = ctx.target.instance
src_instance = ctx.source.instance

config = src_instance.runtime_properties.get('snmp_collector_config', {})

devices_conf = config.get('devices', {})
devices_conf[ctx.target.node.name] = device_config = {}
device_config['instance_id'] = target_instance.id
if 'host' in inputs:
    device_config['host'] = inputs.host
else:
    device_config['host'] = target_instance.host_ip
device_config['port'] = inputs.port
device_config['community'] = inputs.community
device_config['oids'] = inputs.oids

config['devices'] = devices_conf
config['path_suffix'] = inputs.path_suffix

src_instance.runtime_properties['snmp_collector_config'] = config
