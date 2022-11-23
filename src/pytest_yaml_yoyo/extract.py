from requests import Response
import jsonpath
import jmespath
import re
from . import exceptions


def extract_by_object(response: Response, extract_expression: str):
    """
       从response 对象属性取值 [status_code, url, ok, headers, cookies, text, json, encoding]
    :param response: Response Obj
    :param extract_expression: 取值表达式
    :return: 返回取值后的结果
    """
    res = {
        "headers": response.headers,
        "cookies": dict(response.cookies)
    }
    if extract_expression in ["status_code", "url", "ok", "encoding"]:
        return getattr(response, extract_expression)
    elif extract_expression.startswith('headers') or extract_expression.startswith('cookies'):
        return extract_by_jmespath(res, extract_expression)
    elif extract_expression.startswith('body') or extract_expression.startswith('content'):
        try:
            response_parse_dict = response.json()
            return extract_by_jmespath({"body": response_parse_dict}, extract_expression)
        except Exception as msg:
            raise exceptions.ExtractExpressionError(f'expression:<{extract_expression}>, error: {msg}')
    elif extract_expression.startswith('$.'):
        try:
            response_parse_dict = response.json()
            return extract_by_jsonpath(response_parse_dict, extract_expression)
        except Exception as msg:
            raise exceptions.ExtractExpressionError(f'expression:<{extract_expression}>, error: {msg}')
    else:
        # 其它取值 正则匹配
        return extract_by_regex(response.text, extract_expression)

def extract_by_jsonpath(extract_value: dict, extract_expression: str): # noqa
    """
        json path 取值
    :param extract_value: response.json()
    :param extract_expression: eg: '$.code'
    :return: None或 提取的第一个值 或全部
    """
    extract_value = jsonpath.jsonpath(extract_value, extract_expression)
    if not extract_value:
        return
    elif len(extract_value) == 1:
        return extract_value[0]
    else:
        return extract_value


def extract_by_jmespath(extract_obj: dict, extract_expression: str):  # noqa
    """
        jmes path 取值
    :param extract_obj: {
        "body": response.json(),
        "cookies": dict(response.cookies),
        "headers": response.headers,
    }
    :param extract_expression: eg: 'body.code'
    :return: 未提取到返回None, 提取到返回结果
    """  # noqa
    try:
        extract_value = jmespath.search(extract_expression, extract_obj)
        return extract_value
    except Exception as msg:
        raise exceptions.ExtractExpressionError(f'expression:<{extract_expression}>, error: {msg}')


def extract_by_regex(extract_obj: str, extract_expression: str):
    """
       正则表达式提取返回结果
    :param extract_obj: response.text
    :param extract_expression:
    :return:
    """
    extract_value = re.findall(extract_expression, extract_obj, flags=re.S)
    if not extract_value:
        return ''
    elif len(extract_value) == 1:
        return extract_value[0]
    else:
        return extract_value
