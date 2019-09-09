# encoding:utf-8
import logging
import os


def get_app_cpu_usage(package_name, device_name="", device_cores=-1):
    # type: (str, str,int) -> float
    """
    :param package_name: 待检测安卓应用包名【必填】
    :param device_name: 待检测设备名（使用“adb devices”命令获取）【若为空则检测默认设备，当设备数大于一时将报错】
    :param device_cores: 设备核心数，从adb获取到的使用率可能会超过100%，指定这个数字来修正获得的结果（旧版安卓系统指定为1即可）
    :return: 该设备指定应用的CPU占用率（占用15%则return 0.15）
    """
    if device_name.__len__() > 0:
        device_name = "-s " + device_name
    else:
        print "未指定设备名，尝试连接默认设备"
    if device_cores is -1:
        print "未指定CPU核心数，尝试自动获取（结果不一定可靠）"
        try:
            cmd = 'adb ' + device_name + ' shell top -n 1'
            # print cmd
            device_cores = int(os.popen(cmd).readlines()[3].split('%cpu')[0]) / 100
        except:
            device_cores = 1
            logging.error("获取CPU核心数失败，请手动指定CPU核心数！")
    try:
        # 获取进程ID
        cmd = 'adb ' + device_name + ' shell ps -o PID,NAME | findstr ' + package_name
        # print cmd
        p = os.popen(cmd)
        PID = p.readline().split()[0]
    except:
        try:
            # 获取进程ID（旧版命令）
            cmd = 'adb ' + device_name + ' shell ps | findstr ' + package_name
            # print cmd
            p = os.popen(cmd)
            PID = p.readline().split()[1]
        except:
            logging.error("获取进程ID失败，请确认包名是否正确、程序是否打开")
    try:
        # 根据进程ID获取CPU使用率
        cmd = 'adb ' + device_name + ' shell top -n 1  -o %CPU,PID  | findstr ' + PID
        # print cmd
        p = os.popen(cmd)
        return float(p.readline().split()[0]) / (device_cores * 100)
    except:
        try:
            # 根据进程ID获取CPU使用率（旧版命令）
            cmd = 'adb ' + device_name + ' shell top -n 1 | findstr ' + PID
            # print cmd
            p = os.popen(cmd)
            output = p.readline().split()
            for i in range(0, output.__len__()):
                if output[i].__contains__('%'):
                    return float(output[i].split('%')[0]) / (device_cores * 100)
            #     若数据中不带%，尝试直接读取第八列
            return float(output[8]) / (device_cores * 100)
        except:
            logging.error("获取CPU使用率失败")
    return -1


def get_app_pss_in_KB(package_name, device_name=""):
    if device_name.__len__() > 0:
        device_name = "-s " + device_name
    else:
        print "未指定设备名，尝试连接默认设备"
    try:
        cmd = 'adb ' + device_name + ' shell dumpsys meminfo -package | findstr ' + package_name
        # print cmd
        output = os.popen(cmd).readlines()
        return int(output[0].replace(' ', '').replace('k', 'K').split('K')[0].replace(',', ''))
    except:
        logging.error("获取PSS失败，请尝试更改输出信息提取规则，控制台输出为：" + output)


if __name__ == "__main__":
    while True:
        print "current app's cpu usage: %f%%" % (
                get_app_cpu_usage("com.tencent.liteav.demo", device_name='80QBCNQ22W8F', device_cores=1) * 100)
        print "current app's pss: %d KB" % (
            get_app_pss_in_KB(package_name='com.tencent.liteav.demo', device_name='80QBCNQ22W8F'))

        # time.sleep(2)  # 每隔2秒获取一次
