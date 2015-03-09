import os
from shutil import rmtree

from cloudify import ctx
from cloudify.exceptions import NonRecoverableError


def _collectors_path(ctx):
    try:
        return ctx.instance.runtime_properties['diamond_paths']['collectors']
    except KeyError:
        raise NonRecoverableError("Collectors path not in runtime properties")


def _delete_collectors(collectors_path):
    try:
        rmtree(collectors_path)
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            ctx.logger.info("Collectors path already deleted")
        else:
            raise
    else:
        ctx.logger.info(
            "Collectors directory "
            "deleted from {}".format(collectors_path))


ctx.logger.info("Starting cleaning up diamond collectors")
collectors_path = _collectors_path(ctx)
if collectors_path:
    try:
        _delete_collectors(collectors_path)
    except Exception as e:
        raise NonRecoverableError(
            "Couldn't remove collectors from: "
            "{}, error: {}".format(collectors_path, e))
ctx.logger.info("Diamond collectors are cleaned up")
