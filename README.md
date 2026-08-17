# Arecibo neutron diffraction data and analysis code

## Overview

This repository contains neutron diffraction data and analysis code used to evaluate axial residual strain, radial residual strain, gauge-volume alignment sensitivity, and crystallographic texture through pole figures.

The corresponding autoreduced HIDRA diffraction data are publicly available through ORNL's ONCat system:

- DOI: [10.14461/oncat.data/3419321](https://doi.org/10.14461/oncat.data/3419321)
- ONCat: [https://oncat.ornl.gov/dois/6a7b8429ad0a3672374c8379](https://oncat.ornl.gov/dois/6a7b8429ad0a3672374c8379)

## Repository contents

- `reduced_diffraction_data.h5` contains a lossless-compressed copy of the reduced one-dimensional diffraction data in a format convenient for analysis. The data are organized by run number, with each run containing `two_theta`, `intensity`, `intensity_variance`, the subrun index, and the position/orientation coordinates needed to distinguish measurements.
- `run_catalog.csv` maps each published run to its analysis set, physical specimen, wire, measurement direction, reflection, and position.
- `fitted_values.csv` contains the fitted d-spacings, uncertainties, and peak-fitting bounds used in the analyses.
- `alignment-sensitivity/` contains the four-location gauge-volume shift table and Python plot.
- `axial-residual-strain/` contains the axial fitted values, stress-free reference values, plotting order, and MATLAB plot.
- `radial-residual-strain/` contains the paired axial/radial fitted values and MATLAB comparison plot.
- `pole-figures/` contains the texture measurements and MTEX MATLAB script.

## HDF5 compression

The numerical datasets in `reduced_diffraction_data.h5` use lossless gzip compression. Compression does not change the array values, dimensions, data types, or numerical precision, and `h5py` and MATLAB decompress the data transparently when read.

## Peak fitting with pyRS

[pyRS](https://doi.org/10.1107/S1600576721010554) is open-source neutron-diffraction reduction and analysis software developed for the High Intensity Diffractometer for Residual Stress Analysis (HIDRA) at Oak Ridge National Laboratory. Single-peak analyses were carried out using pyRS with individual pseudo-Voigt peak functions and linear backgrounds. The Lorentzian–Gaussian mixture parameter was fixed at `0.6`.

The lower and upper $2\theta$ fitting boundaries, fitted d-spacings, and fitting uncertainties are provided in the relevant `fitted_values.csv` files. `reduced_diffraction_data.h5` contains the corresponding diffraction arrays so users can inspect the patterns and independently repeat or modify the fits.

The MATLAB and Python scripts perform the downstream calculations and visualizations after peak fitting. The repository scripts begin from the exported fitted-value tables and do not invoke pyRS.

## Reading the reduced diffraction data

### Python

```python
import h5py
import matplotlib.pyplot as plt

with h5py.File("reduced_diffraction_data.h5", "r") as h5:
    print(list(h5["runs"]))
    two_theta = h5["runs/run_4394/two_theta"][0]
    intensity = h5["runs/run_4394/intensity"][0]

plt.plot(two_theta, intensity)
plt.xlabel(r"$2\theta$ (degrees)")
plt.ylabel("Intensity (counts)")
plt.show()
```

### MATLAB

```matlab
info = h5info('reduced_diffraction_data.h5', '/runs');
disp({info.Groups.Name}');
two_theta = h5read('reduced_diffraction_data.h5', '/runs/run_4394/two_theta');
intensity = h5read('reduced_diffraction_data.h5', '/runs/run_4394/intensity');
plot(two_theta(:, 1), intensity(:, 1));
xlabel('2\theta (degrees)');
ylabel('Intensity (counts)');
```

## Running the analyses

From the repository root:

```text
python alignment-sensitivity/alignment_sensitivity.py
matlab -batch "run('axial-residual-strain/axial_residual_strain.m')"
matlab -batch "run('radial-residual-strain/radial_residual_strain.m')"
matlab -batch "run('pole-figures/pole_figures.m')"
```

The pole-figure analysis requires MTEX to be installed separately and available on the MATLAB path.

## Software requirements

- Python 3.10 or newer
- `h5py`
- `numpy`
- `scipy`
- `matplotlib`
- MATLAB R2020a or newer for the MATLAB analyses
- MTEX for the pole figures

## Acknowledgment

This research used resources at the High Flux Isotope Reactor, a DOE Office of Science User Facility operated by Oak Ridge National Laboratory. Beam time was allocated to HIDRA under proposal IPTS-32250.0, *Arecibo Telescope Failure: Validating BEI readings through Strain Mapping*.

## Citation

Machine-readable citation metadata are provided in `CITATION.cff`.

A. A. Koç, *Arecibo neutron diffraction data and analysis code*, version 1.0.0 (2026), https://github.com/ahmetalperenkoc/Arecibo-neutron-diffraction-rs.

For the autoreduced neutron diffraction data, cite the ONCat dataset listed above.

## Licenses

- Software and analysis scripts: BSD 3-Clause. See `LICENSE.txt`.
- Data files and fitted-data tables: CC BY 4.0. See `DATA_LICENSE.txt`.
