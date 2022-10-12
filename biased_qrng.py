
from collections import defaultdict
import time
from dwave.system.samplers import DWaveSampler
import numpy as np
from matplotlib import pyplot as plt
import neal
import pandas as pd
from pyqubo import Array, Placeholder, solve_qubo, Constraint
from dwave.system.composites import EmbeddingComposite, FixedEmbeddingComposite
from dimod import AdjVectorBQM
import argparse

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
    samples = args_config['samples']

    if isQPU:
        if Advantage:
            qpu = DWaveSampler(solver={'qpu': True, 'topology__type': 'pegasus'})
        else:
            qpu = DWaveSampler(solver={'qpu': True, 'topology__type': 'chimera'})
        sampler = EmbeddingComposite(qpu)     
    else :
        sampler = neal.SimulatedAnnealingSampler()

    l = {}

    x = Array.create("vector", N, "BINARY")
    for bias in [0.1,0.15,0.2]:        
        H = x[0] - x[0]
        for i in range(N):
            H += bias*(x[i])

        model = H.compile()
        qubo,offset = model.to_qubo()
        
        for itr in range(samples):
            response = sampler.sample_qubo(qubo, num_reads = 1,annealing_time = 1,auto_scale = False) 
            l = np.append(l,(np.array(response.to_pandas_dataframe().drop(columns = ['energy','num_occurrences']))).flatten())

        if Advantage == 1:
            pd.DataFrame(l).to_csv("pegasus_qubits={}_bias={}.csv".format(N,bias))

        else:
            pd.DataFrame(l).to_csv("chimera_qubits={}_bias={}.csv".format(N,bias))

            
if __name__ == '__main__':
    args_config = parseArguments()
    main(args_config)