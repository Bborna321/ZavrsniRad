
import statistics

def std_dev_ema20(ema20):



    normalEma20_list = []
    for i,a_thing in enumerate(ema20['Price']):
            normalEma20_list.append(a_thing)



    computing_std_dev_value = statistics.stdev(normalEma20_list[0:20])
    print(normalEma20_list[0:20])
    print(computing_std_dev_value)

    std_dev_list = []
    computing_std_dev_list = []
    """for k in range(20):
        std_dev_list.append(computing_std_dev_value)
        computing_std_dev_list.append(computing_std_dev_value)"""

    for i,val in enumerate(normalEma20_list):
        if i < 20:
            std_dev_list.append(computing_std_dev_value)
            computing_std_dev_list.append(computing_std_dev_value)
        else:
            std_dev_list.pop(0)
            std_dev_list.append(val)
            computing_std_dev_value = statistics.stdev(std_dev_list)
            computing_std_dev_list.append(computing_std_dev_value)


    return std_dev_list

