"""Popup class is using Tkinter to create many windows to get informations from the user"""

from tkinter import Tk, ttk, font, StringVar, PhotoImage, TclError, HORIZONTAL, EW, E, W
import webbrowser
from os import path


class EmbededBool:
    """Usefull class to pass boolean as a parameter"""
    def __init__(self, value: bool):
        self.boolean = value
    def switch_value(self):
        """False to True / True to False"""
        self.boolean = not self.boolean


class Popup:
    """UI class which display specifics widgets and return the interactions the user made with the widgets"""

    HIDDEN_SCORE_FILE = "rolit_game/.res.txt"
    @staticmethod
    def game_config():
        """Displaying the interface to set up the game"""

        root = Tk()
        root.iconbitmap(default="rolit_game/images/deadCell.ico")
        root.resizable(False, False)

        #Creating a smaller font for several labels
        small_style = ttk.Style()
        small_style.configure('Small.TLabel', font=('Helvetica', 10), padding=0)

        class_bool = EmbededBool(False)

        # Setting the position and the name of the window
        x = int(root.winfo_screenwidth()/4 - root.winfo_reqwidth()/2)
        y = int(root.winfo_screenheight()/4 - root.winfo_reqheight()/2)

        ttk.Style().configure("TButton", padding=3, bg="#ccc", font=('Leelawadee', 10), foreground='green', background="#313638")
        ttk.Style().configure("TLabel", size=20, padding=5, font=('Maiandra GD', 12), background="#313638", foreground="white")
        ttk.Style().configure("TFrame", font=('Helvetica', 10), background="#313638")
        ttk.Style().configure("TRadiobutton", font=('Helvetica', 10), background="#313638", foreground="white")
        ttk.Style().configure("TNotebook", background="white")
        ttk.Style().configure("TSeparator", background="white")
        root.title("Game configuration")

        #String var is like str but with a binding to a widget value
        board_size = StringVar()
        board_size.set("5x5")

        #Notebook includes different tabs and allows to navigate between
        NB = ttk.Notebook(root)
        NB.enable_traversal()
        tab1 = ttk.Frame(width=400, height=300, padding=10)
        tab2 = ttk.Frame(width=400, height=250, padding=10)

        # Setting image into a label
        gif1 = PhotoImage(file='rolit_game/images/rolit_box.png')
        image_l = ttk.Label(tab1, image=gif1, cursor="hand2")
        image_l.bind("<Button-1>", lambda event: webbrowser.open_new(r"https://www.youtube.com/watch?v = hC1sgDNrqq0"))

        blue_style = ttk.Style()
        blue_style.configure('Blue.TLabel', foreground='blue')

        ttk.Label(tab1, text="Before playing take the time to learn the fundamentals : ").pack()
        link = ttk.Label(tab1, text="Rolit Tutorial", cursor="hand2", style='Blue.TLabel')
        link.pack()

        #Needed to obtain underlined text
        f = font.Font(link, 'Helvetica 14 italic')
        f.configure(underline=True)
        link.configure(font=f)

        #Binding a 'key' (mouse) to a function
        link.bind("<Button-1>", lambda event: webbrowser.open_new(r"https://www.youtube.com/watch?v = hC1sgDNrqq0"))

        image_l.pack()

        ttk.Button(tab1, text="I am already familiar with the rules", cursor="hand2", command=lambda: Popup.seek_tab(NB, tab2)).pack()
        ttk.Label(tab2, text="Select the size of the board : ").grid(row=0)
        ttk.Radiobutton(tab2, text="5x5", cursor="hand2", variable=board_size, value="5x5").grid(row=1, column=0)
        ttk.Radiobutton(tab2, text="8x8", cursor="hand2", variable=board_size, value="8x8").grid(row=1, column=1)

        #Simple line separator
        ttk.Separator(tab2, orient=HORIZONTAL).grid(row=2, columnspan=5, sticky=EW)

        # Binding variables
        gamemode = StringVar()
        ai_level = StringVar()
        values = ['1.Easy', '2.Medium', '3.Hard', '4.Expert']    # Change order [::-1]
        ai_level.set(values[0])
        gamemode.set("Player-AI")


        ttk.Label(tab2, text="Which mode do you want to play ?").grid(row=3)

        is_ai_game = ttk.Radiobutton(tab2, text='Me versus AI', cursor='hand2', variable=gamemode, value="Player-AI", command=lambda: Popup.enable_widget(spin))
        is_ai_game.grid(row=4, column=0)
        spin = ttk.Spinbox(tab2, textvariable=ai_level, state='readonly', values=values, takefocus=False, wrap=True, width=15, justify='center', validate='all', validatecommand=tab2.focus())
        spin.grid(row=4, column=1)
        # f value to obtain at the end a empty string -> false value
        ttk.Radiobutton(tab2, text="Two player mod", cursor="hand2", variable=gamemode, value="Player-Player", command=lambda: Popup.disable_widget(spin)).grid(row=5)
        ttk.Radiobutton(tab2, text="2 AI Game", cursor="hand2", variable=gamemode, value="AI-AI", command=lambda: Popup.enable_widget(spin)).grid(row=6)

        ttk.Separator(tab2, orient=HORIZONTAL).grid(row=7, columnspan=5, sticky=EW)

        #Readin the best results from file
        scores = Popup.load_score()
        #Extracting scores
        results = [s.split(':')[1] for s in scores.split('-')]

        ttk.Label(tab2, text="Your personnal best in 5x5 mode against AI : ").grid(row=8)
        #Printing scores
        ttk.Label(tab2, text=f"Easy Mode : {results[0]}", style="Small.TLabel").grid(row=9)
        ttk.Label(tab2, text=f"Medium Mode : {results[1]}", style="Small.TLabel").grid(row=10)
        ttk.Label(tab2, text=f"Hard Mode : {results[2]}", style="Small.TLabel").grid(row=11)
        ttk.Label(tab2, text=f"Expert Mode : {results[3]}", style="Small.TLabel").grid(row=12)

        ttk.Button(tab2, text="Let's play !", cursor="hand2", command=lambda: Popup.user_click(root, class_bool)).grid(row=13, columnspan=2, sticky=E)

        NB.add(tab1, text='Tutorial')
        NB.pack()
        root.geometry(f'+{x}+{y}')
        root.mainloop()

        try:
            root.destroy()
        except TclError:
            pass

        return f'{board_size.get()}  {gamemode.get()}  {ai_level.get()[2:]}  {class_bool.boolean}'

    @staticmethod
    def load_score():
        """Loading scores from file"""
        result_line = []
        if not path.isfile(Popup.HIDDEN_SCORE_FILE):
            with open(Popup.HIDDEN_SCORE_FILE, 'w') as outfile:
                outfile.write('Easy:0\nMedium:0\nHard:0\nExpert:0\n')
        with open(Popup.HIDDEN_SCORE_FILE, 'r') as infile:
            for line in infile:
                line = line.replace('\n', '')
                if line:
                    result_line.append(line)
        result_line = '-'.join(result_line)
        return result_line


    @staticmethod
    def save_score(difficuty: int, score: int):
        """Save the score in the hidden file"""
        current_scores = Popup.load_score().split('-')
        with open(Popup.HIDDEN_SCORE_FILE, 'w') as outfile:
            for scr in current_scores:
                diff, points = scr.split(':')
                if difficuty == diff and score > int(points):
                    points = score
                outfile.write(f'{diff}:{points}\n')

    @staticmethod
    def disable_widget(widget):
        """Disable a specific widget"""
        widget['state'] = 'disable'

    @staticmethod
    def enable_widget(widget):
        """Make a widget """
        widget['state'] = 'normal'

    @staticmethod
    def user_click(root, class_bool: EmbededBool):
        """Detect if the user have click on a button of the UI"""
        class_bool.switch_value()
        root.quit()

    @staticmethod
    def seek_tab(notebook, tab):
        """Display a new tab and add the focus on it"""
        notebook.add(tab)
        notebook.select(".!frame2")

    @staticmethod
    def place_near_coin():
        """Displaying a popup if the player doesn't put his coin near an other one"""
        root = Tk()
        root.iconbitmap(default="rolit_game/images/deadCell.ico")
        root.resizable(False, False)

        #Creating a smaller font for several labels
        small_style = ttk.Style()
        small_style.configure('Small.TLabel', font=('Helvetica', 10), padding=0)

        x = int(root.winfo_screenwidth()/3 - root.winfo_reqwidth()/2)
        y = int(root.winfo_screenheight()/3 - root.winfo_reqheight()/2)

        root.title("Primordial rules")

        ttk.Label(root, text="You need to place your coin in an empty cell near an other one"
                             " filled (side to side or in bias)", style="Small.TLabel", padding=5).pack()

        root.geometry(f'+{x}+{y}')
        root.mainloop()

    @staticmethod
    def display_score(score1: int, score2: int, difficulty: str, need_to_save_score: bool):
        """Display the final score between the two players (human or not)

        Save the score in a 'secret' file if it'a a human score against a AI on a 5x5 grid       """

        #Popup.config()
        root = Tk()
        root.iconbitmap(default="rolit_game/images/deadCell.ico")
        root.resizable(False, False)


        ttk.Style().configure("TButton", padding=3, bg="#ccc", font=('Leelawadee', 10), foreground='green', background="#313638")
        ttk.Style().configure("TLabel", size=20, padding=10, font=('Maiandra GD', 12), background="#313638", foreground="white")
        ttk.Style().configure("TFrame", font=('Helvetica', 10), background="#313638")
        ttk.Style().configure("TRadiobutton", font=('Helvetica', 10), background="#313638", foreground="white")
        ttk.Style().configure("TNotebook", background="white")
        ttk.Style().configure("TSeparator", background="white")

        #Creating a smaller font for several labels
        small_style = ttk.Style()
        small_style.configure('Small.TLabel', font=('Helvetica', 10), padding=0)

        class_bool = EmbededBool(False)


        x = int(root.winfo_screenwidth()/4 - root.winfo_reqwidth()/2)
        y = int(root.winfo_screenheight()/4 - root.winfo_reqheight()/2)


        root.title("Player's scores")

        main_frame = ttk.Frame(root, width=600, height=165, padding=10)
        main_frame.pack()

        green_style = ttk.Style()
        green_style.configure('Green.TLabel', foreground='green')

        red_style = ttk.Style()
        red_style.configure('Red.TLabel', foreground='red')
        if need_to_save_score:
            Popup.save_score(difficulty, score1)

        # More red than green coins
        if score1 > score2:
            ttk.Label(main_frame, text="  Congratulation you won !  ", cursor="star").grid(row=0)
            win = PhotoImage(file='rolit_game/images/win.png')
            ttk.Label(main_frame, image=win, cursor="star").grid(row=1)
        else:
            ttk.Label(main_frame, text="  You lost this one ...  ", cursor="pirate").grid(row=0)
            loose = PhotoImage(file='rolit_game/images/loose.png')
            ttk.Label(main_frame, image=loose, cursor="star").grid(row=1)



        ttk.Label(main_frame, text="        Game played in - {} - mode        ".format(difficulty.lower()), style="Small.TLabel").grid(row=2)
        ttk.Label(main_frame, text="Ⓡ Red - {} ".format(score1), style="Red.TLabel").grid(row=3, sticky=W)
        ttk.Label(main_frame, text="{} - Green Ⓖ".format(score2), style="Green.TLabel").grid(row=3, sticky=E)

        #Progress Bar

        ttk.Button(main_frame, text="Play again", cursor="hand2", command=lambda: Popup.set_play_again(root, class_bool)).grid(row=4)
        ttk.Button(main_frame, text="Quit", cursor="hand2", command=root.quit).grid(row=5)

        root.geometry(f'+{x}+{y}')
        root.mainloop()
        try:
            root.destroy()
        except TclError:
            pass
        return class_bool.boolean

    @staticmethod
    def set_play_again(root, class_bool):
        """Used to know if the player still wanted to play an other game"""
        class_bool.switch_value()
        root.quit()
