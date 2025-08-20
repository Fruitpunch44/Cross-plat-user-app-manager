import ctypes
from ctypes import POINTER
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


Net_user_enumerate = netapi32.NetUserEnum
Net_user_add = netapi32.NetUserAdd
Net_user_del = netapi32.NetUserDel

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

Net_user_add.argtypes = [
    LPCWSTR,  # SERVER_NAME in ourcase local computer
    DWORD,  # LEVEL
    POINTER(LPBYTE),  # BUFFER [OUT]
    LPDWORD  # PARAM_ERR]
]
Net_user_add.restype = DWORD
pointer_buff = LPBYTE()
entries_read = DWORD(0)
total_entries = DWORD(0)
resume = DWORD(0)
