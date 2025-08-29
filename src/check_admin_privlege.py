import ctypes
import os

admin_level = {
    1: "ADMIN",
    0: "USER"
}


def is_user_admin() -> str:
    if os.name != "posix":
        try:
            get_admin_level = ctypes.windll.shell32.IsUserAnAdmin()
            priv_level = admin_level[get_admin_level]
            return priv_level
        except Exception as e:
            print(f"an error {e} occurred")
    else:
        try:
            res = os.getuid()
            return "ROOT" if res == 0 else "USER"
        except AttributeError:
            return "UNKNOWN"
