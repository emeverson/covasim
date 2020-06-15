'''
Set the defaults across each of the different files.
'''

import numpy as np
import sciris as sc

# Specify all externally visible functions this file defines
__all__ = ['get_colors', 'get_sim_plots', 'get_scen_plots']

#%% Specify what data types to use

default_precision = 32 # Use this by default for speed and memory efficiency
result_float = np.float64 # Always use float64 for results, for simplicity
if default_precision == 32:
    default_float = np.float32
    default_int   = np.int32
elif default_precision == 64:
    default_float = np.float64
    default_int   = np.int64
else:
    raise NotImplementedError


#%% Define all properties of people

class PeopleMeta(sc.prettyobj):
    ''' For storing all the keys relating to a person and people '''

    # Set the properties of a person
    person = [
        'uid',         # Int
        'age',         # Float
        'sex',         # Float
        'symp_prob',   # Float
        'severe_prob', # Float
        'crit_prob',   # Float
        'death_prob',  # Float
        'rel_trans',   # Float
        'rel_sus',     # Float
    ]

    # Set the states that a person can be in: these are all booleans per person -- used in people.py
    states = [
        'susceptible',
        'exposed',
        'infectious',
        'symptomatic',
        'severe',
        'critical',
        'tested',
        'diagnosed',
        'recovered',
        'dead',
        'known_contact',
        'quarantined',
    ]

    # Set the dates various events took place: these are floats per person -- used in people.py
    dates = [f'date_{state}' for state in states] # Convert each state into a date
    dates.append('date_pos_test') # Store the date when a person tested which will come back positive
    dates.append('date_end_quarantine') # Store the date when a person comes out of quarantine

    # Duration of different states: these are floats per person -- used in people.py
    durs = [
        'dur_exp2inf',
        'dur_inf2sym',
        'dur_sym2sev',
        'dur_sev2crit',
        'dur_disease',
    ]

    all_states = person + states + dates + durs


#%% Define other defaults

# A subset of the above states are used for results
result_stocks = {
        'susceptible': 'Number susceptible',
        'exposed':     'Number exposed',
        'infectious':  'Number infectious',
        'symptomatic': 'Number symptomatic',
        'severe':      'Number of severe cases',
        'critical':    'Number of critical cases',
        'diagnosed':   'Number of confirmed cases',
        'quarantined': 'Number in quarantine',
}

# The types of result that are counted as flows -- used in sim.py; value is the label suffix
result_flows = {'infections':  'infections',
                'infectious':  'infectious',
                'tests':       'tests',
                'diagnoses':   'diagnoses',
                'recoveries':  'recoveries',
                'symptomatic': 'symptomatic cases',
                'severe':      'severe cases',
                'critical':    'critical cases',
                'deaths':      'deaths',
                'quarantined': 'quarantined people',
}


# Define these here as well
new_result_flows = [f'new_{key}' for key in result_flows.keys()]
cum_result_flows = [f'cum_{key}' for key in result_flows.keys()]


# ML, 4/15/2020: this is Matt's change based on the ACS 2018 survey for Oregon population
default_age_data = np.array([
            [ 0,  4, 0.055],
            [ 5,  9, 0.057],
            [10, 14, 0.061],
            [15, 19, 0.060],
            [20, 24, 0.063],
            [25, 29, 0.072],
            [30, 34, 0.070],
            [35, 39, 0.069],
            [40, 44, 0.064],
            [45, 49, 0.064],
            [50, 54, 0.060],
            [55, 59, 0.064],
            [60, 64, 0.066],
            [65, 69, 0.062],
            [70, 74, 0.045],
            [75, 79, 0.031], # Calculated based on 0.0504 total for >=75
            [80, 84, 0.020],
            [85, 89, 0.0114],
            [90, 99, 0.0076], # EE - used same proportion as above Seattle pop for age 85+
            ])

def get_colors():
    '''
    Specify plot colors -- used in sim.py.

    NB, includes duplicates since stocks and flows are named differently.
    '''
    colors = sc.objdict(
        susceptible = '#5e7544',
        infectious  = '#c78f65',
        infections  = '#c75649',
        exposed     = '#c75649', # Duplicate
        tests       = '#aaa8ff',
        diagnoses   = '#8886cc',
        diagnosed   = '#8886cc', # Duplicate
        recoveries  = '#799956',
        recovered   = '#799956', # Duplicate
        symptomatic = '#c1ad71',
        severe      = '#c1981d',
        quarantined = '#5f1914',
        critical    = '#b86113',
        deaths      = '#000000',
        dead        = '#000000', # Duplicate
    )
    return colors


<<<<<<< HEAD
# Define the 'overview plots', i.e. the most useful set of plots to explore different aspects of a simulation
overview_plots = [
            'cum_infections',
            'cum_severe',
            'cum_critical',
            'cum_deaths',
            'cum_diagnoses',
            'new_infections',
            'new_severe',
            'new_critical',
            'new_deaths',
            'new_diagnoses',
            'n_infectious',
            'n_severe',
            'n_critical',
            'n_susceptible',
            'new_tests',
            'n_symptomatic',
            'new_quarantined',
            'n_quarantined',
            'test_yield',
            'r_eff',
            ]


def get_sim_plots(which='default'):
    '''
    Specify which quantities to plot; used in sim.py.

    Args:
        which (str): either 'default' or 'overview'
    '''
    if which in [None, 'default']:
        plots = sc.odict({
                'Total counts': [
                    'cum_infections',
                    'n_infectious',
                    'cum_diagnoses',
                ],
                'Daily counts': [
                    'new_infections',
                    'new_diagnoses',
                ],
                'Health outcomes': [
                    'cum_severe',
                    'cum_critical',
                    'cum_deaths',
                ],
        })
    elif which == 'overview':
        plots = sc.dcp(overview_plots)
    else:
        errormsg = f'The choice which="{which}" is not supported'
        raise ValueError(errormsg)
    return plots


def get_scen_plots(which='default'):
    ''' Default scenario plots -- used in run.py '''
    if which in [None, 'default']:
        plots = sc.odict({
            'Cumulative infections': [
                'cum_infections',
            ],
            'New infections per day': [
                'new_infections',
            ],
            'Cumulative deaths': [
                'cum_deaths',
            ],
        })
    elif which == 'overview':
        plots = sc.dcp(overview_plots)
    else:
        errormsg = f'The choice which="{which}" is not supported'
        raise ValueError(errormsg)
    return plots

