import openmdao.api as om

class LandBOSSEComponent(om.ExplicitComponent):
    def setup(self):
        self.add_input('construct_duration', units='m/s', desc='Total project construction time (months)')
        self.add_input('hub_height_meters', units='m', 'Hub height m')
        self.add_input('rotor_diameter_m', units='m', desc='Rotor diameter m')
        self.add_input('wind_shear_exponent', units='m', desc='Wind shear exponent')
        self.add_input('turbine_rating_MW', units='m', desc='Turbine rating MW')
        self.add_input('breakpoint_between_base_and_topping_percent', units='m', desc='Breakpoint between base and topping (percent)')
        self.add_input('fuel_usd_per_gal', units='m', desc='Fuel cost USD per gal')
        self.add_input('rate_of_deliveries', units='turbines/week', desc='Rate of deliveries (turbines per week)')
        self.add_input('turbine_spacing_rotor_diameters', units='rotor diameters', desc='Turbine spacing (times rotor diameter)')
        self.add_input('depth', units='m', desc='Foundation depth m')
        self.add_input('rated_thrust_N', units='N', desc='Rated Thrust (N)')
        self.add_input('bearing_pressure_n_m2', units='n/m2', desc='Bearing Pressure (n/m2)')
        self.add_input('gust_velocity_m_per_s', units='m/s', desc='50-year Gust Velocity (m/s)')
        self.add_input('project_size_megawatts', units='MW', desc='(Number of turbines) * (Turbine rating MW)')
        self.add_input('road_length_adder_m', units='m', desc='Road length adder (m)')
        self.add_input('fraction_new_roads', units='percent', desc='Percent of roads that will be constructed')
        self.add_input('road_quality', units='binary', desc='Road Quality (0-1)')
        self.add_input('site_prep_area_m2', units='m2', desc='Site prep area for Distributed wind (m2)')
        self.add_input('line_frequency_hz', units='Hz', desc='Line Frequency (Hz)')
        self.add_input('plant_capacity_MW', units='MW', desc='(Turbine rating MW) * (Number of turbines)')
        self.add_input('row_spacing_rotor_diameters', units='row_spacing_rotor_diameters', desc='Row spacing (times rotor diameter)')      
        self.add_input('user_defined_distance_to_grid_connection', units='binary', desc='Flag for user-defined home run trench length (0 = no; 1 = yes)')
        self.add_input('distance_to_grid_connection_km', units='km', desc='Combined Homerun Trench Length to Substation (km)')
        self.add_input('fuel_cost_usd_per_gal', units='gal', desc='Fuel cost USD per gal')
        self.add_input('user_defined_home_run_trench', units='binary', desc='Flag for user-defined home run trench length (0 = no; 1 = yes)')
        self.add_input('trench_len_to_substation_km', units='km', desc='Combined Homerun Trench Length to Substation (km)')
        self.add_input('distance_to_interconnect_mi', units='mi', desc='Distance to interconnect (miles)')
        self.add_input('interconnect_voltage_kV', units='kV', desc='Interconnect Voltage (kV)')

        # new_switchyard = True
        # if project['New Switchyard (y/n)'] == 'y':
        #     new_switchyard = True
        # else:
        #     new_switchyard = False
        # incomplete_input_dict['new_switchyard'] = new_switchyard

        # incomplete_input_dict['critical_speed_non_erection_wind_delays_m_per_s'] = project['Non-Erection Wind Delay Critical Speed (m/s)']
        # incomplete_input_dict['critical_height_non_erection_wind_delays_m'] = project['Non-Erection Wind Delay Critical Height (m)']

        # incomplete_input_dict['road_width_ft'] = project['Road width (ft)']
        # incomplete_input_dict['road_thickness'] = project['Road thickness (in)']
        # incomplete_input_dict['crane_width'] = project['Crane width (m)']
        # incomplete_input_dict['num_hwy_permits'] = project['Number of highway permits']
        # incomplete_input_dict['num_access_roads'] = project['Number of access roads']
        # incomplete_input_dict['overtime_multiplier'] = project['Overtime multiplier']
        # incomplete_input_dict['allow_same_flag'] = True if project['Allow same flag'] == 'y' else False

        # override_total_mgmt_cost_col_name = 'Override total management cost for distributed (0 does not override)'
        # if override_total_mgmt_cost_col_name in project and project[override_total_mgmt_cost_col_name] > 0:
        #     incomplete_input_dict['override_total_management_cost'] = \
        #         project[override_total_mgmt_cost_col_name]
        # else:
        #     incomplete_input_dict['markup_contingency'] = project['Markup contingency']
        #     incomplete_input_dict['markup_warranty_management'] = project['Markup warranty management']
        #     incomplete_input_dict['markup_sales_and_use_tax'] = project['Markup sales and use tax']
        #     incomplete_input_dict['markup_overhead'] = project['Markup overhead']
        #     incomplete_input_dict['markup_profit_margin'] = project['Markup profit margin']

        # #Read development tab:
        # incomplete_input_dict['development_df'] = pd.read_excel(input_xlsx, 'development')

        self.add_output('total_cost_summed_erection', 0.0, units='m/s', desc='Air velocity at rotor exit plane')

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

    def compute(self):
        pass
