import os
import argparse
import time
import logging
import filecmp
import shutil


def setup_logging(log_path):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_path, mode="a"), logging.StreamHandler()],
    )


def sync_replica_with_source(source_path, replica_path):
    if not os.path.exists(source_path):
        logging.error(f"Source path {source_path} does not exist. Aborting program.")
        return False
    if not os.path.isdir(source_path):
        logging.error(f"Source path {source_path} is not a directory. Aborting program.")
        return False

    os.makedirs(replica_path, exist_ok=True)

    # Copy directories and files from source to replica
    for root, dirs, files in os.walk(source_path):
        for dir in dirs:
            source_dir = os.path.join(root, dir)
            rel_path = os.path.relpath(source_dir, source_path)
            replica_dir = os.path.join(replica_path, rel_path)

            if not os.path.exists(replica_dir):
                os.makedirs(replica_dir, exist_ok=True)
                logging.info(f"Created directory: {replica_dir}")

        for file in files:
            source_file = os.path.join(root, file)
            rel_path = os.path.relpath(source_file, source_path)
            replica_file = os.path.join(replica_path, rel_path)

            os.makedirs(os.path.dirname(replica_file), exist_ok=True)

            if not os.path.exists(replica_file) or not filecmp.cmp(
                source_file, replica_file, shallow=False
            ):
                try:
                    shutil.copy2(source_file, replica_file)
                    logging.info(f"Copied: {source_file} -> {replica_file}")
                except Exception as e:
                    logging.error(f"Failed to copy {source_file} -> {replica_file}: {e}")

    # Remove files and directories that are in replica but not in the source
    for root, dirs, files in os.walk(replica_path, topdown=False):
        for file in files:
            replica_file = os.path.join(root, file)
            rel_path = os.path.relpath(replica_file, replica_path)
            source_file = os.path.join(source_path, rel_path)

            if not os.path.exists(source_file):
                try:
                    os.remove(replica_file)
                    logging.info(f"Deleted file: {replica_file}")
                except Exception as e:
                    logging.error(f"Failed to delete {replica_file}: {e}")

        for dir_name in dirs:
            replica_dir_path = os.path.join(root, dir_name)
            rel_path = os.path.relpath(replica_dir_path, replica_path)
            source_dir_path = os.path.join(source_path, rel_path)

            if not os.path.exists(source_dir_path):
                try:
                    os.rmdir(replica_dir_path)
                    logging.info(f"Deleted directory: {replica_dir_path}")
                except Exception as e:
                    logging.error(f"Failed to delete directory {replica_dir_path}: {e}")

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
        help="Path to folder to be replicated",
    )
    parser.add_argument(
        "-r",
        "--replica_path",
        type=str,
        required=True,
        help="Path to folder that will be the replica",
    )
    parser.add_argument(
        "-l", "--log_path", type=str, required=True, help="Log file path"
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=int,
        required=True,
        help="Time interval in seconds between synchronizations",
    )

    args = parser.parse_args()

    setup_logging(args.log_path)

    logging.info("Starting directory synchronization...")

    try:
        while True:
            sync_replica_with_source(args.source_path, args.replica_path)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        logging.info("One Way Folder Synchronizer stopped by user.")


if __name__ == "__main__":
    main()
