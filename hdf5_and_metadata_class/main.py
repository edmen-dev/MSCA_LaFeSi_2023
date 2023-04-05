import h5py
import json

# external classes to manage metadata and datasets
from .metadata_general import metadata_general
from .metadata_and_dataset_marmot  import metadata_and_dataset_marmot

class hdf5_and_metadata:
    """
    The objective of this class is to create an hdf5 file that
        - centralizes the creation of metadata
        - stores the most final output data

    Author: Eduardo Mendive Tapia
    email: e.mendive.tapia@ub.edu
    MSCA-IF: project: 101025767
    date: March 2023

    Acknowledgements to Anoop Chandran for advice and help
    """

    # initialization of the class
    def __init__(self, type = 'marmot', hdf5_file="marmot.hdf5"):
        self.type = type
        self.hdf5_file = hdf5_file

        self.metadata_general = metadata_general(type=self.type)
        self.metadata_and_dataset_marmot  = metadata_and_dataset_marmot(hdf5_file=hdf5_file)

        return
    
    ###########################################################################
    # General methods for the class

    def h5py_to_json_marmot(self, h5_file_path, json_file_path, list_of_objects, list_of_subfolders):
        with h5py.File(h5_file_path, 'r') as f:
            data = {}
            self.metadata_general.create_description_in_json(data)
            self.metadata_general.create_properties_in_json(data)

            for my_object in list_of_objects:
                my_keys = f[my_object].attrs.keys()
                data[my_object] = {key: f[my_object].attrs[key] for key in my_keys}

                for subfolder in list_of_subfolders:
                    subfolder_path = my_object + subfolder
                    my_keys = f[subfolder_path].attrs.keys()
                    data[my_object][subfolder] = {key: f[subfolder_path].attrs[key] for key in my_keys}

            with open(json_file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
        return

    # to show all groups inside an hdf5-object
    def show_obj(obj, sep='\t', verbose=False):
        """
        Iterate through groups in a HDF5 file and prints the groups and datasets names and datasets attributes
        """
        if type(obj) in [h5py._hl.group.Group,h5py._hl.files.File]:
            for key in obj.keys():
                print(sep,'-',key,':',obj[key])
                if(verbose): print(sep,'\t','Attributes:',obj[key].attrs.keys())
                show_obj(obj[key],sep=sep+'\t')
        elif type(obj)==h5py._hl.dataset.Dataset:
            for key in obj.attrs.keys():
                print(sep+'\t','-',key,':',obj.attrs[key])

        return

    # # old version (deprecrated)
    # def h5py_to_json(self, h5_file_path, json_file_path, list_of_objects):
    #     with h5py.File(h5_file_path, 'r') as f:
    #         data = {}
    #         self.metadata.create_description_in_json(data)
    #         self.metadata.create_properties_in_json(data)

    #         for my_object in list_of_objects:
    #             my_keys = f[my_object].attrs.keys()
    #             data[my_object] = {key: f[my_object].attrs[key] for key in my_keys}

    #         with open(json_file_path, 'w') as json_file:
    #             json.dump(data, json_file, indent=4)
    #     return


    ###########################################################################
    # methods for the class particular for 'marmot'
