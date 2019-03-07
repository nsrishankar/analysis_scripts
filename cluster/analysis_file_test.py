from __future__ import print_function
import csv
import sys
import os
import re
import copy
import numpy as np
import datetime
import pickle
import collections
import glob
import time
import pandas as pd

tic=time.time()
raw_data_dir='*/*.txt'
save_data_dir=''

def eprint(*args,**kwargs):
    print(*args,file=sys.stderr,**kwargs)

eprint("In python file")

def remove_chars(string):
    chars="[^0123456789\.]"
    return re.sub(chars,"",string)

def search_and_return(input_array):
    out_array=np.empty([0,13])
    agree_count=0
    agree_count_soft=0
    for ind in range(len(input_array)):
        if((input_array[ind][6]==input_array[ind][7])):
            agree_count_soft+=1
        if((input_array[ind][6]==input_array[ind][7]) and (input_array[ind][6]>=0.5)):
            out_array=np.vstack((out_array,input_array[ind].reshape(1,13)))
            agree_count+=1
    return agree_count_soft,agree_count,out_array

path=glob.glob(raw_data_dir)
eprint("PATH: ",path)
for dir_name in path:
    data_dictionary=collections.defaultdict(dict)
    timeratio_data_dictionary=collections.defaultdict(dict)
    eprint("Working on: ",dir_name)
    split=dir_name.split("_")[1:]
    # eprint(split)
    noise=remove_chars(split[5])
    density=remove_chars(split[8])
    num_robots=remove_chars(split[6])
    num_liars=remove_chars(split[7])
    seed=split[9].split(".")[0]

    pickle_name="nrobots{}_nliars{}_noise{}_density{}_{}".format(num_robots,num_liars,noise,density,seed)
    timeratio_pickle_name="TIMERATIO_nrobots{}_nliars{}_noise{}_density{}_{}".format(num_robots,num_liars,noise,density,seed)
    working_robots=int(num_robots)-int(num_liars)
    
    data_seed={}
    key_1=dir_name
    # key_1=remove_chars(file_path.split("_")[-1].split(".")[0]) # Seed value. Seeds ran for- value of first dict, key of second
    analyzed_data=np.array([]) # Empty placeholder for analyzed data.
    highest_out_array=np.array([])

    chunk_size=working_robots
    skip=0
    if skip==0:
        for current_tstep,time_chunk in enumerate(pd.read_csv(dir_name,chunksize=chunk_size,delimiter='\t')):
            values=np.asarray(copy.deepcopy(time_chunk))
            # print(values)
            eprint("Working on data from the {} timestep".format(current_tstep+1))
            agree_count_soft,agree_count,out_array=search_and_return(values)
            timeratio_data_dictionary[current_tstep]=[current_tstep,agree_count_soft,agree_count]
            print("TIMERATIO",timeratio_data_dictionary[current_tstep])

            
            if (len(out_array)>len(highest_out_array)):
                highest_agreeing_count=agree_count
                highest_out_array=np.copy(out_array)
                data_dictionary[key_1]=highest_out_array
                if (len(out_array)==int(working_robots)):
                    skip=1
        eprint("Skipping at t= ",current_tstep+1)

    fpkl=open("{}.pkl".format(pickle_name),"wb")
    pickle.dump(data_dictionary,fpkl)
    fpkl.close()
    fpkl=open("{}.pkl".format(timeratio_pickle_name),"wb")
    pickle.dump(timeratio_data_dictionary,fpkl)
    fpkl.close()
    
    eprint("Pickled:",pickle_name)
    eprint("Pickled:",timeratio_pickle_name)
    toc=time.time()
    eprint("Time:", toc-tic)