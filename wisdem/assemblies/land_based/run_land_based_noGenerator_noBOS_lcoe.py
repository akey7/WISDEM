"""
The purpose of this file is to run the land based turbine assembly
in a completely self-contained manner, and test ideas that may
be able to help with regression testing of this assembly.
"""

from __future__ import print_function
from openmdao.api import Group, Problem, ScipyOptimizeDriver, SqliteRecorder, NonlinearRunOnce, DirectSolver
import numpy as np
from io import StringIO
import sys


try:
    from openmdao.api import pyOptSparseDriver
except:
    pass

from wisdem.rotorse.rotor_geometry_yaml import ReferenceBlade

from land_based_noGenerator_noBOS_lcoe import Init_LandBasedAssembly, LandBasedTurbine
from wisdem.rotorse.rotor import RotorSE, Init_RotorSE_wRefBlade


if __name__ == "__main__":
    # Reference rotor design
    fname_schema = "../../rotorse/turbine_inputs/IEAontology_schema.yaml"
    fname_input = "../../rotorse/turbine_inputs/nrel5mw_mod_update.yaml"
    Analysis_Level = 0  # 0: Run CCBlade; 1: Update FAST model at each iteration but do not run; 2: Run FAST w/ ElastoDyn; 3: (Not implemented) Run FAST w/ BeamDyn
    # Initialize blade design
    refBlade = ReferenceBlade()
    refBlade.verbose = True
    refBlade.NINPUT = 8
    refBlade.NPTS = 50
    refBlade.spar_var = ['Spar_Cap_SS', 'Spar_Cap_PS']  # SS, then PS
    refBlade.te_var = 'TE_reinforcement'
    refBlade.validate = False
    refBlade.fname_schema = fname_schema
    blade = refBlade.initialize(fname_input)
    # Initialize tower design
    Nsection_Tow = 6

    prob = Problem()
    prob.model = LandBasedTurbine(RefBlade=blade, Nsection_Tow=Nsection_Tow, VerbosityCosts=True)

    prob.setup(check=True)

    ###
    prob = Init_RotorSE_wRefBlade(prob, blade, Analysis_Level = Analysis_Level, fst_vt = {})
    
    
    # Environmental parameters for the tower
    # prob['wind_reference_speed']           = 11.0
    prob['wind_reference_height']          = prob['hub_height']

    # Steel properties for the tower
    prob['material_density']               = 7850.0
    prob['E']                              = 200e9
    prob['G']                              = 79.3e9
    prob['yield_stress']                   = 3.45e8

    # Design constraints
    prob['max_taper_ratio']                = 0.4
    prob['min_diameter_thickness_ratio']   = 120.0

    # Safety factors
    prob['gamma_fatigue']   = 1.755 # (Float): safety factor for fatigue
    prob['gamma_f']         = 1.35  # (Float): safety factor for loads/stresses
    prob['gamma_m']         = 1.3   # (Float): safety factor for materials
    prob['gamma_freq']      = 1.1   # (Float): safety factor for resonant frequencies
    prob['gamma_n']         = 1.0
    prob['gamma_b']         = 1.1
    
    # Tower
    prob['foundation_height']              = 0.0 #-prob['water_depth']
    # prob['tower_outer_diameter']           = np.linspace(10.0, 3.87, Nsection_Tow+1)
    prob['tower_outer_diameter']           = np.linspace(6.0, 3.87, Nsection_Tow+1)
    prob['tower_section_height']           = (prob['hub_height'] - prob['foundation_height']) / Nsection_Tow * np.ones(Nsection_Tow)
    prob['tower_wall_thickness']           = np.linspace(0.027, 0.019, Nsection_Tow)
    prob['tower_buckling_length']          = 30.0
    prob['tower_outfitting_factor']        = 1.07

    prob['DC']      = 80.0
    prob['shear']   = True
    prob['geom']    = False
    prob['tower_force_discretization'] = 5.0
    prob['nM']      = 2
    prob['Mmethod'] = 1
    prob['lump']    = 0
    prob['tol']     = 1e-9
    prob['shift']   = 0.0
    
    # Plant size
    prob['project_lifetime'] = prob['lifetime'] = 20.0    
    prob['number_of_turbines']             = 200. * 1.e+006 / prob['machine_rating']
    prob['annual_opex']                    = 43.56 # $/kW/yr
    prob['bos_costs']                      = 517.0 # $/kW
    
    # For RNA
    prob['rna_weightM'] = True

    # For turbine costs
    # prob['offshore']             = False
    prob['crane']                = False
    prob['bearing_number']       = 2
    prob['crane_cost']           = 0.0
    prob['labor_cost_rate']      = 3.0
    prob['material_cost_rate']   = 2.0
    prob['painting_cost_rate']   = 28.8
    
    # Gearbox
    prob['drive.gear_ratio']        = 96.76  # 97:1 as listed in the 5 MW reference document
    prob['drive.shaft_angle']       = prob['tilt']*np.pi / 180.0  # rad
    prob['drive.shaft_ratio']       = 0.10
    prob['drive.planet_numbers']    = [3, 3, 1]
    prob['drive.shrink_disc_mass']  = 333.3 * prob['machine_rating'] / 1e6  # estimated
    prob['drive.carrier_mass']      = 8000.0  # estimated
    prob['drive.flange_length']     = 0.5
    prob['overhang']                = 5.0
    prob['drive.distance_hub2mb']   = 1.912  # length from hub center to main bearing, leave zero if unknown
    prob['drive.gearbox_input_xcm'] = 0.1
    prob['drive.hss_input_length']  = 1.5
    prob['drive.yaw_motors_number'] = 1
    ###

    prob.model.nonlinear_solver = NonlinearRunOnce()
    prob.model.linear_solver = DirectSolver()

    # This is an example of capturing the output of run_driver(), which prints
    # directly to stdout, into a string. This output can then be compared be
    # examined as shown a few lines below.

    old_stdout = sys.stdout
    capture_stdout = StringIO()
    try:
        sys.stdout = capture_stdout
        prob.run_driver()
    finally:
        sys.stdout = old_stdout

    print(">>> Begin list of problem vars")
    foo = prob.model.list_inputs(units=True)
    # print(prob['plantfinancese.lcoe'])
    
    # This is how to examine the string output of run_driver
    # print(capture_stdout.getvalue())
    print("<<< End list of problem vars")
