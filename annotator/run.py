import click
from shutil import copyfile
from annotator.global_variable import *
import os


@click.command("run_cluster", short_help='Run workflow on HPC', context_settings=dict(ignore_unknown_options=True, max_content_width=800), no_args_is_help=True)
@click.option('--config', '-c', type=click.Path(exists=True, file_okay=True, readable=True, resolve_path=True), required=True, show_default=True, help='Configuration file for run annotator')
@click.option('--clusterconfig', '-cl', default=ANNOTATOR_CLUSTER_CONFIG, type=click.Path(exists=True, file_okay=True, readable=True, resolve_path=True), required=False, show_default=True, help='Overwrite profile clusterconfig file for run annotator')
# @click.option('--profile', '-p', default=ANNOTATOR_PROFILE, type=click.Path(exists=True, dir_okay=True, readable=True, resolve_path=True), required=False, show_default=True, help='Path to snakemake profile for run annotator')
# @click.option('--tools', '-t', default=ANNOTATOR_TOOLS_PATH, type=click.Path(exists=True, file_okay=True, readable=True, resolve_path=True), required=False, show_default=True, help='Path to tools_path.yaml for run annotator')
@click.option('--pdf', '-pdf', is_flag=True, required=False, default=False, show_default=True, help='run snakemake with --dag, --rulegraph and --filegraph')
@click.argument('snakemake_other', nargs=-1, type=click.UNPROCESSED)
# def run_cluster(config, clusterconfig, profile, tools, pdf, snakemake_other):
def run_cluster(config, clusterconfig, pdf, snakemake_other):
    """
    \b
    Run snakemake command line with mandatory parameters.
    SNAKEMAKE_OTHER: append other snakemake command such '--dry-run'

    Example:
        annotator run_cluster -c config.yaml --dry-run --jobs 200
    """
    profile = ANNOTATOR_PROFILE
    tools = ANNOTATOR_TOOLS_PATH
    # get user arguments
    click.secho(f'    Profile file: {profile}', fg='yellow')
    click.secho(f'    Config file: {config}', fg='yellow')

    if clusterconfig != ANNOTATOR_CLUSTER_CONFIG.as_posix():
        ANNOTATOR_ARGS_CLUSTER_CONFIG.parent.mkdir(parents=True, exist_ok=True)
        copyfile(clusterconfig, ANNOTATOR_ARGS_CLUSTER_CONFIG.as_posix())
        clusterconfig = clusterconfig
    elif ANNOTATOR_USER_CLUSTER_CONFIG.exists():
        clusterconfig = ANNOTATOR_USER_CLUSTER_CONFIG
    else:
        clusterconfig = ANNOTATOR_CLUSTER_CONFIG
    cmd_clusterconfig = f"--cluster-config {clusterconfig}"
    click.secho(f'    Cluster config file load: {clusterconfig}', fg='yellow')

    if tools != ANNOTATOR_TOOLS_PATH.as_posix():
        ANNOTATOR_ARGS_TOOLS_PATH.parent.mkdir(parents=True, exist_ok=True)
        copyfile(tools, ANNOTATOR_ARGS_TOOLS_PATH)
    elif ANNOTATOR_USER_TOOLS_PATH.exists():
        tools = ANNOTATOR_USER_TOOLS_PATH

    cmd_snakemake_base = f"snakemake --show-failed-logs -p -s {ANNOTATOR_SNAKEFILE} --configfile {config} --profile {profile} {cmd_clusterconfig} {' '.join(snakemake_other)}"
    click.secho(f"    {cmd_snakemake_base}\n", fg='bright_blue')
    # exit()
    os.system(cmd_snakemake_base)
    
    if pdf:
        dag_cmd_snakemake = f"{cmd_snakemake_base} --dag | dot -Tpdf > schema_pipeline_dag.pdf"
        click.secho(f"    {dag_cmd_snakemake}\n", fg='bright_blue')
        os.system(dag_cmd_snakemake)
        rulegraph_cmd_snakemake = f"{cmd_snakemake_base} --rulegraph | dot -Tpdf > schema_pipeline_global.pdf"
        click.secho(f"    {rulegraph_cmd_snakemake}\n", fg='bright_blue')
        os.system(rulegraph_cmd_snakemake)
        filegraph_cmd_snakemake = f"{cmd_snakemake_base} --filegraph | dot -Tpdf > schema_pipeline_files.pdf"
        click.secho(f"    {filegraph_cmd_snakemake}\n", fg='bright_blue')
        os.system(filegraph_cmd_snakemake)


@click.command("run_local", short_help='Run workflow on local computer (use singularity mandatory)', context_settings=dict(ignore_unknown_options=True, max_content_width=800),
               no_args_is_help=True)
@click.option('--config', '-c', type=click.Path(exists=True, file_okay=True, readable=True, resolve_path=True), required=True, help='Configuration file for run annotator')
@click.option('--threads', '-t', type=int, required=True, help='number of threads')
@click.option('--pdf', '-p', is_flag=True, required=False, default=False, help='run snakemake with --dag, --rulegraph and --filegraph')
@click.argument('snakemake_other', nargs=-1, type=click.UNPROCESSED)
def run_local(config, threads, pdf, snakemake_other):
    """    Run snakemake command line with mandatory parameters.
    SNAKEMAKE_OTHER: append other snakemake command such '--dry-run'

    Example:
        annotator run_local -c config.yaml --dry-run
    """
    # get user arguments
    click.secho(f'    Config file: {config}', fg='yellow')

    cmd_snakemake_base = f"snakemake --cores {threads} --use-singularity --show-failed-logs --printshellcmds -s {ANNOTATOR_SNAKEFILE} --configfile {config}  {' '.join(snakemake_other)}"
    click.secho(f"    {cmd_snakemake_base}\n", fg='bright_blue')

    os.system(cmd_snakemake_base)
    if pdf:
        dag_cmd_snakemake = f"{cmd_snakemake_base} --dag | dot -Tpdf > schema_pipeline_dag.pdf"
        click.secho(f"    {dag_cmd_snakemake}\n", fg='bright_blue')
        os.system(dag_cmd_snakemake)
        rulegraph_cmd_snakemake = f"{cmd_snakemake_base} --rulegraph | dot -Tpdf > schema_pipeline_global.pdf"
        click.secho(f"    {rulegraph_cmd_snakemake}\n", fg='bright_blue')
        os.system(rulegraph_cmd_snakemake)
        filegraph_cmd_snakemake = f"{cmd_snakemake_base} --filegraph | dot -Tpdf > schema_pipeline_files.pdf"
        click.secho(f"    {filegraph_cmd_snakemake}\n", fg='bright_blue')
        os.system(filegraph_cmd_snakemake)
