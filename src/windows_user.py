import ctypes
from ctypes import POINTER, byref, cast
from ctypes.wintypes import LPWSTR, DWORD, LPCWSTR, LPDWORD, LPBYTE, LPVOID, HANDLE, WORD, BOOL
from logging_helper import logger
import os
import getpass
import check_admin_privlege as priv

# load dll
netapi32 = ctypes.WinDLL("Netapi32.dll")
Advapi32 = ctypes.WinDLL("Advapi32.dll")

# get the current user running the script
user = os.getcwd().split(" ")
current_user = user[0][9:][:7]

# constants
USER_Level = 1
user_filter = 2  # FILTER_NORMAL_ACCOUNT
user_max_preferred_length = DWORD(-1)
user_privilege = 1  # USER_PRIV_USER
UF_SCRIPT = DWORD(0)

Status_codes = {
    0: "NERR_Success",
    5: "Error_Access_denied",
    86: "ERROR_INVALID_PASSWORD",
    2223: "NERR_GroupExists",
    2224: "NERR_UserExists",
    2245: "NERR_PasswordTooShort",
    2351: "NERR_Invalid_Computer",

}
LOGON_WITH_PROFILE = DWORD(1)  # logon_with_profile
CREATE_NEW_CONSOLE = DWORD(10)  # creation flag for log_on_with_user


def return_status_code(status_code: int) -> str:
    res = Status_codes[status_code]
    return res


# incase you want to return the name of users only
class USER_INFO_0(ctypes.Structure):
    _fields_ = [
        ("usri0_name", LPWSTR)
    ]


# create user field structure
class USER_INFO_1(ctypes.Structure):
    _fields_ = [
        ("usri1_name", LPWSTR),
        ("usri1_password", LPWSTR),
        ("usri1_password_age", DWORD),
        ("usri1_priv", DWORD),
        ("usri1_home_dir", LPWSTR),
        ("usri1_comment", LPWSTR),
        ("usri1_flags", DWORD),
        ("usri1_script_path", LPWSTR),
    ]


class STARTUPINFO(ctypes.Structure):
    _fields_ = [
        ("cb", DWORD),
        ("lpReserved", LPWSTR),
        ("lpDesktop", LPWSTR),
        ("lpTitle", LPWSTR),
        ("dwX", DWORD),
        ("dwY", DWORD),
        ("dwXSize", DWORD),
        ("dwYSize", DWORD),
        ("dwXCountChars", DWORD),
        ("dwYCountChars", DWORD),
        ("dwFillAttribute", DWORD),
        ("dwFlags", DWORD),
        ("wShowWindow", WORD),
        ("cbReserved2", WORD),
        ("lpReserved2", ctypes.POINTER(ctypes.c_byte)),
        ("hStdInput", HANDLE),
        ("hStdOutput", HANDLE),
        ("hStdError", HANDLE),
    ]


class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("hProcess", HANDLE),
        ("hThread", HANDLE),
        ("dwProcessId", DWORD),
        ("dwThreadId", DWORD),
    ]


def which_user_info_level(user_info: int) -> object:
    if user_info == 0:
        return USER_INFO_0
    elif user_info == 1:
        return USER_INFO_1
    else:
        print(f"invalid info level {user_info}")
        logger.logging.info(f"{user_info} is invalid")


# api for creating deleting and adding
Net_user_enumerate = netapi32.NetUserEnum
NetApiBufferFree = netapi32.NetApiBufferFree
Net_user_add = netapi32.NetUserAdd
Net_user_del = netapi32.NetUserDel
Create_Process_With_Logon = Advapi32.CreateProcessWithLogonW


def enumerate_users() -> None:
    # add status codes for the return value of net_user_enumerate
    Net_user_enumerate.argtypes = [
        LPCWSTR,  # servername
        DWORD,  # level
        DWORD,  # filter
        POINTER(LPBYTE),  # bufptr (out)
        DWORD,  # prefmaxlen
        LPDWORD,  # entriesread (out)
        LPDWORD,  # totalentries (out)
        LPDWORD  # resume_handle (in/out, optional)
    ]
    Net_user_enumerate.restype = DWORD
    pointer_buff = LPBYTE()
    entries_read = DWORD(0)
    total_entries = DWORD(0)

    status = Net_user_enumerate(
        None,
        USER_Level,
        user_filter,
        byref(pointer_buff),
        user_max_preferred_length,
        byref(entries_read),
        byref(total_entries),
        None
    )
    if status == 0:  # NERR_Success
        user_array = USER_INFO_1 * entries_read.value
        users = cast(pointer_buff, POINTER(user_array)).contents

        for ID, user in enumerate(users):
            print(f"ID:{ID} user:{user.usri1_name} ")
    else:
        print(f"got an error {return_status_code(status)}")


def log_on_with_user(user_name: str, user_pass: str):
    APP_NAME_TO_RUN = "C:\\Windows\\System32\\cmd.exe"
    Create_Process_With_Logon.argtypes = [
        LPCWSTR,
        LPCWSTR,
        LPCWSTR,
        DWORD,
        LPCWSTR,
        LPWSTR,
        DWORD,
        LPVOID,
        LPCWSTR,
        POINTER(STARTUPINFO),
        POINTER(PROCESS_INFORMATION)
    ]
    Create_Process_With_Logon.restype = BOOL

    si = STARTUPINFO()
    si.cb = ctypes.sizeof(STARTUPINFO)
    pi = PROCESS_INFORMATION()

    status = Create_Process_With_Logon(
        user_name,
        None,  # NO DOMAIN SO LOCAL MACHINE
        user_pass,
        LOGON_WITH_PROFILE,  # LOGON_WITH_PROFILE
        APP_NAME_TO_RUN,  # APP NAME
        None,  # command line
        DWORD(0),  # creation flag
        None,  # environment
        None,  # current directory
        byref(si),
        byref(pi)
    )

    if status != 0:
        # it launches a cmd window, and the user profile is created in C: drive
        print("success was able to start process with profile")
        ctypes.windll.kernel32.CloseHandle(pi.hProcess)
        ctypes.windll.kernel32.CloseHandle(pi.hThread)
        # close all open handles to prevent resource leaks
        # anything that returns a handle object should be deallocated
    else:
        error = ctypes.get_last_error()
        print(f'an error occurred {error}')
        logger.logging.info(f"an error {error} occurred refer to ms docs for further info")


def add_user(user_name, user_password=None) -> None:
    Net_user_add.argtypes = [
        LPCWSTR,  # SERVER_NAME in our case local computer
        DWORD,  # LEVEL
        LPBYTE,  # BUFFER [OUT]
        LPDWORD  # PARAM_ERR]
    ]
    Net_user_add.restype = DWORD
    user_info = USER_INFO_1()
    parm_err = DWORD(0)

    # populate the struct
    user_info.usri1_name = user_name
    user_info.usri1_password = user_password
    user_info.usri1_priv = user_privilege
    user_info.usri1_home_dir = None
    user_info.usri1_comment = None
    user_info.usri1_flags = UF_SCRIPT
    user_info.usri1_script_path = None

    status = Net_user_add(
        None,  # Defaults to local host u can always change it
        USER_Level,
        cast(byref(user_info), LPBYTE),
        byref(parm_err)
    )
    if status == 0:  # NERR_Success
        print(f"{user_name} was successfully created")
        log_on_with_user(user_name, user_password)
        logger.logging.info(f"{current_user} with privileges{priv.return_priv_level()} created an account {user_name}")
    else:
        print(f'failed to create {user_name} \n '
              f'STATUS:{return_status_code(status)}')


def delete_user(user_name: str) -> None:
    Net_user_del.argtypes = [
        LPCWSTR,  # LOCAL HOST IN OUR CASE
        LPCWSTR  # USER WE WANT TO KILL
    ]
    Net_user_del.restype = DWORD
    status = Net_user_del(
        None,
        user_name
    )
    if status == 0:  # NERR_Success
        print(f"{user_name} has be deleted from local device ")
        logger.logging.info(f"{current_user} with privileges {priv.return_priv_level()}deleted the user {user_name}")
    else:
        print(f'a system error has occurred {return_status_code(status)}')  # check the ms docs for the error codes
