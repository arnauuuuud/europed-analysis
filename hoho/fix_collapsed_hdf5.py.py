from hoho import europed_analysis_2


def detect_collapsed_givenn(dict_gammas, n):
    dict_gammas_r = europed_analysis_2.reverse_nested_dict(dict_gammas)
    subdict_n = dict_gammas_r[int(n)]

    deltas = sorted(list(subdict_n.keys()))

    