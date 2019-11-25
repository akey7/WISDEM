from wisdem.ccblade import CCAirfoil, CCBlade as CCBlade
from openmdao.api import ExplicitComponent
import numpy as np

cosd = lambda x: np.cos(np.deg2rad(x))
sind = lambda x: np.sin(np.deg2rad(x))

class CCBladeGeometry(ExplicitComponent):
    def initialize(self):
        self.options.declare('NINPUT')
        
        
    def setup(self):
        NINPUT = self.options['NINPUT']
        
        self.add_input('Rtip', val=0.0, units='m', desc='tip radius')
        self.add_input('precurve_in', val=np.zeros(NINPUT), desc='prebend distribution', units='m')
        self.add_input('presweep_in', val=np.zeros(NINPUT), desc='presweep distribution', units='m')
        self.add_input('precone', val=0.0, desc='precone angle', units='deg')
        self.add_output('R', val=0.0, units='m', desc='rotor radius')
        self.add_output('diameter', val=0.0, units='m')
        self.add_output('precurveTip', val=0.0, units='m', desc='tip prebend')
        self.add_output('presweepTip', val=0.0, units='m', desc='tip sweep')
        
        #self.declare_partials('R', '*')
        #self.declare_partials('diameter', '*')
        #self.declare_partials('diameter', 'R')
        
    def compute(self, inputs, outputs):
        
        self.Rtip           = inputs['Rtip']
        self.precone        = inputs['precone']
        
        outputs['precurveTip']  = inputs['precurve_in'][-1]
        outputs['presweepTip']  = inputs['presweep_in'][-1]
        self.precurveTip        = outputs['precurveTip']
        self.R = self.Rtip*cosd(self.precone) + self.precurveTip*sind(self.precone)
        outputs['R']            = self.R
        outputs['diameter']     = self.R*2
        '''

    def compute_partials(self, inputs, J):

        J_sub = np.array([[cosd(self.precone), sind(self.precone),
            (-self.Rtip*sind(self.precone) + self.precurveTip*sind(self.precone))*np.pi/180.0]])

        J['R', 'Rtip'] = J_sub[0][0]
        J['R', 'precurveTip'] = J_sub[0][1]
        J['R', 'precone'] = J_sub[0][2]
        J['diameter', 'Rtip'] = 2.0*J_sub[0][0]
        J['diameter', 'precurveTip'] = 2.0*J_sub[0][1]
        J['diameter', 'precone'] = 2.0*J_sub[0][2]
        J['diameter', 'R'] = 2.0
        '''

        

class CCBladePower(ExplicitComponent):
    def initialize(self):
        self.options.declare('naero')
        self.options.declare('npower')

        self.options.declare('n_aoa_grid')
        self.options.declare('n_Re_grid')

        
    def setup(self):
        self.naero = naero = self.options['naero']
        npower = self.options['npower']
        n_aoa_grid = self.options['n_aoa_grid']
        n_Re_grid  = self.options['n_Re_grid']

        """blade element momentum code"""

        # inputs
        self.add_input('Uhub', val=np.zeros(npower), units='m/s', desc='hub height wind speed')
        self.add_input('Omega', val=np.zeros(npower), units='rpm', desc='rotor rotation speed')
        self.add_input('pitch', val=np.zeros(npower), units='deg', desc='blade pitch setting')

        # outputs
        self.add_output('T', val=np.zeros(npower), units='N', desc='rotor aerodynamic thrust')
        self.add_output('Q', val=np.zeros(npower), units='N*m', desc='rotor aerodynamic torque')
        self.add_output('P', val=np.zeros(npower), units='W', desc='rotor aerodynamic power')

        
        # (potential) variables
        self.add_input('r', val=np.zeros(naero), units='m', desc='radial locations where blade is defined (should be increasing and not go all the way to hub or tip)')
        self.add_input('chord', val=np.zeros(naero), units='m', desc='chord length at each section')
        self.add_input('theta', val=np.zeros(naero),  units='deg', desc='twist angle at each section (positive decreases angle of attack)')
        self.add_input('Rhub', val=0.0, units='m', desc='hub radius')
        self.add_input('Rtip', val=0.0, units='m', desc='tip radius')
        self.add_input('hub_height', val=0.0, units='m', desc='hub height')
        self.add_input('precone', val=0.0, desc='precone angle', units='deg')
        self.add_input('tilt', val=0.0, desc='shaft tilt', units='deg')
        self.add_input('yaw', val=0.0, desc='yaw error', units='deg')

        # TODO: I've not hooked up the gradients for these ones yet.
        self.add_input('precurve', val=np.zeros(naero), units='m', desc='precurve at each section')
        self.add_input('precurveTip', val=0.0, units='m', desc='precurve at tip')

        # parameters
        self.add_input('airfoils_cl', val=np.zeros((n_aoa_grid, naero, n_Re_grid)), desc='lift coefficients, spanwise')
        self.add_input('airfoils_cd', val=np.zeros((n_aoa_grid, naero, n_Re_grid)), desc='drag coefficients, spanwise')
        self.add_input('airfoils_cm', val=np.zeros((n_aoa_grid, naero, n_Re_grid)), desc='moment coefficients, spanwise')
        self.add_input('airfoils_aoa', val=np.zeros((n_aoa_grid)), units='deg', desc='angle of attack grid for polars')
        self.add_input('airfoils_Re', val=np.zeros((n_Re_grid)), desc='Reynolds numbers of polars')
        # self.add_discrete_input('airfoils', val=[0]*naero, desc='CCAirfoil instances')
        self.add_discrete_input('nBlades', val=0, desc='number of blades')
        self.add_input('rho', val=0.0, units='kg/m**3', desc='density of air')
        self.add_input('mu', val=0.0, units='kg/(m*s)', desc='dynamic viscosity of air')
        self.add_input('shearExp', val=0.0, desc='shear exponent')
        self.add_discrete_input('nSector', val=4, desc='number of sectors to divide rotor face into in computing thrust and power')
        self.add_discrete_input('tiploss', val=True, desc='include Prandtl tip loss model')
        self.add_discrete_input('hubloss', val=True, desc='include Prandtl hub loss model')
        self.add_discrete_input('wakerotation', val=True, desc='include effect of wake rotation (i.e., tangential induction factor is nonzero)')
        self.add_discrete_input('usecd', val=True, desc='use drag coefficient in computing induction factors')

        #self.declare_partials(['P', 'T', 'Q'],['precone', 'tilt', 'hub_height', 'Rhub', 'Rtip', 'yaw',
        #                                       'Uhub', 'Omega', 'pitch', 'r', 'chord', 'theta',
        #                                       'precurve', 'precurveTip'])

        
    def compute(self, inputs, outputs, discrete_inputs, discrete_outputs):

        self.r = inputs['r']
        self.chord = inputs['chord']
        self.theta = inputs['theta']
        self.Rhub = inputs['Rhub']
        self.Rtip = inputs['Rtip']
        self.hub_height = inputs['hub_height']
        self.precone = inputs['precone']
        self.tilt = inputs['tilt']
        self.yaw = inputs['yaw']
        self.precurve = inputs['precurve']
        self.precurveTip = inputs['precurveTip']
        # self.airfoils = discrete_inputs['airfoils']
        self.B = discrete_inputs['nBlades']
        self.rho = inputs['rho']
        self.mu = inputs['mu']
        self.shearExp = inputs['shearExp']
        self.nSector = discrete_inputs['nSector']
        self.tiploss = discrete_inputs['tiploss']
        self.hubloss = discrete_inputs['hubloss']
        self.wakerotation = discrete_inputs['wakerotation']
        self.usecd = discrete_inputs['usecd']
        self.Uhub = inputs['Uhub']
        self.Omega = inputs['Omega']
        self.pitch = inputs['pitch']

        af = [None]*self.naero
        for i in range(self.naero):
            af[i] = CCAirfoil(inputs['airfoils_aoa'], inputs['airfoils_Re'], inputs['airfoils_cl'][:,i,:], inputs['airfoils_cd'][:,i,:], inputs['airfoils_cm'][:,i,:])
        
        self.ccblade = CCBlade(self.r, self.chord, self.theta, af, self.Rhub, self.Rtip, self.B,
            self.rho, self.mu, self.precone, self.tilt, self.yaw, self.shearExp, self.hub_height,
            self.nSector, self.precurve, self.precurveTip, tiploss=self.tiploss, hubloss=self.hubloss,
            wakerotation=self.wakerotation, usecd=self.usecd, derivatives=True)

        # power, thrust, torque
        self.P, self.T, self.Q, self.M, self.dP, self.dT, self.dQ \
            = self.ccblade.evaluate(self.Uhub, self.Omega, self.pitch, coefficients=False)
        outputs['T'] = self.T
        outputs['Q'] = self.Q
        outputs['P'] = self.P
        '''

    def compute_partials(self, inputs, J, discrete_inputs):

        dP = self.dP
        dT = self.dT
        dQ = self.dQ
        
        J['P', 'precone']     = dP['dprecone']
        J['P', 'tilt']        = dP['dtilt']
        J['P', 'hub_height']  = dP['dhubHt']
        J['P', 'Rhub']        = dP['dRhub']
        J['P', 'Rtip']        = dP['dRtip']
        J['P', 'yaw']         = dP['dyaw']
        J['P', 'Uhub']        = dP['dUinf']
        J['P', 'Omega']       = dP['dOmega']
        J['P', 'pitch']       = dP['dpitch']
        J['P', 'r']           = dP['dr']
        J['P', 'chord']       = dP['dchord']
        J['P', 'theta']       = dP['dtheta']
        J['P', 'precurve']    = dP['dprecurve']
        J['P', 'precurveTip'] = dP['dprecurveTip']

        J['T', 'precone']     = dT['dprecone']
        J['T', 'tilt']        = dT['dtilt']
        J['T', 'hub_height']  = dT['dhubHt']
        J['T', 'Rhub']        = dT['dRhub']
        J['T', 'Rtip']        = dT['dRtip']
        J['T', 'yaw']         = dT['dyaw']
        J['T', 'Uhub']        = dT['dUinf']
        J['T', 'Omega']       = dT['dOmega']
        J['T', 'pitch']       = dT['dpitch']
        J['T', 'r']           = dT['dr']
        J['T', 'chord']       = dT['dchord']
        J['T', 'theta']       = dT['dtheta']
        J['T', 'precurve']    = dT['dprecurve']
        J['T', 'precurveTip'] = dT['dprecurveTip']

        J['Q', 'precone']     = dQ['dprecone']
        J['Q', 'tilt']        = dQ['dtilt']
        J['Q', 'hub_height']  = dQ['dhubHt']
        J['Q', 'Rhub']        = dQ['dRhub']
        J['Q', 'Rtip']        = dQ['dRtip']
        J['Q', 'yaw']         = dQ['dyaw']
        J['Q', 'Uhub']        = dQ['dUinf']
        J['Q', 'Omega']       = dQ['dOmega']
        J['Q', 'pitch']       = dQ['dpitch']
        J['Q', 'r']           = dQ['dr']
        J['Q', 'chord']       = dQ['dchord']
        J['Q', 'theta']       = dQ['dtheta']
        J['Q', 'precurve']    = dQ['dprecurve']
        J['Q', 'precurveTip'] = dQ['dprecurveTip']
        '''

        


    
class CCBladeLoads(ExplicitComponent):
    def initialize(self):
        self.options.declare('naero')
        self.options.declare('npower')

        self.options.declare('n_aoa_grid')
        self.options.declare('n_Re_grid')
        
    def setup(self):
        self.naero = naero = self.options['naero']
        npower     = self.options['npower']
        n_aoa_grid = self.options['n_aoa_grid']
        n_Re_grid  = self.options['n_Re_grid']
        """blade element momentum code"""

        # inputs
        self.add_input('V_load', val=0.0, units='m/s', desc='hub height wind speed')
        self.add_input('Omega_load', val=0.0, units='rpm', desc='rotor rotation speed')
        self.add_input('pitch_load', val=0.0, units='deg', desc='blade pitch setting')
        self.add_input('azimuth_load', val=0.0, units='deg', desc='blade azimuthal location')

        # outputs
        self.add_output('loads_r', val=np.zeros(naero), units='m', desc='radial positions along blade going toward tip')
        self.add_output('loads_Px', val=np.zeros(naero), units='N/m', desc='distributed loads in blade-aligned x-direction')
        self.add_output('loads_Py', val=np.zeros(naero), units='N/m', desc='distributed loads in blade-aligned y-direction')
        self.add_output('loads_Pz', val=np.zeros(naero), units='N/m', desc='distributed loads in blade-aligned z-direction')

        # corresponding setting for loads
        self.add_output('loads_V', val=0.0, units='m/s', desc='hub height wind speed')
        self.add_output('loads_Omega', val=0.0, units='rpm', desc='rotor rotation speed')
        self.add_output('loads_pitch', val=0.0, units='deg', desc='pitch angle')
        self.add_output('loads_azimuth', val=0.0, units='deg', desc='azimuthal angle')
        
        # (potential) variables
        self.add_input('r', val=np.zeros(naero), units='m', desc='radial locations where blade is defined (should be increasing and not go all the way to hub or tip)')
        self.add_input('chord', val=np.zeros(naero), units='m', desc='chord length at each section')
        self.add_input('theta', val=np.zeros(naero),  units='deg', desc='twist angle at each section (positive decreases angle of attack)')
        self.add_input('Rhub', val=0.0, units='m', desc='hub radius')
        self.add_input('Rtip', val=0.0, units='m', desc='tip radius')
        self.add_input('hub_height', val=0.0, units='m', desc='hub height')
        self.add_input('precone', val=0.0, desc='precone angle', units='deg')
        self.add_input('tilt', val=0.0, desc='shaft tilt', units='deg')
        self.add_input('yaw', val=0.0, desc='yaw error', units='deg')

        # TODO: I've not hooked up the gradients for these ones yet.
        self.add_input('precurve', val=np.zeros(naero), units='m', desc='precurve at each section')
        self.add_input('precurveTip', val=0.0, units='m', desc='precurve at tip')

        # parameters
        # self.add_discrete_input('airfoils', val=[0]*naero, desc='CCAirfoil instances')
        self.add_input('airfoils_cl', val=np.zeros((n_aoa_grid, naero, n_Re_grid)), desc='lift coefficients, spanwise')
        self.add_input('airfoils_cd', val=np.zeros((n_aoa_grid, naero, n_Re_grid)), desc='drag coefficients, spanwise')
        self.add_input('airfoils_cm', val=np.zeros((n_aoa_grid, naero, n_Re_grid)), desc='moment coefficients, spanwise')
        self.add_input('airfoils_aoa', val=np.zeros((n_aoa_grid)), units='deg', desc='angle of attack grid for polars')
        self.add_input('airfoils_Re', val=np.zeros((n_Re_grid)), desc='Reynolds numbers of polars')

        self.add_discrete_input('nBlades', val=0, desc='number of blades')
        self.add_input('rho', val=0.0, units='kg/m**3', desc='density of air')
        self.add_input('mu', val=0.0, units='kg/(m*s)', desc='dynamic viscosity of air')
        self.add_input('shearExp', val=0.0, desc='shear exponent')
        self.add_discrete_input('nSector', val=4, desc='number of sectors to divide rotor face into in computing thrust and power')
        self.add_discrete_input('tiploss', val=True, desc='include Prandtl tip loss model')
        self.add_discrete_input('hubloss', val=True, desc='include Prandtl hub loss model')
        self.add_discrete_input('wakerotation', val=True, desc='include effect of wake rotation (i.e., tangential induction factor is nonzero)')
        self.add_discrete_input('usecd', val=True, desc='use drag coefficient in computing induction factors')

        #self.declare_partials('loads_r', ['r', 'Rhub', 'Rtip'])
        #self.declare_partials(['loads_Px', 'loads_Py'],
        #                      ['r', 'chord', 'theta', 'Rhub', 'Rtip', 'hub_height', 'precone', 'tilt',
        #                       'yaw', 'V_load', 'Omega_load', 'pitch_load', 'azimuth_load', 'precurve'])
        #self.declare_partials('loads_V', 'V_load')
        #self.declare_partials('loads_Omega', 'Omega_load')
        #self.declare_partials('loads_pitch', 'pitch_load')
        #self.declare_partials('loads_azimuth', 'azimuth_load')

        
    def compute(self, inputs, outputs, discrete_inputs, discrete_outputs):
        self.r = inputs['r']
        self.chord = inputs['chord']
        self.theta = inputs['theta']
        self.Rhub = inputs['Rhub']
        self.Rtip = inputs['Rtip']
        self.hub_height = inputs['hub_height']
        self.precone = inputs['precone']
        self.tilt = inputs['tilt']
        self.yaw = inputs['yaw']
        self.precurve = inputs['precurve']
        self.precurveTip = inputs['precurveTip']
        # self.airfoils = discrete_inputs['airfoils']
        self.B = discrete_inputs['nBlades']
        self.rho = inputs['rho']
        self.mu = inputs['mu']
        self.shearExp = inputs['shearExp']
        self.nSector = discrete_inputs['nSector']
        self.tiploss = discrete_inputs['tiploss']
        self.hubloss = discrete_inputs['hubloss']
        self.wakerotation = discrete_inputs['wakerotation']
        self.usecd = discrete_inputs['usecd']
        self.V_load = inputs['V_load']
        self.Omega_load = inputs['Omega_load']
        self.pitch_load = inputs['pitch_load']
        self.azimuth_load = inputs['azimuth_load']


        if len(self.precurve) == 0:
            self.precurve = np.zeros_like(self.r)

        # airfoil files
        # n = len(self.airfoils)
        af = [None]*self.naero
        for i in range(self.naero):
            af[i] = CCAirfoil(inputs['airfoils_aoa'], inputs['airfoils_Re'], inputs['airfoils_cl'][:,i,:], inputs['airfoils_cd'][:,i,:], inputs['airfoils_cm'][:,i,:])
        # af = self.airfoils

        self.ccblade = CCBlade(self.r, self.chord, self.theta, af, self.Rhub, self.Rtip, self.B,
            self.rho, self.mu, self.precone, self.tilt, self.yaw, self.shearExp, self.hub_height,
            self.nSector, self.precurve, self.precurveTip, tiploss=self.tiploss, hubloss=self.hubloss,
            wakerotation=self.wakerotation, usecd=self.usecd, derivatives=True)

        # distributed loads
        Np, Tp, self.dNp, self.dTp \
            = self.ccblade.distributedAeroLoads(self.V_load, self.Omega_load, self.pitch_load, self.azimuth_load)
        
        
        # concatenate loads at root/tip
        outputs['loads_r'] = self.r

        # conform to blade-aligned coordinate system
        outputs['loads_Px'] = Np
        outputs['loads_Py'] = -Tp
        outputs['loads_Pz'] = 0*Np

        # return other outputs needed
        outputs['loads_V'] = self.V_load
        outputs['loads_Omega'] = self.Omega_load
        outputs['loads_pitch'] = self.pitch_load
        outputs['loads_azimuth'] = self.azimuth_load
        '''
    def compute_partials(self, inputs, J, discrete_inputs=None):

        dNp = self.dNp
        dTp = self.dTp
        n = len(self.r)

        dr_dr = np.eye(n)
        dr_dRhub = np.zeros(n)
        dr_dRtip = np.zeros(n)
        dr_dRhub[0] = 1.0
        dr_dRtip[-1] = 1.0

        dV = np.zeros(4*n+10)
        dV[3*n+6] = 1.0
        dOmega = np.zeros(4*n+10)
        dOmega[3*n+7] = 1.0
        dpitch = np.zeros(4*n+10)
        dpitch[3*n+8] = 1.0
        dazimuth = np.zeros(4*n+10)
        dazimuth[3*n+9] = 1.0

        zero = np.zeros(self.naero)
        J['loads_r',      'r']             = dr_dr
        J['loads_r',      'Rhub']          = dr_dRhub
        J['loads_r',      'Rtip']          = dr_dRtip
        J['loads_Px',     'r']             = dNp['dr']
        J['loads_Px',     'chord']         = dNp['dchord']
        J['loads_Px',     'theta']         = dNp['dtheta']
        J['loads_Px',     'Rhub']          = np.squeeze(dNp['dRhub'])
        J['loads_Px',     'Rtip']          = np.squeeze(dNp['dRtip'])
        J['loads_Px',     'hub_height']    = np.squeeze(dNp['dhubHt'])
        J['loads_Px',     'precone']       = np.squeeze(dNp['dprecone'])
        J['loads_Px',     'tilt']          = np.squeeze(dNp['dtilt'])
        J['loads_Px',     'yaw']           = np.squeeze(dNp['dyaw'])
        J['loads_Px',     'V_load']        = np.squeeze(dNp['dUinf'])
        J['loads_Px',     'Omega_load']    = np.squeeze(dNp['dOmega'])
        J['loads_Px',     'pitch_load']    = np.squeeze(dNp['dpitch'])
        J['loads_Px',     'azimuth_load']  = np.squeeze(dNp['dazimuth'])
        J['loads_Px',     'precurve']      = dNp['dprecurve']
        J['loads_Py',     'r']             = -dTp['dr']
        J['loads_Py',     'chord']         = -dTp['dchord']
        J['loads_Py',     'theta']         = -dTp['dtheta']
        J['loads_Py',     'Rhub']          = -np.squeeze(dTp['dRhub'])
        J['loads_Py',     'Rtip']          = -np.squeeze(dTp['dRtip'])
        J['loads_Py',     'hub_height']    = -np.squeeze(dTp['dhubHt'])
        J['loads_Py',     'precone']       = -np.squeeze(dTp['dprecone'])
        J['loads_Py',     'tilt']          = -np.squeeze(dTp['dtilt'])
        J['loads_Py',     'yaw']           = -np.squeeze(dTp['dyaw'])
        J['loads_Py',     'V_load']        = -np.squeeze(dTp['dUinf'])
        J['loads_Py',     'Omega_load']    = -np.squeeze(dTp['dOmega'])
        J['loads_Py',     'pitch_load']    = -np.squeeze(dTp['dpitch'])
        J['loads_Py',     'azimuth_load']  = -np.squeeze(dTp['dazimuth'])
        J['loads_Py',     'precurve']      = -dTp['dprecurve']
        J['loads_V',      'V_load']        = 1.0
        J['loads_Omega',  'Omega_load']    = 1.0
        J['loads_pitch',  'pitch_load']    = 1.0
        J['loads_azimuth', 'azimuth_load'] = 1.0
        '''

        
