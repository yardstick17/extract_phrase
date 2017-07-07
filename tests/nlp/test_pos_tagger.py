#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from unittest import TestCase

import nltk

from nlp.pos_tagger import PosTagger


class TestPosTagger(TestCase):
    def setUp(self):
        self.sentence = 'the food was amazing'
        self.PosTagger = PosTagger(self.sentence)

    def test_pos_tag(self):
        extracted_pos_tagged = self.PosTagger.pos_tag()
        expected_pos_tagged = [('the', 'DT'), ('food', 'NN'), ('was', 'VBD'), ('amazing', 'VBG')]
        self.assertListEqual(extracted_pos_tagged, expected_pos_tagged)

    def test_get_tagger(self):
        tagger = self.PosTagger.get_tagger()
        self.assertEqual(type(tagger), nltk.tag.perceptron.PerceptronTagger)
