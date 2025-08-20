import ctypes
from ctypes import POINTER, byref, cast
from ctypes.wintypes import LPWSTR, DWORD, LPCWSTR, LPDWORD, LPBYTE

'''
TO DO LIST AND RETURN USERS
ADD USERS
DEL USERS 
'''

# load dll
netapi32 = ctypes.WinDLL("Netapi32.dll")

# consts
USER_Level = 1
user_filter = 2  # FILTER_NORMAL_ACCOUNT
user_max_preferred_length = DWORD(-1)

user_privilege = 1  # USER_PRIV_USER


# incase
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


# api for creating deleting and adding

Net_user_enumerate = netapi32.NetUserEnum
NetApiBufferFree = netapi32.NetApiBufferFree
Net_user_add = netapi32.NetUserAdd
Net_user_del = netapi32.NetUserDel


def enumerate_users():
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
            print(f"ID:{ID} user:{user.usri1_name}")
    else:
        print(f"got an error {status}")


def add_user(user_name, password=None):
    '''
    Net_user_add.argtypes = [
        LPCWSTR,  # SERVER_NAME in ourcase local computer
        DWORD,  # LEVEL
        POINTER(LPBYTE),  # BUFFER [OUT]
        LPDWORD  # PARAM_ERR]
    ]
    Net_user_add.restype = DWORD'''
    pass


if __name__ == "__main__":
    enumerate_users()
