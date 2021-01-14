# 2021年毕业设计 (计算机科学与技术专业)

---

## 项目结构

> 在自定义的`Flask`项目通用结构(类似于`Django`)的基础上添加`爬虫`和`数据分析`文件夹

- `/app/`: 类似于Django的app文件夹
  - `__init__.py`: 声明这个文件夹是一个 python package
  - `views.py`: 提供渲染网页模板的蓝图
  - `api.py`: 提供后端API的蓝图, 使用 Ajax POST 方式访问
  - `models.py`: 提供可操作的数据库ORM对象和定义数据模型
  - `decorators.py`: 提供装饰器, 例如: 要求用户必须登录的视图装饰器
  - `utils.py`: 提供一些自定义函数
- `/conf/`: 项目的配置文件夹
  - `__init__.py`: 声明这个文件夹是一个 python package
  - `app.py`: 提供创建 Flask App 对象的函数
  - `config.py`: 将Flask需要的配置打包成一个Class
  - `settings.py`: 提供一些目录的绝对路径和其他杂项
- `/db/`: 存放数据库相关文件
  - `models.db`: SQLite3本地文件
- `/migrations/`: Flask Migrate生成的文件夹
- `/static/`: 存放网站所需的静态文件
  - `/css/`: 存放css文件
  - `/js/`: 存放js文件
  - `/images/`: 存放图片
- `/templates/`: 存放 Jinja2 网页模板
- `/spider/`: 存放爬虫程序
- `/data_analysis/`: 存放数据分析程序
- `manage.py`: 用于启动服务端, 进行数据库的初始化、迁移、升级等
- `push.sh`: 一步推送至远端仓库的shell脚本
- `requirements.txt`: pipreqs生成的引入的第三方库清单, 配合 `pip -r` 命令使用
