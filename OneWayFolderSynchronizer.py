import os
import argparse
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")


def sync_replica_with_source(source_path, replica_path):
    print(f"syncing {source_path} to {replica_path}")


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

    while True:
        sync_replica_with_source(args.source_path, args.replica_path)
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
