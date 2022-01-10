#!/usr/bin/env python3
import os
import click
import annotator
from annotator.module import get_install_mode
from annotator.global_variable import *
from annotator.usefull_function import check_privileges


@click.group(help=click.secho(annotator.description_tools, fg='green', nl=False), context_settings={'help_option_names': ('-h', '--help'),"max_content_width":800},
             invoke_without_command=True, no_args_is_help=True)
@click.option('--restore', '-r', is_flag=True, required=False, default=False, show_default=True, help='Restore installation mode (need root or sudo)')
@click.version_option(annotator.__version__, '--version', '-v')
@click.pass_context
def main(ctx, restore):
    if ctx.invoked_subcommand is None and restore and check_privileges():
        if ANNOTATOR_MODE.exists():
            ANNOTATOR_MODE.unlink()
    pass




# Hack for build docs with unspecified install
args = str(sys.argv)
if "sphinx" in args:
    main.add_command(annotator.run_cluster)
    # main.add_command(annotator.create_cluster_config)
    # main.add_command(annotator.create_config)
    # main.add_command(annotator.edit_tools)
    main.add_command(annotator.run_local)
    main.add_command(annotator.install_cluster)
    main.add_command(annotator.install_local)
    # main.add_command(annotator.test_install)
else:
    mode = get_install_mode()
    if mode == "cluster":
        main.add_command(annotator.test_install)
        main.add_command(annotator.run_cluster)
        # main.add_command(annotator.create_cluster_config)
        # main.add_command(annotator.create_config)
        # main.add_command(annotator.edit_tools)
    elif mode == "local":
        main.add_command(annotator.test_install)
        main.add_command(annotator.run_local)
        # main.add_command(annotator.create_config)
    else:
        main.add_command(annotator.install_cluster)
        main.add_command(annotator.install_local)





if __name__ == '__main__':
    main()
