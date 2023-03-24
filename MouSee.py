import tkinter as tk
from tkinter import messagebox
# from PIL import Image, ImageTk  # pip install pillow
from graphics import * 

class Login(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        

        self.configure(bg='#b4b9cf')
        
        border = tk.LabelFrame(self, text='Login', bg='#5776ff', bd = 10, font=("Arial", 20))
        border.pack(fill="both", expand=True, padx = 150, pady=150)
        
        L1 = tk.Label(border, text="Username", font=("Arial Bold", 15), bg='#5776ff')
        L1.place(x=50, y=20)
        T1 = tk.Entry(border, width = 30, bd = 5)
        T1.place(x=180, y=20)
        
        L2 = tk.Label(border, text="Password", font=("Arial Bold", 15), bg='#5776ff')
        L2.place(x=50, y=80)
        T2 = tk.Entry(border, width = 30, show='*', bd = 5)
        T2.place(x=180, y=80)
        
        def verify():
            #look for login credentials
            try:
                with open("credentials.txt", "r") as f:
                    info = f.readlines()
                    i  = 0
                    for e in info:
                        u, p =e.split(",")
                        if u.strip() == T1.get() and p.strip() == T2.get():
                            controller.show_frame(LandingPage)
                            i = 1
                            break
                    if i==0:
                        messagebox.showinfo("Error", "Please provide correct username and password")
            except:
                messagebox.showinfo("Error", "Please provide correct username and password")
         
        B1 = tk.Button(border, text="Submit", bg= '#5776ff', font=("Arial", 15), command=verify)
        B1.place(x=300, y=115)
        # B1.bind("<Return>", (lambda event: verify())) #check for enter keypress
        # self.bind("<Return>", verify)
        

        
        def register():
            #create new credentials for users to login
            window = tk.Tk()
            window.resizable(False,False)
            window.configure(bg="deep sky blue")
            window.title("Register")
            l1 = tk.Label(window, text="Username:", font=("Arial",15), bg="deep sky blue")
            l1.place(x=10, y=10)
            t1 = tk.Entry(window, width=30, bd=5)
            t1.place(x = 200, y=10)
            
            l2 = tk.Label(window, text="Password:", font=("Arial",15), bg="deep sky blue")
            l2.place(x=10, y=60)
            t2 = tk.Entry(window, width=30, show="*", bd=5)
            t2.place(x = 200, y=60)
            
            l3 = tk.Label(window, text="Confirm Password:", font=("Arial",15), bg="deep sky blue")
            l3.place(x=10, y=110)
            t3 = tk.Entry(window, width=30, show="*", bd=5)
            t3.place(x = 200, y=110)
            
            def check():
                if t1.get()!="" or t2.get()!="" or t3.get()!="":
                    if t2.get()==t3.get():
                        with open("credentials.txt", "a") as f:
                            f.write(t1.get()+","+t2.get()+"\n")
                            messagebox.showinfo("Welcome","You are registered successfully!")
                            window.destroy()
                    else:
                        messagebox.showinfo("Error","Your password didn't match!")
                else:
                    messagebox.showinfo("Error", "Please fill the complete field!")
                    
            b1 = tk.Button(window, text="Sign in", font=("Arial",15), bg="#ffc22a", command=check)
            b1.place(x=170, y=150)
            
            window.geometry("470x220")
            window.mainloop()
            
        B2 = tk.Button(self, text="Register", bg = '#5776ff', font=("Arial",15), command=register)
        B2.place(x=335, y= 300)
        
class LandingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # load = Image.open("eyeball.png")
        # photo = ImageTk.PhotoImage(load)
        # label = tk.Label(self, image=photo)
        # label.image=photo # type: ignore
        # label.place(relx=0.5,rely=0.5, anchor="center")

        L1 = tk.Label(self, text="Welcome to MouSee the state of the art application \n for eye tracking mouse interaction \n What would you like to do?", bg = "light blue", font=("Arial Bold", 20))
        L1.place(x=0, y=10)
        
        
        B1 = tk.Button(self, text="Training Page", font=("Arial", 15), command=lambda: controller.show_frame(TrainingPage))
        B1.place(x=5, y=150)
        
        B2 = tk.Button(self, text="Log Out", font=("Arial", 15), command=lambda: controller.show_frame(Login))
        B2.place(x=700, y=10)
        
class TrainingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.configure(bg='#b4b9cf')
        
        Label = tk.Label(self, text='Welcome to the Algorithm Training Page \n ', bg = '#5776ff', font=("Arial Bold", 20))
        Label.place(x=0, y=10)
        
        B1 = tk.Button(self, text="Log Out", font=("Arial", 15), command=lambda: controller.show_frame(Login))
        B1.place(x=700, y=10)
        
        B2 = tk.Button(self, text="Go Back", font=("Arial", 15), command=lambda: controller.show_frame(LandingPage))
        B2.place(x=5, y=85)

        B3 = tk.Button(self, text="Start Training", font=("Arial", 15), command=lambda: controller.start_training())
        B3.place(x=5, y=125)

        
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        #creating a window
        window = tk.Frame(self)
        window.pack()
        
        #window size for all frames
        window.grid_rowconfigure(0, minsize = 1000)
        window.grid_columnconfigure(0, minsize = 1600)
        
        self.frames = {}
        for F in (Login, LandingPage, TrainingPage):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row = 0, column=0, sticky="nsew")
            
        self.show_frame(Login)
        
    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        self.title("MouSee")
    
    # determine if a point is inside a given polygon or not
    # Polygon is a list of (x,y) pairs.
    #https://www.eecs.umich.edu/courses/eecs380/HANDOUTS/PROJ2/InsidePoly.html
    def point_inside_polygon(self,x,y,poly):
        n = len(poly)
        inside =False

        p1x,p1y = poly[0]
        xinters = 0

        for i in range(n+1):
            p2x,p2y = poly[i % n]
            if y > min(p1y,p2y):
                if y <= max(p1y,p2y):
                    if x <= max(p1x,p2x):
                        if p1y != p2y:
                            xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x,p1y = p2x,p2y
        return inside

    def start_training(self):
        win = GraphWin('Algorithm Training',1600,800) 
        c = Circle(Point(50,50), 25)
        c.setFill("red")
        c.draw(win)
        win.getMouse() # Pause to view result then returns a point or
        win.checkMouse() #just gets the coordinates


        #TODO do things

        win.close()    # Close window when done
        # self.show_frame(TrainingPage)

if __name__ == "__main__":     
    app = Application()
    # app.maxsize(800, 500)
    app.mainloop()