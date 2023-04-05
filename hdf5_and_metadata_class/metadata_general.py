class metadata_general:
    """
    Class containing separately hard-coded metadata attributes for the general header.
    At the moment something similar to the standars of Zenodo is implemented:
    https://zenodo.org/schemas/deposits/records/legacyrecord.json
    """

    # initialization of the class
    def __init__(self, type = 'marmot'):
        self.type = type
        return
    
    def create_properties_in_json(self, data):
        data["properties"] = {     
            "access_conditions": {
                "description": "Conditions under which access is given if record is restricted.",
                "title": "Access conditions",
                "type": "The access to the data in this repository is described in LICENSE files."
            },
            "access_right_of_data": {
                "default": "Creative Commons Attribution 4.0 International",
                "description": "See file ./LICENSE "
            },
            "access_right_of_python_code": {
                "default": "MIT License",
                "description": "See file ./hdf5_and_metadata_class/LICENSE"
            },
            "contributors": {
                "description": "Main contributor",
                "items": {
                    "properties": {
                        "affiliation": {
                            "description": "Affiliation for the purpose of this specific record.",
                            "type": "University of Barcelona"
                        },
                        "name": {
                            "description": "Full name of person or organisation. Personal name format: family, given.",
                            "type": "Mendive Tapia, Eduardo"
                        },
                        "email": {
                            "description": "email address.",
                            "type": "e.mendive.tapia@ub.edu"
                        },
                        "orcid": {
                            "description": "ORCID identifier for creator.",
                            "type": "0000-0001-8328-6945"
                        },
                        "type": {
                            "enum": [
                                "ContactPerson",
                                "DataCollector",
                                "DataCurator",
                                "ProjectLeader",
                                "Researcher"
                            ],
                        }
                    }
                }
            },
            "key words" : {
                "description": "key words for the identification of the interest of this repository",
                "enum": [
                    "Magnetism and magnetic materials",
                    "Caloric effects",
                    "ab initio thermodynamics",
                    "La(Fe,Si)13 compounds",
                    "Density Functional Theory",
                    "disordered local moment (DLM) theory"
                ]
            },
            "target communities" : {
                "description": "scientific communities and research areas with potential interest in this work",
                "enum": [
                    "Caloric refrigeration",
                    "Magnetism and magnetic materials",
                    "Density Functional Theory"
                ]
            },
        "description": {
        "description": "abstract: ",
        "type": "La(FexSi1−x)13 and derived quaternary compounds are well-known for their giant, tunable, magneto- and barocaloric responses around a first-order paramagnetic-ferromagnetic transition near room temperature with low hysteresis. Remarkably, such a transition shows a large spontaneous volume change together with itinerant electron metamagnetic features. While magnetovolume effects are well-established mechanisms driving first-order transitions, purely electronic sources have a long, subtle history and remain poorly understood. Here we apply a disordered local moment picture to quantify electronic and magnetoelastic effects at finite temperature in La(FexSi1−x)13 from first-principles. We obtain results in very good agreement with experiment and demonstrate that the magnetoelastic coupling drives the first-order character and causes at the same time a huge electronic entropy contribution to the caloric response."
        },
        "doi": {
        "description": "Digital Object Identifier (DOI) of publication.",
        "type": "https://doi.org/10.48550/arXiv.2302.06484"
        },
        "grants": {
        "description": "MSCA-IF",
        "project acronym": "MULTICALORICS",
        "project number": "101025767",
        "project title": "Multicaloric refrigeration enhanced by multisite interactions: Bridging theory and experiment"
        }
        }
        return

    def create_description_in_json(self, data):
        data["description"] = "This module contains inputs, outputs, and post-processed data generated and treated using MARMOT, a density functional theory -based code implementing the disordered local moment (DLM) picture."
        return
