import time,sys
import RPi.GPIO as GPIO
import smbus
import math

rev = GPIO.RPI_REVISION
if rev == 2 or rev == 3:
    bus = smbus.SMBus(1)
else:
    bus = smbus.SMBus(0)

class icm20600:
    
    ICM20600_ADDR = 0x69

    #register too mach for me
    XG_OFFS_TC_H = 0x04
    XG_OFFS_TC_L = 0x05
    YG_OFFS_TC_H = 0x07
    YG_OFFS_TC_L = 0x08
    ZG_OFFS_TC_H = 0x0A
    ZG_OFFS_TC_L = 0x0B

    SELF_TEST_X_ACCEL = 0x0D
    SELF_TEST_Y_ACCEL = 0x0E
    SELF_TEST_Z_ACCEL = 0x0F

    XG_OFFS_USRH = 0x13
    XG_OFFS_USRL = 0x14
    YG_OFFS_USRH = 0x15
    YG_OFFS_USRL = 0x16
    ZG_OFFS_USRH = 0x17
    ZG_OFFS_USRL = 0x18

    SMPLRT_DIV = 0x19

    CONFIG = 0x1A
    GYRO_CONFIG = 0x1B
    ACCEL_CONFIG = 0x1C
    ACCEL_CONFIG2 = 0x1D
    LP_MODE_CFG = 0x1E

    ACCEL_WOM_X_THR = 0x20
    ACCEL_WOM_Y_THR = 0x21
    ACCEL_WOM_Z_THR = 0x22

    FIFO_EN = 0x23
    
    FSYNC_INT = 0x36
    INT_PIN_CFG = 0x37
    INT_ENABLE = 0x38
    FIFO_WM_INT_STATUS = 0x39
    INT_STATUS = 0x3A

    ACCEL_XOUT_H = 0x3B
    ACCEL_XOUT_L = 0x3C
    ACCEL_YOUT_H = 0x3D
    ACCEL_YOUT_L = 0x3E
    ACCEL_ZOUT_H = 0x3F
    ACCEL_ZOUT_L = 0x40

    TEMP_OUT_H = 0x41
    TEMP_OUT_L = 0x42

    GYRO_XOUT_H = 0x43
    GYRO_XOUT_L = 0x44
    GYRO_YOUT_H = 0x45
    GYRO_YOUT_L = 0x46
    GYRO_ZOUT_H = 0x47
    GYRO_ZOUT_L = 0x48

    SELF_TEST_X_GYRO = 0x50
    SELF_TEST_Y_GYRO = 0x51
    SELF_TEST_Z_GYRO = 0x52

    FIFO_WM_TH1 = 0x60
    FIFO_WM_TH2 = 0x61

    SIGNAL_PATH_RESET = 0x68
    ACCEL_INTEL_CTRL = 0x69
    USER_CTRL = 0x6A

    PWR_MGMT_1 = 0x6B
    PWR_MGMT_2 = 0x6C

    I2C_IF = 0x70

    FIFO_COUNTH = 0x72
    FIFO_COUNTL = 0x73
    FIFO_R_W = 0x74
    
    WHO_AM_I = 0x75

    XA_OFFSET_H = 0x77
    XA_OFFSET_L = 0x78
    YA_OFFSET_H = 0x7A
    YA_OFFSET_L = 0x7B
    ZA_OFFSET_H = 0x7D
    ZA_OFFSET_L = 0x7E

    def status(self):
        if self.reg_read(self.WHO_AM_I) != 0x11:
#            print self.reg_read(self.WHO_AM_I)
            return -1
        return 1

    def initialize(self):
        print("initialize")
        self.reg_write(self.CONFIG,0x00)
        self.reg_write(self.FIFO_EN,0x00)

        #need def power mode setting
        pwr1 = 0x00
        pwr1 = self.reg_read(self.PWR_MGMT_1)&0x8f
        gyr = self.reg_read(self.LP_MODE_CFG)&0x7f
        self.reg_write(self.PWR_MGMT_1,pwr1)
        self.reg_write(self.PWR_MGMT_2,0x07)
        self.reg_write(self.LP_MODE_CFG,gyr|0x80)
        #need gyro scale,output rate,average setting
        gyr_c = self.reg_read(self.GYRO_CONFIG)&0xe7
        self.reg_write(self.GYRO_CONFIG,gyr_c|0x18)
        self.reg_write(self.CONFIG,0x01|0xf8)
        self.reg_write(self.LP_MODE_CFG,0x00|0x8f)
        #need accel config setting
        ac_c = self.reg_read(self.ACCEL_CONFIG)&0xe7
        self.reg_write(self.ACCEL_CONFIG,0x18|ac_c)
        ac_c2 = self.reg_read(self.ACCEL_CONFIG2)&0xf0
        self.reg_write(self.ACCEL_CONFIG2,0x07|ac_c2)
        ac_c2 = self.reg_read(self.ACCEL_CONFIG2)
        self.reg_write(self.ACCEL_CONFIG2,ac_c2)

        while 1:
            time.sleep(1)
        
            print self.getAccel()

    def reg_write(self,addr,data):
        bus.write_byte_data(self.ICM20600_ADDR,addr,data)

    def reg_read(self,addr):
        print(addr)
        print(bus.read_byte_data(self.ICM20600_ADDR,addr))
        return bus.read_byte_data(self.ICM20600_ADDR,addr)

    def getAccel(self):
        raw_accel=[0,0,0]
        raw_accel[0] = self.reg_read(self.ACCEL_XOUT_L)
        raw_accel[1] = self.reg_read(self.ACCEL_YOUT_H)
        raw_accel[2] = self.reg_read(self.ACCEL_ZOUT_H)
        return raw_accel

class ak09918:
    AK09918_ADDR = 0x0C


if __name__ == "__main__":
    icm20600().status()
    icm20600().initialize()
    
