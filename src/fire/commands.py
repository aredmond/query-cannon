import click
from lib.para_query.para_query import paraquery
from pprint import pprint

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
    """Hit a DNS server with one request after another"""
    paraquery_obj['paraquery'].loop_query(URL=url, loops=int(loops))
    

@fire.command('para')
@click.argument('url')
@click.argument('loops')
@click.argument('threads')
@click.pass_obj
def para(paraquery_obj, url, loops, threads):
    """Run the loop command in parallel"""
    paraquery_obj['paraquery'].para_query(URL=url, loops=int(loops), branches=int(threads))

@fire.command('urlpara')
@click.argument('url_filename')
@click.argument('loops')
@click.argument('threads')
@click.pass_obj
def urlpara(paraquery_obj, url_filename,  loops, threads):
    """Run the parallel command over a file of URLs, quering randomly."""
    url_list = [line.rstrip('\n') for line in open(url_filename)]
    paraquery_obj['paraquery'].para_query_with_diff_URLs(url_list, loops=int(loops), branches=int(threads))