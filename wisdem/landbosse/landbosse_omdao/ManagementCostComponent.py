import openmdao.api as om
from wisdem.landbosse.model import ManagementCost


class ManagementComponent(om.ExplicitComponent):
    def setup(self):
        # Inputs
        self.add_discrete_input('site_facility_building_area',
                                val=None,
                                desc='pd.DataFrame: Site facility building area.')
        self.add_input('project_value_usd', val=1.0, units='USD', desc='Project value, USD')
        self.add_input('foundation_cost_usd', val=1.0, units='USD', desc='Foundation cost')
        self.add_input('construct_duration', val=1.0, desc='Construct duration in months')
        self.add_input('num_hwy_permits', val=1.0, desc='Number of highway permits')
        self.add_input('num_turbines', val=1.0, desc='Number of turbines in project')
        self.add_input('project_size_megawatts', units='MW', desc='Project size in megawatts')
        self.add_input('hub_height_meters', val=1.0, units='m', desc='Hub height in meters')
        self.add_input('num_access_roads', val=1.0, desc='Number of access roads')
        self.add_input('markup_contingency', val=1.0, desc='Markup contingency')
        self.add_input('markup_warranty_management', val=1.0, desc='Markup for warranty management')
        self.add_input('markup_sales_and_use_tax', val=1.0, desc='Markup for sales and use tax')
        self.add_input('markup_overhead', val=1.0, desc='markup_profit_margin')

        # Outputs
        self.add_output('insurance', units='USD', desc='Insurance cost', val=1.0)
        self.add_output('construction_permitting', units='USD', desc='Construction permitting', val=1.0)
        self.add_output('project_management', units='USD', desc='Project management', val=1.0)
        self.add_output('bonding', units='USD', desc='bonding', val=1.0)
        self.add_output('engineering_foundations_and_collections_sys', units='USD', val=1.0)
        self.add_output('site_security', units='USD', val=1.0)
        self.add_output('site_facility', units='USD', val=1.0)
        self.add_output('management_total_cost', units='USD', val=1.0)

    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):
        # Note: inputs, outputs, discrete_inputs and discrete_outputs are not dictionaries
        # though they are accessible with [] brackets and have a keys() method.
        management_cost_continuous_input_dict = {str(key): inputs[str(key)] for key in inputs.keys()}
        management_cost_discrete_input_dict = {key: discrete_inputs[key] for key in discrete_inputs.keys()}
        management_cost_input_dict = {**management_cost_continuous_input_dict, **management_cost_discrete_input_dict}
        management_cost_output_dict = dict()
        project_name = 'WISDEM LandBOSSE'
        management_cost = ManagementCost(management_cost_input_dict, management_cost_output_dict, project_name)
        outputs['management_total_cost'] = 200
        print('################################################')
        print(f"management_total_cost {outputs['management_total_cost']}")
        print('################################################')