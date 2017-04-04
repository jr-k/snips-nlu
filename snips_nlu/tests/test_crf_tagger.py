import cPickle
import json
import unittest

from sklearn_crfsuite import CRF

from snips_nlu.languages import Language
from snips_nlu.slot_filler.crf_tagger import CRFTagger
from snips_nlu.slot_filler.crf_utils import Tagging


class TestCRFTagger(unittest.TestCase):
    def test_should_be_serializable(self):
        # Given
        crf_model = CRF(min_freq=None, c1=.1, c2=.1, max_iterations=None,
                        verbose=False)

        features_signatures = [
            {
                "qual_name": "snips_nlu.features.get_shape_ngram_fn",
                "args": {"n": 1},
                "offsets": [0]
            },
            {
                "qual_name": "snips_nlu.features.get_shape_ngram_fn",
                "args": {"n": 2},
                "offsets": [-1, 0]
            }
        ]
        tagging = Tagging.BILOU
        tagger = CRFTagger(crf_model, features_signatures, tagging,
                           Language.EN)

        # When
        tagger_dict = tagger.to_dict()

        # Then
        try:
            json.dumps(tagger_dict).decode("utf8")
        except:
            self.fail("Tagger dict should be json serializable to utf-8")

        model_pkl = cPickle.dumps(crf_model)
        expected_dict = {
            "@class_name": "CRFTagger",
            "@module_name": "snips_nlu.slot_filler.crf_tagger",
            "crf_model": model_pkl,
            "language": "en",
            "features_signatures": [
                {
                    'args': {'n': 1},
                    'offsets': [0],
                    'qual_name': 'snips_nlu.features.get_shape_ngram_fn'
                },
                {
                    'args': {'n': 2},
                    'offsets': [-1, 0],
                    'qual_name': 'snips_nlu.features.get_shape_ngram_fn'
                }
            ],
            "tagging": 2,
            "fitted": False
        }

        self.assertDictEqual(tagger_dict, expected_dict)

    def test_should_be_deserializable(self):
        # Given
        crf_model = CRF(min_freq=None, c1=.1, c2=.1, max_iterations=None,
                        verbose=False)

        features_signatures = [
            {
                "qual_name": "snips_nlu.features.get_shape_ngram_fn",
                "args": {"n": 1},
                "offsets": [0]
            },
            {
                "qual_name": "snips_nlu.features.get_shape_ngram_fn",
                "args": {"n": 2},
                "offsets": [-1, 0]
            }
        ]
        tagging = Tagging.BILOU
        tagger = CRFTagger(crf_model, features_signatures, tagging,
                           language=Language.EN)
        tagger_dict = tagger.to_dict()
        tagger_json = json.dumps(tagger_dict).decode("utf8")
        try:
            _ = CRFTagger.from_dict(json.loads(tagger_json))
        except:
            self.fail("Tagger should be deserializable from dict with "
                      "unicode values")

        # When
        deserialized_tagger = CRFTagger.from_dict(tagger_dict)

        # Then
        self.assertEqual(deserialized_tagger, tagger)