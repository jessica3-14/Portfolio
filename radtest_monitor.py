#!/usr/bin/env python

from rw_reg import *
from time import *
import array
import struct
import time

OH_NUM = 0
OH_MASK = 1
OUT_DIR = "./data/"
READ_WAIT_SEC = 1.0

RSSI_R1 = 2000.0
RSSI_R2 = 1000.0
RSSI_VCC = 2.5

# Temp(Resist) = Intercept + Slope*Resist
PT1000_Slope = 0.2597
PT1000_Intercept = -259.8956

# SCA Temp = Intercept + Slope*READ_mV
SCA_Temp_Slope = -0.5405
SCA_Temp_Intercept = 388.5135

#~~~~~~~~~~~~Tolerance Settings ~~~~~~~~~~~~~~~
# SEM Delta CNT
SEM1_DMAX = 5
SEM2_DMAX = 1
# VTRX RSSI
RSSI_WARN = 150 # uA
RSSI_MIN  = 100 # uA
# Temperature:
TEMP_WARN = 50
TEMP_MAX  = 60
# Voltage:
VOLT_WARN = 0.05  # 5% range for Warning
VOLT_MAX  = 0.10  # 10% range for Error
VOLT_NOM  = [1.0, 1.0, 1.2, 1.8, 1.5, 2.5]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~CMD Line Output Headers~~~~~~~~~~~~~~~~
SEM_HEAD = ["SEM_CNT", "SEM_D", "CRIT_CNT", "CRIT_D"]
RSSI_HEAD = ["RSSI1","RSSI2"]
VOLT_HEAD = ["1.0V","AVCC","AVTT","1.8V","1.5V", "2.5V"]
TEMP_HEAD = ["FPGA","SCA","U2","U3","U22","U8"]
CURR_HEAD = ["FEAST1", "FEAST2", "FEAST3"]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~Floating Point Precision~~~~~~~
FP = 6
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    #~~~~~~~~~~~~~~~Read Data Store~~~~~~~~~~~~~~~~
    SEM_Val = [0,0,0,0] #1-bit cnt , 1-bit delta , +2-bit cnt , +2-bit delta
    RSSI_Val = [0,0]    # VTRX1 , VTRX2
    VOLT_Val = [0,0,0,0,0,0] # 6 Voltages
    TEMP_Val = [0,0,0,0,0,0] # 6 Temperatures
    CURR_Val = [0,0,0] # FEAST1 , FEAST2 , FEAST3
    prev_sem_corr = 0   # Memory for SEM 1-bit Count
    sem_corr = 0
    prev_sem_crit = 0   # Memory for SEM Critical Count
    sem_crit = 0
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    out_file_name = OUT_DIR + "/" + time.strftime("%Y%m%d-%H%M%S") + ".csv"
    out_file = open(out_file_name, "w")
    out_file.write("FPGA_temperature\tSEM_critical_err_count\tSEM_single_bit_err_cnt\tADC_1.0V\tADC_1.0V_AVCC\tADC_1.2V_AVTT\tADC_1.8V\tADC_1.5V\tADC_2.5V\tADC_RSSI1\tADC_RSSI2\n")

    parseXML()

    iter = 0
    data = {}
    while(True):
        # read FPGA temperature
        tempRaw = parseInt(readReg(getNode('GEM_AMC.OH.OH%d.FPGA.ADC.CTRL.DATA_OUT' % OH_NUM)))
        temp = ((tempRaw >> 4) * 503.975 / 4096) - 273.15
        TEMP_Val[0] = temp
        #print("FPGA temperature: %fC" % temp)

        # read SEM counters
        prev_sem_corr = sem_corr
        prev_sem_crit = sem_crit
        sem_crit = parseInt(readReg(getNode('GEM_AMC.OH.OH%d.FPGA.CONTROL.SEM.CNT_SEM_CRITICAL' % OH_NUM)))
        sem_corr = parseInt(readReg(getNode('GEM_AMC.OH.OH%d.FPGA.CONTROL.SEM.CNT_SEM_CORRECTION' % OH_NUM)))
        SEM_Val[0] = sem_corr
        SEM_Val[1] = sem_corr - prev_sem_corr
        SEM_Val[2] = sem_crit
        SEM_Val[3] = sem_crit - prev_sem_corr
        #print("SEM single bit correction count: %d" % sem_corr)
        #print("SEM double bit (critical) error count: %d" % sem_crit)
        # read TMR counters
        #CONTROL
        tmr_ctrl_ttc = parseInt(readReg(getNode('GEM_AMC.OH.OH%d.FPGA.CONTROL.TMR.TTC_TMR_ERR_CNT' % OH_NUM)))
        tmr_ctrl_ipb_switch = parseInt(readReg(getNode('GEM_AMC.OH.OH%d.FPGA.CONTROL.TMR.IPB_SWITCH_TMR_ERR_CNT' % OH_NUM)))
        tmr_ctrl_ipb_slave = parseInt(readReg(getNode('GEM_AMC.OH.OH%d.FPGA.CONTROL.TMR.IPB_SLAVE_TMR_ERR_CNT' % OH_NUM)))
        # TRIG
        tmr_trig_cluster = parseInt(readReg(getNode('GEM_AMC.OH.OH%d.FPGA.TRIG.TMR.CLUSTER_TMR_ERR_CNT' % OH_NUM)))
        tmr_trig_sbit_rx = parseInt(readReg(getNode('GEM_AMC.OH.OH%d.FPGA.TRIG.TMR.SBIT_RX_TMR_ERR_CNT' % OH_NUM)))
        tmr_trig_formatter = parseInt(readReg(getNode('GEM_AMC.OH.OH%d.FPGA.TRIG.TMR.TRIG_FORMATTER_TMR_ERR_CNT' % OH_NUM)))
        tmr_trig_ipb_slave = parseInt(readReg(getNode('GEM_AMC.OH.OH%d.FPGA.TRIG.TMR.IPB_SLAVE_TMR_ERR_CNT' % OH_NUM)))
        # GBT
        tmr_gbt_link = parseInt(readReg(getNode('GEM_AMC.OH.OH%d.FPGA.GBT.TMR.GBT_LINK_TMR_ERR_CNT' % OH_NUM)))
        tmr_gbt_serdes = parseInt(readReg(getNode('GEM_AMC.OH.OH%d.FPGA.GBT.TMR.GBT_SERDES_TMR_ERR_CNT' % OH_NUM)))
        tmr_gbt_ipb_slave = parseInt(readReg(getNode('GEM_AMC.OH.OH%d.FPGA.GBT.TMR.IPB_SLAVE_TMR_ERR_CNT' % OH_NUM)))

        print("TMR CTRL TTC Count: %d" % tmr_ctrl_ttc)
        print("TMR CTRL IPB SW Count: %d" % tmr_ctrl_ipb_switch)
        print("TMR CTRL IPB Slave Count: %d" % tmr_ctrl_ipb_slave)

        print("TMR TRIG Cluster Count: %d" % tmr_trig_cluster)
        print("TMR TRIG Sbit Count: %d" % tmr_trig_sbit_rx)
        print("TMR TRIG Formatter Count: %d" % tmr_trig_formatter)
        print("TMR TRIG IPB Slave Count: %d" % tmr_trig_ipb_slave)

        print("TMR GBT Link Count: %d" % tmr_gbt_link)
        print("TMR GBT SERDES Count: %d" % tmr_gbt_serdes)
        print("TMR GBT IPB Slave Count: %d" % tmr_gbt_ipb_slave)

        # read the SCA ADCs
        writeReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.MANUAL_CONTROL.LINK_ENABLE_MASK'), OH_MASK)
        sleep(0.01)
        sendScaCommand([OH_NUM], 0x14, 0x60, 0x4, 0x00e00300, False) # setup current sources
        sleep(0.01)
        # Channels 0-5 [Voltages]
        adc_1v0 = readScaAdc(OH_NUM, 0) * 0.004
        adc_1v0avcc = readScaAdc(OH_NUM, 1) * 0.004
        adc_1v2avtt = readScaAdc(OH_NUM, 2) * 0.004
        adc_1v8 = readScaAdc(OH_NUM, 3) * 0.004
        adc_1v5 = readScaAdc(OH_NUM, 4) * 0.004
        adc_2v5 = readScaAdc(OH_NUM, 5) * 0.004
        VOLT_Val[0] = adc_1v0
        VOLT_Val[1] = adc_1v0avcc
        VOLT_Val[2] = adc_1v2avtt
        VOLT_Val[3] = adc_1v8
        VOLT_Val[4] = adc_1v5
        VOLT_Val[5] = adc_2v5

        # Channels 6-7 [RSSI Currents]
        adc_rssi1_v = readScaAdc(OH_NUM, 6) / 1000.0
        adc_rssi1_a = (((adc_rssi1_v / (RSSI_R2/(RSSI_R1+RSSI_R2))) - RSSI_VCC) / RSSI_R1) * -1
        adc_rssi1_ua = adc_rssi1_a * 1000000
        adc_rssi2_v = readScaAdc(OH_NUM, 7) / 1000.0
        adc_rssi2_a = (((adc_rssi2_v / (RSSI_R2/(RSSI_R1+RSSI_R2))) - RSSI_VCC) / RSSI_R1) * -1
        adc_rssi2_ua = adc_rssi2_a * 1000000
        RSSI_Val[0] = adc_rssi1_ua
        RSSI_Val[1] = adc_rssi2_ua

        # Channels 8-12 [FEAST Currents]
        adc_feast1_a = (readScaAdc(OH_NUM,8) * 4) / (200)   # 1.8V
        adc_feast2_a = (readScaAdc(OH_NUM,9) * 4) / (200)   # 1.5V
        adc_feast3_a = (readScaAdc(OH_NUM,10) * 4) / (200)  # 2.5V
        adc_feast4_a = (readScaAdc(OH_NUM,11) * 4) / (200)  # Analog  VFAT power (unused in radtest)
        adc_feast5_a = (readScaAdc(OH_NUM,12) * 4) / (200)  # Digital VFAT power (unused in radtest)
        CURR_Val[0] = adc_feast1_a
        CURR_Val[1] = adc_feast2_a
        CURR_Val[2] = adc_feast3_a

        # read SCA temperature
        # Channel 31 [SCA internal Temp]
        adc_sca_temp = SCA_Temp_Intercept + SCA_Temp_Slope*(readScaAdc(OH_NUM,31))
        # Channels 13-16 [Temperature Sensors]
        adc_u2_ohm = (readScaAdc(OH_NUM,13) / (readScaAdc(OH_NUM,17) / 1000))
        adc_u2_temp = PT1000_Intercept + PT1000_Slope*adc_u2_ohm;
        adc_u3_ohm = (readScaAdc(OH_NUM,14) / (readScaAdc(OH_NUM,17) / 1000))
        adc_u3_temp = PT1000_Intercept + PT1000_Slope*adc_u3_ohm;
        adc_u22_ohm = (readScaAdc(OH_NUM,15) / (readScaAdc(OH_NUM,17) / 1000))
        adc_u22_temp = PT1000_Intercept + PT1000_Slope*adc_u22_ohm;
        adc_u8_ohm = (readScaAdc(OH_NUM,16) / (readScaAdc(OH_NUM,17) / 1000))
        adc_u8_temp = PT1000_Intercept + PT1000_Slope*adc_u8_ohm;
        TEMP_Val[1] = adc_sca_temp
        TEMP_Val[2] = adc_u2_temp
        TEMP_Val[3] = adc_u3_temp
        TEMP_Val[4] = adc_u22_temp
        TEMP_Val[5] = adc_u8_temp

#        print("ADC 1.0V: %fV" % adc_1v0)
#        print("ADC 1.0V AVCC: %fV" % adc_1v0avcc)
#        print("ADC 1.2V AVTT: %fV" % adc_1v2avtt)
#        print("ADC 1.8V: %fV" % adc_1v8)
#        print("ADC 1.5V: %fV" % adc_1v5)
#        print("ADC 2.5V: %fV" % adc_2v5)
#        print("ADC RSSI1: %fuA" % adc_rssi1_ua)
#        print("ADC RSSI2: %fuA" % adc_rssi2_ua)
#        print("ADC FEAST1: %fA" % adc_feast1_a)
#        print("ADC FEAST2: %fA" % adc_feast2_a)
#        print("ADC FEAST3: %fA" % adc_feast3_a)
#        print("ADC FEAST4: %fA" % adc_feast4_a)
#        print("ADC FEAST5: %fA" % adc_feast5_a)
#        print("ADC board temp U2: %fC" % adc_u2_temp)
#        print("ADC board temp U3: %fC" % adc_u3_temp)
#        print("ADC board temp U22: %fC" % adc_u22_temp)
#        print("ADC board temp U8: %fC" % adc_u8_temp)
#        print("ADC SCA temp: %fC" % adc_sca_temp)
#	    print("ADC Current Mirror Calibration: %fuA" % readScaAdc(OH_NUM,17))



        # print and save the data
        data_csv = "%f\t%d\t%d\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f" % (temp, sem_crit, sem_corr, adc_1v0, adc_1v0avcc, adc_1v2avtt, adc_1v8, adc_1v5, adc_2v5, adc_rssi1_ua, adc_rssi2_ua, adc_feast1_a, adc_feast2_a, adc_feast3_a, adc_u2_temp, adc_u3_temp, adc_u22_temp, adc_u8_temp, adc_sca_temp)
        out_file.write("%s\n" % data_csv)
        out_file.flush()

        sleep(READ_WAIT_SEC)
        iter += 1

        CmdOut_SEM(SEM_Val)
    	CmdOut_RSSI(RSSI_Val)
    	CmdOut_TEMP(TEMP_Val)
    	CmdOut_VOLT(VOLT_Val)
    	CmdOut_Curr(CURR_Val)
        print("=============================")

def readScaAdc(oh, channel):
    sendScaCommand([oh], 0x14, 0x50, 0x4, channel << 24, False)
    res = sendScaCommand([oh], 0x14, 0x02, 0x4, 1 << 24, True)[0]
    res = (res >> 24) + ((res >> 8) & 0xff00)
    if (res > 0xfff):
        return -1.0
    res_mv = ((1.0 / 0xfff) * float(res)) * 1000
    sleep(0.01)
    return res_mv

def sendScaCommand(ohList, sca_channel, sca_command, data_length, data, doRead):
    #print('fake send: channel ' + hex(sca_channel) + ', command ' + hex(sca_command) + ', length ' + hex(data_length) + ', data ' + hex(data) + ', doRead ' + str(doRead))
    #return

    d = data

    writeReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.MANUAL_CONTROL.SCA_CMD.SCA_CMD_CHANNEL'), sca_channel)
    writeReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.MANUAL_CONTROL.SCA_CMD.SCA_CMD_COMMAND'), sca_command)
    writeReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.MANUAL_CONTROL.SCA_CMD.SCA_CMD_LENGTH'), data_length)
    writeReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.MANUAL_CONTROL.SCA_CMD.SCA_CMD_DATA'), d)
    writeReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.MANUAL_CONTROL.SCA_CMD.SCA_CMD_EXECUTE'), 0x1)
    reply = []
    if doRead:
        for i in ohList:
            reply.append(parseInt(readReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.MANUAL_CONTROL.SCA_REPLY_OH%d.SCA_RPY_DATA' % i))))
    return reply

def check_bit(byteval,idx):
    return ((byteval&(1<<idx))!=0);

def checkStatus(ohList):
    rxReady       = parseInt(readReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.STATUS.READY')))
    criticalError = parseInt(readReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.STATUS.CRITICAL_ERROR')))

    statusGood = True
    for i in ohList:
        if not check_bit(rxReady, i):
            printRed("OH #%d is not ready: RX ready = %d, critical error = %d" % (i, (rxReady >> i) & 0x1, (criticalError >> i) & 0x1))
            statusGood = False

    return statusGood

def hex(number):
    if number is None:
        return 'None'
    else:
        return "{0:#0x}".format(number)

def myprint(msg, isError = False):
    col = Colors.RED if isError else Colors.GREEN
    print(col + "===> " + msg + Colors.ENDC)

def CmdOut_Curr(rdata):
	ostr_head = "Currents:"
	ostr_data = "    [A] "
	for x in range(len(rdata)):
		ostr_head = ostr_head + "\t" + CURR_HEAD[x]
		ostr_data = ostr_data + "\t" + Colors.GREEN + str(rdata[x])[:FP] + Colors.ENDC
	print(ostr_head)
	print(ostr_data)

def SemTolCheck(rdata):
	if(rdata[1] >= SEM1_DMAX):
		rdata[0] = Colors.RED + str(rdata[0])[:FP] + Colors.ENDC
		rdata[1] = Colors.RED + str(rdata[1])[:FP] + Colors.ENDC
	else:
		rdata[0] = Colors.GREEN + str(rdata[0])[:FP] + Colors.ENDC
                rdata[1] = Colors.GREEN + str(rdata[1])[:FP] + Colors.ENDC
	if(rdata[3] >= SEM2_DMAX):
                rdata[2] = Colors.RED + str(rdata[2])[:FP] + Colors.ENDC
                rdata[3] = Colors.RED + str(rdata[3])[:FP] + Colors.ENDC
        else:
                rdata[2] = Colors.GREEN + str(rdata[2])[:FP] + Colors.ENDC
                rdata[3] = Colors.GREEN + str(rdata[3])[:FP] + Colors.ENDC
	return rdata

def CmdOut_SEM(rdata):
	sem = SemTolCheck(rdata)
	ostr_head = "SEM Monitors:"
        ostr_data = "    [.] "
        for x in range(len(sem)):
                ostr_head = ostr_head + "\t" + SEM_HEAD[x]
                ostr_data = ostr_data + "\t" + sem[x]
        print(ostr_head)
        print(ostr_data)

def RssiTolCheck(rdata):
	for i in range(len(rdata)):
                if((rdata[i] < RSSI_MIN)):
                        rdata[i] = Colors.RED + str(rdata[i])[:FP] + Colors.ENDC
                elif((rdata[i] < RSSI_WARN)):
                        rdata[i] = Colors.YELLOW + str(rdata[i])[:FP] + Colors.ENDC
                else:
                        rdata[i] = Colors.GREEN + str(rdata[i])[:FP] + Colors.ENDC
        return rdata

def CmdOut_RSSI(rdata):
        rssi = RssiTolCheck(rdata)
        ostr_head = "VTRX Strength:"
        ostr_data = "    [uA] "
        for x in range(len(rssi)):
                ostr_head = ostr_head + "\t" + RSSI_HEAD[x]
                ostr_data = ostr_data + "\t" + rssi[x]
        print(ostr_head)
        print(ostr_data)

def SymmTolCheck(rdata, nom, tol_warn, tol_max):
	for i in range(len(rdata)):
		if((rdata[i] > nom[i]*(1+tol_max)) or (rdata[i] < nom[i]*(1-tol_max))):
			rdata[i] = Colors.RED + str(rdata[i])[:FP] + Colors.ENDC
		elif((rdata[i] > nom[i]*(1+tol_warn)) or (rdata[i] < nom[i]*(1-tol_warn))):
			rdata[i] = Colors.YELLOW + str(rdata[i])[:FP] + Colors.ENDC
		else:
			rdata[i] = Colors.GREEN + str(rdata[i])[:FP] + Colors.ENDC
	return rdata

def CmdOut_VOLT(rdata):
	volts = SymmTolCheck(rdata,VOLT_NOM,VOLT_WARN,VOLT_MAX)
	ostr_head = "Voltages:"
	ostr_data = "    [V] "
	for x in range(len(volts)):
		ostr_head = ostr_head + "\t" + VOLT_HEAD[x]
		ostr_data = ostr_data + "\t" + volts[x]
	print(ostr_head)
	print(ostr_data)

def TempTolCheck(temps):
	for i in range(len(temps)):
		if(temps[i] > TEMP_MAX):
			temps[i] = Colors.RED + str(temps[i])[:FP] + Colors.ENDC
		elif(temps[i] > TEMP_WARN):
			temps[i] = Colors.YELLOW + str(temps[i])[:FP] + Colors.ENDC
		else:
			temps[i] = Colors.GREEN + str(temps[i])[:FP] + Colors.ENDC
	return temps

def CmdOut_TEMP(rdata):
	temps = TempTolCheck(rdata)
	ostr_head = "Temperature:"
	ostr_data = "    [C] "
	for x in range(len(temps)):
                ostr_head = ostr_head + "\t" + TEMP_HEAD[x]
                ostr_data = ostr_data + "\t" + temps[x]
        print(ostr_head)
        print(ostr_data)

class Colors:
    WHITE   = '\033[97m'
    CYAN    = '\033[96m'
    MAGENTA = '\033[95m'
    BLUE    = '\033[94m'
    YELLOW  = '\033[93m'
    GREEN   = '\033[92m'
    RED     = '\033[91m'
    ENDC    = '\033[0m'

if __name__ == '__main__':
    main()
