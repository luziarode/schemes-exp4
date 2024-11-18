import random
from . import *


class PlayerBot(Bot):
    cases = [
                "control questions correct",
                "control questions incorrect",
                "two switching points",
                "three switching points",
                "only tournament",
                "only piece rate"
            ]

    def play_round(self):

        print(self.case)

        # Generate some random data for demographics
        gender_other = C.GENDER_OTHER
        random_gender_not_other = random.randint(0, gender_other-1)
        random_birth_year = random.randint(1900, 2019)
        random_belief = random.randint(0, 5)
        random_social_ladder = random.randint(1, 10)

        # Answers to control questions
        answers_incorrect = [4,4,60,60]
        answers_tournament_correct = [0.3, 3, 114, 126]
        answers_piece_rate_correct = [1.39, 1.81, 120, 120]

        # Random fairness judgements
        fairness_overall = random.randint(0, 10)
        fairness_procedural = random.randint(0, 10)
        fairness_outcome = random.randint(0, 10)

        # Show description variables
        show_description = False
        show_scheme = False

        # Example choices for the mpl list
        decisions_one_switching_point = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
        decisions_two_switching_points = [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
        decisions_three_switching_points = [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0]
        decisions_only_tournament = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        decisions_only_piece_rate= [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

        yield GeneralInformation

        # Check treatment (odd number should not be in partial treatment in the absence of dropouts)
        if self.player.id_in_group % 2 == 0:
            expect(self.player.partial, True)
        else:
            expect(self.player.partial, False)

        yield Submission(Demographics, dict(
            gender=0,
            birth_year=1990,
            political_beliefs=random_belief,
            social_ladder=random_social_ladder,
        ))

        expect(self.player.female, False)
        expect(self.player.age, 34)

        yield Instructions

        if self.case == "control questions incorrect":
            # Submission must fail two times first in this case
            yield SubmissionMustFail(Tournament, dict(
                earning_A_tournament = answers_incorrect[0],
                earning_B_tournament = answers_incorrect[1],
                seconds_A_tournament = answers_incorrect[2],
                seconds_B_tournament = answers_incorrect[3],
                show_description_tournament=False,
            ))

            yield SubmissionMustFail(Tournament, dict(
                earning_A_tournament = answers_incorrect[0],
                earning_B_tournament = answers_incorrect[1],
                seconds_A_tournament = answers_incorrect[2],
                seconds_B_tournament = answers_incorrect[3],
                show_description_tournament=False,
            ))

            yield Submission(Tournament, dict(
                earning_A_tournament=answers_tournament_correct[0],
                earning_B_tournament=answers_tournament_correct[1],
                seconds_A_tournament=answers_tournament_correct[2],
                seconds_B_tournament=answers_tournament_correct[3],
                show_description_tournament=False,
            ))

            expect(self.player.controlq_incorrect_tournament_1, True)
            expect(self.player.controlq_incorrect_tournament_2, True)
            expect(self.player.show_description_tournament, False)
        else:
            yield Submission(Tournament, dict(
                earning_A_tournament=answers_tournament_correct[0],
                earning_B_tournament=answers_tournament_correct[1],
                seconds_A_tournament=answers_tournament_correct[2],
                seconds_B_tournament=answers_tournament_correct[3],
                show_description_tournament=False,
            ))

            expect(self.player.controlq_incorrect_tournament_1, False)
            expect(self.player.controlq_incorrect_tournament_2, False)
            expect(self.player.show_description_tournament, False)

        yield Submission(FairnessJudgements1, dict(
            fairness_overall_tournament=fairness_overall,
            show_description_judgement_tournament=show_description,
            show_scheme_judgement_tournament=show_scheme
        ))

        yield Submission(FairnessJudgementsSpec1, dict(
            fairness_procedural_tournament=fairness_procedural,
            fairness_outcome_tournament=fairness_outcome,
            show_description_judgement_tournament_spec=show_description,
            show_scheme_judgement_tournament_spec=show_scheme
        ))

        yield Submission(Transition, dict(
            show_description_transition=show_description
        ))

        if self.case == "control questions incorrect":
            # Submission must fail two times first in this case
            yield SubmissionMustFail(PieceRate, dict(
                earning_A_piece_rate = answers_incorrect[0],
                earning_B_piece_rate = answers_incorrect[1],
                seconds_A_piece_rate = answers_incorrect[2],
                seconds_B_piece_rate = answers_incorrect[3],
                show_description_piece_rate=False,
            ))

            yield SubmissionMustFail(PieceRate, dict(
                earning_A_piece_rate = answers_incorrect[0],
                earning_B_piece_rate = answers_incorrect[1],
                seconds_A_piece_rate = answers_incorrect[2],
                seconds_B_piece_rate = answers_incorrect[3],
                show_description_piece_rate=False,
            ))

            yield Submission(PieceRate, dict(
                earning_A_piece_rate=answers_piece_rate_correct[0],
                earning_B_piece_rate=answers_piece_rate_correct[1],
                seconds_A_piece_rate=answers_piece_rate_correct[2],
                seconds_B_piece_rate=answers_piece_rate_correct[3],
                show_description_piece_rate=False,
            ))

            expect(self.player.controlq_incorrect_piece_rate_1, True)
            expect(self.player.controlq_incorrect_piece_rate_2, True)
            expect(self.player.show_description_piece_rate, False)
        else:
            yield Submission(PieceRate, dict(
                earning_A_piece_rate=answers_piece_rate_correct[0],
                earning_B_piece_rate=answers_piece_rate_correct[1],
                seconds_A_piece_rate=answers_piece_rate_correct[2],
                seconds_B_piece_rate=answers_piece_rate_correct[3],
                show_description_piece_rate=False,
            ))

            expect(self.player.controlq_incorrect_piece_rate_1, False)
            expect(self.player.controlq_incorrect_piece_rate_2, False)
            expect(self.player.show_description_piece_rate, False)

        yield Submission(FairnessJudgements2, dict(
            fairness_overall_piece_rate=fairness_overall,
            show_description_judgement_piece_rate=show_description,
            show_scheme_judgement_piece_rate=show_scheme
        ))

        yield Submission(FairnessJudgementsSpec2, dict(
            fairness_procedural_piece_rate=fairness_procedural,
            fairness_outcome_piece_rate=fairness_outcome,
            show_description_judgement_piece_rate_spec=show_description,
            show_scheme_judgement_piece_rate_spec=show_scheme
        ))

        # Check if participants see the correct text on mpl page
        if self.player.partial:
            expect('will be recruited from the participants of the current online experiment', 'in', self.html)

        else:
            expect('Participants for the lab session will be recruited from the AWI lab pool, excluding', 'in',
                   self.html)

        if self.case == "one switching point":
            yield Submission(MplChoicePage, dict(
                choose_piece_rate_1=decisions_one_switching_point[0],
                choose_piece_rate_2=decisions_one_switching_point[1],
                choose_piece_rate_3=decisions_one_switching_point[2],
                choose_piece_rate_4=decisions_one_switching_point[3],
                choose_piece_rate_5=decisions_one_switching_point[4],
                choose_piece_rate_6=decisions_one_switching_point[5],
                choose_piece_rate_7=decisions_one_switching_point[6],
                choose_piece_rate_8=decisions_one_switching_point[7],
                choose_piece_rate_9=decisions_one_switching_point[8],
                choose_piece_rate_10=decisions_one_switching_point[9],
                choose_piece_rate_11=decisions_one_switching_point[10]
            ))
            expect(self.player.number_switching_points, 1)
            expect(self.player.multiple_switching_points, False)
        if self.case == "two switching points":
            yield Submission(MplChoicePage, dict(
                choose_piece_rate_1=decisions_two_switching_points[0],
                choose_piece_rate_2=decisions_two_switching_points[1],
                choose_piece_rate_3=decisions_two_switching_points[2],
                choose_piece_rate_4=decisions_two_switching_points[3],
                choose_piece_rate_5=decisions_two_switching_points[4],
                choose_piece_rate_6=decisions_two_switching_points[5],
                choose_piece_rate_7=decisions_two_switching_points[6],
                choose_piece_rate_8=decisions_two_switching_points[7],
                choose_piece_rate_9=decisions_two_switching_points[8],
                choose_piece_rate_10=decisions_two_switching_points[9],
                choose_piece_rate_11=decisions_two_switching_points[10]
                ))
            expect(self.player.number_switching_points, 2)
            expect(self.player.multiple_switching_points, True)
        elif self.case == "three switching points":
            yield Submission(MplChoicePage, dict(
                choose_piece_rate_1=decisions_three_switching_points[0],
                choose_piece_rate_2=decisions_three_switching_points[1],
                choose_piece_rate_3=decisions_three_switching_points[2],
                choose_piece_rate_4=decisions_three_switching_points[3],
                choose_piece_rate_5=decisions_three_switching_points[4],
                choose_piece_rate_6=decisions_three_switching_points[5],
                choose_piece_rate_7=decisions_three_switching_points[6],
                choose_piece_rate_8=decisions_three_switching_points[7],
                choose_piece_rate_9=decisions_three_switching_points[8],
                choose_piece_rate_10=decisions_three_switching_points[9],
                choose_piece_rate_11=decisions_three_switching_points[10]
                ))
            expect(self.player.number_switching_points, 3)
            expect(self.player.multiple_switching_points, True)
        # Case where player only picks tournament
        elif self.case == "only_tournament":
            yield Submission(MplChoicePage, dict(
                choose_piece_rate_1=decisions_only_tournament[0],
                choose_piece_rate_2=decisions_only_tournament[1],
                choose_piece_rate_3=decisions_only_tournament[2],
                choose_piece_rate_4=decisions_only_tournament[3],
                choose_piece_rate_5=decisions_only_tournament[4],
                choose_piece_rate_6=decisions_only_tournament[5],
                choose_piece_rate_7=decisions_only_tournament[6],
                choose_piece_rate_8=decisions_only_tournament[7],
                choose_piece_rate_9=decisions_only_tournament[8],
                choose_piece_rate_10=decisions_only_tournament[9],
                choose_piece_rate_11=decisions_only_tournament[10]
            ))
            expect(self.player.number_switching_points, 0)
            expect(self.player.multiple_switching_points, False)
        else:
            yield Submission(MplChoicePage, dict(
                choose_piece_rate_1=decisions_only_piece_rate[0],
                choose_piece_rate_2=decisions_only_piece_rate[1],
                choose_piece_rate_3=decisions_only_piece_rate[2],
                choose_piece_rate_4=decisions_only_piece_rate[3],
                choose_piece_rate_5=decisions_only_piece_rate[4],
                choose_piece_rate_6=decisions_only_piece_rate[5],
                choose_piece_rate_7=decisions_only_piece_rate[6],
                choose_piece_rate_8=decisions_only_piece_rate[7],
                choose_piece_rate_9=decisions_only_piece_rate[8],
                choose_piece_rate_10=decisions_only_piece_rate[9],
                choose_piece_rate_11=decisions_only_piece_rate[10]
            ))
            expect(self.player.number_switching_points, 0)
            expect(self.player.multiple_switching_points, False)

        # Check if last page contains the right payment scheme
        if self.player.selected_option == 0:
            expect('<b>tournament payment mechanism</b> and receive <b>€6', 'in', self.html)
        else:
            expect('piece-rate payment mechanism', 'in', self.html)
            expect(f'€{C.PRICES_PIECE_RATE[self.player.selected_decision - 1]}', 'in', self.html)