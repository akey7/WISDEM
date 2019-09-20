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

# from land_based_noGenerator_noBOS_lcoe import Init_LandBasedAssembly, LandBasedTurbine
from wisdem.assemblies.land_based.land_based_noGenerator_noBOS_lcoe import Init_LandBasedAssembly, LandBasedTurbine
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
    prob = Init_LandBasedAssembly(prob, blade, Nsection_Tow)
    prob.model.nonlinear_solver = NonlinearRunOnce()
    prob.model.linear_solver = DirectSolver()

    # How to print a single output
    # print(prob['plantfinancese.lcoe'])

    # This is an example of capturing the output of run_driver(), which prints
    # directly to stdout, into a string.

    old_stdout = sys.stdout
    capture_stdout = StringIO()
    try:
        sys.stdout = capture_stdout
        prob.run_driver()
    finally:
        sys.stdout = old_stdout

    print("<><><><><><><><><><> Begin problem INPUTS <><><><><><><><><><>")
    prob.model.list_inputs(units=True)
    print("<><><><><><><><><><> End problem INPUTS <><><><><><><><><><>")

    print("<><><><><><><><><><> Begin problem OUTPUTS <><><><><><><><><><>")
    print(capture_stdout.getvalue())
    print("<><><><><><><><><><> End problem OUTPUTS <><><><><><><><><><>")
