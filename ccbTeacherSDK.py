import requests
import config
import httpx
from enum import Enum

def d_print(*args, **kwargs) -> None:
    if config.debug:
        print(*args, **kwargs)

async def is_alive() -> bool:
    server_ip = config.server.ip
    endpoint = "/isalive"
    timeout = config.server.timeout
    debug = config.debug

    try:
        url = f"{server_ip}{endpoint}"
        d_print(f"请求URL: {url}")

        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=timeout)

        if response.text == "True":
            return True
        else:
            d_print("未在签到时间")
            return False

    except requests.exceptions.Timeout:
        d_print("请求超时")
        return False

    except requests.exceptions.RequestException as e:
        d_print(f"未找到服务器或网络错误: {e}")
        return False

async def my_id() -> int | None:
    server_ip = config.server.ip
    endpoint = "/myid"
    timeout = config.server.timeout
    debug = config.debug

    try:
        url = f"{server_ip}{endpoint}"
        d_print(f"请求URL: {url}")

        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=timeout)
        return int(response.text)

    except requests.exceptions.RequestException as e:
        d_print(f"获取ID时发生错误: {e}")
        return None

    except ValueError:
        d_print("服务器返回的ID格式错误")
        return None

class CResult(Enum):
    SUCCESS = 1 # 签到成功
    P_WRONG = 2 # 秘钥错误
    ALREADY = 3 # 已经签到过了
    ERROR = 4 # 签到失败
    FATAL = 5 # 致命错误（如网络问题）

async def check_in(info: dict) -> CResult | None:
    server_ip = config.server.ip
    endpoint = "/checkin"
    timeout = config.server.timeout
    debug = config.debug

    try:
        url = f"{server_ip}{endpoint}"
        if debug():
            print(f"请求URL: {url}")
            print(f"学生信息: {info}")

        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=info, timeout=timeout)

            if response == 200:
                d_print("成功", f"签到成功！状态码: {response}")
                return CResult.SUCCESS
            elif response == 401:
                d_print("失败", "签到失败：秘钥错误")
                return CResult.P_WRONG
            elif response == 409:
                d_print("提示", "已经签到过了")
                return CResult.ALREADY
            else:
                d_print("失败", f"签到失败，状态码: {response}")
                return CResult.ERROR
    except requests.exceptions.RequestException as e:
        if debug():
            print(f"签到时发生错误: {e}")
        return CResult.FATAL