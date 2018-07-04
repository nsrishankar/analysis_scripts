#Convergence:
#    Creates text files containing filenames if more than 1000 timesteps are exceeded (Plot % of working robots that converged)
#    Creates text files containing filenames if less than 1000 timesteps are exceeded (Plot number of timesteps per experiment)

import csv
import sys
import os
import re
import numpy as np
import datetime
import glob

# def converged_check(raw_data_dir,save_data_dir):

raw_data_dir='*.dat'
save_data_dir=''
not_converged='notconverged_details.txt'
converged='converged_details.txt'

path=glob.glob(raw_data_dir,recursive=False)
for p in path: # Path has data files
    print(p)
    # Getting information based on filenames
    fname=p.split('/')[0]
    
    print("Working on {}:".format(fname))
    experiment_details_name=fname.split('_')
	
    arena_length=int(experiment_details_name[1])
    arena_size=arena_length**2
    n_robots=int(float(experiment_details_name[3])*arena_size)
    n_defecting=int(float(experiment_details_name[5])*n_robots)
    communication_radius=int(experiment_details_name[7])
    sensor_noise=float(experiment_details_name[11])
   
    with open(p,'r') as f:
        #
        for i in range(2):
            next(f)
        worlds_truth=(int(next(f).split()[-1]))
        temp=[line.splitlines()[0] for line in f.readlines() if line.strip()]   
        
        # Reading last line to get timestep
        last_line=str(temp[-1]).split(",")
        tstep=int(last_line[0])

        if tstep>1000: # NON-CONVERGED EXPERIMENTS
            # Getting data
            data=temp[-n_robots:]

            count_accurate=0
            
            for l in data:
                l=[float(num) for num in l.split(",")]
                max_index=int(np.argmax(l[-10:]))
                max_proba=l[4+max_index]
                concat_tstep=[int(x) for x in l[0:2]]
                concat_data=np.hstack((concat_tstep,max_index,max_proba))
                if ((max_index==worlds_truth) & (max_proba>=0.5)):
                    count_accurate+=1
            print("\t\tAccurate Robots: {} out of {} working robots, {} total robots".format(
            count_accurate,n_robots-n_defecting,n_robots))
            
            
            
            with open(not_converged,'a+') as nc_file:
                nc_file.write("{}, {}, {}, {}, {}\n".format(p,tstep,count_accurate,n_robots-n_defecting,n_robots))
                nc_file.close()
        else: # CONVERGED EXPERIMENTS
            with open(converged,'a+') as c_file:
                c_file.write("{}, {}, {}, {}\n".format(p,tstep,n_robots-n_defecting,n_robots))
                c_file.close()
                    
# if __name__!="__main__":
# 	print("HERE")
# 	raw_data_dir='data/*'
# 	save_data_dir=''
# 	converged_check(raw_data_dir,save_data_dir)