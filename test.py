import unittest
from unittest.mock import patch
from OneWayFolderSynchronizer import sync_replica_with_source


class TestSyncReplica(unittest.TestCase):
    def test_non_existent_source(self):
        # Test when the source path does not exist.
        source_path = "/folder/to/sync"
        replica_path = "/folder/replicated"
        # Patch os.path.exists to simulate that the source does not exist.
        with patch("os.path.exists", return_value=False):
            with self.assertLogs(level="INFO") as log:
                result = sync_replica_with_source(source_path, replica_path)
                # The function should return False to stop the synchronization loop.
                self.assertFalse(result)
            # Verify the expected log message is produced.
            expected_message = (
                f"The path {source_path} does not exist. Aborting program."
            )
            self.assertIn(expected_message, log.output[0])

    def test_source_is_not_directory(self):
        # Test when the source path exists but is not a directory (e.g. it is a file).
        source_path = "/folder/to/sync"
        replica_path = "/folder/replicated"
        # Patch os.path.exists to simulate that the path exists...
        with patch("os.path.exists", return_value=True):
            # ...and patch os.path.isdir to simulate that it is not a directory.
            with patch("os.path.isdir", return_value=False):
                with self.assertLogs(level="INFO") as log:
                    result = sync_replica_with_source(source_path, replica_path)
                    self.assertFalse(result)
            expected_message = (
                f"The path {source_path} is not a directory. Aborting program."
            )
            self.assertIn(expected_message, log.output[0])


if __name__ == "__main__":
    unittest.main()
