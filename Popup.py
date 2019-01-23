from tkinter import*
from tkinter import ttk
import webbrowser


class Popup():
	"""docstring for Popup"""
	def __init__(self):
		""""""
		self.root = Tk()
		self.play_again = False

	def choose_size(self):
		""""""

		x = int(self.root.winfo_screenwidth()/2 - self.root.winfo_reqwidth()/2)
		y = int(self.root.winfo_screenheight()/2 - self.root.winfo_reqheight()/2) 

		self.root.geometry("+{}+{}".format(x, y))

		self.v = StringVar()
		Label(self.root, text="Before playing take the time to learn the fundamentals : ", fg="black").pack()
		link = Label(self.root, text="Youtube Hyperlink", fg="blue", cursor="hand2")
		link.pack()
		link.bind("<Button-1>", self.get_rules)
		Label(self.root, text="If you are already familiar with the rules you just need to select the size of the board you want : ", fg="black").pack()
		Radiobutton(self.root, text="5x5", variable=self.v, value="5x5",tristatevalue="x",command=self.root.quit).pack(anchor=W)
		Radiobutton(self.root, text="8x8", variable=self.v, value="8x8",tristatevalue="x",command=self.root.quit).pack(anchor=W)
		self.root.mainloop()
		try : 
			self.root.destroy()
		except TclError:
			pass
		return self.v.get()

	def get_rules(self,*args):
		""""""
		webbrowser.open_new(r"https://www.youtube.com/watch?v=hC1sgDNrqq0")
		self.root.quit()

	def place_near_coin(self):
		""""""

		x = int(self.root.winfo_screenwidth()/2 - self.root.winfo_reqwidth()/2)
		y = int(self.root.winfo_screenheight()/2 - self.root.winfo_reqheight()/2) 

		self.root.geometry("+{}+{}".format(x, y))

		question = Label(self.root, text="You need to place your coin in an empty cell near an other one filled (side to side or in bias)", fg="black")
		question.pack()
		self.root.mainloop()
		try : 
			self.root.destroy()
		except TclError:
			pass

	def display_score(self,score1,score2):
		""""""
		x = int(self.root.winfo_screenwidth()/2 - self.root.winfo_reqwidth()/2)
		y = int(self.root.winfo_screenheight()/2 - self.root.winfo_reqheight()/2) 

		self.root.geometry("+{}+{}".format(x, y))

		question = Label(self.root, text="Score ---> rouge - {} : {} - vert".format(score1,score2), fg="black")
		question.pack()
		Button(self.root, text="Play again", command=self.set_play_again ).pack()
		Button(self.root, text="Quit", command=self.root.quit).pack()
		self.root.mainloop()
		try : 
			self.root.destroy()
		except TclError:
			pass
		return self.play_again

	def set_play_again(self):
		self.play_again = True
		self.root.quit()


if __name__ == '__main__':
    popup_manager = Popup()
    res = popup_manager.choose_size()
    print(res)
    
    