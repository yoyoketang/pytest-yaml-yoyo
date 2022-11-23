from jinja2 import Template


def rend_template_str(t_str, *args, **kwargs):
    """
       渲染模板字符串, 改写了默认的引用变量语法{{var}}, 换成${var}
            模板中引用变量语法 ${var},
            调用函数 ${fun()}
        :return: 渲染之后的值
    """
    t = Template(t_str, variable_start_string='${', variable_end_string='}')
    res = t.render(*args, **kwargs)
    if t_str.startswith("${") and t_str.endswith("}"):
        try:
            return eval(res)
        except Exception:      # noqa
            return res
    else:
        return res


def rend_template_obj(t_obj: dict, *args, **kwargs):
    """
       传 dict 对象，通过模板字符串递归查找模板字符串，转行成新的数据
    """
    if isinstance(t_obj, dict):
        for key, value in t_obj.items():
            if isinstance(value, str):
                t_obj[key] = rend_template_str(value, *args, **kwargs)
            elif isinstance(value, dict):
                rend_template_obj(value, *args, **kwargs)
            elif isinstance(value, list):
                t_obj[key] = rend_template_array(value, *args, **kwargs)
            else:
                pass
    return t_obj


def rend_template_array(t_array, *args, **kwargs):
    """
       传 list 对象，通过模板字符串递归查找模板字符串
    """
    if isinstance(t_array, list):
        new_array = []
        for item in t_array:
            if isinstance(item, str):
                new_array.append(rend_template_str(item, *args, **kwargs))
            elif isinstance(item, list):
                new_array.append(rend_template_array(item, *args, **kwargs))
            elif isinstance(item, dict):
                new_array.append(rend_template_obj(item, *args, **kwargs))
            else:
                new_array.append(item)
        return new_array
    else:
        return t_array


def rend_template_any(any_obj, *args, **kwargs):
    """渲染模板对象:str, dict, list"""
    if isinstance(any_obj, str):
        return rend_template_str(any_obj, *args, **kwargs)
    elif isinstance(any_obj, dict):
        return rend_template_obj(any_obj, *args, **kwargs)
    elif isinstance(any_obj, list):
        return rend_template_array(any_obj, *args, **kwargs)
    else:
        return any_obj


"""
# 渲染 yaml 转的dict数据, 示例:
variables = {
    "username": "${user()}",
    "password": "123456",
    "age": "${age}",
    "data": {
        "key": "${user()}",
        "name": ["x", {"info": {"x": "1", "y": "${user()}"}}]
    }
}

def user():
    return "test"
age = 22
rend_template_obj(variables, user=user, age=age)
print(variables)
"""