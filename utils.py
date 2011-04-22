def context_dict(source_dict, *varnames):
    # helper to initialize template context from locals()
    return dict((varname, source_dict[varname]) for varname in varnames)
