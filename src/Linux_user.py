import subprocess
import shlex
import logging_helper
import check_admin_privlege
import os

# get the current user running the script
user = os.getcwd().split(" ")
current_user = user[0][9:][:7]


def list_users():
    list_command = "awk -F':' '{ print $1}' /etc/passwd"
    args = shlex.split(list_command)
    try:
        res = subprocess.run(args, capture_output=True, text=True)
        print(res.stdout)
    except subprocess.SubprocessError as e:
        print(f"an error {e} occurred ")
        logging_helper.logger.error(f'an error {e} occurred')


def create_user(username: str, password=None):
    add_user_command = f"sudo useradd {username}"
    if password:
        command = f"sudo useradd {username}"
        args = shlex.split(command)
        try:
            subprocess.run(args)
            subprocess.run(
                ["sudo", "chpasswd"],
                input=f"{username}:{password}",
                text=True,
                check=True
            )
            print(f"have created {username}")
            logging_helper.logger.info(
                f'current user:{current_user} created the account {username} '
                f'and has the privileges {check_admin_privlege.return_priv_level()}')
        except subprocess.SubprocessError as e:
            print(f"an error {e} occurred ")
            logging_helper.logger.error(f'an error {e} occurred')
    else:
        args = shlex.split(add_user_command)
        try:
            subprocess.run(args,
                           check=True)
        except subprocess.SubprocessError as e:
            print(f"an error {e} occurred ")
            logging_helper.logger.error(f'an error {e} occurred')


def del_user(username: str):
    delete_user_command = f"sudo userdel {username}"
    args = shlex.split(delete_user_command)
    try:
        subprocess.run(args)
        print(f"have successfully deleted {username}")
        logging_helper.logger.info(f'current user:{current_user} deleted the account {username} and has the privileges {check_admin_privlege.return_priv_level()}')
    except subprocess.SubprocessError as e:
        print(f"an error {e} occurred")
        logging_helper.logger.error(f'an error {e} occurred')
