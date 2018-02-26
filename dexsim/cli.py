#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from time import clock
import click
from dexsim.sim import DexSim


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option('-i', '--include-pattern',
              help='Only optimize methods and classes matching the pattern, e.g. La/b/c;->decode')
@click.option('-o', '--output', type=click.Path(), default=None, help='Output file path', show_default=True)
@click.option('-l', '--logfile', default='dexsim.log', help='Logfile output', show_default=True)
@click.option('-D', '--debug', is_flag=True, help='Enable debug mode')
@click.argument('targets', nargs=-1, )
def command1(include_pattern, output, logfile, debug, targets):
    """Simulate APK/DEX/JAR"""
    # TODO: add support for DEBUG and log files
    start = clock()
    d = DexSim()

    try:

        for t in targets:
            d.run(t, output, include_pattern)
            # try:
            #     d.run(t, output, include_pattern)
            # except Exception as ex:
            #     print('Exception while parsing %s %s' % (t, ex))
            #     continue

    except KeyboardInterrupt:
        print('KeyboardInterrupt caught. Exiting...')
        sys.exit(-1)
    finally:
        finish = clock()
        print('\n%fs' % (finish - start))


def main():
    command1()


if __name__ == '__main__':
    command1()
