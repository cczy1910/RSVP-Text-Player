import pickle


class TextReader:
    """
    Reader for particular file
    Allows to read file and iterate through words
    :param file_name: file name
    :param position: starting position
    """

    def __init__(self, file_name, position):
        self._file_name = file_name
        text = open(file_name).read()
        self._words = self._split_text(text)
        self._position = position - 1

    class TextBorderException(Exception):
        """Exception indicating the border of file"""

        def __init__(self):
            super().__init__(self)

    @staticmethod
    def _split_text(text):
        return text.split()

    def get_file_name(self):
        return self._file_name

    def get_position(self):
        return self._position

    def get_word(self):
        if self._position < 0:
            raise IndexError
        return self._words[self._position]

    def next_word(self):
        """Go to next word"""
        self._position += 1
        try:
            word = self.get_word()
            return word
        except IndexError:
            self._position = len(self._words) - 1
            raise self.TextBorderException()

    def prev_word(self):
        """Go to previous word"""
        self._position -= 1
        try:
            word = self.get_word()
            return word
        except IndexError:
            self._position = 0
            raise self.TextBorderException()


class Controller:
    """
    Controller for all the readers
    Allows to create new readers and switch between existing
    """

    def __init__(self):
        self._positions = {}
        self._cur_reader = None
        try:
            positions_file = open("positions.pkl", "rb")
            self._positions = pickle.load(positions_file)
            positions_file.close()
        except (FileNotFoundError, IOError, EOFError):
            pass

    def open(self, file_name):
        """
        Create reader for new file or switch to existing
        Position in current reader is saved
        :param file_name: file name
        """
        self._close_reader()
        position = 0
        if file_name in self._positions.keys():
            position = self._positions[file_name]
        self._cur_reader = TextReader(file_name, position)

    def _close_reader(self):
        if self._cur_reader is not None:
            self._positions[self._cur_reader.get_file_name()] = self._cur_reader.get_position()
            self._cur_reader = None

    def close(self):
        """
        Close controller and dump the readers information to file
        """
        self._close_reader()
        positions_file = open("positions.pkl", "wb")
        pickle.dump(self._positions, positions_file)
        positions_file.close()

    def prev_word(self):
        """
        Get next word in current reader
        """
        return self._cur_reader.prev_word()

    def next_word(self):
        """
        Get previous word in current reader
        """
        return self._cur_reader.next_word()
