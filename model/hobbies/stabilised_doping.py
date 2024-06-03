import pandas,os,numpy,random
from random import randint

def stabilised_doping(from_csv,to_csv,threshold_p,dope_from,dope_to,column_names,feedback=False):
    dataset = pandas.read_csv(f"model/{from_csv}")
    dataset_array = numpy.array(dataset)
    threshold = threshold_p
    for _ in dataset_array:
        if random.random() <= threshold:
            doping_row = random.randint(0,len(dataset_array)-1)
            doping_column = random.randint(0,len(dataset_array[0])-1)
            dataset_array[doping_row][doping_column] = random.randint(dope_from,dope_to)
            if feedback:
                print(f"Doped record #{doping_row} at {doping_column}")
    dataframe = pandas.DataFrame(dataset_array,columns=column_names)
    dataframe.to_csv(f"model/{to_csv}",index=False,header=True)
