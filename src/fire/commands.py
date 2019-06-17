import click
from lib.para_query.para_query import paraquery

@click.group()
@click.argument('ns_ip')
@click.pass_context
def fire(ctx, ns_ip):
    """This is a test command group"""
    # ctx.obj = testclass()
    ctx.obj['paraquery'] = paraquery(NS_IP=ns_ip)

@fire.command('print')
@click.pass_obj
def print(paraquery_obj):
    """Call a click echo from a lib"""
    paraquery_obj['paraquery'].test_function()

@fire.command('loop')
@click.argument('url')
@click.argument('loops')
@click.pass_obj
def loop(paraquery_obj, url, loops):
    """Call a click echo from a lib"""
    paraquery_obj['paraquery'].loop_query(URL=url, loops=int(loops))
    

@fire.command('para')
@click.argument('url')
@click.argument('loops')
@click.argument('threads')
@click.pass_obj
def loop(paraquery_obj, url, loops, threads):
    """Call a click echo from a lib"""
    paraquery_obj['paraquery'].para_query(URL=url, loops=int(loops), branches=int(threads))