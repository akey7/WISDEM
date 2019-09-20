from unittest import TestCase

from openmdao.api import Group, Problem, ScipyOptimizeDriver, SqliteRecorder, NonlinearRunOnce, DirectSolver
import numpy as np
from io import StringIO
import sys

try:
    from openmdao.api import pyOptSparseDriver
except:
    pass

from wisdem.rotorse.rotor_geometry_yaml import ReferenceBlade

from wisdem.assemblies.land_based.land_based_noGenerator_noBOS_lcoe import Init_LandBasedAssembly, LandBasedTurbine
from wisdem.rotorse.rotor import RotorSE, Init_RotorSE_wRefBlade

class Test_land_based_noGenerator_noBOS_lcoe(TestCase):
    def setUp(self):
        """
        This setup method sets up the Problem and runs the driver.

        Caveat: If there are more methods to test individual outputs, this should
        be refactored to a class or module setUp so that the calculation
        doesn't run for each test. That would be very inefficient!
        """
        # Reference rotor design
        fname_schema = "../wisdem/rotorse/turbine_inputs/IEAontology_schema.yaml"
        fname_input = "../wisdem/rotorse/turbine_inputs/nrel5mw_mod_update.yaml"
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

        # Set up the problem
        self.prob = Problem()
        self.prob.model = LandBasedTurbine(RefBlade=blade, Nsection_Tow=Nsection_Tow, VerbosityCosts=True)
        self.prob.setup(check=True)
        self.prob = Init_LandBasedAssembly(self.prob, blade, Nsection_Tow)
        self.prob.model.nonlinear_solver = NonlinearRunOnce()
        self.prob.model.linear_solver = DirectSolver()

        # Run the problem, while capturing the output run_driver() would print
        # to stdout
        old_stdout = sys.stdout
        self.capture_stdout = StringIO()
        try:
            sys.stdout = self.capture_stdout
            self.prob.run_driver()
        finally:
            sys.stdout = old_stdout

    def test_land_based_noGenerator_noBOS_lcoe(self):
        """
        For this test, find out if the LCOE cost calculates correctly.
        If it does, simply pass. If not, print inputs and outputs
        and then fail the test.
        """
        expected = 0.0346
        actual = round(self.prob['plantfinancese.lcoe'][0], 4)

        if expected != actual:
            print(">>>>>>>>>>>>>>>> test_land_based_noGenerator_noBOS_lcoe fail <<<<<<<<<<<<<<<<<<<<")
            self.print_inputs_and_outputs()

        self.assertTrue(expected == actual)

    def print_inputs_and_outputs(self):
        """
        If the tests fail to pass then this method is called to report
        the inputs and the outputs.
        """
        print("<><><><><><><><><><> Begin problem INPUTS <><><><><><><><><><>")
        self.prob.model.list_inputs(units=True)
        print("<><><><><><><><><><> End problem INPUTS <><><><><><><><><><>")

        print("<><><><><><><><><><> Begin problem OUTPUTS <><><><><><><><><><>")
        print(self.capture_stdout.getvalue())
        print("<><><><><><><><><><> End problem OUTPUTS <><><><><><><><><><>")
