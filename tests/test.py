import unittest
from unittest.mock import patch, MagicMock
import sys

# import your functions
from src import check_admin_privlege


class TestPrivilegeFunctions(unittest.TestCase):

    @patch("os.name", "nt")
    @patch("ctypes.windll.shell32.IsUserAnAdmin", return_value=1)
    def test_is_user_admin_windows_admin(self, mock_admin):
        self.assertEqual(check_admin_privlege.is_user_admin(), 1)

    @patch("os.name", "nt")
    @patch("ctypes.windll.shell32.IsUserAnAdmin", return_value=0)
    def test_is_user_admin_windows_user(self, mock_admin):
        self.assertEqual(check_admin_privlege.is_user_admin(),  0)

    @patch("os.name", "posix")
    @patch("os.getuid", return_value=0)
    def test_return_priv_level_posix_root(self, mock_uid):
        self.assertEqual(check_admin_privlege.return_priv_level(), "ROOT")

    @patch("os.name", "posix")
    @patch("os.getuid", return_value=1000)
    def test_return_priv_level_posix_user(self, mock_uid):
        self.assertEqual(check_admin_privlege.return_priv_level(), "USER")

    @patch("os.name", "nt")
    @patch("ctypes.windll.shell32.IsUserAnAdmin", return_value=1)
    def test_return_priv_level_windows_admin(self, mock_admin):
        self.assertEqual(check_admin_privlege.return_priv_level(), "ADMIN")

    @patch("os.name", "nt")
    @patch("ctypes.windll.shell32.IsUserAnAdmin", return_value=0)
    def test_return_priv_level_windows_user(self, mock_admin):
        self.assertEqual(check_admin_privlege.return_priv_level(), "USER")


if __name__ == "__main__":
    unittest.main()
