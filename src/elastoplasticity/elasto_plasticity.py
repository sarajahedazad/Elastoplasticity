import numpy as np

class ElastoPlasticIsoHard:
  def __init__(self, E, H, Y0):
    self.E = E # Young's modulus
    self.H = H # Plastic modulus
    self.Y0 = Y0 # Yeild strength
    self.Y = self.Y0
    self.sigma = 0
    self.epsilon = 0
    self.epsilon_p = 0 # Plastic strain

  def calc_sigma_trial( self, delta_epsilon ):
    sigma_trial = self.sigma + self.E * delta_epsilon
    return sigma_trial

  def cal_yield_trial( self, sigma_trial ):
    yield_trial = np.abs( sigma_trial ) - self.Y
    return yield_trial

  def yields( self, yield_trial ):
    return yield_trial > 0

  def update_epsilon(self, delta_epsilon):
    self.epsilon += delta_epsilon

  def update_epsilon_p(self, delta_epsilon_p):
    self.epsilon_p += delta_epsilon_p

  def update_sigma_elastic(self, sigma_trial):
    self.sigma = sigma_trial

  def correct_sigma_plastic( self, sigma_trial, delta_epsilon_p ):
    sigma_correction = self.cal_sigma_correction( sigma_trial, delta_epsilon_p )
    self.sigma = sigma_trial - sigma_correction

  def elastic_predicter(self, delta_epsilon, sigma_trial ):
    self.update_epsilon( delta_epsilon )
    self.update_sigma_elastic( sigma_trial )

  def cal_delta_epsilon_p( self, yield_trial ):
    delta_epsilon_p = yield_trial/( self.E + self.H)
    return delta_epsilon_p

  def cal_sigma_correction( self, sigma_trial, delta_epsilon_p ):
    sigma_correction = np.sign( sigma_trial ) * self.E * delta_epsilon_p
    return sigma_correction

  def plastic_predictor( self, yield_trial, delta_epsilon, sigma_trial ):
    self.update_epsilon(delta_epsilon)
    delta_epsilon_p = self.cal_delta_epsilon_p( yield_trial )
    self.correct_sigma_plastic( sigma_trial, delta_epsilon_p )
    self.update_epsilon_p( delta_epsilon_p )

  def update_yield_stress( self ):
    self.Y = self.Y0 + self.H * self.epsilon_p

  def update_step( self, delta_epsilon, epsilon0, sigma0 ):
    self.epsilon = epsilon0
    self.sigma = sigma0

    self.update_yield_stress( )

    sigma_trial = self.calc_sigma_trial( delta_epsilon )
    yield_trial = self.cal_yield_trial( sigma_trial )

    if self.yields( yield_trial ):
      self.plastic_predictor( yield_trial, delta_epsilon, sigma_trial )
    else:
      self.elastic_predicter(delta_epsilon, sigma_trial )


  def cal_sigma_array( self, epsilon_arr, sigma0 ):
    sigma_lst = [ sigma0 ]
    delta_epsilon_arr = epsilon_arr[1:] - epsilon_arr[:-1]
    for i, epsilon0 in enumerate( epsilon_arr[: -1] ):
      delta_epsilon = delta_epsilon_arr[ i ]
      self.update_step( delta_epsilon, epsilon0, sigma0 )
      sigma0 = self.sigma
      sigma_lst.append( self.sigma )
    return np.array( sigma_lst )


class ElastoPlasticKinematicHard:
  def __init__(self, E, H, Y):
    self.E = E # Young's modulus
    self.H = H # Plastic modulus
    self.Y = Y
    self.alpha = 0 # backstress
    self.sigma = 0
    self.epsilon = 0
    self.epsilon_p = 0 # Plastic strain

  def cal_sigma_trail( self, delta_epsilon ):
    return self.sigma + self.E * delta_epsilon

  def cal_eta_trial( self, sigma_trial ):
    return sigma_trial - self.alpha

  def cal_yield_trial( self, eta_trial):
    return np.abs( eta_trial ) - self.Y

  def cal_trials(self, delta_epsilon):
    sigma_trial = self.cal_sigma_trail( delta_epsilon )
    eta_trial = self.cal_eta_trial( sigma_trial )
    yield_trial = self.cal_yield_trial( eta_trial)
    return sigma_trial, eta_trial, yield_trial

  def initialize_sigma_epsilon( self, sigma0, epsilon0  ):
    self.sigma = sigma0
    self.epsilon = epsilon0

  def yields( self, yield_trial):
    return yield_trial > 0

  def elastic_predictor( self, sigma_trial, delta_epsilon ):
    self.epsilon += delta_epsilon
    self.sigma = sigma_trial

  def cal_delta_epsilon_p( self, yield_trial ):
    return yield_trial / ( self.H + self.E )

  def cal_sigma_correction( self, eta_trial, delta_epsilon_p ):
    return np.sign( eta_trial ) * self.E * delta_epsilon_p

  def cal_sigma_corrected( self, sigma_trial, eta_trial, delta_epsilon_p ):
    return sigma_trial - self.cal_sigma_correction( eta_trial, delta_epsilon_p )

  def cal_alpha_correction( self, eta_trial, delta_epsilon_p ):
    return np.sign( eta_trial ) * self.H * delta_epsilon_p

  def cal_alpha_corrected( self, eta_trial, delta_epsilon_p ):
    return self.alpha + self.cal_alpha_correction( eta_trial, delta_epsilon_p )

  def plastic_predictor( self, sigma_trial, delta_epsilon, eta_trial, yield_trial ):
    delta_epsilon_p = self.cal_delta_epsilon_p( yield_trial )
    self.epsilon += delta_epsilon
    self.sigma = self.cal_sigma_corrected( sigma_trial, eta_trial, delta_epsilon_p )
    self.alpha = self.cal_alpha_corrected( eta_trial, delta_epsilon_p )
    self.epsilon_p += delta_epsilon_p

  def update_step( self, delta_epsilon, sigma0, epsilon0 ):
    self.initialize_sigma_epsilon( sigma0, epsilon0 )
    sigma_trial, eta_trial, yield_trial = self.cal_trials(delta_epsilon)
    if self.yields( yield_trial):
      self.plastic_predictor( sigma_trial, delta_epsilon, eta_trial, yield_trial )
    else:
      self.elastic_predictor( sigma_trial, delta_epsilon )

  def cal_sigma_array( self, epsilon_arr, sigma0 ):
    sigma_lst = [ sigma0 ]
    delta_epsilon_arr = epsilon_arr[1:] - epsilon_arr[:-1]
    for i, epsilon0 in enumerate( epsilon_arr[:-1] ):
      delta_epsilon = delta_epsilon_arr[ i ]
      self.update_step( delta_epsilon, sigma0, epsilon0 )
      sigma0 = self.sigma
      sigma_lst.append( self.sigma )
    return np.array( sigma_lst )
