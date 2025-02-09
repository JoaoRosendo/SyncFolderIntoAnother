import os
import argparse
import time
import logging
import filecmp
import shutil

logging.basicConfig(level=logging.INFO, format="%(message)s")


def sync_replica_with_source(source_path, replica_path):
    if not os.path.exists(source_path):
        logging.info(f"The path {source_path} does not exist. Aborting program.")
        return False
    if not os.path.isdir(source_path):
        logging.info(f"The path {source_path} is not a directory. Aborting program.")
        return False

    os.makedirs(replica_path, exist_ok=True)

    for root, _, files in os.walk(source_path):
        for file in files:
            source_file = os.path.join(root, file)
            rel_path = os.path.relpath(source_file, source_path)
            target_file = os.path.join(replica_path, rel_path)
            os.makedirs(os.path.dirname(target_file), exist_ok=True)

            should_copy = False
            if not os.path.exists(target_file):
                should_copy = True
            else:
                # Compare files with the same path and name to see if they're equal
                if not filecmp.cmp(source_file, target_file, shallow=False):
                    should_copy = True

            if should_copy:
                shutil.copy2(source_file, target_file)

    # Missing second part where it checks if replica has files that do not exist in source
    return True


def main():

    # Set up parsing for collecting command line arguments
    parser = argparse.ArgumentParser(
        description="This tool replicates a directory into another directory. Synchronization is periodic."
    )
    parser.add_argument(
        "-s",
        "--source_path",
        type=str,
        required=True,
        help="Path to folder which will be replicated (Required)",
    )
    parser.add_argument(
        "-r",
        "--replica_path",
        type=str,
        required=True,
        help="Path to folder which will be the replica (Required)",
    )
    parser.add_argument(
        "-l",
        "--log_path",
        type=str,
        required=True,
        help="Path to file where the program's log will be stored",
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=int,
        required=True,
        help="Time interval in seconds between each synchronization (Required)",
    )
    args = parser.parse_args()

    loop = True
    while loop == True:
        loop = sync_replica_with_source(args.source_path, args.replica_path)
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
