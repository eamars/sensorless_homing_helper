Klipper 无限位插件增强
===
[English](readme.md)

# 关于插件
此插件复刻了[现有无限位归零宏](https://docs.vorondesign.com/community/howto/clee/sensorless_xy_homing.html)的所有功能，并且在归零X与Y轴之前会向相反方向运动一定距离以保证XY归零的可重复性。
插件在以下情况将向与归零相反方向运动：
* X或Y轴从未归零。
* 滑车离X或Y距离小于一定阈值。

# 安装（集成 Moonraker）
将代码同步到当前用户根目录。

    cd ~
    git clone https://github.com/eamars/sensorless_homing_helper.git

第一次安装时需要执行安装脚本。

    source sensorless_homing_helper/install.sh

同时将以下内容复制到 moonraker.conf 以开启自动更新检查。

    [update_manager client ercf_driver]
    type: git_repo
    primary_branch: main
    path: /home/pi/ercf_driver
    origin: https://github.com/eamars/ercf_driver.git
    install_script: install.sh

# 示例配置
用户需要将以下内容根据实际配置复制到`printer.cfg`当中。

    [sensorless_homing_helper]
    tmc_stepper_y_name: tmc5160 stepper_y       # Y电机TMC驱动定义
    tmc_stepper_x_name: tmc5160 stepper_x       # X电机TMC驱动定义
    home_current: 0.5                           # 归零时的运行电流

    minimum_homing_distance: 10                 #（可选）最低无限位归零运动距离
    retract_distance: 10                        #（可选）归零后回抽距离
    retract_speed: 20                           #（可选）归零前后回抽速度
    stallguard_reset_time: 1                    #（可选）TMC Stall Guard 自动重置时间

# GCode 宏
`sensorless.cfg`提供了与 Klicky 或者第三方插件交互的宏。用户需要在`printer.cfg`中包含此文件。