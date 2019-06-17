from __future__ import print_function

import click
import socket
import time
import dns.flags
import dns.rdatatype
import dns.resolver
import sys
import ray
import random

class paraquery(object):
    """Parallel DNS queries

    Attributes:
        NS_IP: The IP address of the DNS server to load test
    """

    def __init__(self, NS_IP, verbose=False):
        """Set attributes"""
        self.NS_IP = NS_IP
        self.verbose = verbose
        self.resolver = dns.resolver.Resolver()
        self.resolver.nameservers = [NS_IP]
        self.resolver.retry_servfail = 0

    def test_function(self):
        click.echo(f'This is only a test. {self.NS_IP}')

    #################################################
    ## DNS Functions
    #################################################
    def query(self, URL):
        """Make a DNS query"""
        try:
            stime = time.perf_counter()
            answers = self.resolver.query(URL, raise_on_no_answer=False)
            etime = time.perf_counter()
        except dns.resolver.NoNameservers as e:
            if self.verbose:
                print("No response to dns request", file=sys.stderr, flush=True)
            sys.exit(1)
        except dns.resolver.NXDOMAIN as e:
            if self.verbose:
                print("Hostname does not exist", file=sys.stderr, flush=True)
            sys.exit(1)
        except dns.resolver.Timeout:
            if self.verbose:
                print("Request timeout", flush=True)
            pass
        except dns.resolver.NoAnswer:
            if self.verbose:
                print("No answer", flush=True)
            pass
        else:
            elapsed = answers.response.time * 1000  # convert to milliseconds
            if self.verbose:
                print(
                    "%d bytes request: %s from %s: time=%.3f ms" % (
                        len(str(answers.rrset)), URL, self.NS_IP, elapsed), flush=True)
            # print(answers.rrset, flush=True)
            # print("flags:", dns.flags.to_text(answers.response.flags), flush=True)

            tot_time = stime  - etime
            return (answers, tot_time)

    def simple_query(self, URL):
        """Make a DNS query"""
        q_start = time.time()
        response = socket.gethostbyname(URL)
        q_end = time.time()
        q_time = q_end - q_start
        return (response, q_time)

    def loop_query(self, URL, loops=5):
        """Make several DNS queries in succession"""

        if self.verbose:
            click.echo(f'Making {loops} query/ies.')
        for loop in range(loops):
            result, q_time = self.query(URL)
            # click.echo(f'{result} {q_time}')

    def loop_query_with_diff_URLs(self, URL_list, loops=5):
        """Make several DNS queries in succession"""

        if self.verbose:
            click.echo(f'Making {loops} query/ies.')
        for loop in range(loops):
            url = random.choice(URL_list)
            # url = 'google.com'

            result, q_time = self.query(url)
            # click.echo(f'{result} {q_time}')

    def para_query(self, URL, loops=5, branches=2):
        """Make several DNS queries in succession"""
        click.echo(f'Making {loops*branches} query/ies. Across {branches} process/es.')

        @ray.remote
        def call_loop_in_thread(URL, loops):
            self.loop_query(URL, loops)

        ray.init()
        results = ray.get([call_loop_in_thread.remote(URL, loops) for i in range(branches) ])  # Execute in parallel


    def para_query_with_diff_URLs(self, URL_list, loops=5, branches=2):
        """Make several DNS queries in succession"""
        click.echo(f'Making {loops*branches} query/ies. Across {branches} process/es.')

        @ray.remote
        def call_loop_in_thread(URL_list, loops):
            self.loop_query_with_diff_URLs(URL_list, loops)

        ray.init()
        results = ray.get([call_loop_in_thread.remote(URL_list, loops) for i in range(branches) ])  # Execute in parallel

    # resolver = dns.resolver.Resolver()
    # resolver.nameservers = [dnsserver]
    # resolver.timeout = timeout
    # resolver.lifetime = timeout
    # resolver.port = dst_port
    # resolver.retry_servfail = 0

        # try:
        #     stime = time.perf_counter()
        #     answers = resolver.query(hostname, dnsrecord, source_port=src_port, source=src_ip, tcp=use_tcp,
        #                              raise_on_no_answer=False)
        #     etime = time.perf_counter()
        # except dns.resolver.NoNameservers as e:
        #     if not quiet:
        #         print("No response to dns request", file=sys.stderr, flush=True)
        #         if verbose:
        #             print("error:", e, file=sys.stderr, flush=True)
        #     sys.exit(1)
        # except dns.resolver.NXDOMAIN as e:
        #     if not quiet:
        #         print("Hostname does not exist", file=sys.stderr, flush=True)
        #     if verbose:
        #         print("Error:", e, file=sys.stderr, flush=True)
        #     sys.exit(1)
        # except dns.resolver.Timeout:
        #     if not quiet:
        #         print("Request timeout", flush=True)
        #     pass
        # except dns.resolver.NoAnswer:
        #     if not quiet:
        #         print("No answer", flush=True)
        #     pass
        # else:
        #     elapsed = answers.response.time * 1000  # convert to milliseconds
        #     response_time.append(elapsed)
        #     if not quiet:
        #         print(
        #             "%d bytes from %s: seq=%-3d time=%.3f ms" % (
        #                 len(str(answers.rrset)), dnsserver, i, elapsed), flush=True)
        #     if verbose:
        #         print(answers.rrset, flush=True)
        #         print("flags:", dns.flags.to_text(answers.response.flags), flush=True)

        #     time_to_next = (stime + interval) - etime
        #     if time_to_next > 0:
        #         time.sleep(time_to_next)

    # r_sent = i + 1
    # r_received = len(response_time)
    # r_lost = r_sent - r_received
    # r_lost_percent = (100 * r_lost) / r_sent
    # if response_time:
    #     r_min = min(response_time)
    #     r_max = max(response_time)
    #     r_avg = sum(response_time) / r_received
    #     if len(response_time) > 1:
    #         r_stddev = stdev(response_time)
    #     else:
    #         r_stddev = 0
    # else:
    #     r_min = 0
    #     r_max = 0
    #     r_avg = 0
    #     r_stddev = 0

    