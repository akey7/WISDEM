from __future__ import print_function
from openmdao.api import Group, Problem, ScipyOptimizeDriver, SqliteRecorder, NonlinearRunOnce, DirectSolver

try:
    from openmdao.api import pyOptSparseDriver
except:
    pass

from wisdem.rotorse.rotor_geometry_yaml import ReferenceBlade
from wisdem.commonse.mpi_tools import MPI

from .land_based_noGenerator_noBOS_lcoe import Init_LandBasedAssembly, LandBasedTurbine


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

    if not MPI:
        prob.model.approx_totals()

    prob.run_driver()
