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

    # Copy directories and files from source into the replica
    for root, dirs, files in os.walk(source_path):
        for dir in dirs:
            source_dir = os.path.join(root, dir)
            rel_path = os.path.relpath(source_dir, source_path)
            target_dir = os.path.join(replica_path, rel_path)
            os.makedirs(target_dir, exist_ok=True)

        for file in files:
            source_file = os.path.join(root, file)
            rel_path = os.path.relpath(source_file, source_path)
            target_file = os.path.join(replica_path, rel_path)
            os.makedirs(os.path.dirname(target_file), exist_ok=True)

            # Check first if file doesn't exist, and then if it's different to the source. Copy if any verify
            if not os.path.exists(target_file) or not filecmp.cmp(source_file, target_file, shallow=False):
                shutil.copy2(source_file, target_file)

    # Remove directories and files present in the replica that aren't present in the source
    for root, dirs, files in os.walk(replica_path, topdown=False):
        for file in files:
            target_file = os.path.join(root, file)
            rel_path = os.path.relpath(target_file, replica_path)
            source_file = os.path.join(source_path, rel_path)

            if not os.path.exists(source_file):
                os.remove(target_file)

        for dir_name in dirs:
            target_dir_path = os.path.join(root, dir_name)
            rel_path = os.path.relpath(target_dir_path, replica_path)
            source_dir_path = os.path.join(source_path, rel_path)

            if not os.path.exists(source_dir_path):
                os.rmdir(target_dir_path)
    return True


def main():

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
