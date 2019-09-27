import openmdao.api as om

# incomplete_input_dict['construct_duration'] = project['Total project construction time (months)']
# incomplete_input_dict['hub_height_meters'] = project['Hub height m']
# incomplete_input_dict['rotor_diameter_m'] = project['Rotor diameter m']
# incomplete_input_dict['wind_shear_exponent'] = project['Wind shear exponent']
# incomplete_input_dict['turbine_rating_MW'] = project['Turbine rating MW']
# incomplete_input_dict['breakpoint_between_base_and_topping_percent'] = \
#     project['Breakpoint between base and topping (percent)']
# incomplete_input_dict['fuel_usd_per_gal'] = project['Fuel cost USD per gal']
# incomplete_input_dict['rate_of_deliveries'] = project['Rate of deliveries (turbines per week)']
# incomplete_input_dict['turbine_spacing_rotor_diameters'] = project['Turbine spacing (times rotor diameter)']
# incomplete_input_dict['depth'] = project['Foundation depth m']
# incomplete_input_dict['rated_thrust_N'] = project['Rated Thrust (N)']
# incomplete_input_dict['bearing_pressure_n_m2'] = project['Bearing Pressure (n/m2)']
# incomplete_input_dict['gust_velocity_m_per_s'] = project['50-year Gust Velocity (m/s)']
# incomplete_input_dict['project_size_megawatts'] = project['Number of turbines'] * project['Turbine rating MW']

# incomplete_input_dict['road_length_adder_m'] = project['Road length adder (m)']
# incomplete_input_dict['fraction_new_roads'] = project['Percent of roads that will be constructed']
# incomplete_input_dict['road_quality'] = project['Road Quality (0-1)']
# incomplete_input_dict['site_prep_area_m2'] = project['Site prep area for Distributed wind (m2)']
# if project['Calculate road cost for distributed wind? (y/n)'] == 'y':
#     incomplete_input_dict['road_distributed_wind'] = True
# else:
#     incomplete_input_dict['road_distributed_wind'] = False


# incomplete_input_dict['cable_specs_pd'] = pd.read_excel(input_xlsx, 'cable_specs')
# incomplete_input_dict['line_frequency_hz'] = project['Line Frequency (Hz)']
# incomplete_input_dict['plant_capacity_MW'] = project['Turbine rating MW'] * project['Number of turbines']
# incomplete_input_dict['row_spacing_rotor_diameters'] = project['Row spacing (times rotor diameter)']
# incomplete_input_dict['user_defined_distance_to_grid_connection'] = project['Flag for user-defined home run trench length (0 = no; 1 = yes)']
# incomplete_input_dict['distance_to_grid_connection_km'] = project['Combined Homerun Trench Length to Substation (km)']
# incomplete_input_dict['crew'] = incomplete_input_dict['project_data']['crew']
# incomplete_input_dict['crew_cost'] = incomplete_input_dict['project_data']['crew_price']

# #read in RSMeans per diem:
# crew_cost = incomplete_input_dict['project_data']['crew_price']
# crew_cost = crew_cost.set_index("Labor type ID", drop=False)
# incomplete_input_dict['rsmeans_per_diem'] = crew_cost.loc['RSMeans', 'Per diem USD per day']

# incomplete_input_dict['fuel_cost_usd_per_gal'] = project['Fuel cost USD per gal']

# incomplete_input_dict['cable_specs_pd'] = pd.read_excel(input_xlsx, 'cable_specs')
# incomplete_input_dict['line_frequency_hz'] = project['Line Frequency (Hz)']
# incomplete_input_dict['plant_capacity_MW'] = project['Turbine rating MW'] * project['Number of turbines']
# incomplete_input_dict['row_spacing_rotor_diameters'] = project['Row spacing (times rotor diameter)']
# incomplete_input_dict['user_defined_home_run_trench'] = project[
#     'Flag for user-defined home run trench length (0 = no; 1 = yes)']
# incomplete_input_dict['trench_len_to_substation_km'] = project[
#     'Combined Homerun Trench Length to Substation (km)']

# # Add inputs for transmission & Substation modules:
# incomplete_input_dict['distance_to_interconnect_mi'] = project['Distance to interconnect (miles)']
# incomplete_input_dict['interconnect_voltage_kV'] = project['Interconnect Voltage (kV)']
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

class OpenMDAOComponent(om.ExplicitComponent):
    def non_numeric_inputs(self):
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

    def setup(self):
        self.add_output('construct_duration', units='m/s', desc='Total project construction time (months)')

        self.add_output('hub_height_meters', units='m', 'Hub height m')
        # incomplete_input_dict['hub_height_meters'] = project['Hub height m']

        self.add_output('rotor_diameter_m', units='m', desc='Rotor diameter m')
        # incomplete_input_dict['rotor_diameter_m'] = project['Rotor diameter m']

        self.add_output('wind_shear_exponent', units='m', desc='Wind shear exponent')
        # incomplete_input_dict['wind_shear_exponent'] = project['Wind shear exponent']

        self.add_output('turbine_rating_MW', units='m', desc='Turbine rating MW')
        # incomplete_input_dict['turbine_rating_MW'] = project['Turbine rating MW']

        self.add_output('breakpoint_between_base_and_topping_percent', units='m', desc='Breakpoint between base and topping (percent)')
        # incomplete_input_dict['breakpoint_between_base_and_topping_percent'] = \
        #     project['Breakpoint between base and topping (percent)']

        self.add_output('fuel_usd_per_gal', units='m', desc='Fuel cost USD per gal')
        # incomplete_input_dict['fuel_usd_per_gal'] = project['Fuel cost USD per gal']

        self.add_output('rate_of_deliveries', units='turbines/week', desc='Rate of deliveries (turbines per week)')
        # incomplete_input_dict['rate_of_deliveries'] = project['Rate of deliveries (turbines per week)']
        
        self.add_output('turbine_spacing_rotor_diameters', units='rotor diameters', desc='Turbine spacing (times rotor diameter)')
        # incomplete_input_dict['turbine_spacing_rotor_diameters'] = project['Turbine spacing (times rotor diameter)']

        self.add_output('depth', units='m', desc='Foundation depth m')
        # incomplete_input_dict['depth'] = project['Foundation depth m']

        self.add_output('rated_thrust_N', units='N', desc='Rated Thrust (N)')
        # incomplete_input_dict['rated_thrust_N'] = project['Rated Thrust (N)']

        self.add_output('bearing_pressure_n_m2', units='n/m2', desc='Bearing Pressure (n/m2)')
        # incomplete_input_dict['bearing_pressure_n_m2'] = project['Bearing Pressure (n/m2)']

        self.add_output('gust_velocity_m_per_s', units='m/s', desc='50-year Gust Velocity (m/s)')
        # incomplete_input_dict['gust_velocity_m_per_s'] = project['50-year Gust Velocity (m/s)']

        self.add_output('project_size_megawatts', units='MW', desc='(Number of turbines) * (Turbine rating MW)')
        # incomplete_input_dict['project_size_megawatts'] = project['Number of turbines'] * project['Turbine rating MW']

        self.add_output('road_length_adder_m', units='m', desc='Road length adder (m)')
        # incomplete_input_dict['road_length_adder_m'] = project['Road length adder (m)']

        self.add_output('fraction_new_roads', units='percent', desc='Percent of roads that will be constructed')
        # incomplete_input_dict['fraction_new_roads'] = project['Percent of roads that will be constructed']

        self.add_output('road_quality', units='binary', desc='Road Quality (0-1)')
        # incomplete_input_dict['road_quality'] = project['Road Quality (0-1)']

        self.add_output('site_prep_area_m2', units='m2', desc='Site prep area for Distributed wind (m2)')
        # incomplete_input_dict['site_prep_area_m2'] = project['Site prep area for Distributed wind (m2)']

        self.add_output('line_frequency_hz', units='Hz', desc='Line Frequency (Hz)')
        # incomplete_input_dict['line_frequency_hz'] = project['Line Frequency (Hz)']

        self.add_output('plant_capacity_MW', units='MW', desc='(Turbine rating MW) * (Number of turbines)')
        # incomplete_input_dict['plant_capacity_MW'] = project['Turbine rating MW'] * project['Number of turbines']

        self.add_output('row_spacing_rotor_diameters', units='row_spacing_rotor_diameters', desc='Row spacing (times rotor diameter)')
        # incomplete_input_dict['row_spacing_rotor_diameters'] = project['Row spacing (times rotor diameter)']
        
        self.add_output('user_defined_distance_to_grid_connection', units='binary', desc='Flag for user-defined home run trench length (0 = no; 1 = yes)')
        # incomplete_input_dict['user_defined_distance_to_grid_connection'] = project['Flag for user-defined home run trench length (0 = no; 1 = yes)']

        self.add_output('distance_to_grid_connection_km', units='km', desc='Combined Homerun Trench Length to Substation (km)')
        # incomplete_input_dict['distance_to_grid_connection_km'] = project['Combined Homerun Trench Length to Substation (km)']

        self.add_output('fuel_cost_usd_per_gal', units='gal', desc='Fuel cost USD per gal')
        # incomplete_input_dict['fuel_cost_usd_per_gal'] = project['Fuel cost USD per gal']

        self.add_output('user_defined_home_run_trench', units='binary', desc='Flag for user-defined home run trench length (0 = no; 1 = yes)')
        # incomplete_input_dict['user_defined_home_run_trench'] = project[
        #     'Flag for user-defined home run trench length (0 = no; 1 = yes)']

        self.add_output('trench_len_to_substation_km', units='km', desc='Combined Homerun Trench Length to Substation (km)')
        # incomplete_input_dict['trench_len_to_substation_km'] = project[
        #     'Combined Homerun Trench Length to Substation (km)']

        # Add inputs for transmission & Substation modules:

        self.add_output()
        incomplete_input_dict['distance_to_interconnect_mi'] = project['Distance to interconnect (miles)']
        incomplete_input_dict['interconnect_voltage_kV'] = project['Interconnect Voltage (kV)']
        new_switchyard = True
        if project['New Switchyard (y/n)'] == 'y':
            new_switchyard = True
        else:
            new_switchyard = False
        incomplete_input_dict['new_switchyard'] = new_switchyard

        incomplete_input_dict['critical_speed_non_erection_wind_delays_m_per_s'] = project['Non-Erection Wind Delay Critical Speed (m/s)']
        incomplete_input_dict['critical_height_non_erection_wind_delays_m'] = project['Non-Erection Wind Delay Critical Height (m)']

        incomplete_input_dict['road_width_ft'] = project['Road width (ft)']
        incomplete_input_dict['road_thickness'] = project['Road thickness (in)']
        incomplete_input_dict['crane_width'] = project['Crane width (m)']
        incomplete_input_dict['num_hwy_permits'] = project['Number of highway permits']
        incomplete_input_dict['num_access_roads'] = project['Number of access roads']
        incomplete_input_dict['overtime_multiplier'] = project['Overtime multiplier']
        incomplete_input_dict['allow_same_flag'] = True if project['Allow same flag'] == 'y' else False

        override_total_mgmt_cost_col_name = 'Override total management cost for distributed (0 does not override)'
        if override_total_mgmt_cost_col_name in project and project[override_total_mgmt_cost_col_name] > 0:
            incomplete_input_dict['override_total_management_cost'] = \
                project[override_total_mgmt_cost_col_name]
        else:
            incomplete_input_dict['markup_contingency'] = project['Markup contingency']
            incomplete_input_dict['markup_warranty_management'] = project['Markup warranty management']
            incomplete_input_dict['markup_sales_and_use_tax'] = project['Markup sales and use tax']
            incomplete_input_dict['markup_overhead'] = project['Markup overhead']
            incomplete_input_dict['markup_profit_margin'] = project['Markup profit margin']

        #Read development tab:
        incomplete_input_dict['development_df'] = pd.read_excel(input_xlsx, 'development')

        self.add_output('total_cost_summed_erection', 0.0, units='m/s', desc='Air velocity at rotor exit plane')

    def compute(self):
        pass
