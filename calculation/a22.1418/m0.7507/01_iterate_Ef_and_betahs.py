from pymarmot.marmot import dlm
from pymarmot.constants import RydineV
from subprocess import run
from os import getcwd
import numpy as np
import re

from parsers.dft_codes import parser
my_parser = parser()



####################################################################################################
# DEFINITIONS
####################################################################################################

####################################################################################################
def get_positions_in_lattice_vector_units(lattice_parameters, cell, hutsepot_positions):
    transf_cell_to_cartesian = np.zeros((3,3))
    for i in range(3):
        transf_cell_to_cartesian[:,i] = cell[i][:] /lattice_parameters[i]
    transf_cartesian_to_cell = np.linalg.inv(transf_cell_to_cartesian)
    number_of_atoms = len(hutsepot_positions)
    position_cell = np.zeros((number_of_atoms,3))
    for i_position, position_cartesian in enumerate(hutsepot_positions):
        for i_dir in range(3):
            for j in range(3):
                position_cell[i_position, i_dir] +=  transf_cartesian_to_cell[i_dir, j] * position_cartesian[j] 

    return position_cell

####################################################################################################
def run_dlm_calculation(dlm_inputs, prec=True, lmax=3, relativistic='scalar', parapot=True):
    Efnew          = dlm_inputs[0]
    hutsepot_ebot  = dlm_inputs[1]
    abspos         = dlm_inputs[2][0]
    fracpos        = dlm_inputs[2][1]
    units          = dlm_inputs[3]
    potentiallist  = dlm_inputs[4]
    my_betahlist   = dlm_inputs[5]
    nhatlist       = dlm_inputs[6]
    sites          = dlm_inputs[7]
    concentrations = dlm_inputs[8]

    Ef = Efnew * 1.0
    my_calculation = dlm(cell=cell,
                #fracpos=fracpos, # in lattice vector units
                abspos=abspos, # hutsepot_positions
                units=units,
                potentials=potentiallist,
                sites=sites,
                concentrations=concentrations,
                betahlist=my_betahlist,
                nhatlist=nhatlist
                )

    my_calculation.set_energygrid(eF=Ef, ebot=hutsepot_ebot)
    my_calculation.prepare_calculation(lmax=lmax,
                                relativistic=relativistic,
                                parapot=parapot)
    # Modification of tolint
    if prec==False:
        run('sed -i \'s/1e-05/1e-04/g\' ./lattice.dat',shell=True)

    run(fortmarmotcommand,shell=True)
    my_calculation = dlm(restart=True)
    Nelec = my_calculation.get_totaldos()[0]
    Efnew = my_calculation.get_newEf(targetelec)[0]

    T_a = my_calculation.get_speciesT()
    h_a = my_calculation.get_weissfields()
    DoSinfo = my_calculation.get_totaldos(units='muB')
    DoSatEf = my_calculation.get_DoSatEf()

    return Efnew, Nelec, Ef, T_a, h_a, DoSinfo, DoSatEf

####################################################################################################
def write_results(iteration, betahlist, output_dlm_calculation, prec = True):
    Efnew     = output_dlm_calculation[0]
    Nelec     = output_dlm_calculation[1]
    Ef        = output_dlm_calculation[2]
    T_a       = output_dlm_calculation[3]
    h_a       = output_dlm_calculation[4]
    DoSinfo   = output_dlm_calculation[5]
    DoSatEf   = output_dlm_calculation[6]

    rydberg_to_K = 13.605693/8.617333e-5
    if prec:
        results_file_name = './results_' + str(iteration) + '_prec.dat'
    else:
        results_file_name = './results_' + str(iteration) + '.dat'

    s = '# site betah h T M DoS(Ef) N Ef\n'
    with open(results_file_name, 'w') as outfile:
        outfile.write(s)

    current_field_1 = np.sum(h_a[0:24])/24
    current_field_2 = np.sum(h_a[24:26])/2
    current_betah_1 = betahlist[0]
    current_betah_2 = betahlist[24]
    s = 'sublattice 1'
    s += ' ' + str(current_betah_1)
    s += ' ' + str(current_field_1)
    s += ' ' + str(current_field_1/current_betah_1*rydberg_to_K)
    s += '\n'
    with open(results_file_name, 'a') as outfile:
        outfile.write(s)

    s = 'sublattice 2'
    s += ' ' + str(current_betah_2)
    s += ' ' + str(current_field_2)
    s += ' ' + str(current_field_2/current_betah_2*rydberg_to_K)
    s += '\n'
    with open(results_file_name, 'a') as outfile:
        outfile.write(s)

    for i_site, this_weiss_field in enumerate(h_a):
        s = str(i_site + 1)
        s += ' ' + str(betahlist[i_site])
        s += ' ' + str(this_weiss_field[2])
        s += ' ' + str(T_a[i_site])
        s += ' ' + str(DoSinfo[1])
        s += ' ' + str(DoSatEf)
        s += ' ' + str(DoSinfo[0])
        s += ' ' + str(Ef)
        s += '\n'
        with open(results_file_name, 'a') as outfile:
            outfile.write(s)

    current_fields = [current_field_1, current_field_2]
    current_betahs = [current_betah_1, current_betah_2]
    return current_fields, current_betahs

####################################################################################################
def check_convergence(converged_list, betahlist, Nelec, targetelec, current_fields, current_betahs):
    current_field_1 = current_fields[0]
    current_field_2 = current_fields[1]
    current_betah_1 = current_betahs[0]
    current_betah_2 = current_betahs[1]

    converged       = converged_list[0]
    converged_Ef    = converged_list[1]
    converged_betah = converged_list[2]

#   Check to see if Ef and betahs have converged
    if converged_Ef == False:
        if ( np.isclose(Nelec, targetelec, atol=0.001) ):
            converged_Ef = True

    if converged_betah == False:
        current_target_betah_2 = current_betah_1 * current_field_2/current_field_1
        ##  current_target_betah_2 = 0.0
        if ( np.isclose(current_betah_2,current_target_betah_2,rtol=0.005) ):
            converged_betah = True
        else:
            betahlist[24] = current_target_betah_2
            betahlist[25] = current_target_betah_2

    if (converged_Ef == True) and (converged_betah == True):
        converged = True

    return converged, betahlist

####################################################################################################
def write_final_results(Ef, betahlist, T_a, h_a, DoSinfo, DoSatEf):
    s = '# site betah h T M DoS(Ef) N Ef\n'
    with open('./results_final.dat', 'w') as outfile:
        outfile.write(s)

    for i_site, this_weiss_field in enumerate(h_a):
        s = str(i_site + 1)
        s += ' ' + str(betahlist[i_site])
        s += ' ' + str(this_weiss_field[2])
        s += ' ' + str(T_a[i_site])
        s += ' ' + str(DoSinfo[1])
        s += ' ' + str(DoSatEf)
        s += ' ' + str(DoSinfo[0])
        s += ' ' + str(Ef)
        s += '\n'
        with open('./results_final.dat', 'a') as outfile:
            outfile.write(s)
    return




# Command to run fortmarmot
fortmarmotexe = '/home/za317506/workbench/devel/codes/marmot21_190422/fortmarmot/bin/main.x'
fortmarmotcommand = 'srun ' + fortmarmotexe + ' > ./out'
# this directory
thisdir = '\"' + getcwd() + '/\"\n'
with open('./thisdir.txt','w') as outfile:
    outfile.write(thisdir)
####################################################################################################
# PREPARING CALCULATION
####################################################################################################

####################################################################################################
# CRYSTAL STRUCTURE
# Getting information from Hutsepot
hutsepot_path = getcwd() + '/../hutsepot/'
hutsepot_data = my_parser.get_information_from_hutsepot(hutsepot_path)
lattice_parameters = hutsepot_data[0]
lattice_vectors    = hutsepot_data[1]
hutsepot_positions = hutsepot_data[2]
hutsepot_ebot      = hutsepot_data[3]
hutsepot_ef        = hutsepot_data[4]
ETOT_lloyd         = hutsepot_data[5]

#  Info  about the crystal structure
a0 = lattice_parameters[0]
b0 = lattice_parameters[1]
c0 = lattice_parameters[2]

# The three lattice vectors a, b and c, here
# given in units of Bohr
a = a0 * lattice_vectors[0]
b = b0 * lattice_vectors[1]
c = c0 * lattice_vectors[2]
cell = [a,b,c]
position_cell = get_positions_in_lattice_vector_units(lattice_parameters, cell, hutsepot_positions)

# The positions of the atoms, given in units
# of the lattice vectors (fracpos) or absolute cartesian (abspos)
fracpos = []
for current_position in position_cell:
    fracpos.append( np.array([current_position[0], current_position[1], current_position[2]]) )
abspos = []
for current_position in hutsepot_positions:
    abspos.append( np.array([a0*current_position[0], b0*current_position[1], c0*current_position[2]]) )

####################################################################################################
# DLM INPUTS
# input betahs and concentration
betahs_in = 4.00
p_Si = 0.120
p_Fe = 1.0-p_Si
targetelec = 9*2 + 8*2 + (8*p_Fe + 4*p_Si)*24 # Number of electrons in unit cell
# Initial guess of Ef (will be iterated)
Efnew = hutsepot_ef
print('targetelec = ', targetelec)
print('Initial guess of Ef = ', Efnew)

number_of_Fe_DLM_potentials = 26
number_of_La_potentials = 2
number_of_Si_potentials = 24
potentiallist = []
betahlist = []
nhatlist = []
concentrations = []
sites = []
for i in range(number_of_Fe_DLM_potentials):
    potentiallist.append(hutsepot_path + 'Fe' + str(2*i+1) + '.pot')
    if i > 23:
        betahlist.append(np.array(betahs_in*1.1))
        nhatlist.append(np.array([0.0,0.0,1.0]))
        concentrations.append(np.array(1.000))
    else:
        betahlist.append(np.array(betahs_in))
        nhatlist.append(np.array([0.0,0.0,1.0]))
        concentrations.append(np.array(p_Fe))
    sites.append(np.array( i+1 ))
for i in range(number_of_La_potentials):
    potentiallist.append(hutsepot_path + 'La' + str(i+1) + '.pot')
    betahlist.append(np.array(0.00))
    nhatlist.append(np.array([0.0,0.0,1.0]))
    concentrations.append(np.array(1.000))
    sites.append(np.array( i+1 + 26 ))
for i in range(number_of_Si_potentials):
    potentiallist.append(hutsepot_path + 'Si' + str(i+1) + '.pot')
    betahlist.append(np.array(0.00))
    nhatlist.append(np.array([0.0,0.0,1.0]))
    concentrations.append(np.array(p_Si))
    sites.append(np.array( i+1 ))
##sites = None
##concentrations = None

##################################################
# RUN CALCULATION
##################################################

dlm_inputs = []
dlm_inputs.append(Efnew)
dlm_inputs.append(hutsepot_ebot)
dlm_inputs.append([abspos, fracpos])
dlm_inputs.append('Bohr')
dlm_inputs.append(potentiallist)
dlm_inputs.append(betahlist)
dlm_inputs.append(nhatlist)
dlm_inputs.append(sites)
dlm_inputs.append(concentrations)

# with lower tolint
prec = False
for my_betahlist in [betahlist]:
    converged       = False
    converged_Ef    = False
    converged_betah = False
    iteration = 0
    while (converged == False):
        output_dlm_calculation = run_dlm_calculation(dlm_inputs, prec=prec, lmax=3, relativistic='scalar', parapot=True)
        Efnew     = output_dlm_calculation[0]
        Nelec     = output_dlm_calculation[1]
        Ef        = output_dlm_calculation[2]
        T_a       = output_dlm_calculation[3]
        h_a       = output_dlm_calculation[4]
        DoSinfo   = output_dlm_calculation[5]
        DoSatEf   = output_dlm_calculation[6]
        
        current_fields, current_betahs = write_results(iteration, betahlist, output_dlm_calculation, prec=prec)
        converged_list = [converged, converged_Ef, converged_betah]
        converged, betahlist = check_convergence(converged_list, betahlist, Nelec, targetelec, current_fields, current_betahs)

        iteration += 1
        if converged_Ef == False:
            dlm_inputs[0] = Efnew # Updating Efnew
    if prec:
        write_final_results(Ef, betahlist, T_a, h_a, DoSinfo, DoSatEf)

# with higher tolint
prec = True
for my_betahlist in [betahlist]:
    converged       = False
    converged_Ef    = False
    converged_betah = False
    iteration = 0
    while (converged == False):
        output_dlm_calculation = run_dlm_calculation(dlm_inputs, prec=prec, lmax=3, relativistic='scalar', parapot=True)
        Efnew     = output_dlm_calculation[0]
        Nelec     = output_dlm_calculation[1]
        Ef        = output_dlm_calculation[2]
        T_a       = output_dlm_calculation[3]
        h_a       = output_dlm_calculation[4]
        DoSinfo   = output_dlm_calculation[5]
        DoSatEf   = output_dlm_calculation[6]
        
        current_fields, current_betahs = write_results(iteration, betahlist, output_dlm_calculation, prec=prec)
        converged_list = [converged, converged_Ef, converged_betah]
        converged, betahlist = check_convergence(converged_list, betahlist, Nelec, targetelec, current_fields, current_betahs)

        iteration += 1
        if converged_Ef == False:
            dlm_inputs[0] = Efnew # Updating Efnew
    if prec:
        write_final_results(Ef, betahlist, T_a, h_a, DoSinfo, DoSatEf)


# Compression and cleaning to reduce the number of output files
folder_name_for_compression = 'energy_dependent_output_data'
files_to_be_compressed = 'dos.* taumat.* torq.* weiss.*'

run('mkdir ' + folder_name_for_compression, shell=True)
run('mv '+ files_to_be_compressed + ' ./' + folder_name_for_compression, shell=True)
run('tar -czvf ' + folder_name_for_compression + '.tar.gz' + ' ./' + folder_name_for_compression + ' > ' + folder_name_for_compression + '.txt', shell=True)
run('rm -r ' + folder_name_for_compression, shell=True)
