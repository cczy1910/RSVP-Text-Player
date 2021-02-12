from rsvp_controller import *
import math
import tkinter
import tkinter.filedialog


class Player:
    """
    Player UI
    """

    def __init__(self):
        self._active = False
        self._wpm = 300
        self._controller = Controller()
        self._root = tkinter.Tk()
        self._buff_multiplier = 1

        self._build_view()

        self._load_file()

        self._run()

        self._root.mainloop()

        self._controller.close()

    def _build_view(self):
        """
        Create the UI for player
        """
        self._root.title("RSVP Player")
        self._root.config(bg="lightgray")

        self._wpm_view = tkinter.StringVar("")
        self._current_word_l = tkinter.StringVar("")
        self._current_word_m = tkinter.StringVar("")
        self._current_word_r = tkinter.StringVar("")
        self._message = tkinter.StringVar("")

        self._print_wpm()

        load_button = tkinter.Button(
            self._root,
            text="Open File",
            font=("Helvetica", 12),
            bg="lightgray")
        wpm_box = tkinter.Label(
            self._root,
            textvariable=self._wpm_view,
            anchor="w",
            font=("Verdana", 10),
            bg="lightgray")
        word_box_l = tkinter.Label(
            self._root,
            textvariable=self._current_word_l,
            font=("Courier", 14),
            padx=0,
            bg="white",
            width=16,
            height=4,
            borderwidth=0,
            anchor="e")
        word_box_m = tkinter.Label(
            self._root,
            textvariable=self._current_word_m,
            font=("Courier", 14),
            fg="red",
            padx=0,
            bg="white",
            width=0,
            height=4,
            borderwidth=0)
        word_box_r = tkinter.Label(
            self._root,
            textvariable=self._current_word_r,
            font=("Courier", 14),
            padx=0,
            bg="white",
            width=22,
            height=4,
            borderwidth=0,
            anchor="w")
        message_box = tkinter.Label(
            self._root,
            textvariable=self._message,
            fg="red",
            borderwidth=0,
            padx=0,
            bg="lightgray")

        load_button.bind("<Button-1>", self._load_file)
        self._root.bind("<space>", self._toggle)
        self._root.bind("<Right>", self._next_word)
        self._root.bind("<Left>", self._prev_word)
        self._root.bind("<Up>", self._wpm_up)
        self._root.bind("<Down>", self._wpm_down)

        wpm_box.grid(
            row=2,
            column=0,
            padx=(5, 10),
            pady=(0, 15))
        load_button.grid(
            row=2,
            column=2,
            padx=(10, 5),
            pady=(0, 20))

        word_box_l.grid(
            row=0,
            column=0,
            padx=(30, 0),
            pady=(30, 0),
            ipadx=0,
            sticky="e")
        word_box_m.grid(
            row=0,
            column=1,
            padx=0,
            pady=(30, 0),
            ipadx=0,
            sticky="ew")
        word_box_r.grid(
            row=0,
            column=2,
            padx=(0, 30),
            pady=(30, 0),
            ipadx=0,
            sticky="w")

        message_box.grid(
            row=1,
            column=0,
            columnspan=3,
            pady=6)

    def _print_word(self, word):
        """
        Print word in main field
        :param word: word to print
        """
        pref_len = math.floor(len(word) / 3)
        self._current_word_l.set(word[:pref_len])
        self._current_word_m.set(word[pref_len])
        self._current_word_r.set(word[pref_len + 1:])

    def _print_message(self, message):
        """
        Print the alert message
        :param message: alert message
        """
        self._message.set(message)
        self._root.after(1500, self._message.set, "")

    def _print_wpm(self):
        """
        Print current words per minute rate
        """
        self._wpm_view.set("WPM: " + str(self._wpm))

    def _load_file(self):
        """
        Open new file
        """
        file_name = tkinter.filedialog.Open(self._root).show()
        if file_name == '':
            self._print_message("Empty file name")
            return

        try:
            self._controller.open(file_name)
        except (IOError, UnicodeDecodeError):
            self._print_message("File reading error!")
            return
        self._active = False
        self._next_word()

    def _toggle(self):
        """
        Play/pause the player
        """
        self._active = not self._active
        if self._active:
            self._buff_multiplier = min(100 / self._wpm, 1)

    def _get_multiplier(self, word: str):
        """
        Get WPM multiplier
        :param word: next word
        """
        result = 1
        if self._buff_multiplier < 1:
            result = self._buff_multiplier
            self._buff_multiplier *= 1.2
        if len(word) > 8:
            result *= 0.7
        elif word.endswith(".") and len(word) > 3:
            result *= 0.8
        return result

    def _run(self):
        """
        Run the player
        """
        multipiler = 1
        if self._active:
            try:
                word = self._controller.next_word()
                self._print_word(word)
                multipiler = self._get_multiplier(word)
            except TextReader.TextBorderException:
                self._active = False
                self._print_message("End of text!")
        self._root.after(math.ceil(60 * 1000 / (self._wpm * multipiler)), self._run)

    def _wpm_up(self):
        """
        Increase WPM
        """
        if self._wpm < 1000:
            self._wpm += 10
            self._print_wpm()
        else:
            self._print_message("Maximal wpm!")

    def _wpm_down(self):
        """
        Decrease WPM
        """
        if self._wpm > 20:
            self._wpm -= 10
            self._print_wpm()
        else:
            self._print_message("Minimal wpm!")

    def _next_word(self):
        if not self._active:
            try:
                self._print_word(self._controller.next_word())
            except TextReader.TextBorderException:
                self._print_message("End of text!")
        else:
            self._print_message("Player is on!")

    def _prev_word(self):
        if not self._active:
            try:
                self._print_word(self._controller.prev_word())
            except TextReader.TextBorderException:
                self._print_message("Begin of text!")
        else:
            self._print_message("Player is on!")


if __name__ == '__main__':
    player = Player()
