Klipper Sensorless Homing Helper
===
[中文版](readme_zh_cn.md)

# What is it?
This Klipper plugin implements the [sensorless homing routine](https://docs.vorondesign.com/community/howto/clee/sensorless_xy_homing.html) with additional 
retraction along XY axis when 
* X or Y is not homed or
* The last known location of the toolhead is too closed to the gantry. 

The sensorless homing requires certain speed while hitting the gantry to get repeatable XY coordinate. The additional XY retraction allows the carriage to accelerate 
to the calibrated speed during the calibration. 

# Install via Moonraker
Clone the repository to the home directory

    cd ~
    git clone https://github.com/eamars/sensorless_homing_helper.git

You need to manually install the plugin for the first time. It will prompt for password to restart the Klipper process. 
    
    source sensorless_homing_helper/install.sh

Then copy the below block into the moonraker.conf to allow automatic update.

    [update_manager client sensorless_homing_helper]
    type: git_repo
    primary_branch: main
    path: ~/sensorless_homing_helper
    origin: https://github.com/eamars/sensorless_homing_helper.git
    install_script: install.sh

# Configurations
The `[sensorless_homing_helper]` section along with required parameters need to be declared under `printer.cfg`. 

    [sensorless_homing_helper]
    tmc_stepper_y_name: tmc5160 stepper_y       # The TMC stepper section name for Y
    tmc_stepper_x_name: tmc5160 stepper_x       # The TMC stepper section name for X
    home_current: 0.5                           # The current while running the sensorless homing

    minimum_homing_distance: 10                 # (Optional) The minimum distance to achieve the repeatible sensorless homing
    retract_distance: 10                        # (Optional) The retract distance after the axis is homed
    retract_speed: 20                           # (Optional) The speed while running the retraction (both before and after homing)
    stallguard_reset_time: 1                    # (Optional) The time for stallguard to reset before the next homing move

# GCode Macros
An example `sensorless.cfg` macro is provided to allow 3rd party plugin (eg. Klicky) to call the sensorless homing routine. This 
file need to be included in your `printer.cfg` too. 