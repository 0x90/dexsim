#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
import os
import sys
from time import clock

import click
# from click_help_colors import HelpColorsGroup, HelpColorsCommand


from dexsim import DexSim

# CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

# @click.command(
#     cls=HelpColorsCommand,
#     help_options_color='blue',
#     # context_settings=CONTEXT_SETTINGS
# )

@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option('-i', '--include-pattern',
              help='Only optimize methods and classes matching the pattern, e.g. La/b/c;->decode')
@click.option('-o', '--output', type=click.Path(), default='output', help='Output file path', show_default=True)
@click.option('-l', '--logfile', default='dexsim.log', help='Logfile output', show_default=True)
@click.option('-D', '--debug', is_flag=True, help='Enable debug mode')
@click.argument('targets', nargs=-1, )
def command1(include_pattern, output, logfile, debug, targets):
    """Simulate APK/DEX/JAR"""
    #
    try:
        start = clock()

        d = DexSim()
        for t in targets:
            d.run(t, output, include_pattern)

        finish = clock()
        print('\n%fs' % (finish - start))

    except KeyboardInterrupt:
        print('KeyboardInterrupt caught. Exiting...')
        sys.exit(-1)


def main():
    command1()


if __name__ == '__main__':
    main()
