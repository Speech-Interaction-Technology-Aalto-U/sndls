import os
from argparse import Namespace
from ..utils.config import get_allowed_audio_file_extensions
from ..utils.fmt import exit_error


def lsa(args: Namespace) -> None:
    """Main routine triggered by the `lsa` command.
    
    Args:
        args (Namespace): Main namespace containing user provided input.
    """
    # Check file extensions
    for ext in args.extension:
        if ext not in get_allowed_audio_file_extensions():
            exit_error(
                "Currently only the following extensions are supported: "
                f"{', '.join(get_allowed_audio_file_extensions())}"
            )
    
    # Check incompatible args that are not handled by mutually exclusive groups
    if args.meta and (
        args.sha256
        or args.sha256_short
        or args.csv
        or args.filter
        or args.select 
    ):
        exit_error(
            "--meta not allowed with: --sha256, --sha256-short, --csv, "
            "--filter or --select"
        )
    
    # Check csv does not exist already if it should be written
    if args.csv and os.path.isfile(args.csv) and not args.csv_overwrite:
        exit_error(
            f"'{args.csv}' already exists. Please choose a different filename "
            "or use --csv-overwrite to allow overwriting existing files"
        )
    
    if args.sample is not None and args.sample <= 0.0:
        exit_error(
            "--sample should be 1 or greater to sample a concrete number of "
            "samples or between 0.0 and 1.0 to sample a percentage of all "
            "samples"
        )
