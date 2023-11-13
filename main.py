import tkinter as tk
import tkinter.messagebox
import customtkinter as ctk
from Dataframe import Data
from PIL import Image, ImageTk
from urllib.request import urlopen 
import io 


ctk.set_appearance_mode("System") # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-green") # Themes: "blue" (standard), "green", "dark-blue"

class HomePage(ctk.CTk):
    
    WIDTH = 950
    HEIGHT = 650

    def __init__(self):
        super().__init__()

        self.title("Movie/Series Selector")
        self.geometry(f"{HomePage.WIDTH}x{HomePage.HEIGHT}")


        # -------- create frame --------

        # configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0,1,2,3,4), weight=1)

        self.frame_left = ctk.CTkFrame(master=self)
        self.frame_left.grid(row=0, column=0, sticky="nswe", padx=(10,5), pady=20)


        self.frame_right = ctk.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=(5,10), pady=20)


        #---Left Frame
        
        #Time
        self.label_1 = ctk.CTkLabel(master=self.frame_left,
                                              text="How much time do you have?",
                                              text_font=("Roboto Medium", -16))  
        self.label_1.grid(row=1, column=0, pady=(50,10), padx=30, sticky="we")

        self.optionMenu_1 = ctk.CTkOptionMenu(master=self.frame_left,
                                                    width = 120,
                                                    values=["Select", 
                                                            "<30mins", 
                                                            "30mins - 1hr", 
                                                            "1hr - 2hrs 30mins", 
                                                            "+2hrs 30mins"], 
                                                    command=self.disable_enable) 
        self.optionMenu_1.grid(row=2, column=0, pady=10, padx=30, sticky="we")


        #Streaming Service
        self.label_2 = ctk.CTkLabel(master=self.frame_left,
                                              text="What streaming service do you have?",
                                              text_font=("Roboto Medium", -16))
        self.label_2.grid(row=4, column=0, padx=30, pady=(35,10))

        self.optionMenu_2 = ctk.CTkOptionMenu(master=self.frame_left,
                                                    values=["Select", 
                                                            "Netflix",
                                                            "Prime",
                                                            "Disney",
                                                            "Apple",
                                                            "Hulu",
                                                            "HBO"], 
                                                    command=self.disable_enable) 
        self.optionMenu_2.grid(row=5, column=0, pady=10, padx=30, sticky="we")


        #Movie or Series
        self.label_3 = ctk.CTkLabel(master=self.frame_left,
                                              text="Do you want to watch a Movie or Series?",
                                              text_font=("Roboto Medium", -16)) 
        self.label_3.grid(row=10, column=0, pady=(35,10), padx=30)

        self.optionMenu_3 = ctk.CTkOptionMenu(master=self.frame_left,
                                                    values=["Select", "Movie", "Series"], command=self.disable_enable) 
        self.optionMenu_3.grid(row=12, column=0, pady=10, padx=30, sticky="we")

        
        #Genre
        self.label_4 = ctk.CTkLabel(master=self.frame_left,
                                              text="What Genre are you in the mood for?",
                                              text_font=("Roboto Medium", -16)) 
        self.label_4.grid(row=15, column=0, pady=(35,10), padx=30)

        self.optionMenu_4 = ctk.CTkOptionMenu(master=self.frame_left,
                                                            values=["Any", 
                                                                    "Biography",
                                                                    "Film Noir",
                                                                    "Game Show",
                                                                    "Musical",
                                                                    "Sport",
                                                                    "Short",
                                                                    "Adventure",
                                                                    "Fantasy",
                                                                    "Animation",
                                                                    "Drama",
                                                                    "Horror",
                                                                    "Action",
                                                                    "Comedy",
                                                                    "History",
                                                                    "Western",
                                                                    "Thriller",
                                                                    "Crime",
                                                                    "Documentary",
                                                                    "Science Fiction",
                                                                    "Mystery",
                                                                    "Music",
                                                                    "Romance",
                                                                    "Family",
                                                                    "War",
                                                                    "News",
                                                                    "Reality",
                                                                    "Talk Show"])
        self.optionMenu_4.grid(row=17, column=0, pady=10, padx=30, sticky="we")

        
        #Submit Button
        self.searchButton = ctk.CTkButton(master=self.frame_left,
                                                width= 100,
                                                height= 40,
                                                text="Search",
                                                text_font = ("Roboto Medium",15),
                                                state=tk.DISABLED,
                                                command=self.search)
        self.searchButton.grid(row=20, column=0, padx=(10,150), pady=(35,20))
        self.searchButton.bind("<Return>",self.search)
        self.searchButton.bind("<Return>",self.switchButton, add='+')


        #Reset button
        self.resetButton = ctk.CTkButton(master=self.frame_left,
                                                width= 100,
                                                height= 40,
                                                text="Reset",
                                                text_font = ("Roboto Medium",15),
                                                state=tk.DISABLED,
                                                command= self.resetClick)
        self.resetButton.grid(row=20, column=0, padx=(150,10), pady=(35,20))
        self.resetButton.bind("<Return>",self.resetClick)
        self.resetButton.bind("<Return>",self.switchButton, add='+')


        #---Right Frame

         #Image Box
        self.imageButton = ctk.CTkButton(master=self.frame_right,
                                                text = "", fg_color=None, hover_color=None)
        self.imageButton.grid(row=0, column=0, columnspan=2, padx=20, pady=(5, 0), sticky="nsew")

        self.SMselectedLabel = ctk.CTkLabel(master=self.frame_right,
                                                width= 250,
                                                text = "", anchor="w", 
                                                text_font = ("Roboto Medium",5))
        self.SMselectedLabel.grid(row=1, column=0, padx=50, pady=5, sticky="nsew")

        self.castLabel = ctk.CTkLabel(master=self.frame_right,
                                                width= 250,
                                                text = "",
                                                text_font = ("Roboto Medium",20))
        self.castLabel.grid(row=2, column=0, columnspan=2, padx=20, pady=(5), sticky="nsew")

        self.overviewLabel = ctk.CTkLabel(master=self.frame_right,
                                                width= 250,
                                                text = "",
                                                text_font = ("Roboto Medium",20))
        self.overviewLabel.grid(row=3, column=0, columnspan=2, padx=20, pady=(5), sticky="nsew")


        

    ### Command function for the option menues ###
    def disable_enable(self, value):
        if self.optionMenu_1.get()!="Select" and self.optionMenu_2.get()!="Select" and self.optionMenu_3.get()!="Select":
            self.searchButton.configure(state=tk.NORMAL) 
            self.resetButton.configure(state=tk.NORMAL) 
        else:
            self.searchButton.configure(state=tk.DISABLED)
            self.resetButton.configure(state=tk.DISABLED)


    def search(self):
        time = self.optionMenu_1.get()
        service = self.optionMenu_2.get()
        SorM = self.optionMenu_3.get()
        genre = self.optionMenu_4.get()
        #new = self.check_box_1.get()
        results = (Data(time, service, SorM, genre)).getData()

        def converter(imageURL):
             u = urlopen(imageURL)
             raw_data = u.read()
             u.close()
             poster = io.BytesIO(raw_data)
             return (poster)


        if isinstance(results, list):
            #output = "How about watching: ", results[0],  "%s (%s)\n"%(results[1],results[-1]), "%s\n"%results[3], "%s\n"%results[4]
            self.SMselectedLabel.configure(text = "How about watching: "+results[0]+" ("+results[1]+") \n"+results[-1], text_font = ("Roboto Medium",20), wraplength=500)
            self.castLabel.configure(text = results[3], text_font = ("Roboto Medium",13), wraplength=500)
            self.overviewLabel.configure(text = results[4], text_font = ("Roboto Medium",10), wraplength=500)
            #display image
            image = converter(results[2])
            rawImage = ImageTk.PhotoImage(Image.open(image).resize((350, 400), Image.Resampling.LANCZOS))
            self.imageButton.configure(image = rawImage)
             
        else:
            output = results
            self.castLabel.configure(text = output, text_font = ("Roboto Medium",40), wraplength=500)


    
    def resetClick(self):
        self.optionMenu_1.set("Select")
        self.optionMenu_2.set("Select")
        self.optionMenu_3.set("Select")
        self.optionMenu_4.set("Any")
        self.disable_enable(None) 
        self.imageButton.configure(image = None)
        self.SMselectedLabel.configure(text = "")
        self.castLabel.configure(text = "")
        self.overviewLabel.configure(text = "")
    

    def switchButton(self):
        self.resetButton['state']=tk.NORMAL
    
    def start(self):
        self.mainloop()
        
if __name__ == "__main__":
    app = HomePage()
    app.start()