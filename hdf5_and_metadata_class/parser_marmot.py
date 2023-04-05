import numpy as np

class parser_marmot:
    """
    Class to extract final data from marmot outputs and process it.
    It is called by class metadata_and_dataset_marmot
    """

    # initialization of the class
    def __init__(self):

        # hard-coded values for calculations on LaFeSi in the DLM state
        self.results_file_name = 'results_final.dat'
        self.number_of_columns = 8
        self.number_of_rows = 52

        return
    
    def get_information_from_results_final(self, results_path):
        if results_path[-1] != '/':
            results_path += '/'
        results = np.loadtxt(results_path + self.results_file_name)
        
        return results
    
    def get_m_from_betahs(self, betahs, tol=1e-4):
        if np.abs(betahs) > tol:
            return -1/betahs + 1/np.tanh(betahs)
        else:
            return 0.0