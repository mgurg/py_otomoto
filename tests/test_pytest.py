import sys
import os.path
import pytest

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from py_otomoto import plot_data

def test_env_setup():
    assert plot_data.openblas_setup() == 'Sandybridge'

def test_numbers_6():
    assert plot_data.sums(3) == 6