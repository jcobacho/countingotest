from django.forms import inlineformset_factory
from django.test import TestCase


# Create your tests here.
from announcement.forms import AnnouncementForm, CandidateForm, UserForm
from announcement.models import Candidate, CandidateTech
from core.tests.factories import AnnouncementFactory, UserFactory, TechnologyFactory


class AnnouncementFormTestCase(TestCase):

    def setUp(self):

        self.announcement = AnnouncementFactory.create()
        self.user = UserFactory.create()

    def test_announcement_form_all_fields(self):

        form = AnnouncementForm({'name': "hola", "description": "mundo"})
        self.assertEqual(form.is_valid(), True)

    def test_announcement_form_missing_description(self):

        form = AnnouncementForm({'name': "hola"})
        self.assertEqual(form.is_valid(), True)

    def test_announcement_form_missing_name(self):

        form = AnnouncementForm({'description': "mundo"})
        self.assertEqual(form.is_valid(), False)


class CandidateFormTestCase(TestCase):

    def setUp(self):

        self.announcement = AnnouncementFactory.create()
        self.user = UserFactory.create()

    def test_candidate_form_all_fields(self):

        form = CandidateForm({'announcement': self.announcement.id})
        self.assertEqual(form.is_valid(), True)

    def test_candidate_form_missing_announcement(self):

        form = CandidateForm({})
        self.assertEqual(form.is_valid(), False)

    def test_candidate_form_wrong_announcement(self):

        form = CandidateForm({'announcement': 3})
        self.assertEqual(form.is_valid(), False)


class UserFormTestCase(TestCase):

    def setUp(self):

        self.announcement = AnnouncementFactory.create()
        self.user = UserFactory.create()

    def test_user_form_all_fields(self):

        form = UserForm({'first_name': "john", 'middle_name': "doe", 'last_name': 'ben', 'ci': '90111827468', 'age': 22,
                         'sex': 'm', "address": "LALALA"})

        self.assertEqual(form.is_valid(), True)

    def test_user_form_no_middle_name(self):

        form = UserForm({'first_name': "john", 'last_name': 'ben', 'ci': '90111827468', 'age': 22,
                         'sex': 'm', "address": "LALALA"})

        self.assertEqual(form.is_valid(), True)

    def test_user_form_wrong_age(self):

        form = UserForm({'first_name': "john", 'middle_name': "doe", 'last_name': 'ben', 'ci': '90111827468', 'age': -1,
                                 'sex': 'm', "address": "LALALA"})

        self.assertEqual(form.is_valid(), False)
        self.assertEqual('age' in form.errors.as_json(), True)

    def test_user_form_0_age(self):

        form = UserForm({'first_name': "john", 'middle_name': "doe", 'last_name': 'ben', 'ci': '90111827468', 'age': 0,
                                 'sex': 'm', "address": "LALALA"})

        self.assertEqual(form.is_valid(), False)
        self.assertEqual('age' in form.errors.as_json(), True)

    def test_user_form_long_ci(self):

        form = UserForm({'ci': '901118274689090'})
        self.assertEqual(form.is_valid(), False)
        self.assertEqual('ci' in form.errors.as_json(), True)

    def test_user_form_short_ci(self):

        form = UserForm({'ci': '9011'})
        self.assertEqual(form.is_valid(), False)
        self.assertEqual('ci' in form.errors.as_json(), True)

    def test_user_form_words_in_ci(self):

        form = UserForm({'ci': '9011sdfa22'})
        self.assertEqual(form.is_valid(), False)
        self.assertEqual('ci' in form.errors.as_json(), True)


class CandidateTechFormsetTestCase(TestCase):

    def setUp(self):

        self.technologies = TechnologyFactory.create_batch(3)

    def test_candidate_tech_formset_all_fields_correct(self):
        data = {'candidatetech_set-TOTAL_FORMS': 1,
                'candidatetech_set-INITIAL_FORMS': 0,
                'candidatetech_set-MIN_NUM_FORMS': 1,
                'candidatetech_set-MAX_NUM_FORMS': 1000,
                'candidatetech_set-0-tech': self.technologies[0].id,
                'candidatetech_set-0-years_of_experience': 4,
                }

        formset_class = inlineformset_factory(Candidate, CandidateTech, fields=('tech', 'years_of_experience'),
                              min_num=1, validate_min=True, extra=0, can_delete=False)

        formset = formset_class(data)

        self.assertEqual(formset.is_valid(), True)

    def test_candidate_tech_formset_empty(self):
        data = {'candidatetech_set-TOTAL_FORMS': 1,
                'candidatetech_set-INITIAL_FORMS': 0,
                'candidatetech_set-MIN_NUM_FORMS': 1,
                'candidatetech_set-MAX_NUM_FORMS': 1000,

                }

        formset_class = inlineformset_factory(Candidate, CandidateTech, fields=('tech', 'years_of_experience'),
                              min_num=1, validate_min=True, extra=0, can_delete=False)

        formset = formset_class(data)

        self.assertEqual(formset.is_valid(), False)
        self.assertEqual(any(['tech' in e for e in formset.errors]), True)
        self.assertEqual(any(['years_of_experience' in e for e in formset.errors]), True)

    def test_candidate_tech_formset_missing_field(self):
        data = {'candidatetech_set-TOTAL_FORMS': 1,
                'candidatetech_set-INITIAL_FORMS': 0,
                'candidatetech_set-MIN_NUM_FORMS': 1,
                'candidatetech_set-MAX_NUM_FORMS': 1000,
                'candidatetech_set-0-tech': self.technologies[0].id,

                }

        formset_class = inlineformset_factory(Candidate, CandidateTech, fields=('tech', 'years_of_experience'),
                                                     min_num=1, validate_min=True, extra=0, can_delete=False)

        formset = formset_class(data)

        self.assertEqual(formset.is_valid(), False)
        self.assertEqual(any(['years_of_experience' in e for e in formset.errors]), True)

    def test_candidate_tech_formset_age_0(self):
        data = {'candidatetech_set-TOTAL_FORMS': 1,
                'candidatetech_set-INITIAL_FORMS': 0,
                'candidatetech_set-MIN_NUM_FORMS': 1,
                'candidatetech_set-MAX_NUM_FORMS': 1000,
                'candidatetech_set-0-years_of_experience': 0,

                }

        formset_class = inlineformset_factory(Candidate, CandidateTech, fields=('tech', 'years_of_experience'),
                                                     min_num=1, validate_min=True, extra=0, can_delete=False)

        formset = formset_class(data)

        self.assertEqual(formset.is_valid(), False)
        self.assertEqual(any(['years_of_experience' in e for e in formset.errors]), True)

    def test_candidate_tech_formset_wrong_tech(self):
        data = {'candidatetech_set-TOTAL_FORMS': 1,
                'candidatetech_set-INITIAL_FORMS': 0,
                'candidatetech_set-MIN_NUM_FORMS': 1,
                'candidatetech_set-MAX_NUM_FORMS': 1000,
                'candidatetech_set-0-tech': 10,
                'candidatetech_set-0-years_of_experience': 5,

                }

        formset_class = inlineformset_factory(Candidate, CandidateTech, fields=('tech', 'years_of_experience'),
                                                     min_num=1, validate_min=True, extra=0, can_delete=False)

        formset = formset_class(data)

        self.assertEqual(formset.is_valid(), False)
        self.assertEqual(any(['tech' in e for e in formset.errors]), True)

    def test_candidate_tech_formset_multiple_techs_duplicate(self):
        data = {'candidatetech_set-TOTAL_FORMS': 2,
                'candidatetech_set-INITIAL_FORMS': 0,
                'candidatetech_set-MIN_NUM_FORMS': 1,
                'candidatetech_set-MAX_NUM_FORMS': 1000,
                'candidatetech_set-0-tech': self.technologies[0].id,
                'candidatetech_set-0-years_of_experience': 3,
                'candidatetech_set-1-tech': self.technologies[0].id,
                'candidatetech_set-1-years_of_experience': 5,

                }

        formset_class = inlineformset_factory(Candidate, CandidateTech, fields=('tech', 'years_of_experience'),
                                                     min_num=1, validate_min=True, extra=0, can_delete=False)

        formset = formset_class(data)

        self.assertEqual(formset.is_valid(), False)
        self.assertEqual(any(['__all__' in e for e in formset.errors]), True)

    def test_candidate_tech_formset_multiple_techs(self):
        data = {'candidatetech_set-TOTAL_FORMS': 2,
                'candidatetech_set-INITIAL_FORMS': 0,
                'candidatetech_set-MIN_NUM_FORMS': 1,
                'candidatetech_set-MAX_NUM_FORMS': 1000,
                'candidatetech_set-0-tech': self.technologies[0].id,
                'candidatetech_set-0-years_of_experience': 3,
                'candidatetech_set-1-tech': self.technologies[1].id,
                'candidatetech_set-1-years_of_experience': 5,

                }

        formset_class = inlineformset_factory(Candidate, CandidateTech, fields=('tech', 'years_of_experience'),
                                                     min_num=1, validate_min=True, extra=0, can_delete=False)

        formset = formset_class(data)

        self.assertEqual(formset.is_valid(), True)