# dockerpypbc-ringsignature
本科毕设异构环签名


windows需要环境：安装docker，mingw，配置环境变量并修改make命令名称

使用  
```shell
  make br
```
命令创建docker环境

使用
```docker
  docker run -it --rm <id>
```
命令运行容器





这个docker是从下面这里搞的
```
https://github.com/Hesamsrk/docker-env-pypbc
```
修改：
1.这个makefile里build dockerfile的d没大写导致报错，我给改了
2.给换了个更适合CN特色地区用户的源
# 不是我说，这个pypbc正常一步步安装真是麻烦死了
