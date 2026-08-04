close all; clear; clc;

script_dir = fileparts(mfilename('fullpath'));
data = readtable(fullfile(script_dir, 'fitted_values.csv'), 'TextType', 'string');

colors = [
    55, 126, 184;
    255, 127, 0;
    77, 175, 74
] / 255;

plot_specimen(data, "B12W", ["Wire D", "Wire E", "Wire F"], colors, ...
    [-5, 200]);
plot_specimen(data, "M8N", ["Wire A", "Wire B", "Wire C"], colors, ...
    [-5, 120]);


function plot_specimen(data, specimen, wires, colors, x_limits)
    figure; hold on;
    for index = 1:numel(wires)
        selected = data.specimen == specimen & data.wire == wires(index);
        wire_data = sortrows(data(selected, :), 'plot_order');

        d = wire_data.d_spacing_angstrom;
        d_uncertainty = wire_data.d_spacing_uncertainty_angstrom;
        d0 = wire_data.d0_angstrom;
        d0_uncertainty = wire_data.d0_uncertainty_angstrom;
        strain = (d - d0) ./ d0 * 1e6;
        strain_uncertainty = sqrt( ...
            (d_uncertainty ./ d0).^2 + ...
            (d .* d0_uncertainty ./ d0.^2).^2) * 1e6;

        errorbar( ...
            wire_data.measurement_position_mm, strain, strain_uncertainty, ...
            'd-', 'LineWidth', 1, 'Color', colors(index, :), ...
            'MarkerEdgeColor', colors(index, :), ...
            'MarkerFaceColor', colors(index, :));
    end

    xlabel('Distance from the tip of the wire (mm)', ...
        'FontName', 'Arial', 'FontWeight', 'bold');
    ylabel('Microstrain (\mu\epsilon)', ...
        'FontName', 'Arial', 'FontWeight', 'bold');
    legend(cellstr(wires), 'Location', 'northeast', 'Box', 'off', ...
        'FontName', 'Arial');
    xlim(x_limits);
    ylim([-1000, 1000]);
    xticks(0:20:200);
    yticks(-1000:250:1000);
end
