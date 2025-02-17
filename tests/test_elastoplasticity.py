import numpy as np
import matplotlib.pyplot as plt
import pytest
from elastoplasticity import elasto_plasticity as ep

def test_episotropic():
  E, H, Y0= 1000, 111, 10
  ep_iso = ep.ElastoPlasticIsoHard( E, H, Y0)
  delta_epsilon = 0.001
  epsilon0, sigma0 = 0, 0
  ep_iso.update_step( delta_epsilon, epsilon0, sigma0 )
  known = 1
  found = ep_iso.sigma
  assert np.isclose( known , found ) 

  E, H, Y0= 1000, 111, 10
  ep_iso = ep.ElastoPlasticIsoHard( E, H, Y0)
  delta_epsilon = 0.1
  epsilon0, sigma0 = 0, 0
  ep_iso.update_step( delta_epsilon, epsilon0, sigma0 )
  known = 18.991899189918996
  found = ep_iso.sigma
  assert np.isclose( known , found )

  E, H, Y0= 1000, 111, 10
  ep_iso = ep.ElastoPlasticIsoHard( E, H, Yo)
  epsilon_arr = np.array( [0, 0.001, 0.1] )
  sigma_arr_found = ep_iso.cal_sigma_array( epsilon_arr, 0  )
  sigma_arr_known = np.array( [0, 1, 18.991899189918996] )
  assert np.all( np.isclose( sigma_arr_found , sigma_arr_known ) )


def test_kinematic():
  E, H, Y= 1000, 111, 10
  ep_k = ep.ElastoPlasticKinematicHard( E, H, Y)
  delta_epsilon = 0.001
  epsilon0, sigma0 = 0, 0
  ep_k.update_step( delta_epsilon, epsilon0, sigma0 )
  known = 1
  found = ep_k.sigma
  assert np.isclose( known , found ) 

  E, H, Y= 1000, 111, 10
  ep_k = ep.ElastoPlasticKinematicHard( E, H, Y)
  delta_epsilon = 0.1
  epsilon0, sigma0 = 0, 0
  ep_k.update_step( delta_epsilon, epsilon0, sigma0 )
  known = 18.991899189918996
  found = ep_k.sigma
  assert np.isclose( known , found ) 

  E, H, Y= 1000, 111, 10
  ep_k = ep.ElastoPlasticKinematicHard( E, H, Y)
  epsilon_arr = np.array( [0, 0.001, 0.1] )
  sigma_arr_found = ep_k.cal_sigma_array( epsilon_arr, 0  )
  sigma_arr_known = np.array( [0, 1, 18.991899189918996] )
  assert np.all( np.isclose( sigma_arr_found , sigma_arr_known ) )
