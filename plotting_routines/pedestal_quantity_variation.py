#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import europed_analysis, global_functions,startup
import argparse
import matplotlib.pyplot as plt
import numpy as np

def parse_modes(mode_str):
    return mode_str.split(',')

def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Plots the profile of the critical alpha versus density shift")
    parser.add_argument("prefixes", type=parse_modes, help = "list of prefixes to construct the Europed run names")
    parser.add_argument("variations", type=parse_modes, help = "name variations of the Europed runs (the Europed runs will have the name [prefix]+[variation]{+[suffix]})  If set to 'full_list', variations=['-0.0100','-0.0050','0.0000','0.050','0.0100','0.0050','0.0150','0.0200','0.0250','0.0350','0.0400']")


    parser.add_argument("-d", "--diamag", action = 'store_const', const = 'diamag', dest = 'crit', default = 'alfven', help = "use diamagnetic criterion instead of Alfven")
    parser.add_argument("-l", "--labels", type=parse_modes, help= "labels to display for the different Europed run prefixes")
    parser.add_argument("-L", "--legendtitle", help= "legend title")

    args = parser.parse_args()

    prefixes = args.prefixes
    labels = args.labels
    legendtitle = args.legendtitle
    if prefixes == ["allneped"]:
        prefixes = global_functions.allneped_prefixes
        labels = global_functions.allneped_labels
        legendtitle = "neped"

    variations = args.variations
    if variations == ["full_list"]:
        variations = global_functions.full_list

    return prefixes, variations, labels, legendtitle, args.crit


def main(prefixes, variations, labels, legendtitle, crit):

    fig, axs = plt.subplots(2,2)
    plt.subplots_adjust(wspace=0, hspace=0)

    ax1 = axs[0][0]
    ax2 = axs[0][1]
    ax3 = axs[1][0]
    ax4 = axs[1][1]

    # Set y-axis label position for right plots
    ax2.yaxis.tick_right()
    ax4.yaxis.tick_right()
    ax2.yaxis.set_label_position("right")
    ax4.yaxis.set_label_position("right")

    for iprefix,prefix in enumerate(prefixes):
        list_width = []
        list_pressure = []
        list_temperature = []
        list_density = []

        for dshift in variations:
            europed_run = prefix+dshift
            try:
                width = europed_analysis.critical_width(europed_run, crit)
                pressure = europed_analysis.pressure_at_tpos(europed_run, crit)
                temperature = europed_analysis.temperature_at_tpos(europed_run, crit)
                density = europed_analysis.density_at_tpos(europed_run, crit)

                list_width.append(width)
                list_pressure.append(pressure)
                list_temperature.append(temperature)
                list_density.append(density)

            except Exception:
                print(f"{europed_run:>40} FILE NOT FOUND")
                list_width.append(None)
                list_pressure.append(None)
                list_temperature.append(None)
                list_density.append(None)

        dshifts_plot = [float(dshift) for dshift,width in zip(variations,list_width) if width is not None]
        list_width_plot = [width for width in list_width if width is not None]
        list_pressure_plot = [pressure for pressure in list_pressure if pressure is not None]
        list_temperature_plot = [temperature for temperature in list_temperature if temperature is not None]
        list_density_plot = [density for density in list_density if density is not None]

        if labels is not None:
            ax1.plot(dshifts_plot, list_width_plot, 'o-',label=labels[iprefix], color=global_functions.dict_neped_color[labels[iprefix]])
        else:
            ax1.plot(dshifts_plot, list_width_plot, 'o-', color=global_functions.dict_neped_color[labels[iprefix]])

        ax2.plot(dshifts_plot, list_pressure_plot, 'o-', color=global_functions.dict_neped_color[labels[iprefix]])
        ax3.plot(dshifts_plot, list_temperature_plot, 'o-', color=global_functions.dict_neped_color[labels[iprefix]])
        ax4.plot(dshifts_plot, list_density_plot, 'o-', color=global_functions.dict_neped_color[labels[iprefix]])

        
    if labels is not None:
        if legendtitle == "neped":
            fig.legend(title=r"$n_e^{\mathrm{ped}} [10^{19}e.s^{-1}]$", fontsize=8)
        elif legendtitle == "eta":
            fig.legend(title=r"$\eta$", fontsize=8)
        else:
            fig.legend(title=legendtitle, fontsize=8)

    ax1.set_xlabel("Density shift")
    ax2.set_xlabel("Density shift")
    ax3.set_xlabel("Density shift")
    ax4.set_xlabel("Density shift")

    ax1.set_ylim(bottom=0)
    ax2.set_ylim(bottom=0)
    ax3.set_ylim(bottom=0)
    ax4.set_ylim(bottom=0)


    ax1.set_ylabel(r"Critical width [$\psi_N$]")
    ax2.set_ylabel(r"Critical $p_e$ at $T_e^{\mathrm{pos}}$ [$kPa$]")
    ax3.set_ylabel(r"Critical $T_e$ at $T_e^{\mathrm{pos}}$ [$keV$]")
    ax4.set_ylabel(r"Critical $n_e$ at $T_e^{\mathrm{pos}}$ [$10^{19} e\cdot m^{-3}$]")

    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    prefixes, variations, labels, legendtitle, crit = argument_parser()
    main(prefixes, variations, labels, legendtitle, crit)