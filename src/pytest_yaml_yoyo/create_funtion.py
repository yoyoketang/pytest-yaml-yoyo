import sys
import types
from typing import Any, Callable, Mapping, Sequence
from inspect import Parameter, Signature


def create_function_from_parameters(
        func: Callable[[Mapping[str, Any]], Any],
        parameters: Sequence[Parameter],
        documentation=None,
        func_name=None,
        func_filename=None):
    """
        动态创建函数
    :param func: callback 回调函数
    :param parameters: 调用函数的参数
    :param documentation: 函数描述文档
    :param func_name: 函数名称
    :param func_filename: 函数文件名称
    :return: 返回函数对象function obj
    """
    new_signature = Signature(parameters)  # Checks the parameter consistency

    def pass_locals():
        return dict_func(locals())  # noqa: F821

    code = pass_locals.__code__
    mod_co_arg_count = len(parameters)
    mod_co_n_locals = len(parameters)
    mod_co_var_names = tuple(param.name for param in parameters)
    mod_co_name = func_name or code.co_name
    if func_filename:
        mod_co_filename = func_filename
        mod_co_first_lineno = 1
    else:
        mod_co_filename = code.co_filename
        mod_co_first_lineno = code.co_firstlineno

    if sys.version_info >= (3, 8):
        modified_code = code.replace(
            co_argcount=mod_co_arg_count,
            co_nlocals=mod_co_n_locals,
            co_varnames=mod_co_var_names,
            co_filename=mod_co_filename,
            co_name=mod_co_name,
            co_firstlineno=mod_co_first_lineno,
        )
    else:
        modified_code = types.CodeType(
            mod_co_arg_count,
            code.co_kwonlyargcount,
            mod_co_n_locals,
            code.co_stacksize,
            code.co_flags,
            code.co_code,
            code.co_consts,
            code.co_names,
            mod_co_var_names,
            mod_co_filename,
            mod_co_name,
            mod_co_first_lineno,
            code.co_lnotab
        )

    default_arg_values = tuple(
        p.default for p in parameters if p.default != Parameter.empty
    )
    modified_func = types.FunctionType(
        modified_code,
        {'dict_func': func, 'locals': locals},
        name=func_name,
        argdefs=default_arg_values
    )
    modified_func.__doc__ = documentation
    modified_func.__signature__ = new_signature
    return modified_func
