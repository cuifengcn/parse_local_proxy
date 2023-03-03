import winreg
import re
import requests

# method1
import urllib.request

print(urllib.request.getproxies())

# method2
def get_proxy():
    proxy = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings")
    server, _type = winreg.QueryValueEx(proxy, "ProxyServer")  # 代理的地址
    enabled, _type = winreg.QueryValueEx(proxy, "ProxyEnable")  # 是否启用了手动代理
    auto_config = None
    try:
        auto_config = winreg.QueryValueEx(proxy, "AutoConfigURL")
    except FileNotFoundError:
        pass
    if enabled == 1:
        proxy = server
    elif auto_config is not None:
        try:
            config_file = auto_config[0]
            config_file = requests.get(config_file, timeout=10)
            content = config_file.text
            # return "PROXY 127.0.0.1:19180"
            _reg = re.compile(r'return "PROXY ([0-9a-zA-Z\.:]*)"')
            _reg2 = re.compile(r'return \'PROXY ([0-9a-zA-Z\.:]*)\'')
            res = _reg.findall(content)
            if not res:
                res = _reg2.findall(content)
                if not res:
                    print("查询代理-正则匹配失败")
                    return None
            proxy = res[0]
        except Exception as e:
            print(e.__str__())
            proxy = None
    else:
        proxy = None
    if proxy and not proxy.startswith("http") and proxy[0].isdigit():
        proxy = "http://" + proxy
    if proxy and ";" in proxy:
        proxy = proxy.split(";")[0]
    if proxy and "=" in proxy:
        proxy = proxy.replace("=", "://")
    return proxy
