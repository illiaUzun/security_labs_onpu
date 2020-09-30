import argparse

from labsrc.analysis.LetterFrequencyAnalysis import LetterFrequencyAnalysis
from labsrc.analysis.ResultsFormatter import ResultsFormatter


def main():
    '''Performs letter frequency analysis and print results'''
    parser = argparse.ArgumentParser()

    parser.add_argument('--input', '-i', required=True, type=argparse.FileType('r'))

    arguments = parser.parse_args()

    results = LetterFrequencyAnalysis().analyze(arguments.input)
    word_count, characters_relative_freq, letters_relative_freq, top_bigrams, top_trigrams = ResultsFormatter().format(results)

    print(f'Analysis completed. Total {word_count} word found.'
          f'\nRelative Frequency:'
          f'\nAll chars:')
    for char, freq in characters_relative_freq:
        print(f"{char:<14}{freq:<11}")

    print(f'\nLetters only:')
    for char, freq in letters_relative_freq:
        print(f"{char:<14}{freq:<11}")

    print(f'\nN-grams:'
          f'\nBigrams:')
    for char, freq in top_bigrams:
        print(f"{char:<14}{freq:<11}")

    print(f'\nTrigrams:')
    for char, freq in top_trigrams:
        print(f"{char:<14}{freq:<11}")


if __name__ == '__main__':
    main()
