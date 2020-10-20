from Reactor.ReactCreator import Reactor
import argparse

def execute():
    parser = argparse.ArgumentParser(
        description="Creates a React project."
    )
    parser.add_argument("-p", "--path", required=True,
                        help="path/to/directory")
    parser.add_argument("-nm", "--no_install_modules", action="store_true",
                        help="no install modules")
    parser.add_argument("-nf", "--no_create_files", action="store_true",
                        help="no create files")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="show output files creation")
    args = parser.parse_args()

    Reactor(
        path_directory=args.path,
        verbose=args.verbose,
        no_create_files=args.no_create_files,
        no_install_npm=args.no_install_modules
    )
