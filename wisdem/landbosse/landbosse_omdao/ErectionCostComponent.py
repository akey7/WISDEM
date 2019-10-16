from .LandBOSSEComponent import LandBOSSEComponent
from wisdem.landbosse.model import ErectionCost

class ErectionCostComopnent(LandBOSSEComponent):
    """
    This class is an OpenMDAO wrapper around the ErectionCost component.
    """

    def setup(self):
        # Inputs, continuous
        self.add_input('num_turbines', val=1.0, desc='Number of turbines in project')
        self.add_input('hub_height_meters', val=1.0, units='m', desc='Hub height in meters')
        self.add_input('rotor_diameter_m', val=1.0, units='m', desc='Rotor diameter in m')
        self.add_input('overtime_multiplier', val=1.0, desc='Multiplier for overtime labor rates')
        self.add_input('fuel_cost_usd_per_gal', val=1.0, units='usd/galUS', desc='Fuel cost USD/gal')

        self.add_input('turbine_spacing_rotor_diameters',
                       val=1.0,
                       units='m',
                       desc='Turbine spacing in rotor diameters')

        self.add_input('operational_construction_time',
                       val=1.0,
                       units='hours',
                       desc='Number of hours each day for construction.')

        # Inputs, discrete, dataframes
        self.add_discrete_input('components', desc='Dataframe of components for tower, blade, nacelle')
        self.add_discrete_input('crane_specs', desc='Dataframe of specifications of cranes')
        self.add_discrete_input('weather_window', desc='Dataframe of wind toolkit data')
        self.add_discrete_input('crew', desc='Dataframe of crew configurations')
        self.add_discrete_input('crew_price', desc='Dataframe of costs per hour for each type of worker.')

        # Inputs, discrete, non dataframes
        self.add_discrete_input('allow_same_flag',
                                desc='True if the same crane can be used for base and topping, False otherwise')
        self.add_discrete_input('hour_day',
                                desc="Dictionary of normal and long hours for construction in a day in the form of {'long': 24, 'normal': 10}")

        # Outputs, continuous

        # Outputs, discrete
