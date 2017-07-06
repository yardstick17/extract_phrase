import collections

import logging
import nltk
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from tqdm import tqdm

from nlp.chunker import Chunker
from nlp.pattern_grammer import PatternGrammar
from nlp.pos_tagger import PosTagger
from nlp.string_cleaner import StringCleaner

MULTIPLE_WHITESPACE_REGEX = nltk.re.compile(r'\s+')

import click


def merge_two_dict(dict_x, dict_y):
    """
    :param dict_x: {'a': [3, 4], 'b': [6]}
    :param dict_y: {'c': [3], 'a': [1, 2]}
    :return: {'c': [3], 'a': [3, 4, 1, 2], 'b': [6]}
    """
    dict_z = dict_x.copy()  # Never modify input param , or take inplace as param for explicit use case
    for key, value in dict_y.items():
        if dict_z.get(key):
            dict_z[key].extend(value)
        else:
            dict_z[key] = value
    return dict_z


def get_phrase_list(grammar, pos_tagged_sentences):
    chunk_dict = {}
    chunker_obj = Chunker(grammar)

    for pos_tagged_sentence in pos_tagged_sentences:
        single_chunk_dict = chunker_obj.chunk_pos_tagged_sentence(pos_tagged_sentence)
        chunk_dict = merge_two_dict(chunk_dict, single_chunk_dict)

    phrase_list = list()
    for rule, pos_tagged_chunk_list in chunk_dict.items():
        for pos_tagged_phrase_chunk in pos_tagged_chunk_list:
            phrase = ' '.join(list(map(lambda x: x[0], pos_tagged_phrase_chunk)))
            phrase_list.append(phrase)
    return phrase_list


valid_phrase_grammar_clause = ['NN_all', 'NN_CC_JJ_multi']


def get_phrases(compiled_grammar, pos_tagged_sentences, testing_clauses):
    phrase_list = list()
    for grammar in testing_clauses:
        phrase = get_phrase_list(grammar=compiled_grammar[grammar], pos_tagged_sentences=pos_tagged_sentences)
        phrase_list.extend(phrase)
    return phrase_list


# @click.command()
# @click.option('--text', help='text or string in which top phrases need to be extracted')
# @click.option('--top_k', default=100, help='text or string in which top phrases need to be extracted')
def frequent_phrases(text, top_k):
    sentences = nltk.sent_tokenize(text)
    compiled_grammar = PatternGrammar().init_all_clause()
    pos_tagged_sentences = [PosTagger(sentence=sentence).pos_tag() for sentence in sentences]
    testing_clauses = ['NN_all', 'NN_CC_JJ_multi']
    phrase_list = get_phrases(compiled_grammar, pos_tagged_sentences, testing_clauses)
    count_object = collections.Counter(phrase_list)
    return count_object.most_common(n=top_k)


def extract_phrases(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
        lines_list = [StringCleaner.clean(line).rstrip('\n') for line in lines]
        text = ' '.join(lines_list)
        top_phrases = frequent_phrases(text, top_k=100)
        logging.info('Got total {} frequent phrases.'.format(len(top_phrases)))
        logging.info('Frequent phrases:%s', top_phrases[:5])
        return dict(top_phrases)


def get_ngrams(text, n):
    n_grams = ngrams(word_tokenize(text), n)
    return [' '.join(grams).strip() for grams in n_grams]


@click.command()
@click.option('--input_file', help='The input file need to be processed')
@click.option('--output_file', help='The out file need to be written after processing')
def process_large_text_file(input_file, output_file):
    logging.info('Evaluating file: {} for extracting frequent tags'.format(input_file))

    frequent_phrases = set(extract_phrases(input_file).keys())
    with open(input_file, "r") as review_text, open(output_file, "a") as updated_review_text:
        lines = review_text.readlines()
        total = len(lines)
        for index, line in tqdm(enumerate(lines), total=total, unit='line'):
            two_grams = get_ngrams(line, 2)
            for gram in two_grams:
                if gram in frequent_phrases:
                    line = line.replace(gram, '_'.join(gram.split()))

            updated_review_text.writelines(line)


if __name__ == '__main__':
    logging.basicConfig(format='[%(asctime)s] %(levelname)s : %(message)s', level=logging.INFO)
    process_large_text_file()
