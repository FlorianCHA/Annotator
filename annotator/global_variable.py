import sys
from pathlib import Path

DOCS="https://ANNOTATOR-pipeline.readthedocs.io/en/latest/"
# Hack for build docs with unspecified path install
args = str(sys.argv)
if "sphinx" in args:
    ANNOTATOR_PATH = Path("/Path/to/ANNOTATOR_install/")
else:
    ANNOTATOR_PATH = Path(__file__).resolve().parent
ANNOTATOR_SNAKEFILE = ANNOTATOR_PATH.joinpath("Snakefile")
ANNOTATOR_MODE = ANNOTATOR_PATH.joinpath(".mode.txt")
ANNOTATOR_SCRIPTS = ANNOTATOR_PATH.joinpath("scripts")
ANNOTATOR_PROFILE = ANNOTATOR_PATH.joinpath("default_profile")
ANNOTATOR_CONFIG_PATH = ANNOTATOR_PATH.joinpath("install_files", "config.yaml")

ANNOTATOR_TOOLS_PATH = ANNOTATOR_PATH.joinpath("install_files", "tools_path.yaml")
ANNOTATOR_USER_TOOLS_PATH = Path("~/.config/ANNOTATOR/tools_path.yaml").expanduser()
ANNOTATOR_ARGS_TOOLS_PATH = Path("~/.config/ANNOTATOR/tools_path_args.yaml").expanduser()

ANNOTATOR_CLUSTER_CONFIG = ANNOTATOR_PROFILE.joinpath("cluster_config.yaml")
ANNOTATOR_USER_CLUSTER_CONFIG = Path("~/.config/ANNOTATOR/cluster_config.yaml").expanduser()
ANNOTATOR_ARGS_CLUSTER_CONFIG = Path("~/.config/ANNOTATOR/cluster_config_args.yaml").expanduser()

SINGULARITY_URL_FILES = [('https://itrop.ird.fr/ANNOTATOR_utilities/singularity_build/Singularity.ANNOTATOR_tools.sif',
              f'{ANNOTATOR_PATH}/containers/Singularity.ANNOTATOR_tools.sif'),
             ('https://itrop.ird.fr/ANNOTATOR_utilities/singularity_build/Singularity.report.sif',
              f'{ANNOTATOR_PATH}/containers/Singularity.report.sif')]
