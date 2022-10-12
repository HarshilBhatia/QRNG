
from collections import defaultdict

from dwave.system.samplers import DWaveSampler
import numpy as np
from matplotlib import pyplot as plt
import neal
import pandas as pd
from dwave.system.composites import EmbeddingComposite
import time
from pyqubo import Array, Placeholder, solve_qubo, Constraint
import argparse
#import dwave.minorminer.find_embedding



def parseArguments():
    parser = argparse.ArgumentParser(description="Change Config File")

    #QPU Arguments
    parser.add_argument("--qpu",default=False,action = 'store_true',help = 'Use QPU')
    parser.add_argument("--N",type = int,default = 4950, help = 'number of bits')
    parser.add_argument("--arch",default = 'ADV',choices= ['ADV','2000Q'])
    parser.add_argument("--samples",type = int,default = 200,help = 'number of samples')

    args = parser.parse_args()
    args_config = vars(args)

    if args_config['qpu']:
        if((args_config['N'] > 2100 and args_config['arch'] == '2000Q') or ( args_config['arch'] =='ADV' and args_config['N'] > 5000)):
            print("The number of bits exceed the qubits in the architecture")

    return args_config


def main(args_config):
    print(args_config)
    N = args_config['N'] # number of qubots
    isQPU = args_config['qpu'] # 
    Advantage = (args_config['arch'] == 'ADV')

    if isQPU:
        if Advantage:
            qpu = DWaveSampler(solver={'qpu': True, 'topology__type': 'pegasus'})
        else:
            qpu = DWaveSampler(solver={'qpu': True, 'topology__type': 'chimera'})
        sampler = EmbeddingComposite(qpu)       
    else :
        sampler = neal.SimulatedAnnealingSampler()

    samples = args_config['samples']
    print("Number of Samples = ",samples*N)

    l = np.array([])

    x = Array.create("vector", N, "BINARY")
    H = x[0] - x[0]

    for i in range(N):
        H += (x[i]-x[i])

    model = H.compile()
    qubo,offset = model.to_qubo()
    total = 0 

    for itr in range(samples):
        response = sampler.sample_qubo(qubo, num_reads = 1,annealing_time = 1,auto_scale = False) 
        l = np.append(l,(np.array(response.to_pandas_dataframe().drop(columns = ['energy','num_occurrences']))).flatten())
    
        if(itr% 50 == 0):
            print(itr)

    if isQPU:
        if Advantage:
            pd.DataFrame(l).to_csv("pegasus_qubits={}_samples={}.csv".format(N,samples))
        else: 
            pd.DataFrame(l).to_csv("chimera_qubits={}_samples={}.csv".format(N,samples))

    else:
        pd.DataFrame(l).to_csv("SA_qubits={}_samples={}.csv".format(N,samples))

if __name__ == '__main__':
    args_config = parseArguments()
    main(args_config)