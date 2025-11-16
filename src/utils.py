# uitlity functions 

def average_payoff(t_fraction, theta):
    return theta * (1 - 2 * t_fraction) + 8 * (t_fraction + t_fraction * t_fraction)

def get_fname(**params):
    N = params['N']
    f_cultural = params['f_cultural']
    theta_list = params['theta_list']
    beta = params['beta']
    max_steps = params['max_steps']
    ensemble_size = params['ensemble_size']
    update_fraction = params['update_fraction']
    seed = params.get('seed')
    # convert theta_list to string
    theta_list = [str(theta) for theta in theta_list]
    theta_list = '_'.join(theta_list)
    # use fp to format the string

    seed_str = 'none' if seed is None else str(seed)
    fname = f"data_N_{N}_f_cultural_{f_cultural}_theta_list_{theta_list}_beta_{beta:.3f}_max_steps_{max_steps}_ensemble_size_{ensemble_size}_update_fraction_{update_fraction:.3f}_seed_{seed_str}.pkl"
    return fname
    