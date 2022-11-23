from setuptools import setup

"""The setup script.
# 作者-上海悠悠 微信wx:283340479
# blog地址 https://www.cnblogs.com/yoyoketang/
"""

setup(
    name='pytest-yaml-yoyo',
    url='https://github.com/yoyoketang/pytest-yaml-yoyo',
    version='1.0',
    author="上海-悠悠",
    author_email='283340479@qq.com',
    description='http/https API run by yaml',
    long_description=open("README.rst").read(),
    package_dir={"": "src"},
    packages=["pytest_yaml_yoyo"],
    classifiers=[
        'Framework :: Pytest',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 3.8',
    ],
    license='proprietary',
    keywords=[
        'pytest', 'py.test', 'pytest-yaml', 'pytest-yaml-yoyo',
    ],
    python_requires=">=3.8",
    install_requires=[
        'Jinja2==3.1.2',
        'jmespath==0.9.5',
        'jsonpath==0.82',
        'pytest==7.2.0',
        'PyYAML==6.0',
        'requests==2.28.1',
    ],
    entry_points={
        'pytest11': [
            'pytest-yaml-yoyo = pytest_yaml_yoyo.plugin',
        ]
    }
)
