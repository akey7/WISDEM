import openmdao.api as om

from .DummyComponent import DummyComponent
from .ManagementCostComponent import ManagementComponent

class LandBOSSEGroup(om.Group):
    def initialize(self):
        self.options.declare('top_level_flag', default=True)

    def setup(self):
        # if self.options['top_level_flag']:
        #     shared_indeps = om.IndepVarComp()
        #     shared_indeps.add_output('hub_height', val=0.0, units='m')
        #     self.add_subsystem('indeps', shared_indeps, promotes=['*'])

        # Numeric inputs
        indeps = self.add_subsystem('indeps', om.IndepVarComp(), promotes=['*'])
        indeps.add_output('construct_duration', desc='Total project construction time (months)', val=9)
        indeps.add_output('hub_height_meters', units='m', desc='Hub height m', val=80)
        indeps.add_output('rotor_diameter_m', units='m', desc='Rotor diameter m', val=77)
        indeps.add_output('wind_shear_exponent', units='m', desc='Wind shear exponent', val=0.2)
        indeps.add_output('turbine_rating_MW', units='MW', desc='Turbine rating MW', val=1.5)
        indeps.add_output('breakpoint_between_base_and_topping_percent', units='m', desc='Breakpoint between base and topping (percent)', val=0.7)
        indeps.add_output('fuel_usd_per_gal', units='m', desc='Fuel cost USD per gal', val=1.5)

        # Could not place units in rate_of_deliveries
        # indeps.add_output('rate_of_deliveries', units='turb/wk', desc='Rate of deliveries (turbines per week)', val=10)
        indeps.add_output('rate_of_deliveries', desc='Rate of deliveries (turbines per week)', val=10)

        # Could not place units in turbine_spacing_rotor_diameters
        # indeps.add_output('turbine_spacing_rotor_diameters', units='rotor diameters', desc='Turbine spacing (times rotor diameter)', val=4)
        indeps.add_output('turbine_spacing_rotor_diameters', desc='Turbine spacing (times rotor diameter)', val=4)

        indeps.add_output('depth', units='m', desc='Foundation depth m', val=2.36)
        indeps.add_output('rated_thrust_N', units='N', desc='Rated Thrust (N)', val=5.89e5)

        # Can't set units
        # indeps.add_output('bearing_pressure_n_m2', units='n/m2', desc='Bearing Pressure (n/m2)', val=191521)
        indeps.add_output('bearing_pressure_n_m2', desc='Bearing Pressure (n/m2)', val=191521)

        indeps.add_output('gust_velocity_m_per_s', units='m/s', desc='50-year Gust Velocity (m/s)', val=59.5)
        indeps.add_output('road_length_adder_m', units='m', desc='Road length adder (m)', val=5000)

        # Can't set units
        # indeps.add_output('fraction_new_roads', units='fraction', desc='Percent of roads that will be constructed (0.0 - 1.0)', val=0.33)
        indeps.add_output('fraction_new_roads',
                          desc='Percent of roads that will be constructed (0.0 - 1.0)', val=0.33)

        indeps.add_output('road_quality', desc='Road Quality (0-1)', val=0.6)
        indeps.add_output('line_frequency_hz', units='Hz', desc='Line Frequency (Hz)', val=60)

        # Can't set units
        # indeps.add_output('row_spacing_rotor_diameters', units='row_spacing_rotor_diameters', desc='Row spacing (times rotor diameter)', val=4)
        indeps.add_output('row_spacing_rotor_diameters',
                          desc='Row spacing (times rotor diameter)', val=4)

        indeps.add_output(
            'user_defined_distance_to_grid_connection',
            desc='Flag for user-defined home run trench length (True or False)',
            val=False
        )

        indeps.add_output('trench_len_to_substation_km', units='km', desc='Combined Homerun Trench Length to Substation (km)', val=50)
        indeps.add_output('distance_to_interconnect_mi', units='mi', desc='Distance to interconnect (miles)', val=5)
        indeps.add_output('interconnect_voltage_kV', units='kV', desc='Interconnect Voltage (kV)', val=130)

        indeps.add_output('new_switchyard', desc='New Switchyard (True or False)', val=True)


        indeps.add_output('critical_speed_non_erection_wind_delays_m_per_s', units='m/s', desc='Non-Erection Wind Delay Critical Speed (m/s)', val=15)
        indeps.add_output('critical_height_non_erection_wind_delays_m', units='m/s', desc='Non-Erection Wind Delay Critical Height (m)', val=10)
        indeps.add_output('road_width_ft', units='ft', desc='Road width (ft)', val=20)

        # Can't add units
        # indeps.add_output('road_thickness', units='in', desc='Road thickness (in)', val=8)
        indeps.add_output('road_thickness', desc='Road thickness (in)', val=8)

        indeps.add_output('crane_width', units='m', desc='Crane width (m)', val=12.2)
        indeps.add_output('num_hwy_permits', desc='Number of highway permits', val=10)
        indeps.add_output('num_access_roads', desc='Number of access roads', val=2)
        indeps.add_output('overtime_multiplier', desc='Overtime multiplier', val=1.4)

        indeps.add_output(
            'allow_same_flag',
            desc='Allow same crane for base and topping (True or False)',
            val=False
        )

        # Dropping the column 'Override total management cost for distributed (0 does not override)'

        indeps.add_output('markup_contingency', desc='Markup contingency', val=0.03)
        indeps.add_output('markup_warranty_management', desc='Markup warranty management', val=0.0002)
        indeps.add_output('markup_sales_and_use_tax', desc='Markup sales and use tax', val=0)
        indeps.add_output('markup_overhead', desc='Markup overhead', val=0.05)
        indeps.add_output('markup_profit_margin', desc='Markup profit margin', val=0.05)

        # Discrete inputs like dataframes
        indeps.add_discrete_output('site_facility_building_area_df', val=None, desc='site_facility_building_area DataFrame')

        # self.add_subsystem('dummy', DummyComponent(), promotes=['*'])

        self.add_subsystem('management_cost', ManagementComponent(), promotes=['*'])

# Calculate this input instead
# self.add_input('project_size_megawatts', units='MW', desc='(Number of turbines) * (Turbine rating MW)', value=)

