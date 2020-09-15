from lab2.analysis.LetterFrequencyAnalysis import AnalysisResults


class ResultsFormatter(object):

    def format(self, counts: AnalysisResults):
        """Returns results of letter frequency analysis in suitable format"""
        word_count = self.format_word_count(counts.words)
        characters_relative_freq = self.calculate_characters_relative_frequency(counts)
        letters_relative_freq = self.calculate_letters_relative_frequency(counts)
        top_bigrams = counts.bigrams.most_common(10)
        top_trigrams = counts.trigrams.most_common(10)

        return word_count, characters_relative_freq, letters_relative_freq, top_bigrams, top_trigrams

    def format_word_count(self, word_count: int) -> str:
        return "{:,}".format(word_count)

    def calculate_characters_relative_frequency(self, counts: AnalysisResults) -> list:
        """Returns relative frequency of all characters"""
        total = sum(counts.characters.values())

        def format_percentage(count: int) -> str:
            return "{:.3f}%".format((count / total) * 100)

        percentages = sorted([
            (character, format_percentage(count))
            for character, count in counts.letters.items()
        ])

        percentages.append(('&nbsp;', format_percentage(counts.characters[' '])))
        percentages.append(('punct', format_percentage(counts.characters['[[:punct:]]'])))
        percentages.append(('digit', format_percentage(counts.characters['[[:digit:]]'])))

        return percentages

    def calculate_letters_relative_frequency(self, counts: AnalysisResults) -> list:
        """Returns relative frequency of letters"""
        total = sum(counts.letters.values())
        percentages = sorted([
            (character, ("{:.3f}%".format((count / total) * 100)))
            for character, count in counts.letters.items()
        ])
        return percentages
