import json
import requests
import application_checker as check


def check_app_list_availability_and_download(app_name: str):
    with open("list.json", "r") as file:
        res = file.read()
        data = json.loads(res)
        found = False
        for app in data['applications']:
            if app['name'] == app_name:
                print(f"found {app_name} in the available app list")
                found = True
                app_url = str(app['url'])
                try:
                    req = requests.get(app_url, timeout=10, stream=True)
                    if req.status_code == 200:
                        print("success was able to find given url")
                        file_name = app_url.split('/')[-1]
                        with open(file_name, "wb") as downloaded_file:
                            # adjust the chunk size if the download speed is too slow
                            # and my internet is bad
                            for chunk in req.iter_content(chunk_size=256 * 1024):  # 256 KB
                                if chunk:
                                    downloaded_file.write(chunk)
                        print(f'downloaded file saved as {file_name}')
                        return f'download {app_name} successful'
                    else:
                        print(f'returned error code {req.status_code}')
                except (
                        requests.ConnectionError,
                        requests.HTTPError,
                        requests.RequestException,
                        OSError) as e:
                    print(f'an error {e} occurred ')
        if not found:
            print(f"{app_name} not found in the list")


print(check_app_list_availability_and_download("Google Chrome"))
