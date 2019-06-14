import click
import pkg_resources

from .test import commands as test
from .fire import commands as fire

@click.group()
@click.pass_context
def entry_point(ctx):
    """This is the entry point function"""
    ctx.ensure_object(dict)

entry_point.add_command(test.test)
entry_point.add_command(fire.fire)
