准备开发环境
============

#. fork 仓库
#. 克隆你fork的仓库 :code:`git clone git@github.com:yournamehere/biblishelf.git`
#. 安装依赖 :code:`pip install -r requirement.txt`
#. 开启git commit强制检查 :code:`pre-commit install` 确保每次提交代码都经过了静态检查
#. 静态检查／修改变更记录中的文件 :code:`pre-commit run`
#. 静态检查／修改所有文件 :code:`pre-commit run --all`
#. build 文档 :code:`./setup.py sphinx_build`
#. 运行测试 :code:`pytest`
#. 兼容性测试 :code:`tox`
