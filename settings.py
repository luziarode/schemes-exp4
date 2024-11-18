from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=0.00,
    doc='',
)

TIME_IN_MINUTES = 10
PROLIFIC_TIME_FACTOR = 6  # Factor with which Prolific calculates the maximum time. This is just a guesstimate!

SESSION_CONFIGS = [
    {
        'name': 'payment_scheme',
        'display_name': 'Payment scheme',
        'num_demo_participants': 10,
        'app_sequence': ['payment_schemes_exp4'],
        'time_in_minutes': TIME_IN_MINUTES,
        'time_max_in_seconds': (TIME_IN_MINUTES*PROLIFIC_TIME_FACTOR) * 60,  # Time after which otree times out
        'participation_fee': 6,
    }
]

SESSION_FIELDS = [
    'treatment_iterator',  # Iterator for balancing the treatment groups
    'dropout_treatments',  # List containing tuples with treatment information of drop-outs to be reassigned

]

PARTICIPANT_FIELDS = ['expiry']

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en-US'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'  # Adjust if run not on Prolific
USE_POINTS = False

ROOMS = [
    dict(
        name='survey',
        display_name='Uni HD survey room'
    ),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = ''' '''

SECRET_KEY = '5am@h_nfhh)iu$z1=d3!lr@pd!5uoebdar2i3&ieag=*&_6^27'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
