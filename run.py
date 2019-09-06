# encoding:utf-8
import os
import time

import logging


def get_app_cpu_usage(package_name, device_name="", device_cores=-1, silence=True):
    # type: (str, str,int,bool) -> float
    """
    :param package_name: 待检测安卓应用包名【必填】
    :param device_name: 待检测设备名（使用“adb devices”命令获取）【若为空则检测默认设备，当设备数大于一时将报错】
    :param device_cores: 设备CPU核心数，为-1时程序将自动获取核心数（依赖adb工具的输出格式，不保证后续版本的正确性）
    :param silence: 是否静默运行，为True时只打印错误信息，为False时将会打印全部信息
    :return: 该设备指定应用的CPU占用率（例如：占用15%则return 0.15）

    使用前，请确保您已正确安装adb工具并将其添加到系统环境变量，若您使用pycharm来执行此方法，
    请确认pycharm的环境配置是否包括了adb所在路径，即pycharm下运行shell命令是否能够调用adb工具

    验证方法：
    在pycharm的terminal中输入adb，是否能够执行相关命令，若显示“'adb' 不是内部或外部命令，也不是可运行的程序”
    请在File->Settings->Tools->Terminal->Project Settings->Environment Variables中确认是否包含了adb的环境变量
    """
    if device_name.__len__() > 0:
        device_name = "-s" + device_name
    else:
        if not silence:
            print "未指定设备名，尝试连接默认设备"
    if device_cores is -1 and not silence:
        print "未指定CPU核心数，尝试自动获取（结果不一定可靠）"
        try:
            cmd = 'adb ' + device_name + ' shell top -n 1'
            device_cores = int(os.popen(cmd).readlines()[3].split('%cpu')[0]) / 100
        except:
            logging.error("获取CPU核心数失败")
    try:
        # 获取进程ID
        cmd = 'adb ' + device_name + ' shell ps -o PID,NAME | findstr ' + package_name
        p = os.popen(cmd)
        PID = p.readline().split()[0]
    except:
        logging.error("获取进程ID失败")
    try:
        # 根据进程ID获取CPU使用率
        cmd = 'adb ' + device_name + ' shell top -n 1  -o %CPU,PID  | findstr ' + PID
        p = os.popen(cmd)
        return float(p.readline().split()[0]) / (device_cores * 100)
    except:
        logging.error("获取CPU使用率失败")
    return -1


if __name__ == "__main__":
    # 请指定待测程序包名
    package_name = 'com.tencent.liteav.demo'
    while True:
        print "当前应用的CPU用量：%f%%" % (get_app_cpu_usage(package_name, silence=False) * 100)
        time.sleep(2)  # 每隔2秒获取一次
