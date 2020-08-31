## 制作镜像

* 下载项目仓库

```
# cd /root/
# git clone http://gitlab.corp.awcloud.com/aistack/aistack-ai-example.git
```

* 镜像制作

```
# cd aistack-ai-example/facenet/api-server
# docker build -t facenet:1.0-cpu -f docker/Dockerfile .
```

## 准备算法

```
# cd /root/
# git clone http://gitlab.corp.awcloud.com/aistack/aistack-ai-example.git
```

## 准备模型

```
# cd /root/aistack-ai-example/facenet
# mkdir model
# cd model
# wget http://172.16.9.25/aistack/aistack-ai-example/facenet/model/20180402-114759.zip
# unzip 20180402-114759.zip
```


## 启动 API 服务

* 命令格式

```
# docker run --name {容器名} -d -p {宿主机暴露端口}:80 -v {宿主机模型存放目录}:{容器中模型存放路径} -v {宿主机API服务代码存放路径}:{容器中API服务代码存放路径} {镜像名} {启动命令}
```

* 命令示例

```
# docker run --name facenet-api-server -d -p 30000:80 -v /root/aistack-ai-example/facenet/model/:/root/data/volume1/model/ -v /root/aistack-ai-example/:/root/data/volume1/code/ facenet:1.0-cpu sh -c 'export MODEL_PATH="/root/data/volume1/model/20180402-114759/" && export PYTHONPATH="/root/data/volume1/code/facenet/api-server" && python /root/data/volume1/code/facenet/api-server/api.py'
```
