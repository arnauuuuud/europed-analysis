from hoho import europed_analysis_2, h5_manipulation, pedestal_values, global_functions, experimental_values, hdf5_data
import numpy as np
import matplotlib.tri as tri
import os


def plot(ax, europed_name, color, crit_value, crit, q_ped_def, marker = 'o', open_markers=False, xy='alphapeped', exclude_modes=[]):
    print(europed_name)
    crit_x, crit_y = give_critx_crity(europed_name, crit, crit_value, xy, q_ped_def, exclude_modes)

    if not open_markers:
        ax.scatter(crit_x, crit_y, marker=marker, color=color, edgecolor='k', s=50)
    else:
        ax.scatter(crit_x, crit_y, marker=marker, color='white', edgecolor=color, s=50)

def plot_line_threshold(ax, europed_name, color, crit_values, crit, q_ped_def, xy='alphapeped', exclude_modes=[]):

    x = []
    y = []
    for c in crit_values:
        crit_x, crit_y = give_critx_crity(europed_name, crit, c, xy, q_ped_def, exclude_modes)
        x.append(crit_x)
        y.append(crit_y)

    x_filt = [xi for xi in x if not xi is None]
    y_filt = [yi for yi in y if not yi is None]
    ax.plot(x_filt, y_filt, color=color, linewidth=0.5, zorder=-1, marker='+')


def give_critx_crity(europed_name, crit, crit_value, xy, q_ped_def, exclude_modes=[]):
    try:
        fixed_width = europed_name.startswith('fw')

        crit_x_def = None
        crit_y_def = None

        if xy == 'alphapeped':
            xs = hdf5_data.get_xparam(europed_name, 'alpha_helena_max')
            # ys = hdf5_data.get_xparam(europed_name, 'peped',q_ped_def)
            crit_y_def = pedestal_values.pedestal_value_all_definition('pe', europed_name, crit=crit, crit_value=crit_value, q_ped_def=q_ped_def, exclud_mode=exclude_modes)

        elif xy == 'nepedteped':
            # xs = hdf5_data.get_xparam(europed_name, 'neped',q_ped_def)
            # ys = hdf5_data.get_xparam(europed_name, 'teped', q_ped_def)
            crit_x_def = pedestal_values.pedestal_value_all_definition('ne', europed_name, crit=crit, crit_value=crit_value, q_ped_def=q_ped_def, exclud_mode=exclude_modes)
            crit_y_def = pedestal_values.pedestal_value_all_definition('te', europed_name, crit=crit, crit_value=crit_value, q_ped_def=q_ped_def, exclud_mode=exclude_modes)

        elif xy == 'sepedwidth':
            crit_x_def = pedestal_values.nesep_neped(europed_name, crit=crit, crit_value=crit_value, q_ped_def=q_ped_def, exclud_mode=exclude_modes)
            ys = hdf5_data.get_xparam(europed_name, 'delta', q_ped_def)

        elif xy == 'sepedwidthbis':
            crit_x_def = pedestal_values.nesep_neped(europed_name, crit=crit, crit_value=crit_value, q_ped_def=q_ped_def, exclud_mode=exclude_modes)
            crit_y_def = pedestal_values.get_fit_width(europed_name, q='pe', crit=crit, crit_value=crit_value, fixed_width=fixed_width, exclud_mode=exclude_modes)

        elif xy == 'deltadelta':
            crit_x_def = pedestal_values.get_fit_width(europed_name, q='ne', crit=crit, crit_value=crit_value, fixed_width=fixed_width, exclud_mode=exclude_modes)
            crit_y_def = pedestal_values.get_fit_width(europed_name, q='te', crit=crit, crit_value=crit_value, fixed_width=fixed_width, exclud_mode=exclude_modes)

        elif xy == 'betapbetan':
            xs = hdf5_data.get_xparam(europed_name, 'betap')
            ys = hdf5_data.get_xparam(europed_name, 'betan')

        elif xy == 'relshrelsh':
            crit_x_def = pedestal_values.get_fit_rs(europed_name, crit=crit, crit_value=crit_value, fixed_width=fixed_width, exclud_mode=exclude_modes)
            crit_y_def = pedestal_values.get_rs(europed_name, crit=crit, crit_value=crit_value, fixed_width=fixed_width, exclud_mode=exclude_modes)

        
        deltas = hdf5_data.get_xparam(europed_name, 'betaped')  if fixed_width else hdf5_data.get_xparam(europed_name, 'delta') 
 

        dict_gamma = europed_analysis_2.get_gammas(europed_name, crit, fixed_width)
        dict_gamma = europed_analysis_2.filter_dict(dict_gamma, exclud_mode=exclude_modes)
        if crit == 'diamag':
            dict_gamma = europed_analysis_2.remove_wrong_slope(dict_gamma)

        if crit_x_def is None:
            bo, crit_x, bi = europed_analysis_2.find_critical(xs, deltas, dict_gamma, crit_value)
        else:
            crit_x = crit_x_def

        if crit_y_def is None:
            bo, crit_y, bi = europed_analysis_2.find_critical(ys, deltas, dict_gamma, crit_value)
        else:
            crit_y = crit_y_def

        return crit_x, crit_y
    except ValueError:
        print('ValueError')
        return None, None
    except TypeError:
        print(crit)
        print('TypeError')
        return None, None



def plot_experimental_point(ax, xy, shotnos, colors):

    ddas = [global_functions.dict_shot_dda[s] for s in shotnos]

    if xy == 'alphapeped':
        for (shotno, dda, color) in zip(shotnos, ddas, colors):
            alpha, alpha_error = experimental_values.get_alpha_max(shotno, dda)
            peped, peped_error = experimental_values.get_peped(shotno, dda)
            ax.errorbar([alpha], [peped], xerr=[alpha_error], yerr=[peped_error], fmt='*', color=color, zorder=-1)

    elif xy == 'nepedteped':
        for (shotno, dda, color) in zip(shotnos, ddas, colors):
            teped, teped_error = experimental_values.get_teped(shotno, dda)
            neped, neped_error = experimental_values.get_neped(shotno, dda)
            ax.errorbar([neped], [teped], xerr=[neped_error], yerr=[teped_error], fmt='*', color=color, zorder=-1)

    elif xy == 'sepedwidth':
        for (shotno, dda, color) in zip(shotnos, ddas, colors):
            nesepneped, nesepneped_error = experimental_values.get_nesepneped(shotno, dda)
            wp, wp_error = experimental_values.get_width_pe(shotno, dda)
            ax.errorbar([nesepneped], [wp], xerr=[nesepneped_error], yerr=[wp_error], fmt='*', color=color, zorder=-1)
    
    elif xy == 'sepedwidthbis':
        for (shotno, dda, color) in zip(shotnos, ddas, colors):
            nesepneped, nesepneped_error = experimental_values.get_nesepneped(shotno, dda)
            wp, wp_error = experimental_values.get_width_pe(shotno, dda)
            wp_fit = experimental_values.get_my_fit_width(shotno, dda, 'pe')
            wp_fit_error = wp_fit / wp * wp_error
            ax.errorbar([nesepneped], [wp_fit], xerr=[nesepneped_error], yerr=[wp_fit_error], fmt='*', color=color, zorder=-1)    

    elif xy == 'deltadelta':
        for (shotno, dda, color) in zip(shotnos, ddas, colors):
            wn, wn_error = experimental_values.get_width_ne(shotno, dda)
            wt, wt_error = experimental_values.get_width_te(shotno, dda)

            wn_fit = experimental_values.get_my_fit_width(shotno, dda, 'ne')
            wn_fit_error = wn_fit/wn *wn_error
            wt_fit = experimental_values.get_my_fit_width(shotno, dda, 'te')
            wt_fit_error = wt_fit/wt *wt_error

            ax.errorbar([wn_fit], [wt_fit], xerr=[wn_fit_error], yerr=[wt_fit_error], fmt='*', color=color, zorder=-1)

    elif xy == 'betapbetan':
        for (shotno, dda, color) in zip(shotnos, ddas, colors):
            betap, betap_error = experimental_values.get_betap(shotno, dda)
            betan, betan_error = experimental_values.get_betan(shotno, dda)

            ax.errorbar([betap], [betan], xerr=[betap_error], yerr=[betan_error], fmt='*', color=color, zorder=-1)

    elif xy == 'relshrelsh':
        for (shotno, dda, color) in zip(shotnos, ddas, colors):
            nepostepos, nepostepos_error = experimental_values.get_nepostepos(shotno, dda)
            nepostepos_myfit, nepostepos_myfit_error = experimental_values.get_nepostepos_myfit(shotno, dda)

            ax.errorbar([nepostepos], [nepostepos_myfit], xerr=[nepostepos_error], yerr=[nepostepos_myfit_error], fmt='*', color=color, zorder=-1)


def add_labels(ax, xy):
    if xy == 'alphapeped':
        xlabel = global_functions.alpha_label        
        ylabel = global_functions.peped_label

    elif xy == 'nepedteped':
        xlabel = global_functions.neped_label
        ylabel = global_functions.teped_label

    elif xy == 'sepedwidth':
        xlabel = global_functions.nesepneped_label
        ylabel = global_functions.delta_label

    elif xy == 'sepedwidthbis':
        xlabel = global_functions.nesepneped_label
        ylabel = global_functions.delta_pe_label

    elif xy == 'deltadelta':
        xlabel = global_functions.delta_ne_label
        ylabel = global_functions.delta_te_label

    elif xy == 'betapbetan':
        xlabel = global_functions.betap_label
        ylabel = global_functions.betan_label

    elif xy == 'relshrelsh':
        ylabel = global_functions.rs_label
        xlabel = global_functions.rs2_label

    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)