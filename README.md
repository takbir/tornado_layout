tornado_layout
==============

这是一个使用Tornado的web框架所搭建基本结构。


* 已经将目录结构组织完成.
* 添加一些python web开发的基础组件
* 将url映射集中在urls.py中
* 将项目的配置项移至settings.py中; 项目启动时会尝试从local_settings.py中导入, 这个动作会覆盖settings.py中定义的配置项.
* 添加restart_port.py这个启动脚本, 用于测试以及在生产环境中配合nginx启动.
