import json
from tkinter import *
from PIL import Image, ImageTk
from logic.Grid import Grid


def load_preferences():
    with open('resources/preferences.json5') as json_data:
        preferences = json.load(json_data)
        return preferences


def save_preferences(preferences):
    with open('resources/preferences.json5', 'w') as json_data:
        json.dump(preferences, json_data)


class GlobalButton(Button):
    def __init__(self, father, font_color, color, **kw):
        super().__init__(father,
                         font=("Arial", 15),
                         width=10,
                         fg=font_color,
                         bg=color,
                         activebackground=font_color,
                         activeforeground=color,
                         relief=GROOVE,
                         **kw)


class GUISquare(Canvas):
    def __init__(self, father, color, **kw):
        super().__init__(father, **kw)
        self.color = color
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.configure(bg="red")

    def on_leave(self, event):
        self.configure(bg=self.color)


class BarBarGUI(Tk):
    def __init__(self):
        self.pref = load_preferences()
        self.lvl = (8, 10)
        self.active_page = self.start_page
        self.grid = Grid()
        self.color, self.font_color, self.label_mode = self.load_color()
        super().__init__()
        self.var = StringVar()
        self.geometry('600x600')
        self.title("Minesweeper")
        self.configure(background=self.color)
        self.maxsize(600, 600)
        self.minsize(600, 600)
        self.add_menubar()
        self.start_page()

    def load_color(self):
        mode = self.pref['preferences']
        if mode == 'dark':
            return 'gray20', 'white', 'Light'
        else:
            return 'white', 'black', 'Dark'

    def refresh_pane(self):
        for child in self.winfo_children():
            child.destroy()

    def change_mode(self, option_menu):
        mode = self.pref['preferences']
        if mode == 'dark':
            self.pref['preferences'] = 'light'
            save_preferences(self.pref)
            option_menu.entryconfigure(0, label="Dark Mode")
        else:
            self.pref['preferences'] = 'dark'
            save_preferences(self.pref)
            option_menu.entryconfigure(0, label="Light Mode")
        self.refresh_pane()
        self.color, self.font_color, self.label_mode = self.load_color()
        self.configure(background=self.color)
        self.active_page()

    def add_menubar(self):
        menubar = Menu(self)  # create the menu bar
        # add the options buttons
        option_menu = Menu(menubar, tearoff=0)
        option_menu.add_command(label=self.label_mode + " Mode",
                                command=lambda: self.change_mode(option_menu))
        menubar.add_separator()
        option_menu.add_command(label="Exit", command=self.quit)
        # give label
        menubar.add_cascade(label="Options", menu=option_menu)

        level_menu = Menu(menubar, tearoff=0)
        level_menu.add_command(label="Beginner", command=lambda: self.level(0))
        level_menu.add_command(label="Intermediate", command=lambda: self.level(1))
        level_menu.add_command(label="Expert", command=lambda: self.level(2))
        menubar.add_cascade(label="Level", menu=level_menu)

        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="About...", command=self.about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

    def level(self, lvl):
        lvl_list = self.pref["level"][str(lvl)]
        self.lvl = int(lvl_list[0]), int(lvl_list[1])
        self.refresh_pane()
        self.add_menubar()
        self.active_page()

    def about(self):
        top = Toplevel(width=200, height=100)
        top.title("About")
        label = Label(top, text="Minesweeper v1.0", padx=30, pady=10)
        description = Label(top, text="Minesweeper game", padx=10, pady=10)
        author = Label(top, text="Author: Cyril AUBOURG", padx=30, pady=10)
        label.pack()
        description.pack()
        author.pack()
        top.mainloop()

    def game_over(self, message):
        top = Toplevel(width=300, height=200, bg=self.color)
        top.title("Game Over")
        label = Label(top, text=message, padx=30, pady=10, bg=self.color, fg=self.font_color)
        restart_app = GlobalButton(top, self.font_color, self.color, text="RESTART", command=self.game_page)
        quit_app = GlobalButton(top, self.font_color, self.color, text="QUIT", command=self.quit)
        restart_app.place(relx=0.5, rely=0.40, anchor=CENTER)
        label.place(relx=0.5, rely=0, anchor=N)
        quit_app.place(relx=0.5, rely=0.60, anchor=CENTER)
        top.mainloop()

    def game_page(self):
        self.refresh_pane()
        self.add_menubar()
        self.active_page = self.game_page
        self.grid = Grid()
        size = self.lvl[0]
        mines = self.lvl[1]
        self.grid.init_size(size, mines)
        for row in range(size):
            for col in range(size):
                gs = GUISquare(self, self.color,
                               bg=self.color,
                               bd=3,
                               relief=GROOVE,
                               width=int(600 / size),
                               height=int(600 / size),
                               )
                gs.bind("<Button-1>", lambda event, a=row, b=col: self.activate_square(a, b))
                gs.grid(row=row, column=col)
                self.grid_rowconfigure(row, minsize=int(600 / size), weight=1)
                self.grid_columnconfigure(col, minsize=int(600 / size), weight=1)

    def activate_square(self, row, col):
        square = self.grid.mine_grid[row][col]
        result = self.grid.show_square(square)
        self.refresh_pane()
        self.add_menubar()
        size = self.lvl[0]
        if result:
            for r in range(size):
                for c in range(size):
                    if self.grid.mine_grid[r][c].is_discovered():
                        gs = self.set_discovered_square(c, r, size)
                    else:
                        gs = self.set_square(r, c, size)
                    gs.grid(row=r, column=c)
                    self.grid_rowconfigure(r, minsize=int(600 / size), weight=1)
                    self.grid_columnconfigure(c, minsize=int(600 / size), weight=1)
            if self.grid.end_game():
                self.game_over("VICTORY: You pacified the place !")
        else:
            for r in range(size):
                for c in range(size):
                    gs = self.set_discovered_square(c, r, size)
                    gs.grid(row=r, column=c)
                    self.grid_rowconfigure(r, minsize=int(600 / size), weight=1)
                    self.grid_columnconfigure(c, minsize=int(600 / size), weight=1)
            self.game_over("GAME OVER: You hit a bomb !")

    def set_square(self, r, c, size):
        gs = GUISquare(self, self.color,
                       bg=self.color,
                       bd=3,
                       relief=GROOVE,
                       width=int(600 / size),
                       height=int(600 / size),
                       )
        gs.bind("<Button-1>", lambda event, a=r, b=c: self.activate_square(a, b))

        return gs

    def set_discovered_square(self, c, r, size):
        gs = GUISquare(self, self.color,
                       bg=self.color,
                       bd=3,
                       relief=GROOVE,
                       width=int(600 / size),
                       height=int(600 / size),
                       )
        if self.grid.mine_grid[r][c].has_mine():
            load = Image.open("resources/mine.png")
        else:
            load = Image.open("resources/" + str(self.grid.mine_grid[r][c].mined_neighbors) + ".png")
        image = load.resize((int(600 / size), int(600 / size)), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)
        gs.create_image(0, 0, image=img, anchor=NW)
        gs.image = img
        return gs

    def start_page(self):
        self.refresh_pane()
        self.add_menubar()
        self.active_page = self.start_page
        zoom = 0.3
        load = Image.open("resources/minesweeper.png")
        pixels_x, pixels_y = tuple([int(zoom * x) for x in load.size])
        image = load.resize((pixels_x, pixels_y), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(image)
        img = Label(self, image=render, bg=self.color, borderwidth=0)
        img.image = render
        enter_app = GlobalButton(self, self.font_color, self.color, text="ENTER", command=self.game_page)
        quit_app = GlobalButton(self, self.font_color, self.color, text="QUIT", command=self.quit)
        enter_app.place(relx=0.5, rely=0.45, anchor=CENTER)
        img.place(relx=0.5, rely=0, anchor=N)
        quit_app.place(relx=0.5, rely=0.55, anchor=CENTER)


if __name__ == "__main__":
    app = BarBarGUI()
    app.mainloop()
