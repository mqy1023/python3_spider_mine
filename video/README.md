# 线程池下载资源网的视频资源(2020-06-13)

#####  一、`mac`下载安装 `ffmpeg` 环境

* 1、[ffmpeg下载链接](https://ffmpeg.zeranoe.com/builds/)

* 2、下载完成后配置本地环境变量

```
export FFMPEG_HOME=/Users/eric/envirs/ffmpeg/
export PATH=$PATH:$FFMPEG_HOME/bin
```

* 3、对应的下载命令

`ffmpeg -i "http://youku.com-youku.net/20180614/11920_4c9e1cc1/index.m3u8" "第001集.mp4"`


> 如果用 Python 接口，也只需要两行代码：

```python
import ffmpy3
ffmpy3.FFmpeg(inputs={'http://youku.com-youku.net/20180614/11920_4c9e1cc1/index.m3u8': None}, outputs={'第001集.mp4':None}).run()
```

##### 二、资源网

[OK资源网](http://www.jisudhw.com/index.php)
