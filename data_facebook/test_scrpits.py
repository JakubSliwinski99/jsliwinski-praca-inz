import unittest

from scripts import facebook_model
import numpy as np


class TestClass(unittest.TestCase):

    def test_create_mini_model(self):
        test_text = "To jest testowy tekst"
        test_best = "To jest najlepszy tekst"

        result = facebook_model.get_mini_model_for_a_text_facebook(test_text, test_best)

        assert np.all(result.columns == ['Intercept', 'POLARITY', 'SUBJECTIVITY', 'POSTS_LENGTH', 'SIMILARITY_TO_BEST',
                                         'TWENTY_REACTS_BAYES', 'FIFTY_REACTS_BAYES', 'HUNDRED_REACTS_BAYES',
                                         'TWO_HUNDRED_REACTS_BAYES'])

        assert 0 <= result['POLARITY'][0] <= 1
        assert 0 <= result['SUBJECTIVITY'][0] <= 1
        assert 0 <= result['SIMILARITY_TO_BEST'][0] <= 1

        assert result['TWENTY_REACTS_BAYES'] == 0 or result['TWENTY_REACTS_BAYES'] == 1