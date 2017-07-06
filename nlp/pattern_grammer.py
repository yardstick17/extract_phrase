#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import nltk

compiled_grammar = {}


class PatternGrammar:
    @property
    def noun_and_adj_phrases(self):
        noun_phrase_extractor = {
            'NN_all': """NP: {(<FW|NN|NN.>+<JJ|JJ.|VB|VB.>?)+<JJ|JJ.|VB|VB.>*<NN|NN.>+}""",
            'NN_CC_JJ_multi': """NP:     { (<,|CC>*<JJ|JJ.>+<NN|NN.>+)+ }""",
        }
        return noun_phrase_extractor

    def get_key_clause_grammar(self, key_clause):
        global compiled_grammar
        grammar = compiled_grammar.get(key_clause, None)
        if grammar is None:
            grammar = self.get_noun_and_adj_phrases_grammar(key_clause)
            compiled_grammar[key_clause] = grammar
        return grammar

    @staticmethod
    def get_noun_and_adj_phrases_grammar(key_clause):
        return nltk.RegexpParser(PatternGrammar().noun_and_adj_phrases[key_clause])

    def init_all_clause(self):
        global compiled_grammar
        valid_clause = list(self.noun_and_adj_phrases.keys())
        for clause in valid_clause:
            _ = self.get_key_clause_grammar(clause)
        return compiled_grammar
