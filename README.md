Licensing described in LICENSE files:
  - Python code found in folder `hdf5_and_metadata_class`: **MIT license**
  - Datasets in folder `calculation`: **Creative Commons Attribution 4.0 International**

Authorship and publication:
  - **Main author:** Eduardo Mendive Tapia
  - **email:** e.mendive.tapia@ub.edu
  - Work published in https://arxiv.org/abs/2302.06484

---

This repository contains the data generated and used for the work published in https://arxiv.org/abs/2302.06484. The notebook `notebook.ipynb` shows how to access and manipulate the most important data stored in this repository:
 1. `Weiss field` and `density of states` datasets are stored in marmot.hdf5
 2. The folder `calculation` contains all inputs and outputs, produced by `marmot code` (https://warwick.ac.uk/fac/sci/physics/research/theory/research/electrstr/marmot/). Inside there is a list of folders corresponding to different values of the lattice parameter for the DFT calculation. Each one of these folders contains another set of folders:
       - **Hutsepot**: Contains an initial DFT calculation using `hutsepot code` to generate input potentials.
       - **m.0...**: Contains inputs and outputs of a calculation made by `marmot code` for specific values of the magnetic order parameter ***m***.
 3. For further information on this repository, metadata is described in `marmot.json` file.
 4. The folder `hdf5_and_metadata_class` contains a python class called by `set_hdf5.ipynb` used to create:
    - `marmot.hdf5`
    - `marmot.json`
