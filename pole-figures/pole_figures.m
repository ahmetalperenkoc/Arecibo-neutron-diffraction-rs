clear; close all; clc;

script_dir = fileparts(mfilename('fullpath'));
data = readtable(fullfile(script_dir, 'texture_data.csv'), 'TextType', 'string');

setMTEXpref('pfAnnotations', @(varargin) []);
crystal_symmetry = crystalSymmetry( ...
    'm-3m', [2.866, 2.866, 2.866], 'mineral', 'Iron alpha');
specimen_symmetry = specimenSymmetry('triclinic');

make_pole_figure(data, "{211}", Miller({2, 1, 1}, crystal_symmetry), ...
    crystal_symmetry, specimen_symmetry);
make_pole_figure(data, "{220}", Miller({2, 2, 0}, crystal_symmetry), ...
    crystal_symmetry, specimen_symmetry);


function make_pole_figure(data, reflection, miller_index, crystal_symmetry, ...
        specimen_symmetry)
    selected = data(data.reflection == reflection, :);
    direction = vector3d( ...
        'polar', selected.chi_deg * degree, selected.phi_deg * degree);
    pole_figure = PoleFigure( ...
        miller_index, direction, selected.intensity, ...
        'CS', crystal_symmetry, 'SS', specimen_symmetry);
    orientation_distribution = calcODF(pole_figure, 'silent');
    fit_error = calcError(orientation_distribution, pole_figure);
    fprintf('%s pole-figure fit error: %.8g\n', reflection, fit_error);

    figure;
    plotPDF(orientation_distribution, pole_figure.h, 'minmax');
    set(gca, 'LooseInset', get(gca, 'TightInset'));
    mtexColorbar;
end
