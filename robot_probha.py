#!/usr/bin/env python

"""
robot_probha - class for robot simulator with hybrid automaton architecture and probabilistic localization
"""

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import robot_ha
import robot_prob
import robot
import math
import mapdef
import ogmap
import mcl
import numpy as np
import random


class RobotProbHA(robot_prob.RobotProb, robot_ha.RobotHA):
    def __init__(self, parameters, sonar):
        robot_prob.RobotProb.__init__(self, parameters, sonar)
        robot_ha.RobotHA.__init__(self, parameters, sonar)

    def situate(self
                , this_map
                , this_pose
                , this_goal
                , this_ens):
        robot_prob.RobotProb.situate(self, this_map, this_pose, this_goal, this_ens)
        robot_ha.RobotHA.situate(self, this_map, this_pose, this_goal)

    def control_policy(self):
        return robot_ha.RobotHA.control_policy(self)

    def show_state(self):
        pass


def main():
    """


    :return:
    """
    parameters = robot_prob.ParametersProb()
    this_goal = robot_prob.Goal(location=(random.randrange(20, 80), random.randrange(10, 60), math.pi)
                     , radius=3)
    true_pose = (random.randrange(10, 50), 90, 0.1)
    this_map = mapdef.mapdef()
    sonar_params = {'RMAX': 100
        , 'EXP_LEN': 0.1
        , 'r_rez': 2
    }
    this_sonar = ogmap.Sonar(NUM_THETA=16
                             , GAUSS_VAR=0.1
                             , params=sonar_params
    )
    this_ens = mcl.Ensemble(pose=true_pose
                            , N=50
                            , acc_var=np.array((0.0001, 0.0001, 0.0001))
                            , meas_var=np.array((0.01, 0.01, 0.01)))
    this_robot = RobotProbHA(parameters, this_sonar)
    this_robot.situate(this_map, true_pose, this_goal, this_ens)

    # plt.ion()
    #fig = plt.figure()
    #fig.set_size_inches(20,20)
    #plt.get_current_fig_manager().resize(1000, 1000)

    #    print "Robot Running"
    this_robot.automate(numsteps=100)
    #plt.close()
    if robot.check_success(this_goal, this_robot):
        print "SUCCESS"
        return True
    else:
        print "FAILURE"
        return False


if __name__ == "__main__":
    main()
