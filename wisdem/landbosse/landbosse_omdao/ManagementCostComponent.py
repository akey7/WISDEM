import openmdao.api as om


class ManagementComponent(om.ExplicitComponent):
    def setup(self):
        self.add_output('insurance', units='USD', desc='Insurance cost', val=1.0)
        self.add_output('construction_permitting', units='USD', desc='Construction permitting', val=1.0)
        self.add_output('project_management', units='USD', desc='Project management', val=1.0)
        self.add_output('bonding', units='USD', desc='bonding', val=1.0)
        self.add_output('engineering_foundations_and_collections_sys', units='USD', val=1.0)
        self.add_output('site_security', units='USD', val=1.0)
        self.add_output('site_facility', units='USD', val=1.0)
        self.add_output('markup_contingency', units='USD', val=1.0)
        self.add_output('management_total_cost', units='USD', val=1.0)

    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):
        outputs['management_total_cost'] = 200
        print('################################################')
        print(f"Dummy {outputs['landbosse_foo']}")
        print('################################################')