import tkinter as tk 
from PIL import ImageTk, Image
from tkinter import filedialog
import os

#Big resolution picture take some time to open
#Create a hidden file to store a deleted picture

class frame():

    def __init__(self):

        self.current_index = 0
        self.current_picture =""
        self.dir_picture = []   #stores pictures names only
        self.current_path = ""
        self.backup_img = None
        self.backup_img_name =""

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
        img = Image.open(self.current_path+"/"+self.dir_picture[self.current_index])
        self.backup_img = img.copy()
        self.backup_img_name = self.current_picture
        img.close()
    
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
        img = ImageTk.PhotoImage((Image.open(self.current_path+"/"+self.dir_picture[self.current_index]).resize((250,250))))
        framel = tk.Label(frame,bg='blue', image = img)
        framel.place(relx = 0.1, rely= 0.1, relwidth=0.8,relheight=0.8)
        root.mainloop()
    


a = frame()


HEIGHT = 400
WIDTH = 450
    
root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT,width=WIDTH)
canvas.pack()
img = ImageTk.PhotoImage((Image.open("rr.jpg").resize((250,250))))

    #filename = filedialog.askopenfilename(title='open')

    #directory = filename.rpartition("/") #rpartition : everything before the last occurence of the argument
    #print(directory)
    #os.listdir("C:/Users/pc1/Desktop") 
    #print(os.listdir("C:/Users/pc1/Desktop"))

frame = tk.Frame(root,bg='yellow')
frame.place(relx = 0.1, rely= 0.1, relwidth=0.8,relheight=0.8)

framel = tk.Label(frame,bg='blue', image = img)
framel.place(relx = 0.1, rely= 0.1, relwidth=0.8,relheight=0.8)
    

    #framel.pack()
button = tk.Button(frame, text="open",bg="grey", command=lambda:a.open_image())
button.pack(side='top')

buttonl = tk.Button(frame, text="left",bg="grey", command=lambda:a.explore(-1))
buttonl.pack(side='left')

buttonr = tk.Button(frame, text="right",bg="grey", command=lambda:a.explore(1))
buttonr.pack(side='right')

buttond = tk.Button(frame, text="delete",bg="grey", command=lambda:a.delete_image())
buttond.pack(side='bottom')

buttonr = tk.Button(frame, text="restore",bg="grey", command=lambda:a.restore_deleted_image())
buttonr.pack(side='bottom')

   

root.mainloop()
    
