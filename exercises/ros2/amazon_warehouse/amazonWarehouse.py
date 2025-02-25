#!/usr/bin/python3
#  Copyright (C) 1997-2020 JDE Developers Team
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see http://www.gnu.org/licenses/.
#  Authors :
#       Arsalan Akhter <arsalanakhter.wpi AT gmail DOT com>
#       Shyngyskhan Abilkassov <s.abilkassov AT gmail DOT com>
#       Shreyas Gokhale <shreyas6gokhale AT gmail DOT com>

import sys, config
from connector import connector

from gui.GUI import MainWindow
from gui.threadGUI import ThreadGUI
from MyAlgorithm import MyAlgorithm
from PyQt5.QtWidgets import QApplication

from sensors.threadMotors import ThreadMotors
from sensors.threadMotors import Velocity
from sensors.sensor import Sensor
from sensors.grid import Grid

from interfaces.navigation2ActionClient import NavigateToPoseActionClient

import yaml
import signal

def removeMapFromArgs():
    for arg in sys.argv:
        if (arg.split(".")[1] == "conf"):
            sys.argv.remove(arg)

signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('ERROR: python3 globalNavigation.py [MAP CONFIG file] [YAML CONFIG file]')
        sys.exit(-1)

    # cfg = config.load()

    with open(sys.argv[2]) as f:
        # using safe_load instead load
        cfg = yaml.safe_load(f)
        jdrc = connector.Connector(cfg, 'Amazon')
        motors = jdrc.getMotorPubObject()
        pose3d = jdrc.getPoseListnerObject()
        laser = jdrc.getLaserListnerObject()
        # pathListener = ListenerPath("/amazon_warehouse_robot/move_base/NavfnROS/plan")

        # This is to be updated
        navigation_client = NavigateToPoseActionClient()
        print("Subscribed To Move Base Client, Starting Application")

        app = QApplication(sys.argv)
        myGUI = MainWindow()

        grid = Grid(myGUI)

        vel = Velocity(0.0, 0.0, motors.getMaxV(), motors.getMaxW())
        sensor = Sensor(grid, pose3d, True)
        sensor.setGetPathSignal(myGUI.getPathSig)
        

        myGUI.setVelocity(vel)
        myGUI.setGrid(grid)
        myGUI.setSensor(sensor)
        algorithm = MyAlgorithm(grid, sensor, vel, navigation_client)
        myGUI.setAlgorithm(algorithm)
        myGUI.show()

        removeMapFromArgs()

        t1 = ThreadMotors(motors, vel)
        t1.daemon = True
        t1.start()
        t2 = ThreadGUI(myGUI)
        t2.daemon = True
        t2.start()

        sys.exit(app.exec_())
