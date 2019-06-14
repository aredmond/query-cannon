import click
from lib.testlib.testlib import testclass

@click.group()
@click.pass_context
def test(ctx):
    """This is a test command group"""
    # ctx.obj = testclass()
    ctx.obj['test'] = testclass()

@test.command('print')
@click.pass_obj
def print(test_obj):
    """Call a click echo from a lib"""
    test_obj['test'].test_function()
