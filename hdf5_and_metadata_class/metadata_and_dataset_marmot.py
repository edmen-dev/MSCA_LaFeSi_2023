import h5py
import numpy as np

# external classes to manage outputs from marmot
from .parser_marmot import parser_marmot

class metadata_and_dataset_marmot:
    """
    Class containing separately hard-coded metadata attributes for marmot code.
    It calls calls parser_marmot to construct datasets
    """

    # initialization of the class
    def __init__(self, hdf5_file="marmot.hdf5"):
        self.hdf5_file = hdf5_file

        self.subfolder_hutsepot = "/hutsepot"
        self.subfolder_ini      = "/ini"
        self.subfolder_samp     = "/m"
        self.list_of_subfolders = []
        self.weiss_field_vs_m_buffer = []
        self.dos_vs_m_buffer = []

        self.name_of_calculation = None

        self.parser_marmot = parser_marmot()

        return
    
    def set_name_of_calculation(self, name_of_calculation):
        self.name_of_calculation = name_of_calculation
        return

    def check_name_of_calculation(self, name_of_calculation):
        if name_of_calculation is None:
            raise ValueError('No name_of_calculation provided, call set_name_of_calculation')
        return
    
    def check_alat(self, alat):
        if alat is None:
            raise ValueError('No lattice constant provided')
        return

    def set_group_0(self, alat=None, method_File = "w"):
        self.check_name_of_calculation(self.name_of_calculation)
        self.check_alat(alat)

        with h5py.File(self.hdf5_file, method_File) as f:
            group_0             = f.create_group(self.name_of_calculation)
            group_0.attrs['description'] = "This folder contains a full marmot calculation, for different values of the local order parameter m and a fixed lattice constant"
            group_0.attrs['name of calculation'] = self.name_of_calculation
            group_0.attrs['value of the lattice constant (Bohr units)'] = str(alat)
            # group_0.attrs['submission script:'] = 'submit.sh (used to run all slurm jobs running marmot for different values of m)'
            group_0.attrs['dataset of weiss fields vs order parameter in hdf5 file'] = self.name_of_calculation + "/weiss_field_vs_m"
            group_0.attrs['dataset of dos vs order parameter in hdf5 file'] = self.name_of_calculation + "/dos_vs_m"

        return group_0
    
    def set_group_hutsepot(self):
        self.check_name_of_calculation(self.name_of_calculation)
        subfolder = self.subfolder_hutsepot # hutsepot

        self.list_of_subfolders.append(subfolder)

        with h5py.File(self.hdf5_file, "a") as f:
            folder_name = self.name_of_calculation + subfolder

            group_hutsepot = f.create_group(folder_name)
            group_hutsepot.attrs['description'] = 'Initial DFT calculation to generate the input potentials for their use as inputs for marmot'
            group_hutsepot.attrs['type of files'] = 'inputs and outputs'
            group_hutsepot.attrs['name of the folder'] = folder_name
            group_hutsepot.attrs['DFT code'] = 'hutsepot'
            group_hutsepot.attrs['type of potentials'] = 'Disordered Local Moment (DLM) potentials'
            group_hutsepot.attrs['other files in this folder'] = 'input used for hutsepot code and generated standard outputs'

        return group_hutsepot
    
    def set_group_ini(self):
        self.check_name_of_calculation(self.name_of_calculation)
        subfolder = self.subfolder_ini # ini

        self.list_of_subfolders.append(subfolder)

        with h5py.File(self.hdf5_file, "a") as f:
            folder_name = self.name_of_calculation + subfolder
            group_ini = f.create_group(folder_name)
            group_ini.attrs['description'] = "This folder contains a python script to run marmot, as well a slurm job script, which is used in all folders /samp* for different values of m"
            group_ini.attrs['type of files'] = 'inputs'
            group_ini.attrs['name of the folder'] = folder_name
            group_ini.attrs['DFT code'] = 'marmot'
            
        return group_ini
    
    def set_group_samp(self, value_of_m=0.0033):
        value_of_m_string = '{0:.4f}'.format(value_of_m)

        self.check_name_of_calculation(self.name_of_calculation)
        subfolder = self.subfolder_samp + value_of_m_string # samp

        self.list_of_subfolders.append(subfolder)

        with h5py.File(self.hdf5_file, "a") as f:
            folder_name = self.name_of_calculation + subfolder
            group_samp = f.create_group(folder_name)
            group_samp.attrs['description'] = "This folder contains the output generated by marmot for m=" + value_of_m_string
            group_samp.attrs['type of files'] = 'outputs'
            group_samp.attrs['name of the folder'] = folder_name
            group_samp.attrs['DFT code'] = 'marmot'

            # create dataset
            dataset_samp, current_results = self.set_dataset_samp(group_samp, folder_name)
        
        self.collect_marmot_data(value_of_m, current_results)
            
        return group_samp, dataset_samp

    def set_dataset_samp(self, group_samp, folder_name):
        n = self.parser_marmot.number_of_rows
        m = self.parser_marmot.number_of_columns
        results_path = folder_name
        results = self.parser_marmot.get_information_from_results_final(results_path)

        dataset_samp = group_samp.create_dataset("results_final", (n,m), dtype='f')
        current_results = results.copy()
        dataset_samp[:,:] = current_results
        
        return dataset_samp, current_results
    
    def collect_marmot_data(self, value_of_m, current_results):
        current_hs = current_results[:,2]
        h_1 = np.sum(current_hs[0:24]) / len(current_hs[0:24])
        dos = current_results[0][-3]
        self.weiss_field_vs_m_buffer.append([ value_of_m, h_1 ])
        self.dos_vs_m_buffer.append([ value_of_m, dos ])

        return
    
    def set_dataset_vs_m(self, name_of_calculation):
        unit_factor = 13.606
        number_of_m = len(self.weiss_field_vs_m_buffer)
        weiss_field_vs_m = np.zeros((number_of_m,2))
        dos_vs_m = np.zeros((number_of_m,2))
        for im, point in enumerate(self.weiss_field_vs_m_buffer):
            weiss_field_vs_m[im,0] = point[0]
            weiss_field_vs_m[im,1] = point[1] * unit_factor*1e3 # in meV
        for im, point in enumerate(self.dos_vs_m_buffer):
            dos_vs_m[im,0] = point[0]
            dos_vs_m[im,1] = point[1] / unit_factor

        with h5py.File(self.hdf5_file, "a") as f:
            dataset_weiss_field_vs_m = f.create_dataset(name_of_calculation + "/weiss_field_vs_m", (number_of_m,2), dtype='f')
            dataset_weiss_field_vs_m[:,:] = weiss_field_vs_m.copy()
            dataset_dos_vs_m = f.create_dataset(name_of_calculation + "/dos_vs_m", (number_of_m,2), dtype='f')
            dataset_dos_vs_m[:,:] = dos_vs_m.copy()

        return