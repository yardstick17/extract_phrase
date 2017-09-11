import collections
import logging
from concurrent.futures import ProcessPoolExecutor
from functools import partial

import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from tqdm import tqdm

from nlp.chunker import Chunker
from nlp.pattern_grammer import PatternGrammar
from nlp.pos_tagger import PosTagger
from nlp.string_cleaner import StringCleaner

MULTIPLE_WHITESPACE_REGEX = nltk.re.compile(r'\s+')

import click

TOP_PHRASE_COUNT = 1000000


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


def extract_chunk_dict(pos_tagged_sentence, chunker_obj):
    return chunker_obj.chunk_pos_tagged_sentence(pos_tagged_sentence)


def get_phrase_list(grammar, pos_tagged_sentences):
    chunk_dict = {}
    chunker_obj = Chunker(grammar)
    with ProcessPoolExecutor(max_workers=10) as pool:
        worker = partial(extract_chunk_dict, chunker_obj=chunker_obj)
        single_chunk_dict_list = pool.map(worker, pos_tagged_sentences)
        for single_chunk_dict in single_chunk_dict_list:
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


def frequent_phrases(text, top_k):
    sentences = nltk.sent_tokenize(text)
    valid_clauses = ['NN_all', 'NN_CC_JJ_multi']
    compiled_grammar = PatternGrammar().init_all_clause()
    phrase_list = sentence_phrase_extract(compiled_grammar, sentences, valid_clauses)
    count_object = collections.Counter(phrase_list)
    return count_object.most_common(n=top_k)


def sentence_phrase_extract(compiled_grammar, sentences, valid_clauses):
    pos_tagged_sentences = [PosTagger(sentence=sentence).pos_tag() for sentence in sentences]
    phrase_list = get_phrases(compiled_grammar, pos_tagged_sentences, valid_clauses)
    return phrase_list


def extract_phrases(filepath):
    with open(filepath, 'r') as file:
        file_read_iterator = file.readlines()
        logging.info('Initializing for roller coaster ride')
        overall_top_phrases_dict = dict()
        for batch_lines in split_every(size=10000, iterable=tqdm(file_read_iterator, unit='line processed', ncols=120)):
            logging.info('Length of line being processed:{}'.format(len(batch_lines)))
            logging.debug('Length of single-line in batch  being processed:{}'.format(len(batch_lines[0])))
            lines_list = [StringCleaner.clean(line).rstrip('\n') for line in batch_lines]
            text = ' '.join(lines_list)
            logging.debug('Processing text:{}..'.format(text[:100]))
            batch_top_phrases_dict = dict(frequent_phrases(text, top_k=100))
            update_top_phrase_dict(overall_top_phrases_dict, batch_top_phrases_dict)
            logging.debug('Got total {} frequent phrases.'.format(len(batch_top_phrases_dict)))
            logging.debug('Frequent phrases in batch:%s ...', list(batch_top_phrases_dict.keys())[:5])
            overall_top_phrases_dict = update_top_phrase_dict(overall_top_phrases_dict, batch_top_phrases_dict)
        return overall_top_phrases_dict


def update_top_phrase_dict(overall_top_phrases_dict, batch_top_phrases_dict):
    overall_keys = set(overall_top_phrases_dict.keys())
    batch_keys = set(batch_top_phrases_dict.keys())
    for key in batch_keys:
        if key in overall_keys:
            overall_top_phrases_dict[key] += batch_top_phrases_dict[key]
        else:
            overall_top_phrases_dict[key] = batch_top_phrases_dict[key]

    return dict(sorted(overall_top_phrases_dict.items(), reverse=True)[:TOP_PHRASE_COUNT])


def get_ngrams(text, n):
    n_grams = ngrams(word_tokenize(text), n)
    return [' '.join(grams).strip() for grams in n_grams]


from itertools import count
from itertools import groupby


def split_every(size, iterable):
    c = count()
    for k, g in groupby(iterable, lambda x: next(c) // size):
        yield list(g)  # or yield g if you want to output a generator


@click.command()
@click.option('--input_file', '-i', help='The input file need to be processed')
@click.option('--output_file', '-o', help='The out file need to be written after processing')
def process_large_text_file(input_file, output_file):
    logging.info('Evaluating file: {} for extracting frequent tags'.format(input_file))
    frequent_phrases_dict = extract_phrases(input_file)
    pd.to_pickle(frequent_phrases_dict, 'frequent_phrases_dict.pkl')
    logging.info('Got a frequent_phrases_dict of size:{}'.format(len(frequent_phrases_dict)))
    frequent_phrases_dict = {key: value for key, value in frequent_phrases_dict.items() if value > 10}
    logging.info('Got a frequent_phrases_dict of size:{} after pruning.'.format(len(frequent_phrases_dict)))
    frequent_phrases = set(frequent_phrases_dict.keys())
    with open(input_file, 'r') as review_text, open(output_file, 'w') as updated_review_text:
        lines = review_text.readlines()
        total = len(lines)
        for index, line in tqdm(enumerate(lines), total=total, unit='line'):
            logging.info('Starting to process file')
            two_grams = get_ngrams(line, 2)
            for gram in two_grams:
                if gram in frequent_phrases:
                    line = line.replace(gram, '_'.join(gram.split()))
            updated_review_text.writelines(line + '\n')
    logging.info('Output file: %s is written with most frequent phrases updated', output_file)


if __name__ == '__main__':
    logging.basicConfig(format='[%(asctime)s] %(levelname)s : %(message)s', level=logging.INFO)
    process_large_text_file()
