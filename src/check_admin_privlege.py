import ctypes
import os

admin_level = {
    1: "ADMIN",
    0: "USER"
}


def return_priv_level() -> str:
    priv_level = is_user_admin()
    if os.name == "nt":
        res = admin_level[priv_level]
        return res
    else:
        try:
            res = os.getuid()
            return "ROOT" if res == 0 else "USER"
        except AttributeError:
            return "UNKNOWN"


def is_user_admin() -> int:
    if os.name != "posix":
        try:
            res = ctypes.windll.shell32.IsUserAnAdmin()
            return res
        except Exception as e:
            print(f"an error {e} occurred")
