from . import create_funtion
import types
from inspect import Parameter
from . import validate
from . import extract
from . import my_builtins
from . import render_template_obj
from . import exceptions


class RunYaml(object):
    """ 运行yaml """

    def __init__(self, raw: dict, module: types.ModuleType):
        self.raw = raw   # 读取yaml 原始数据
        self.module = module   # 动态创建的 module 模型
        self.module_variable = {}  # 模块变量
        self.context = {}

    def run(self):
        # config 获取用例名称 name 和 base_url
        case_name = self.raw.get('config').get('name', '')
        base_url = self.raw.get('config').get('base_url')
        config_variables = self.raw.get('config').get('variables')
        # 模块变量渲染
        self.context.update(__builtins__)  # noqa 内置函数加载
        self.context.update(my_builtins.__dict__)  # 自定义函数对象
        self.module_variable = render_template_obj.rend_template_any(config_variables, **self.context)
        teststeps = self.raw.get('teststeps', [])        # noqa

        def execute_yaml_case(args):
            for step in teststeps:
                response = None
                for item, value in step.items():
                    # 执行用例里面的方法
                    if item == 'name':
                        pass          # noqa
                    elif item == 'request':
                        request_session = args.get('requests_session')  # session 请求会话
                        if isinstance(self.module_variable, dict):
                            self.context.update(self.module_variable)    # 加载模块变量
                        request_value = render_template_obj.rend_template_any(value, **self.context)
                        response = request_session.send_request(
                            method=str(request_value.pop('method')).upper(),
                            url=request_value.pop('url'),
                            base_url=base_url,
                            **request_value
                        )
                    elif item == 'validate':
                        validate_value = render_template_obj.rend_template_any(value, **self.context)
                        self.validate_response(response, validate_value)
                    else:
                        try:
                            eval(item)(value)
                        except Exception as msg:
                            raise exceptions.ParserError(f'Parsers error: {msg}')

        f = create_funtion.create_function_from_parameters(
            func=execute_yaml_case,
            # parameters 传内置fixture
            parameters=[
                Parameter('request', Parameter.POSITIONAL_OR_KEYWORD),
                Parameter('requests_session', Parameter.POSITIONAL_OR_KEYWORD),
            ],
            documentation=case_name,
            func_name=str(self.module.__name__),
            func_filename=f"{self.module.__name__}.py",
        )

        # 向 module 中加入函数
        setattr(self.module, str(self.module.__name__), f)

    @staticmethod
    def validate_response(response, validate_check: list) -> None:
        """校验结果"""
        for check in validate_check:
            for check_type, check_value in check.items():
                actual_value = extract.extract_by_object(response, check_value[0])  # 实际结果
                expect_value = check_value[1]  # 期望结果
                if check_type in ["eq", "equals", "equal"]:
                    validate.equals(actual_value, expect_value)
                elif check_type in ["lt", "less_than"]:
                    validate.less_than(actual_value, expect_value)
                elif check_type in ["le", "less_or_equals"]:
                    validate.less_than_or_equals(actual_value, expect_value)
                elif check_type in ["gt", "greater_than"]:
                    validate.greater_than(actual_value, expect_value)
                elif check_type in ["ne", "not_equal"]:
                    validate.not_equals(actual_value, expect_value)
                elif check_type in ["str_eq", "string_equals"]:
                    validate.string_equals(actual_value, expect_value)
                elif check_type in ["len_eq", "length_equal"]:
                    validate.length_equals(actual_value, expect_value)
                elif check_type in ["len_gt", "length_greater_than"]:
                    validate.length_greater_than(actual_value, expect_value)
                elif check_type in ["len_ge", "length_greater_or_equals"]:
                    validate.length_greater_than_or_equals(actual_value, expect_value)
                elif check_type in ["len_lt", "length_less_than"]:
                    validate.length_less_than(actual_value, expect_value)
                elif check_type in ["len_le", "length_less_or_equals"]:
                    validate.length_less_than_or_equals(actual_value, expect_value)
                elif check_type in ["contains"]:
                    validate.contains(actual_value, expect_value)
                else:
                    if hasattr(validate, check_type):
                        getattr(validate, check_type)(actual_value, expect_value)
                    else:
                        print(f'{check_type}  not valid check type')
