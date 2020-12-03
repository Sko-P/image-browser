import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import os

#Big resolution picture take some time to open

#Checkbox to delete the original picture after conversion
#ADD keyboard support keybindings and delete
#dropping an image on it and opening it



class frame(tk.Frame):

    def __init__(self):

        self.current_index = 0
        self.current_picture =""
        self.current_picture_type=""
        self.dir_picture = []   #stores pictures names only of the current directory
        self.current_path = ""
        self.current_img = None #pillow structure img
        self.backup_img = None
        self.backup_img_name =""
        self.current_img_file = None
        self.clicked = None

    def open_image(self):
        filename = filedialog.askopenfilename(title='open picture')
        if(filename != ''):
            directory = filename.rpartition("/")
            print(directory) #rpartition : everything before the last occurence of the argument
            picture = filename.rpartition("/")
            self.current_picture = picture[len(picture)-1]
            print(self.current_picture)
            self.current_path = directory[0]
            self.filter_dir_content(self.current_path) #Get the names of the pictures

    def filter_dir_content(self,dir_): #search for .png/.bmp/.jpg/
        all_content =os.listdir(dir_)
        for i in all_content:
            if (".png" in i or ".bmp" in i or ".jpg" in i or ".jpeg" in i):
                self.dir_picture.append(i)
        self.current_index = self.dir_picture.index(self.current_picture)
        link = self.current_path+"/"+self.dir_picture[self.current_index]
        print(link)
        self.load_and_display_img()
        
    
    def explore(self, direction):
        if(len(self.dir_picture) != 0):
            if(direction == 1):
                self.update_index_current_pic(1)
                self.load_and_display_img()
            else:
                self.update_index_current_pic(-1)
                self.load_and_display_img()

    def update_after_delete(self):
        self.dir_picture.remove(self.current_picture)
        #print(self.dir_picture)
        self.update_index_current_pic(-1)
        print(self.current_picture)


    def update_index_current_pic(self, n): #Used after changing a picture or deleting (update) picture
        index = self.current_index + n
        if(index <0):
            index = index = len(self.dir_picture) - 1
        else:
            if(index >= len(self.dir_picture)):
                index = 0
        self.current_index = index
        self.current_picture = self.dir_picture[self.current_index]

    def backup_before_delete(self):
        self.current_img = Image.open(self.current_path+"/"+self.dir_picture[self.current_index])
        self.backup_img = self.current_img.copy()
        self.backup_img_name = self.current_picture
        self.current_img.close()
    
    def restore_deleted_image(self):
        print(self.backup_img)
        print(self.backup_img_name)
        if(self.backup_img != None):
            print("Restoring section")
            self.dir_picture.append(self.backup_img_name)
            self.backup_img.save(self.current_path+"/"+self.backup_img_name)
            self.backup_img = None
            self.backup_img_name = ""
        
    def delete_image(self):
        if(len(self.dir_picture) > 0):
            self.backup_before_delete()
            os.remove(self.current_path+"/"+self.dir_picture[self.current_index])
            self.update_after_delete()
            self.load_and_display_img()
            #Make the restore button appear after deleting an image
    
    def load_and_display_img(self):
        self.current_img_file = Image.open(self.current_path+"/"+self.dir_picture[self.current_index])
        self.current_img = ImageTk.PhotoImage(self.current_img_file.resize((720,540)))
        framel = tk.Label(frame,bg='blue', image = self.current_img)
        framel.place(relx = 0.1, rely= 0.1, relwidth=0.8,relheight=0.8)
        self.convert_dropdown()
        root.mainloop()
        

    def convert_dropdown(self):
        if(len(self.dir_picture) != 0):
            buttonc = tk.Button(frame, text="convert",bg="grey",command=lambda:a.convert_picture())
            buttonc.place(relx=0.85, rely=0.92)
            array = ['png', 'jpeg', 'bmp','jpg']
            print(self.current_picture)
            self.current_picture_type = self.current_picture.split(".")[1]
            array.remove(self.current_picture_type)
            print(array)
            self.clicked = StringVar()
            self.clicked.set(".x")
            print(self.clicked)
            drop = OptionMenu(frame,self.clicked, *array)
            drop.place(relx=0.7, rely=0.91)
            
    def convert_picture(self):
        print(self.clicked.get())
        if(self.clicked.get() != ".x"):
            print(self.current_picture)
            new_picture = self.current_picture.split(".")[0]+"."+self.clicked.get()
            print(new_picture)
            a = self.current_img_file.save(self.current_path+"/"+new_picture)
            print(a)


    def close_window(self, event):
        root.destroy()
    def left_key(self,event):
        self.explore(-1)

    def right_key(self,event):
        self.explore(1)

    def delete_key(self,event):
        self.delete_image()
    '''
    def keys_process(self):
        print("launched")
        while(1):
            key = ord(getch()) #key = getkey()
            if(key ==75) :
                #L : 75 R: 77 U : 72 D : 80
                a.explore(-1)
                print("left")
            elif key == 77 :
                a.explore(1)
                print("right")
    '''         
def printkey(event):
    print("a")



a = frame()

#t1 = threading.Thread(target=a.keys_process)
#t1.start()

HEIGHT = 400
WIDTH = 450
    
root = tk.Tk()
root.title("Image browser")

#root.icon
canvas = tk.Canvas(root, height=HEIGHT,width=WIDTH)
root.bind('<Left>', a.right_key)
root.bind('<Right>', a.left_key)
root.bind('<Delete>', a.delete_key)
root.bind('<Escape>', a.close_window)
canvas.pack()
#img = ImageTk.PhotoImage((Image.open("rr.jpg").resize((250,250))))

#filename = filedialog.askopenfilename(title='open')

#directory = filename.rpartition("/") #rpartition : everything before the last occurence of the argument
#print(directory)
#os.listdir("C:/Users/pc1/Desktop") 
#print(os.listdir("C:/Users/pc1/Desktop"))

frame = tk.Frame(root,bg='yellow')
frame.place(relx = 0.05, rely= 0.05, relwidth=0.9,relheight=0.9)

framel = tk.Label(frame,bg='blue', image = None)
framel.place(relx = 0.05, rely= 0.05, relwidth=0.9,relheight=0.9)

button = tk.Button(frame, text="open",bg="grey", command=lambda:a.open_image())
button.pack(side='top')

buttonl = tk.Button(frame, text="left",bg="grey", command=lambda:a.explore(-1))
buttonl.pack(side='left')

buttonr = tk.Button(frame, text="right",bg="grey", command=lambda:a.explore(1))
buttonr.pack(side='right')

buttond = tk.Button(frame, text="delete",bg="grey", command=lambda:a.delete_image())
buttond.pack(side='bottom')

buttonr = tk.Button(frame, text="restore",bg="grey", command=lambda:a.restore_deleted_image())
buttonr.place(relx=0.55, rely=0.92)


'''
buttonc = tk.Button(frame, text="convert",bg="grey")
buttonc.place(relx=0.85, rely=0.92)

array = ['png', 'jpeg', 'bmp']

clicked = StringVar()
clicked.set(".x")
print(clicked)

drop = OptionMenu(frame,clicked, *array)
drop.place(relx=0.7, rely=0.91)
'''   
root.mainloop()
#t1.join()



    

    
