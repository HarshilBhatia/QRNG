
from collections import defaultdict

from dwave.system.samplers import DWaveSampler
import numpy as np
from matplotlib import pyplot as plt
import neal
import pandas as pd
from pyqubo import Array, Placeholder, solve_qubo, Constraint
from dwave.system.composites import EmbeddingComposite, FixedEmbeddingComposite
from dimod import AdjVectorBQM
import time
#import dwave.minorminer.find_embedding

N = 4950
isQPU = 1
Advantage = 1

if isQPU:
    print("QPU")
    if Advantage:
        print("Advantage")
        qpu = DWaveSampler(solver={'qpu': True, 'topology__type': 'pegasus'})
    else:
        print("Chimera")
        qpu = DWaveSampler(solver={'qpu': True, 'topology__type': 'chimera'})
    sampler = EmbeddingComposite(qpu)       
else :
    print("SA")
    sampler = neal.SimulatedAnnealingSampler()

samples = 2000
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
