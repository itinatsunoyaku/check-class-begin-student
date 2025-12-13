import requests
import config

def is_alive() -> bool:
    server_ip = config.server.ip
    endpoint = "/isalive"
    timeout = config.server.timeout
    debug = config.debug

    try:
        url = f"{server_ip}{endpoint}"
        if debug:
            print(f"请求URL: {url}")

        response = requests.get(url, timeout=timeout)
        if response.text == "True":
            return True
        else:
            if debug:
                print("未在签到时间")
            return False

    except requests.exceptions.Timeout:
        if debug:
            print("请求超时")
        return False

    except requests.exceptions.RequestException as e:
        if debug:
            print(f"未找到服务器或网络错误: {e}")
        return False

def my_id() -> str | None:
    server_ip = config.server.ip
    endpoint = "/myid"
    timeout = config.server.timeout
    debug = config.debug

    try:
        url = f"{server_ip}{endpoint}"
        if debug:
            print(f"请求URL: {url}")

        response = requests.get(url, timeout=timeout)
        return response.text

    except requests.exceptions.RequestException as e:
        if debug:
            print(f"获取ID时发生错误: {e}")
        return None

def check_in(info: dict) -> int:
    server_ip = config.server.ip
    endpoint = "/checkin"
    timeout = config.server.timeout
    debug = config.debug

    try:
        url = f"{server_ip}{endpoint}"
        if debug():
            print(f"请求URL: {url}")
            print(f"学生信息: {info}")

        response = requests.post(url, json=info, timeout=timeout)
        return response.status_code

    except requests.exceptions.RequestException as e:
        if debug():
            print(f"签到时发生错误: {e}")
        return -1