import yaml
import os

_config = None

def load_config(config_file="config.yaml"):
    """加载配置文件"""
    global _config

    if not os.path.isabs(config_file):
        config_path = os.path.join(os.getcwd(), config_file)
    else:
        config_path = config_file

    if not os.path.exists(config_path):
        print(f"配置文件不存在: {config_path}")
        return None

    try:
        with open(config_path, 'r', encoding='utf-8') as stream:
            _config = yaml.safe_load(stream)
            print(f"配置文件加载成功: {config_path}")
            return _config
    except yaml.YAMLError as exc:
        print(f"配置文件格式错误: {exc}")
        return None
    except Exception as exc:
        print(f"加载配置文件时发生错误: {exc}")
        return None

def get_config():
    """获取配置对象"""
    global _config
    if _config is None:
        load_config()
    return _config

def get_value(key_path, default=None):
    """
    获取配置值，支持嵌套键访问
    例如: get_value('server.ip') 或 get_value('student.name')
    """
    global _config
    config = _config
    if config is None:
        return default

    keys = key_path.split('.')
    value = config

    try:
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        return default

def reload_config():
    """重新加载配置文件"""
    global _config
    _config = None
    return load_config()

def __getattr__(name):
    """
    当访问不存在的属性时，返回配置对象
    这样可以通过任何不存在的属性名访问到完整的配置
    """
    return get_config()

# 模块导入时自动加载配置
load_config()
