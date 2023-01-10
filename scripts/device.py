"""
main device
"""
from rollsmart.scripts.dbconfig import *
import Littelfuse_59025_020
import Sunfounder_ST0064
import Bosch_BNO055
import NEXTION_WI1802AX4_WI0728
import Daoki_BF350_3AA


def main():
    print("roll smart")
    """
    littelfuse_59025_020 = Littelfuse_59025_020()
    sunfounder_st0064 = Sunfounder_ST0064()
    bosch_bno055 = Bosch_BNO055()
    nextion_wi1802ax4_wi0728 = NEXTION_WI1802AX4_WI0728()
    daoki_bf350_3aa = Daoki_BF350_3AA()
    """
    # set up database
    # set up sensors
    # poll sensors, read data
    # decode data
    # write data to database

if __name__ == '__main__':
    main()