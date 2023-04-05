Licensing described in LICENSE files:
  - Python code found in folder `hdf5_and_metadata_class`: **MIT license**
  - Data in folder `calculation`: **Creative Commons Attribution 4.0 International**

Authorship and publication:
  - **Main author:** Eduardo Mendive Tapia
  - **email:** e.mendive.tapia@ub.edu
  - Work published in https://arxiv.org/abs/2302.06484

---

This notebook shows how to access and manipulate the most important data stored in this repository:
 1. `Weiss field` and `density of states` data are stored in marmot.hdf5
 2. The folder `calculation` contains all inputs and outputs, produced by `marmot code` (https://warwick.ac.uk/fac/sci/physics/research/theory/research/electrstr/marmot/) 3. Metadata is described in `marmot.json` file.
 4. The folder `hdf5_and_metadata_class` contains a python class called by `set_hdf5.ipynb` used to create:
    - `marmot.hdf5`
    - `marmot.json`
