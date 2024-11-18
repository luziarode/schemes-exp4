import itertools
import time
from datetime import datetime
from otree.api import *
import random

# Conditions from Experiment 2
# condition | situation | name       | experiment 2 name
#     1     |     1     | piece_rate | Low inequality with base pay (Low_with base pay)
#     3     |     3     | tournament | High inequality, with time advantage (High_time bonus) 14

# Treatments Experiment 3:
# T1: Impartial observer -  rates payment schemes, but is never affected
# T2: Partial observer - rates payment schemes, might get reinvited to play them


class C(BaseConstants):
    NAME_IN_URL = 'uni_hd_survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    # Designate "Other" options in demographics here for later use
    GENDER_OTHER = 2
    CONTACT = 'christoph.becker@awi.uni-heidelberg.de'

    # Expected answers to the control questions
    EXPECTED = {
        'piece_rate': (1.39, 1.81, 120, 120),
        'tournament': (0.3, 3.00, 114, 126),
        'flat': (1.6, 1.6, 120, 120)
    }

    # Multiple price list options
    PRICES_PIECE_RATE = [6.0, 5.7, 5.4, 5.1, 4.8, 4.5, 4.2, 3.9, 3.6, 3.3, 3.0]
    PRICE_TOURNAMENT = 6


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Timeout
    has_timeout = models.BooleanField(initial=False)

    # Treatment variables (piece_rate=1 if piece rate was seen first)
    piece_rate = models.BooleanField()

    # Demographic variables
    age = models.IntegerField()

    gender = models.IntegerField(
        label="1. Please indicate your gender:",
        choices=[[0, 'Male'], [1, 'Female'], [C.GENDER_OTHER, 'Other'],
                 [-1, 'Prefer not to answer']],
        widget=widgets.RadioSelect,
    )

    female = models.BooleanField(initial=False, blank=True)

    other_gender = models.StringField(blank=True, verbose_name="Other: ")

    birth_year = models.IntegerField(
        label="2. What is your year of birth? (YYYY, leave blank if you prefer not to answer):",
        min=1900, max=2019, blank=True)

    political_beliefs = models.IntegerField(
        label="3. On a continuum from liberal to conservative, how would you describe your "
              "political beliefs?",
        choices=[
            [0, 'Strongly left-leaning'],
            [1, 'Moderately left-leaning'],
            [2, 'Slightly left-leaning'],
            [3, 'Slightly right-leaning'],
            [4, 'Moderately right-leaning'],
            [5, 'Strongly right-leaning'],
            [-1, 'Prefer not to answer']
        ],
        widget=widgets.RadioSelect,
    )

    social_ladder = models.IntegerField(
        choices=[[10, '10'],
                 [9, '9'],
                 [8, '8'],
                 [7, '7'],
                 [6, '6'],
                 [5, '5'],
                 [4, '4'],
                 [3, '3'],
                 [2, '2'],
                 [1, '1'],
                 [-1, 'Prefer not to answer']], widget=widgets.RadioSelect, verbose_name=""
    )

    # Answers to control questions
    earning_A_tournament = models.FloatField(verbose_name="")
    earning_B_tournament = models.FloatField(verbose_name="")
    seconds_A_tournament = models.IntegerField(verbose_name="")
    seconds_B_tournament = models.IntegerField(verbose_name="")

    earning_A_piece_rate = models.FloatField(verbose_name="")
    earning_B_piece_rate = models.FloatField(verbose_name="")
    seconds_A_piece_rate = models.IntegerField(verbose_name="")
    seconds_B_piece_rate = models.IntegerField(verbose_name="")

    earning_A_flat = models.FloatField(verbose_name="")
    earning_B_flat = models.FloatField(verbose_name="")
    seconds_A_flat = models.IntegerField(verbose_name="")
    seconds_B_flat = models.IntegerField(verbose_name="")

    # Recording of number of errors in the control questions

    # Temporary trackers, reused on both pages
    control_question_incorrect_1 = models.BooleanField(initial=False)
    control_question_incorrect_2 = models.BooleanField(initial=False)

    # Actual trackers in the data set
    controlq_incorrect_tournament_1 = models.BooleanField(initial=False)
    controlq_incorrect_tournament_2 = models.BooleanField(initial=False)
    controlq_incorrect_piece_rate_1 = models.BooleanField(initial=False)
    controlq_incorrect_piece_rate_2 = models.BooleanField(initial=False)
    controlq_incorrect_flat_rate_1 = models.BooleanField(initial=False)
    controlq_incorrect_flat_rate_2 = models.BooleanField(initial=False)

    # Recording of participant looking at task descriptions/payment schemes again
    show_description_tournament = models.BooleanField(initial=False, blank=True)
    show_description_judgement_tournament = models.BooleanField(initial=False, blank=True)
    show_scheme_judgement_tournament = models.BooleanField(initial=False, blank=True)
    show_description_judgement_tournament_spec = models.BooleanField(initial=False, blank=True)
    show_scheme_judgement_tournament_spec = models.BooleanField(initial=False, blank=True)

    show_description_piece_rate = models.BooleanField(initial=False, blank=True)
    show_description_judgement_piece_rate = models.BooleanField(initial=False, blank=True)
    show_scheme_judgement_piece_rate = models.BooleanField(initial=False, blank=True)
    show_description_judgement_piece_rate_spec = models.BooleanField(initial=False, blank=True)
    show_scheme_judgement_piece_rate_spec = models.BooleanField(initial=False, blank=True)

    show_description_transition = models.BooleanField(initial=False, blank=True)

    show_description_flat = models.BooleanField(initial=False, blank=True)
    show_description_judgement_flat = models.BooleanField(initial=False, blank=True)
    show_scheme_judgement_flat = models.BooleanField(initial=False, blank=True)
    show_description_judgement_flat_spec = models.BooleanField(initial=False, blank=True)
    show_scheme_judgement_flat_spec = models.BooleanField(initial=False, blank=True)

    # Fairness judgements
    fairness_overall_tournament = models.IntegerField(label="",
                                                     widget=widgets.RadioSelectHorizontal,
                                                     choices=list(range(0, 11)))
    fairness_procedural_tournament = models.IntegerField(label="",
                                                        widget=widgets.RadioSelectHorizontal,
                                                        choices=list(range(0, 11)))
    fairness_outcome_tournament = models.IntegerField(label="",
                                                     widget=widgets.RadioSelectHorizontal,
                                                     choices=list(range(0, 11)))

    fairness_overall_piece_rate = models.IntegerField(label="",
                                                     widget=widgets.RadioSelectHorizontal,
                                                     choices=list(range(0, 11)))
    fairness_procedural_piece_rate = models.IntegerField(label="",
                                                        widget=widgets.RadioSelectHorizontal,
                                                        choices=list(range(0, 11)))
    fairness_outcome_piece_rate = models.IntegerField(label="",
                                                     widget=widgets.RadioSelectHorizontal,
                                                     choices=list(range(0, 11)))

    fairness_overall_flat = models.IntegerField(label="",
                                                     widget=widgets.RadioSelectHorizontal,
                                                     choices=list(range(0, 11)))
    fairness_procedural_flat = models.IntegerField(label="",
                                                        widget=widgets.RadioSelectHorizontal,
                                                        choices=list(range(0, 11)))
    fairness_outcome_flat = models.IntegerField(label="",
                                                     widget=widgets.RadioSelectHorizontal,
                                                     choices=list(range(0, 11)))


# Functions
def creating_session(subsession: Subsession):
    # Treatment options: 0 for tournament first, 1 for piece rate first
    piece_rate = [False, True]

    # Cycle over treatment options
    subsession.session.treatment_iterator = itertools.cycle(piece_rate)
    subsession.session.dropout_treatments = []


def choose_treatment(player: Player):
    # Set expiry time to current time plus extra time
    player.participant.expiry = time.time() + player.subsession.session.config['time_max_in_seconds']

    try:
        # Check if there have been any drop-outs whose treatments should be reassigned
        player.piece_rate = player.session.dropout_treatments.pop()
    except IndexError:  # If there is an IndexError, dropout_treatments has been empty
        player.piece_rate = next(player.subsession.session.treatment_iterator)


def age(player: Player):
    player.age = datetime.now().year - player.birth_year


def timeout_handler(player: Player):
    player.has_timeout = True
    player.session.dropout_treatments.append(player.piece_rate)


def control_questions_errors(player, q, fields, scheme):
    expected = C.EXPECTED[scheme]
    error_messages1 = ['Please enter the correct earning of worker A.',
                       'Please enter the correct earning of worker B.',
                       'Please enter the correct time for worker A.',
                       'Please enter the correct time for worker B.']
    error_messages2 = ['Please enter the correct earning of worker A. The correct answer is {0}.'.format(expected[0]),
                       'Please enter the correct earning of worker B. The correct answer is {0}.'.format(expected[1]),
                       'Please enter the correct time for worker A. The correct answer is {0} seconds.'.format(expected[2]),
                       'Please enter the correct time for worker B. The correct answer is {0} seconds.'.format(expected[3])]
    errors_displayed = dict()

    i = 0
    for field in fields:
        if q[field] != expected[i]:
            if player.control_question_incorrect_1:
                errors_displayed[field] = error_messages2[i]
            else:
                errors_displayed[field] = error_messages1[i]
        i += 1

    if errors_displayed:
        if not player.control_question_incorrect_1:
            # Mark first time control questions are wrong
            player.control_question_incorrect_1 = True
        elif player.control_question_incorrect_1 and not player.control_question_incorrect_2:
            # Second time
            player.control_question_incorrect_2 = True
        else:
            # Continue after second time
            return None
        return errors_displayed
    # Directly go on if there are no errors
    return None


# Pages
class GeneralInformation(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return {'show_up_fee': player.session.config['participation_fee'],
                'time': player.session.config['time_in_minutes'],
                'time_max': int(player.session.config['time_max_in_seconds']/60)
                }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        choose_treatment(player)


class Demographics(Page):
    form_model = Player
    form_fields = [
        'gender',
        'other_gender',
        'female',
        'birth_year',
        'social_ladder',
        'political_beliefs',
    ]

    @staticmethod
    def is_displayed(player: Player):
        return not player.has_timeout

    @staticmethod
    def get_timeout_seconds(player):  # Use the timeout defined in the session config
        return player.participant.expiry - time.time()

    @staticmethod
    def error_message(player: Player, educ):
        if educ['gender'] != C.GENDER_OTHER and (educ['other_gender'] is not None and
                                                       educ['other_gender'] != ""):
            return "Question 1: Fill in the field labeled 'Other' only if you have ticked the " \
                   "button labeled 'other'"
        if educ['gender'] == C.GENDER_OTHER and (educ['other_gender'] is None or
                                                       educ['other_gender'] == ""):
            return "Question 1: Please indicate your gender or select 'Prefer not to answer'"
        return None

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            timeout_handler(player)
        if player.gender == 1:
            player.female = True
        try:
            if player.birth_year is not None:
                age(player)
        except TypeError:
            pass  # Necessary because oTree does not like "None"


class Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return not player.has_timeout

    @staticmethod
    def get_timeout_seconds(player):  # Use the timeout defined in the session config
        return player.participant.expiry - time.time()

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            timeout_handler(player)


class Tournament(Page):
    form_model = Player
    form_fields = ['earning_A_tournament', 'earning_B_tournament', 'seconds_A_tournament', 'seconds_B_tournament',
                   'show_description_tournament']

    @staticmethod
    def is_displayed(player: Player):
        return not player.has_timeout

    @staticmethod
    def get_timeout_seconds(player):  # Use the timeout defined in the session config
        return player.participant.expiry - time.time()

    @staticmethod
    def error_message(player: Player, q):
        fields = ['earning_A_tournament', 'earning_B_tournament', 'seconds_A_tournament', 'seconds_B_tournament']
        return control_questions_errors(player, q, fields, 'tournament')

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Transcribe control question error recording and reset variables for the function
        player.controlq_incorrect_tournament_1 = player.control_question_incorrect_1
        player.controlq_incorrect_tournament_2 = player.control_question_incorrect_2
        player.control_question_incorrect_1 = player.control_question_incorrect_2 = False

        if timeout_happened:
            timeout_handler(player)


class FairnessTournamentOverall(Page):
    form_model = Player
    form_fields = ['fairness_overall_tournament', 'show_description_judgement_tournament', 'show_scheme_judgement_tournament']

    @staticmethod
    def is_displayed(player: Player):
        return not player.has_timeout

    @staticmethod
    def get_timeout_seconds(player):  # Use the timeout defined in the session config
        return player.participant.expiry - time.time()

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            timeout_handler(player)


class FairnessTournamentSpec(Page):
    form_model = Player
    form_fields = ['fairness_procedural_tournament', 'fairness_outcome_tournament',
                   'show_description_judgement_tournament_spec', 'show_scheme_judgement_tournament_spec']

    @staticmethod
    def is_displayed(player: Player):
        return not player.has_timeout

    @staticmethod
    def get_timeout_seconds(player):  # Use the timeout defined in the session config
        return player.participant.expiry - time.time()

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            timeout_handler(player)


class PieceRate(Page):
    form_model = Player
    form_fields = ['earning_A_piece_rate', 'earning_B_piece_rate', 'seconds_A_piece_rate', 'seconds_B_piece_rate',
                   'show_description_piece_rate']

    @staticmethod
    def is_displayed(player: Player):
        return not player.has_timeout and player.piece_rate

    @staticmethod
    def get_timeout_seconds(player):  # Use the timeout defined in the session config
        return player.participant.expiry - time.time()

    @staticmethod
    def error_message(player: Player, q):
        fields = ['earning_A_piece_rate', 'earning_B_piece_rate', 'seconds_A_piece_rate', 'seconds_B_piece_rate']
        return control_questions_errors(player, q, fields, 'piece_rate')

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Transcribe control question error recording and reset variables for the function
        player.controlq_incorrect_piece_rate_1 = player.control_question_incorrect_1
        player.controlq_incorrect_piece_rate_2 = player.control_question_incorrect_2

        if timeout_happened:
            timeout_handler(player)


class FairnessPieceRateOverall(Page):
    form_model = Player
    form_fields = ['fairness_overall_piece_rate', 'show_description_judgement_piece_rate', 'show_scheme_judgement_piece_rate']

    @staticmethod
    def is_displayed(player: Player):
        return not player.has_timeout and player.piece_rate

    @staticmethod
    def get_timeout_seconds(player):  # Use the timeout defined in the session config
        return player.participant.expiry - time.time()

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            timeout_handler(player)


class FairnessPieceRateSpec(Page):
    form_model = Player
    form_fields = ['fairness_procedural_piece_rate', 'fairness_outcome_piece_rate',
                   'show_description_judgement_piece_rate_spec', 'show_scheme_judgement_piece_rate_spec']

    @staticmethod
    def is_displayed(player: Player):
        return not player.has_timeout and player.piece_rate

    @staticmethod
    def get_timeout_seconds(player):  # Use the timeout defined in the session config
        return player.participant.expiry - time.time()

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            timeout_handler(player)


class Transition(Page):
    form_model = 'player'
    form_fields = ['show_description_transition']

    @staticmethod
    def is_displayed(player: Player):
        return not player.has_timeout


class FlatPayment(Page):
    form_model = Player
    form_fields = ['earning_A_flat', 'earning_B_flat', 'seconds_A_flat', 'seconds_B_flat',
                   'show_description_flat']

    @staticmethod
    def is_displayed(player: Player):
        return not player.has_timeout and not player.piece_rate

    @staticmethod
    def get_timeout_seconds(player):  # Use the timeout defined in the session config
        return player.participant.expiry - time.time()

    @staticmethod
    def error_message(player: Player, q):
        fields = ['earning_A_flat', 'earning_B_flat', 'seconds_A_flat', 'seconds_B_flat']
        return control_questions_errors(player, q, fields, 'flat')

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Transcribe control question error recording and reset variables for the function
        player.controlq_incorrect_piece_rate_1 = player.control_question_incorrect_1
        player.controlq_incorrect_piece_rate_2 = player.control_question_incorrect_2

        if timeout_happened:
            timeout_handler(player)


class FairnessFlatOverall(Page):
    form_model = Player
    form_fields = ['fairness_overall_flat', 'show_description_judgement_flat', 'show_scheme_judgement_flat']

    @staticmethod
    def is_displayed(player: Player):
        return not player.has_timeout and not player.piece_rate

    @staticmethod
    def get_timeout_seconds(player):  # Use the timeout defined in the session config
        return player.participant.expiry - time.time()

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            timeout_handler(player)


class FairnessFlatSpec(Page):
    form_model = Player
    form_fields = ['fairness_procedural_flat', 'fairness_outcome_flat',
                   'show_description_judgement_flat_spec', 'show_scheme_judgement_flat_spec']

    @staticmethod
    def is_displayed(player: Player):
        return not player.has_timeout and not player.piece_rate

    @staticmethod
    def get_timeout_seconds(player):  # Use the timeout defined in the session config
        return player.participant.expiry - time.time()

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            timeout_handler(player)


class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return not player.has_timeout

    @staticmethod
    def vars_for_template(player: Player):
        link = "<a href='{0}'>{1}</a>".format(player.session.config['limesurvey_link'] + f'&PAYMENTCODE={player.participant.label}',
                                              'Click here to confirm your participation and proceed to payoff survey.')

        return {
            'link': link,
        }


class NoConsentTimeout(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.has_timeout


page_sequence = [GeneralInformation, Demographics, Instructions,
                 Tournament, FairnessTournamentOverall, FairnessTournamentSpec, Transition,
                 PieceRate, FairnessPieceRateOverall, FairnessPieceRateSpec,
                  FlatPayment, FairnessFlatOverall, FairnessFlatSpec,
                 Results, NoConsentTimeout]
