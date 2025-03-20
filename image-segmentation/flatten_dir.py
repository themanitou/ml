import os
from pathlib import Path
from argparse import ArgumentParser
import shutil


def error(message : str):
    print(message)
    exit(1)


def flatten_dir(input_dir, output_dir, filename_regex):
    filenames = [str(i) for i in sorted(Path(input_dir).glob(filename_regex))]
    files_count = len(filenames)
    print(f"Found {files_count} files matching regex in input dir")
    print(f"Here are a few filenames that have been picked up:")
    for i in range(min(5, files_count)):
        print(f"{filenames[i]}")

    count = 0
    for filename in filenames:
        new_filename = filename[len(input_dir):].lstrip(os.sep).replace(os.sep, "_")
        shutil.copy(filename, os.path.join(output_dir, new_filename))


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        description="A tool to recursively copy files matching a regex from all subdirectories \
                     to an output directory, and automatically append the subdirectories' names \
                     to the new file name to avoid name conflict.")
    arg_parser.add_argument("--input-dir", required=True,
                            dest="input_dir", type=str,
                            help="Input directory")
    arg_parser.add_argument("--output-dir", required=True,
                            dest="output_dir", type=str,
                            help="Output directory")
    arg_parser.add_argument("--filename-regex", required=True,
                            dest="filename_regex", type=str,
                            help="Only copy the files whose name matches this regex")
    args = arg_parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    if not output_dir.is_dir():
        error(f"Directory {args.output_dir} does not exist and cannot be created.")

    flatten_dir(args.input_dir, args.output_dir, args.filename_regex)
