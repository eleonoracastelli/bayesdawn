# -*- coding: utf-8 -*-
# Author: Quentin Baghi 2018
import h5py
import configparser

def load_simulation(hdf5_name,
                    param_keylist=['m1', 'm2', 'xi1', 'xi2', 'tc', 'dist', 'inc', 'phi0', 'lam', 'beta', 'psi'],
                    signal_keylist=['tdi_a', 'tdi_e', 'tdi_ts']):

    # Load data
    fh5 = h5py.File(hdf5_name, 'r')
    params = [fh5["parameters/" + par][()]for par in param_keylist]
    time_vect = fh5["signal/time"][()]
    signal_list = [fh5["signal/" + sig][()] for sig in signal_keylist]
    noise_list = [fh5["noise/" + sig][()] for sig in signal_keylist]
    fh5.close()

    return time_vect, signal_list, noise_list, params


def create_config_file(file_name='example.ini'):

    config = configparser.ConfigParser()
    config['InputData'] = {'FilePath': '/Users/qbaghi/Codes/data/simulations/mbhb/simulation_3.hdf5',
                           'StartTime': 850880,
                           'EndTime': 2161600}

    config['Model'] = {'Likelihood': 'full',
                       'MinimumFrequency': 1e-5,
                       'MaximumFrequency': 1e-2}

    config['Sampler'] = {'Type': 'dynesty',
                         'WalkerNumber': 44,
                         'TemperatureNumber': 10,
                         'MaximumIterationNumber': 100000,
                         'ThinningNumber': 1,
                         'AuxiliaryParameterUpdateNumber': 100,
                         'SavingNumber': 100,
                         'PSDEstimation': False,
                         'MissingDataImputation': False}

    config['OutputData'] = {'DirectoryPath': '/Users/qbaghi/Codes/data/results_dynesty/local/',
                            'FileSuffix': 'chains.hdf5'}

    with open(file_name, 'w') as configfile:
        config.write(configfile)