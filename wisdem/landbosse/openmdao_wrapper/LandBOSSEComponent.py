import openmdao.api as om

class LandBOSSEComponent(om.ExplicitComponent):
    def setup(self):
        # Numeric inputs
        self.add_input('construct_duration', units='m/s', desc='Total project construction time (months)', value=9)
        self.add_input('hub_height_meters', units='m', desc='Hub height m', value=80)
        self.add_input('rotor_diameter_m', units='m', desc='Rotor diameter m', value=77)
        self.add_input('wind_shear_exponent', units='m', desc='Wind shear exponent', value=0.2)
        self.add_input('turbine_rating_MW', units='m', desc='Turbine rating MW', value=1.5)
        self.add_input('breakpoint_between_base_and_topping_percent', units='m', desc='Breakpoint between base and topping (percent)', value=0.7)
        self.add_input('fuel_usd_per_gal', units='m', desc='Fuel cost USD per gal', value=1.5)
        self.add_input('rate_of_deliveries', units='turbines/week', desc='Rate of deliveries (turbines per week)', value=10)
        self.add_input('turbine_spacing_rotor_diameters', units='rotor diameters', desc='Turbine spacing (times rotor diameter)', value=4)
        self.add_input('depth', units='m', desc='Foundation depth m', value=2.36)
        self.add_input('rated_thrust_N', units='N', desc='Rated Thrust (N)', value=5.89e5)
        self.add_input('bearing_pressure_n_m2', units='n/m2', desc='Bearing Pressure (n/m2)', value=191521)
        self.add_input('gust_velocity_m_per_s', units='m/s', desc='50-year Gust Velocity (m/s)', value=59.5)
        self.add_input('road_length_adder_m', units='m', desc='Road length adder (m)', value=5000)
        self.add_input('fraction_new_roads', units='fraction', desc='Percent of roads that will be constructed (0.0 - 1.0)', value=0.33)
        self.add_input('road_quality', units='none', desc='Road Quality (0-1)', value=0.6)
        self.add_input('line_frequency_hz', units='Hz', desc='Line Frequency (Hz)', value=60)
        self.add_input('row_spacing_rotor_diameters', units='row_spacing_rotor_diameters', desc='Row spacing (times rotor diameter)', value=4)      
        
        self.add_input(
            'user_defined_distance_to_grid_connection',
            units='boolean', 
            desc='Flag for user-defined home run trench length (True or False)',
            value=False
        )

        self.add_input('trench_len_to_substation_km', units='km', desc='Combined Homerun Trench Length to Substation (km)', value=50)
        self.add_input('distance_to_interconnect_mi', units='mi', desc='Distance to interconnect (miles)', value=5)
        self.add_input('interconnect_voltage_kV', units='kV', desc='Interconnect Voltage (kV)', value=130)
        self.add_input('new_switchyard', units='boolean', desc='New Switchyard (True or False)', value=True)
        self.add_input('critical_speed_non_erection_wind_delays_m_per_s', units='m/s', desc='Non-Erection Wind Delay Critical Speed (m/s)', value=15)
        self.add_input('critical_height_non_erection_wind_delays_m', units='m/s', desc='Non-Erection Wind Delay Critical Height (m)', value=10)
        self.add_input('road_width_ft', units='ft', desc='Road width (ft)', value=20)
        self.add_input('road_thickness', units='in', desc='Road thickness (in)', value=8)
        self.add_input('crane_width', units='m', desc='Crane width (m)', value=12.2)
        self.add_input('num_hwy_permits', units='none', desc='Number of highway permits', value=10)
        self.add_input('num_access_roads', units='none', desc='Number of access roads', value=2)
        self.add_input('overtime_multiplier', units='none', desc='Overtime multiplier', value=1.4)
        
        self.add_input(
            'allow_same_flag',
            units='boolean', 
            desc='Allow same crane for base and topping (True or False)',
            value=False
        )

        # Dropping the column 'Override total management cost for distributed (0 does not override)'

        self.add_input('markup_contingency', units='USD', desc='Markup contingency', value=0.03)
        self.add_input('markup_warranty_management', units='USD', desc='Markup warranty management', value=0.0002)
        self.add_input('markup_sales_and_use_tax', units='USD', desc='Markup sales and use tax', value=0)
        self.add_input('markup_overhead', units='USD', desc='Markup overhead', value=0.05)
        self.add_input('markup_profit_margin', units='USD', desc='Markup profit margin', value=0.05)

        # Numeric outputs
        # self.add_output('total_cost_summed_erection', 0.0, units='m/s', desc='Air velocity at rotor exit plane')
        self.add_output('dummy_output', 1.0, units='dummy', desc='dummy')

    # Calculate this input instead
    # self.add_input('project_size_megawatts', units='MW', desc='(Number of turbines) * (Turbine rating MW)', value=)

    @staticmethod
    def non_numeric_inputs(cls):
        pass
        # if project['Calculate road cost for distributed wind? (y/n)'] == 'y':
        #     incomplete_input_dict['road_distributed_wind'] = True
        # else:
        #     incomplete_input_dict['road_distributed_wind'] = False
        #
        # incomplete_input_dict['cable_specs_pd'] = pd.read_excel(input_xlsx, 'cable_specs')
        # incomplete_input_dict['crew'] = incomplete_input_dict['project_data']['crew']
        # incomplete_input_dict['crew_cost'] = incomplete_input_dict['project_data']['crew_price']

        # #read in RSMeans per diem:
        # crew_cost = incomplete_input_dict['project_data']['crew_price']
        # crew_cost = crew_cost.set_index("Labor type ID", drop=False)
        # incomplete_input_dict['rsmeans_per_diem'] = crew_cost.loc['RSMeans', 'Per diem USD per day']
        # incomplete_input_dict['cable_specs_pd'] = pd.read_excel(input_xlsx, 'cable_specs')

        # #Read development tab:
        # incomplete_input_dict['development_df'] = pd.read_excel(input_xlsx, 'development')

        # Set the list and dictionary values on the master dictionary
        # self.default_input_dict['season_construct'] = ['spring', 'summer', 'fall']
        # self.default_input_dict['time_construct'] = 'normal'
        # self.default_input_dict['hour_day'] = {'long': 24, 'normal': 10}
        # self.default_input_dict['operational_construction_time'] = self.default_input_dict['hour_day'][
        #     self.default_input_dict['time_construct']]

    def compute(self):
        pass
