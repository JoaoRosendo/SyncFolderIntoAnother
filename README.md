# Sync Folder Into Another

## Overview
This tool periodically synchronizes two directories, ensuring that a replica remains synchronized with the source.

## Example use case
You have the directory "Images" with a file called "cat.png". You choose that as your source directory, and "Backup" as your replica directory. While the program is running, "Backup" will contain "cat.png" and nothing more, even if other files were stored there before.

## Features
- Copies all files and subdirectories from the source directory to a replica.
- Removes files and directories from the replica that are not present in the source.
- Periodically syncs based on a user-defined interval.
- Logs the synchronization process to a user-defined file and to the console.

## Usage
Run the script with the following (required) arguments:

```sh
python sync.py -s <source_path> -r <replica_path> -l <log_path> -i <interval>
```

### Arguments:
- `-s`, `--source_path`: Path to the folder which will be replicated (Required)
- `-r`, `--replica_path`: Path to the folder which will be the replica (Required)
- `-l`, `--log_path`: Path to the file where the program's log will be stored (Required)
- `-i`, `--interval`: Time interval in seconds between each synchronization (Required)

## Known Limitations
As with every program, this one comes with some limitations, some of which may be:
- Built only with Linux in mind.
- Does not account for permissions or limited access (e.g., files without read permission).
- Does not account for special files (e.g. device files).
- Does not check if the replica directory has enough free space.

## License
This project is under the GNU License. Whatever.
