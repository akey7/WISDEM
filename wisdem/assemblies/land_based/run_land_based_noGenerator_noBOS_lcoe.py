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
    optFlag = False

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

    # Initialize OpenMDAO problem and FloatingSE Group
    if MPI:
        num_par_fd = MPI.COMM_WORLD.Get_size()
        prob = Problem(model=Group(num_par_fd=num_par_fd))
        prob.model.approx_totals(method='fd')
        prob.model.add_subsystem('comp',
                                 LandBasedTurbine(RefBlade=blade, Nsection_Tow=Nsection_Tow, VerbosityCosts=True),
                                 promotes=['*'])
    else:
        prob = Problem()
        prob.model = LandBasedTurbine(RefBlade=blade, Nsection_Tow=Nsection_Tow, VerbosityCosts=True)

    if optFlag:
        # --- Solver ---
        prob.driver = ScipyOptimizeDriver()
        prob.driver.options['optimizer'] = 'SLSQP'
        prob.driver.options['tol'] = 1.e-6
        prob.driver.options['maxiter'] = 100
        # ----------------------

        # --- Objective ---
        prob.model.add_objective('lcoe')
        # ----------------------

        # --- Design Variables ---
        indices_no_root = range(2, refBlade.NINPUT)
        indices_no_root_no_tip = range(2, refBlade.NINPUT - 1)
        prob.model.add_design_var('chord_in', indices=indices_no_root_no_tip, lower=0.5, upper=7.0)
        prob.model.add_design_var('theta_in', indices=indices_no_root, lower=-5.0, upper=20.0)
        prob.model.add_design_var('sparT_in', indices=indices_no_root_no_tip, lower=0.001, upper=0.200)
        prob.model.add_design_var('control_tsr', lower=6.000, upper=11.00)
        prob.model.add_design_var('tower_section_height', lower=5.0, upper=80.0)
        prob.model.add_design_var('tower_outer_diameter', lower=3.87, upper=30.0)
        prob.model.add_design_var('tower_wall_thickness', lower=4e-3, upper=2e-1)
        # ----------------------

        # --- Constraints ---
        # Rotor
        prob.model.add_constraint('tip_deflection_ratio', upper=1.0)
        # Tower
        prob.model.add_constraint('tow.height_constraint', lower=-1e-2, upper=1.e-2)
        prob.model.add_constraint('tow.post.stress', upper=1.0)
        prob.model.add_constraint('tow.post.global_buckling', upper=1.0)
        prob.model.add_constraint('tow.post.shell_buckling', upper=1.0)
        prob.model.add_constraint('tow.weldability', upper=0.0)
        prob.model.add_constraint('tow.manufacturability', lower=0.0)
        prob.model.add_constraint('frequencyNP_margin', upper=0.)
        prob.model.add_constraint('frequency1P_margin', upper=0.)
        prob.model.add_constraint('ground_clearance', lower=20.0)
        # ----------------------

        # --- Recorder ---
        prob.driver.add_recorder(SqliteRecorder('log_opt.sql'))
        prob.driver.recording_options['includes'] = ['AEP', 'rc.total_blade_cost', 'lcoe', 'tip_deflection_ratio']
        prob.driver.recording_options['record_objectives'] = True
        prob.driver.recording_options['record_constraints'] = True
        prob.driver.recording_options['record_desvars'] = True
        # ----------------------

    prob.setup(check=True)

    prob = Init_LandBasedAssembly(prob, blade, Nsection_Tow)
    prob.model.nonlinear_solver = NonlinearRunOnce()
    prob.model.linear_solver = DirectSolver()

    if not MPI:
        prob.model.approx_totals()

    prob.run_driver()
