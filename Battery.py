from upspackv2 import *

def reflash_data():
    test = UPS2("/dev/ttyS0")
    cap_var= "empty"
    vin_var =  "empty"
    version,vin,batcap,vout = test.decode_uart()
#    loc_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # cur_time = time.time()
    # cur_time = cur_time - load_time
#    print(cur_time)
    # time_var.set("Running: "+str(int(cur_time)) + "s")    
    batcap_int = int(batcap)
#    print(type(batcap_int))
    if vin == "NG":
        vin_var = "Power NOT connected!"
    else:
        vin_var = "Power connected!"
    # if batcap_int< 30:
        # if batcap_int == 1:
            # cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            # stop_time = "\nHalt time :"+cur_time
            # with open("log.txt","a+") as f:
                # f.write(stop_time)
            # os.system("sudo shutdown -t now")
            # sys.exit()            
    cap_var = "Battery Capacity: "+str(batcap)+"%"
    vout_var = "Output Voltage: "+vout+" mV"
    return batcap
 