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

