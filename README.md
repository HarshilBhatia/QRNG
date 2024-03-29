# Generation of Truly Random Numbers on a Quantum Annealer
[Paper](https://ieeexplore.ieee.org/abstract/document/9923932/) | 
[Code](https://github.com/HarshilBhatia/QRNG) | 
[Project Page](https://4dqv.mpi-inf.mpg.de/QRNG/)

This is the code for the experiments in the IEEE Access publication 'Generation of Truly Random Numbers on a Quantum Annealer'.

[Harshil Bhatia <sup> 1,2 </sup>](https://scholar.google.com/citations?user=8rU1AaQAAAAJ&hl=en), [Edith Tretschk <sup>2</sup>](https://people.mpi-inf.mpg.de/~tretschk/), [Christian Theobalt<sup>2</sup>](https://people.mpi-inf.mpg.de/~theobalt/) and [Vladislav Golyanik <sup>2</sup>](https://people.mpi-inf.mpg.de/~golyanik/)

<sup>1</sup> Indian Institute of Technology, Jodhpur , <sup>2</sup>Max Planck Institute for Informatics 

<img src="teaser.png" alt="teaser image" />

## Running the Code
The code can be executed directly on [D-Wave's Leap IDE](https://www.dwavesys.com/take-leap) or locally by installing [D-Wave Ocean SDK]( https://docs.ocean.dwavesys.com/en/stable/)

### Installation
If running the code locally, we recommend the user to create a virtual environment (optionally using conda)

```
conda env create -n ocean
pip install dwave-ocean-sdk
pip install pyqubo
```

The next step is to configure access to the Leap's Solvers. To achieve this, the user needs to create an account to gain access (a free account provides upto 1 minute of QPU time) to the solvers and retrieve their respective API tokens. Now run, 

``` dwave setup```

For more information related to the configuration please refer to this [guide](https://docs.ocean.dwavesys.com/en/stable/overview/sapi.html#sapi-access)


### Unbiased Random Number Generation
To generate 990,000 raw bits from the Advantage Architecture run the following code:
```
python unbiased_qrng.py --qpu --N 4950 --samples 200 --arch ADV
```
### Biased Random Number Generation
To generate 400,000 raw biased bits from the 2000Q Architecture run the following code:
```
python unbiased_qrng.py --qpu --N 2000 --samples 200 --arch 2000Q --bias 0.1
```


## Random Numbers 
We provide large sets of generated unbiased and biased random numbers [here](https://4dqv.mpi-inf.mpg.de/QRNG/) 

## Citation 
If you find our work useful in your research, please consider citing:

```
@article{bhatia2022qrng,
 title = {Generation of Truly Random Numbers on a Quantum Annealer},
 author = {Bhatia, Harshil and Tretschk, Edith and Theobalt, Christian and Golyanik, Vladislav },
 journal = {IEEE Access},
 year = {2022},
 volume = {},
 pages= {},
}
```
## License
Permission is hereby granted, free of charge, to any person or company obtaining a copy of this software and associated documentation files (the "Software") from the copyright holders to use the Software for any non-commercial purpose. Publication, redistribution and (re)selling of the software, of modifications, extensions, and derivates of it, and of other software containing portions of the licensed Software, are not permitted. The Copyright holder is permitted to publically disclose and advertise the use of the software by any licensee.

Packaging or distributing parts or whole of the provided software (including code, models and data) as is or as part of other software is prohibited. Commercial use of parts or whole of the provided software (including code, models and data) is strictly prohibited. Using the provided software for promotion of a commercial entity or product, or in any other manner which directly or indirectly results in commercial gains is strictly prohibited.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
