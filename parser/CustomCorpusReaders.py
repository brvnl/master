from nltk.corpus import PlaintextCorpusReader

class TitleCorpusReader(PlaintextCorpusReader):
    def _read_word_block(self, stream):
        # Discard the first line (URL)
        # Reads the second line (title)
        # Discards the rest of lines (body)

        words = []
        stream.readline()
        words.extend(self._word_tokenizer.tokenize(stream.readline()))

        return words

    def _read_sent_block(self, stream):
        sents = []

        # Gets only the seccond line (the title)
        paraList = self._para_block_reader(stream)
        sents.extend([self._word_tokenizer.tokenize(sent)
                        for sent in self._sent_tokenizer.tokenize(paraList[1])])

        return sents

    def _read_para_block(self, stream):
        paras = []

        # Gets only the seccond line (the title)
        paraList = self._para_block_reader(stream)
        paras.append([self._word_tokenizer.tokenize(sent)
                        for sent in self._sent_tokenizer.tokenize(paraList[1])])

        return paras


class FullCorpusReader(PlaintextCorpusReader):
    def _read_word_block(self, stream):
        words = []

        # Discards URL
        stream.readline()

        for i in range(20): # Read 20 lines at a time.
            words.extend(self._word_tokenizer.tokenize(stream.readline()))
        return words

    def _read_sent_block(self, stream):
        sents = []

        l_para = self._para_block_reader(stream)

        # Discards URL
        l_para.pop()

        for para in l_para:
            sents.extend([self._word_tokenizer.tokenize(sent)
                          for sent in self._sent_tokenizer.tokenize(para)])
        return sents

    def _read_para_block(self, stream):
        paras = []

        l_para = self._para_block_reader(stream)

        # Discards URL
        l_para.pop()

        for para in l_para:
            paras.append([self._word_tokenizer.tokenize(sent)
                          for sent in self._sent_tokenizer.tokenize(para)])
        return paras


class BodyCorpusReader(PlaintextCorpusReader):
    def _read_word_block(self, stream):
        words = []

        # Discards URL and title
        stream.readline()
        stream.readline()

        for i in range(20): # Read 20 lines at a time.
            words.extend(self._word_tokenizer.tokenize(stream.readline()))
        return words

    def _read_sent_block(self, stream):
        sents = []

        l_para = self._para_block_reader(stream)

        # Discards URL
        l_para.pop()
        l_para.pop()

        for para in l_para:
            sents.extend([self._word_tokenizer.tokenize(sent)
                          for sent in self._sent_tokenizer.tokenize(para)])
        return sents

    def _read_para_block(self, stream):
        paras = []

        l_para = self._para_block_reader(stream)

        # Discards URL
        l_para.pop()
        l_para.pop()

        for para in l_para:
            paras.append([self._word_tokenizer.tokenize(sent)
                          for sent in self._sent_tokenizer.tokenize(para)])
        return paras