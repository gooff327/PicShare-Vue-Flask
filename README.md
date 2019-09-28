## PicShare 网站简介


这是一个图片分享平台，借鉴Instagram的基础功能和页面布局并进行一点减法的移动端网页，也是我在移动端乃至Web项目的处女作，文章或者项目有问题的地方欢迎大家多多指正(o^^o)

## 先来点图

------

**登录&注册**
![图片描述](https://i.loli.net/2019/06/17/5d0708ab3b3aa93675.png)
**首页&内容发布**
![图片描述](https://i.loli.net/2019/06/17/5d07493b691ed83770.png)
**评论&转发**
![图片描述](https://i.loli.net/2019/06/17/5d074a1032fca73912.png)
**消息**
![图片描述](https://i.loli.net/2019/06/17/5d074a6f0ab9748294.png)
**个人中心**
![图片描述](https://i.loli.net/2019/06/17/5d074ac85ff3c61679.png)
![图片描述](https://i.loli.net/2019/06/17/5d074ac55b40c90913.png)
## 项目技术栈

------

- **前端**：Vue.js + Vue Router + Vuex + ElementUI
- **后端**： Python Flask
- **数据**： MariaDB,对象云存储,图床

## 功能模块

------

### 登录&注册

网站的内容需要登录使用，其中注册的第一项为设置头像，不少小伙伴及面试官没有看见而导致提交时候失败，这个地方是我的疏忽，后期有时间了进行优化其显示与验证功能

### 首页&关注

用户登录成功后进入首页，首页可以获取到所有用户最近发表的图文动态，关注页面可以获取到所有关注用户的最近动态，用户可以通过点击点赞按钮对动态进行点赞操作，点击转发按钮进入内容转发页面，点击评论按钮进入评论页面

### 发表&转发

提供给用户一个可以自由发表与转发的面板

### 消息

用户可以收到与自己发表或者转发内容相关的消息，包括点赞，转发，评论，同时用户还可以收到与账户关系相关的消息，如关注，私信（有待实现）

### 个人中心

页面的布局及内容完全模仿Instagram的移动端网页，用户可以通过个人中心展示自己或者他人的信息，他人信息的入口为显示用户头像及用户名的地方（首页&关注的内容去，评论内容区，消息详情区域）

### 粉丝&关注

通过一个列表展示用户之间的关系，同时提供给用户关注与取消关注的按钮

## 项目部署

------

### 前端

默认当前目录为前端目录(frontend/)

1. 安装所有的npm依赖

   ```shell
   npm install
   ```

2. build

   ```shell
   npm run build
   ```

   此时前端目录上一级得到的dist文件夹就是我们服务器部署需要的文件夹

### 后端

默认当前的目录为后端目录(backend/)

1. 确保你的服务器已安装Python 3 （推荐Python 3.6及以上）及虚拟环境 venv

2. 创建虚拟环境

   ```shell
   python3 -m venv ./venv
   ```

3. 激活虚拟环境

   ```shell
   source ./venv/bin/activate
   ```

4. 安装后端需要的依赖

   ```shell
   pip install -r requirements.txt
   ```

5. 编辑自己的private_config.py
   1. SECRET_KEY 可以是字符串，通过这个字符串进行密码加密存储时的加盐
   2. HOST 数据库的地址，默认为本地
   3. USERNAME 数据库的连接用户名，我使用的是root
   4. PASSWORD 数据库的连接密码
   5. PORT 数据库的监听端口，默认为3306
   6. DATABASE 数据库的名称，需要先建立数据库，不用建立表结构
   7. 如果需要使用对象云存储服务，则需要对Bucket进行相应的配置

### 服务器

1. 使用Nginx进行反向代理，配置文件参考backend目录下的default文件
2. 使用Heroku进行持续部署，配置文件参考backend目录下的Procfile文件

### 部署结果

- 个人主机：[Picshare_running on_host](http://gooff.me)
- Heroku：[Picshare runing on Heroku](https://gooff.herokuapp.com)
- Azure: [Picshare running on Azure](https://picshare.azurewebsites.net)

## 总结

------

这是我的第一次接触到Web开发，不断爬坑不断学习，从中学习到了如何使用H5，CSS3，JS，Python以及服务器部署
由于对这方面的学习更加的深入，回过头来看，自己以前的写法着实青涩，后期有重构的打算
