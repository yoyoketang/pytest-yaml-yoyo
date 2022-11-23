import types
import yaml
from pathlib import Path
from _pytest.python import Module
import pytest
from requests.adapters import HTTPAdapter
from . import request_session
from . import runner


@pytest.fixture(scope="session")
def requests_session():
    """全局session"""
    s = request_session.HttpSession()
    # max_retries=2 重试2次
    s.mount('http://', HTTPAdapter(max_retries=2))
    s.mount('https://', HTTPAdapter(max_retries=2))
    yield s
    s.close()


@pytest.fixture()
def requests_function():
    """全局session"""
    s = request_session.HttpSession()
    # max_retries=2 重试2次
    s.mount('http://', HTTPAdapter(max_retries=2))
    s.mount('https://', HTTPAdapter(max_retries=2))
    yield s
    s.close()


@pytest.fixture(scope="module")
def requests_module():
    """全局session"""
    s = request_session.HttpSession()
    # max_retries=2 重试2次
    s.mount('http://', HTTPAdapter(max_retries=2))
    s.mount('https://', HTTPAdapter(max_retries=2))
    yield s
    s.close()


def pytest_collect_file(file_path: Path, parent):  # noqa
    if file_path.suffix == ".yml" and file_path.name.startswith("test"):
        py_module = Module.from_parent(parent, path=file_path)
        # 动态创建 module
        module = types.ModuleType(file_path.stem)
        # 解析 yaml 内容
        raw_dict = yaml.safe_load(file_path.open(encoding='utf-8'))
        # 用例名称test_开头
        run = runner.RunYaml(raw_dict, module)
        run.run()  # 执行用例
        # 重写属性
        py_module._getobj = lambda: module  # noqa
        return py_module
