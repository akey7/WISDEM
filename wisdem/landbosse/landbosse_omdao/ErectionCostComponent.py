from .LandBOSSEComponent import LandBOSSEComponent
from wisdem.landbosse.model import ErectionCost

class ErectionCostComopnent(LandBOSSEComponent):
    """
    This class is an OpenMDAO wrapper around the ErectionCost component.
    """

    def setup(self):
        # Inputs, continuous
        self.add_input('num_turbines', val=1, desc='Number of turbines in project')
        self.add_input('hub_height_meters', val=1.0, units='m', desc='Hub height in meters')
        self.add_input('rotor_diameter_m', val=1.0, units='m', desc='Rotor diameter in m')
        self.add_input('overtime_multiplier', val=1.0, desc='Multiplier for overtime labor rates')
        self.add_input('fuel_cost_usd_per_gal', val=1.0, desc='Fuel cost USD/gal')

        self.add_input('turbine_spacing_rotor_diameters',
                       val=1.0,
                       units='m',
                       desc='Turbine spacing in rotor diameters')

        self.add_input('operational_construction_time',
                       val=1.0,
                       units='hours',
                       desc='Number of hours each day for construction.')
        #
        # Inputs, discrete, dataframes
        self.add_discrete_input('components', desc='Dataframe of components for tower, blade, nacelle')
        self.add_discrete_input('crane_specs', desc='Dataframe of specifications of cranes')
        self.add_discrete_input('weather_window', desc='Dataframe of wind toolkit data')
        self.add_discrete_input('crew', desc='Dataframe of crew configurations')
        self.add_discrete_input('crew_price', desc='Dataframe of costs per hour for each type of worker.')
        #
        # # Inputs, discrete, non dataframes
        self.add_discrete_input('allow_same_flag',
                                desc='True if the same crane can be used for base and topping, False otherwise')
        self.add_discrete_input('hour_day',
                                desc="Dictionary of normal and long hours for construction in a day in the form of {'long': 24, 'normal': 10}")

        # Outputs, continuous
        self.add_output('erection_wind_mult', val=1.0, desc='Wind multiplier for erection operations')
        self.add_output('total_cost_summed_erection', val=1.0, units='usd', desc='Sum of all erection costs')

        # Outputs, discrete, non dataframes
        self.add_discrete_output('erection_module_type_operation',
                                 desc='List of dictionaries with costs by module, type and operation')
        self.add_discrete_output('erection_cost_csv', desc='List of dictionaries with details about erection costs')

        # Outputs, discrete, dataframes
        self.add_discrete_output('total_erection_cost', desc='Dataframe of total erection costs')
        self.add_discrete_output('crane_data_output', desc='Costs and times for each crane-boom-operation combination')
        self.add_discrete_output('crane_cost_details', desc='Costs for each crane-boom-operation')
        self.add_discrete_output('management_crews_cost', desc='Costs for each type of labor of each management crew')
        self.add_discrete_output('management_crews_cost_grouped',
                                 desc='Costs for labor grouped by management crew type')
        self.add_discrete_output('component_name_topvbase',
                                 desc='Dataframe with eac component and whether that component is a topping or a base operation.')
        self.add_discrete_output('possible_cranes',
                                 desc='Dataframe of all cranes/booms capable of lifting all components during a particular operation.')
        self.add_discrete_output('crane_specs_with_offload',
                                 desc='Operation times for each possible base or topping crane')
        self.add_discrete_output('separate_topbase_crane_cost',
                                 desc='Dataframe of crane costs where base and topping are separate operations')
        self.add_discrete_output('topbase_same_crane_cost',
                                 desc='Dataframe of crane costs where Base+Top is one operation')

        # This output is particularly important.
        self.add_discrete_output('crane_choice', desc='The cranes ultimately selected for offload, base and top.')

    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):
        """
        Note: inputs, discrete_inputs are not dictionaries. They do support
        [] notation. inputs is of class 'openmdao.vectors.default_vector.DefaultVector'
        discrete_inputs is of class openmdao.core.component._DictValues. Other than
        [] brackets, they do not behave like dictionaries. See the following
        documentation for details.

        http://openmdao.org/twodocs/versions/latest/_srcdocs/packages/vectors/default_vector.html
        https://mdolab.github.io/OpenAeroStruct/_modules/openmdao/core/component.html

        Parameters
        ----------
        inputs : openmdao.vectors.default_vector.DefaultVector
            A dictionary-like object with NumPy arrays that hold float
            inputs. Note that since these are NumPy arrays, they
            need indexing to pull out simple float64 values.

        outputs : openmdao.vectors.default_vector.DefaultVector
            A dictionary-like object to store outputs.

        discrete_inputs : openmdao.core.component._DictValues
            A dictionary-like with the non-numeric inputs (like
            pandas.DataFrame)

        discrete_outputs : openmdao.core.component._DictValues
            A dictionary-like for non-numeric outputs (like
            pandas.DataFrame)
        """
        # Create real dictionaries to pass to the module
        inputs_dict = {key: inputs[key][0] for key in inputs.keys()}
        discrete_inputs_dict = {key: value for key, value in discrete_inputs.items()}
        master_inputs_dict = {**inputs_dict, **discrete_inputs_dict}
        master_outputs_dict = dict()
        module = ErectionCost(master_inputs_dict, master_outputs_dict, 'WISDEM')
        module.run_module()

        # Copy the numeric outputs into the outputs object
        for key in outputs.keys():
            outputs[key] = master_outputs_dict[key]

        # Copy the discrete outputs into their object
        discrete_outputs['erection_cost_details'] = master_outputs_dict['erection_cost_csv']
        discrete_outputs['erection_module_type_operation'] = master_outputs_dict['erection_module_type_operation']

        # Log the outputs if needed
        if self.options['verbosity']:
            self.print_verbose_module_type_operation('ErectionCost',
                                                     master_outputs_dict['mangement_module_type_operation'])