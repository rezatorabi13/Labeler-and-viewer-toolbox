#Importing libraries
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
import cv2

import shutil
import gzip
import bz2
import numpy as np

from tkinter import filedialog
from tkinter import messagebox
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#functions

def delete_data():
    global i
    
    try:
        edited_list.remove(path_list[i])
        edited_labels.remove(labels[i])
    except:
        pass

def show_label():
    global i
    global label_info
    
    if initializing==True:
        label_info = Label(text=labels[i]+'                    ', fg = 'red', bg = 'SystemButtonFace', font = 'Aria -13 bold')
        label_info.place(x = 450, y = 40)
    else:
        label_info.configure(text=labels[i]+'                    ')
        label_info.place(x = 450, y = 40)


def save_edited_data():
    global path_list
    global labels
    
    output_path='edited.xlsx'
    df=pd.DataFrame(edited_list, columns=['Name'])
    df['Label']=edited_labels
    df.to_excel(output_path)
    print('The edited data has been saved')

def switch():
    global is_on
    global on_button
     
    if is_on==True:
        on_button.config(text='OFF', bg = 'SystemButtonFace')
        is_on=False
        show_figures()
    else:
        on_button.config(text='ON', bg = 'green')
        is_on=True
        show_figures()

def bytescale(data, cmax, cmin=None, high=65535, low=0):
    if high > 65535:
        raise ValueError("`high` should be less than or equal to 65535.")
    if low < 0:
        raise ValueError("`low` should be greater than or equal to 0.")
    if high < low:
        raise ValueError("`high` should be greater than or equal to `low`.")

    if cmin is None:
        cmin = data.min()
    if cmax is None:
        cmax = data.max()
        
    if cmax<cmin:
        cmin=0

    cscale = cmax - cmin
    if cscale < 0:
        raise ValueError("`cmax` should be larger than `cmin`.")
    elif cscale == 0:
        cscale = 1

    scale = float(high - low) / cscale
    bytedata = (data - cmin) * scale + low
    return (bytedata.clip(low, high) + 0.5).astype(np.uint16)

def show_figures():
    global i
    #global j
    global filename1
    global filename2
    global filename3
    global filename4
    global filename5
    global filename6
    global panel
    global parent_info
    global label_global
    #global child_info
    
 #Load an image in the script
    #img= (Image.open(path_list[i]))
    img=cv2.imread(str(path_list[i]))
    #print(str(path_list[i]))
    
    img = cv2.rectangle(img, (0, 0), (100, 255), (0, 255, 0))
    img = cv2.rectangle(img, (100, 0), (200, 255), (0, 255, 0))
    img = cv2.rectangle(img, (200, 0), (300, 255), (0, 255, 0))
    img = cv2.rectangle(img, (300, 0), (400, 255), (0, 255, 0))
    img = cv2.rectangle(img, (400, 0), (500, 255), (0, 255, 0))
    img = cv2.rectangle(img, (500, 0), (600, 255), (0, 255, 0))
    
    im = Image.fromarray(img)
    resized_image= im.resize((900,350), Image.ANTIALIAS)
    new_image = ImageTk.PhotoImage(image=resized_image)
               
    
    if initializing==True:
        panel = Label(image = new_image)
    else:
        panel.configure(image = new_image)
    panel.image = new_image        #keep a reference
    panel.place(x =10 , y =290)
        
    #Showing information relating to parrent path (1 hour keogram)
    if initializing==True:
        parent_info = Label(text=str(path_list[i])+'     ', fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12 bold')
    else:
        parent_info.configure(text=str(path_list[i])+'     ')
    parent_info.place(x = 160, y = 60)
    if initializing==True:
        parent_title = Label(text='1 hour keogram:', fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12')
        parent_title.place(x = 10, y = 60) 

    #find upper panel paths (full sky image paths)
    filename1,filename2,filename3,filename4,filename5,filename6 = find_fullsky_paths(str(path_list[i]))
    
    if initializing==True:
        label_title = Label(text='Label:', fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12').place(x = 10, y = 40)
        label_info =  Label(text=label_global , fg = 'red', bg = 'SystemButtonFace', font = 'Aria -13').place(x = 450, y = 40)
    #Show full upper pannel images
    plot_upper_images(filename1,filename2,filename3,filename4,filename5,filename6,alpha_global,beta_global,cmax_global)    
  
def update_i(number):
    global i
    
    i=int(number)
    show_figures()
    show_label()
    
def plot_not_available(xp,yp,t):
    global panel_im1
    global panel_im2
    global panel_im3
    global panel_im4
    global panel_im5
    global panel_im6
    
    img=cv2.imread('not_available.jpg')
    adj_img = cv2.convertScaleAbs(img)
    
    im = Image.fromarray(adj_img)
    im= im.resize((150,150), Image.ANTIALIAS)
    imgtk = ImageTk.PhotoImage(image=im)
    

    if t==1:
        if initializing==True:
            panel_im1 = Label(image = imgtk)
        else:
            panel_im1.configure(image=imgtk)  #label is a better name than panel in here
        panel_im1.image = imgtk        #keep a reference
        panel_im1.place(x =xp , y =yp)

    if t==2:
        if initializing==True:
            panel_im2 = Label(image = imgtk)
        else:
            panel_im2.configure(image=imgtk)
        panel_im2.image = imgtk        #keep a reference
        panel_im2.place(x =xp , y =yp)

    if t==3:
        if initializing==True:
            panel_im3 = Label(image = imgtk)
        else:
            panel_im3.configure(image=imgtk)
        panel_im3.image = imgtk        #keep a reference
        panel_im3.place(x =xp , y =yp)
        
    if t==4:
        if initializing==True:
            panel_im4 = Label(image = imgtk)
        else:
            panel_im4.configure(image=imgtk)
        panel_im4.image = imgtk        #keep a reference
        panel_im4.place(x =xp , y =yp)        
        
    if t==5:
        if initializing==True:
            panel_im5 = Label(image = imgtk)
        else:
            panel_im5.configure(image=imgtk)
        panel_im5.image = imgtk        #keep a reference
        panel_im5.place(x =xp , y =yp)

    if t==6:
        if initializing==True:
            panel_im6 = Label(image = imgtk)
        else:
            panel_im6.configure(image=imgtk)
        panel_im6.image = imgtk        #keep a reference
        panel_im6.place(x =xp , y =yp)


def find_fullsky_paths(path):
    YY=path.split('\\')[2]
    MM=path.split('\\')[3]
    DD=path.split('\\')[4]
    Site=path.split('\\')[5]
    UT=path.split('\\')[6][2:]
    path_fulls='F:\\stream0\\'+YY+'\\'+MM+'\\'+DD+'\\'+Site+'\\'
    path_name= YY+MM+DD+'_'+UT

    path_full1=[]
    path_full2=[]
    path_full3=[]
    path_full4=[]
    path_full5=[]
    path_full6=[]

    for filename in Path(path_fulls).rglob(path_name+'00'+'*.png'):
        path_full1.append(filename)
    for filename in Path(path_fulls).rglob(path_name+'10'+'*.png'):
        path_full2.append(filename)    
    for filename in Path(path_fulls).rglob(path_name+'20'+'*.png'):
        path_full3.append(filename)
    for filename in Path(path_fulls).rglob(path_name+'30'+'*.png'):
        path_full4.append(filename)
    for filename in Path(path_fulls).rglob(path_name+'40'+'*.png'):
        path_full5.append(filename)
    for filename in Path(path_fulls).rglob(path_name+'50'+'*.png'):
        path_full6.append(filename)
        
    if path_full1==[]:
        f1=''
    else: f1=str(path_full1[0])
    
    if path_full2==[]:
        f2=''
    else: f2=str(path_full2[0])  
    
    if path_full3==[]:
        f3=''
    else: f3=str(path_full3[0])
    
    if path_full4==[]:
        f4=''
    else: f4=str(path_full4[0])
    
    if path_full5==[]:
        f5=''
    else: f5=str(path_full5[0])
    
    if path_full6==[]:
        f6=''
    else: f6=str(path_full6[0])

    return f1,f2,f3,f4,f5,f6

    
def plot_full_sky(filename, alpha, beta ,xp, yp,cmax,t):
    global j
    global panel_im1
    global panel_im2
    global panel_im3
    global panel_im4
    global panel_im5
    global panel_im6

    
    # Read RGB image
    img=cv2.imread(filename, cv2.IMREAD_ANYDEPTH)
    
    if is_on == True:
        adj_img=bytescale(img,cmax)
    else:
        adj_img=img  
    
        
    adj_img =(adj_img/(adj_img.max()))*255
    adj_img = cv2.convertScaleAbs(adj_img, alpha=alpha, beta=beta)
    
    
    im = Image.fromarray(adj_img)
    im= im.resize((150,150), Image.ANTIALIAS)
    imgtk = ImageTk.PhotoImage(image=im)
    
    
    if t==1:
        if initializing==True:
            panel_im1 = Label(image = imgtk)
        else:
            panel_im1.configure(image=imgtk)
        panel_im1.image = imgtk        #keep a reference
        panel_im1.place(x =xp , y =yp)

    if t==2:
        if initializing==True:
            panel_im2 = Label(image = imgtk)
        else:
            panel_im2.configure(image=imgtk)
        panel_im2.image = imgtk        #keep a reference
        panel_im2.place(x =xp , y =yp)

    if t==3:
        if initializing==True:
            panel_im3 = Label(image = imgtk)
        else:
            panel_im3.configure(image=imgtk)
        panel_im3.image = imgtk        #keep a reference
        panel_im3.place(x =xp , y =yp)
        
    if t==4:
        if initializing==True:
            panel_im4 = Label(image = imgtk)
        else:
            panel_im4.configure(image=imgtk)
        panel_im4.image = imgtk        #keep a reference
        panel_im4.place(x =xp , y =yp)        
        
    if t==5:
        if initializing==True:
            panel_im5 = Label(image = imgtk)
        else:
            panel_im5.configure(image=imgtk)
        panel_im5.image = imgtk        #keep a reference
        panel_im5.place(x =xp , y =yp)

    if t==6:
        if initializing==True:
            panel_im6 = Label(image = imgtk)
        else:
            panel_im6.configure(image=imgtk)
        panel_im6.image = imgtk  
        panel_im6.place(x =xp , y =yp)
    
def plot_upper_images(filename1,filename2,filename3,filename4,filename5,filename6,alpha,beta,cmax):
   
    if filename1!='':
        plot_full_sky(filename1,alpha,beta,10,130,cmax,1)
    else:
        plot_not_available(10,130,1)
        
    if filename2!='':        
        plot_full_sky(filename2,alpha,beta,160,130,cmax,2)
    else:
        plot_not_available(160,130,2)  
        
    if filename3!='':
        plot_full_sky(filename3,alpha,beta,310,130,cmax,3)
    else:
        plot_not_available(310,130,3)     
    
    if filename4!='':    
        plot_full_sky(filename4,alpha,beta,460,130,cmax,4)
    else:
        plot_not_available(460,130,4)     
    
    if filename5!='':      
        plot_full_sky(filename5,alpha,beta,610,130,cmax,5)
    else:
        plot_not_available(610,130,5)             
        
    if filename6!='':        
        plot_full_sky(filename6,alpha,beta,760,130,cmax,6)
    else:
        plot_not_available(760,130,6)
    
def update_contrast(alpha):
    global beta_global
    global alpha_global
    global cmax_global
    global filename1
    global filename2
    global filename3
    global filename4
    global filename5
    global filename6

    alpha=int(alpha)
    alpha_global=alpha
    plot_upper_images(filename1,filename2,filename3,filename4,filename5,filename6, alpha, beta_global,cmax_global)
    
    
def update_brightness(beta):
    global alpha_global
    global beta_global
    global cmax_global
    global filename1
    global filename2
    global filename3
    global filename4
    global filename5
    global filename6

    beta=int(beta)
    beta_global=beta
    plot_upper_images(filename1,filename2,filename3,filename4,filename5,filename6, alpha_global, beta, cmax_global)
    
def update_bytescale(cmax):
    global alpha_global
    global beta_global
    global cmax_global
    global filename1
    global filename2
    global filename3
    global filename4
    global filename5
    global filename6

    cmax=int(cmax)
    cmax_global=cmax
    plot_upper_images(filename1,filename2,filename3,filename4,filename5,filename6, alpha_global, beta_global, cmax)
    
    
def show_next(): 
    global i
    #global j
    global alpha_global
    global beta_global
    
    global filename1
    global filename2
    global filename3
    global filename4
    global filename5
    global filename6
    
    global filter_list
    
    filter_flag=True
    while filter_flag:
        if i<len(filter_list)-1:
            i+=1
            scroll_i.set(i)
        if filter_list[i]=='no':
           filter_flag=False 
        if i>=len(filter_list)-1:
           filter_flag=False  
    
    show_figures()
    show_label()
    
def show_previous(): 
    global i
    #global j
    global alpha_global
    global beta_global
    
    global filename1
    global filename2
    global filename3
    global filename4
    global filename5
    global filename6
    

    filter_flag=True
    while filter_flag:
        i-=1
        scroll_i.set(i)
        if filter_list[i]=='no':
           filter_flag=False 
        if i<0:
           filter_flag=False  
           i+=1
           #print('Reached to the begining of the list')
    
    show_figures()
    show_label()
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#Initializing the program and global variables
i=0 #1hour keogram indicator
#j=1 #10 minute keogram indicator
#n=0
#path_list=[]  #i is its indicator
#path_list_child=[]  #n is its indicator

alpha_global = 2 # Contrast control (1.0-3.0) --- This is the default contrast
beta_global = 10 # Brightness control (0-100) --- This is the default brightness
#high_global = 250
is_on = True   #Global is_on
label_global=''
cmax_global = 10000 #255
#filter_on=False #for filtering site
#selected_list=[]
#selected_label=[]

#load the data for the selected file       
df = pd.read_excel('selected.xlsx')
#df = pd.DataFrame(data, columns= ['Name','Label'])
path_list=list(df['Name'])
labels=list(df['Label'])

edited_list=path_list.copy()

edited_labels=labels.copy()


print("Selected data has been loaded succesfully!")
#path_list=[find_labeled_path(i) for i in range(len(selected_df))]
print('The number of the data is: ',len(path_list))
    
#names=labeled_list
#labels=len(names)*['not_assigned']
filter_list=len(path_list)*['no'] #filtering is based on argument i

print('The data has been loaded!')
    
#------------------------------------------------------------------------------
#Creating main window
window = Tk()
window.geometry('1180x685+50+5')
window.title('Aurora Image Viewer Toolbox v1')

#initialize upper panel paths (full sky image paths)
filename1,filename2,filename3,filename4,filename5,filename6 = find_fullsky_paths(str(path_list[i]))
#Show keogram and upper panel figures
initializing=True
show_figures()
show_label()
initializing=False

#------------------------------------------------------------------------------
#Designing Menu bar
menuBar = Menu(window)
window.config(menu=menuBar)

filemenu = Menu(menuBar)
menuBar.add_cascade(label="File", menu=filemenu)

#filemenu.add_command(label="Open", command=load_selected)
#filemenu.add_separator()
filemenu.add_command(label="Save edited data", command=save_edited_data)
#------------------------------------------------------------------------------
#Designing labaling keys

forward = Button(command=show_next)
forward.place(x =1070 , y =280)

logof = PhotoImage(file = 'forward.png')
forward.config(image = logof, compound = LEFT)
small_logo_f = logof.subsample(3, 3)
forward.config(image = small_logo_f)


backward = Button(command=show_previous)
backward.place(x =970 , y =280)

logob = PhotoImage(file = 'backward.png')
backward.config(image = logob, compound = LEFT)
small_logo_b = logob.subsample(3, 3)
backward.config(image = small_logo_b)

delet_button = Button(text="delete", relief= RAISED, width=15, height= 3,
                        bg='gray', fg='black', bd=7, activebackground='green', 
                        activeforeground='white',command=delete_data).place(x =1000 , y =450)

#------------------------------------------------------------------------------
#Scroll bar for changing contrast, brightness and keogram image 
value_c = IntVar()
scroll_c = Scale(window, orient = HORIZONTAL, length = 200, variable = value_c, from_ = 1.0, to = 3.0, command = update_contrast)

scroll_c.place(x=70,y=85)
scroll_c.set(alpha_global)

label_contrast = Label(text='Contrast:', fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12 bold').place(x = 10, y = 103)

value_b = IntVar()
scroll_b = Scale(window, orient = HORIZONTAL, length = 200, variable = value_b, from_ = 0.0, to = 100.0, command = update_brightness)

scroll_b.place(x=360,y=85)
scroll_b.set(beta_global)

label_brighness = Label(text='Brighness:', fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12 bold').place(x = 290, y = 103)

value_h = IntVar()
scroll_h = Scale(window, orient = HORIZONTAL, length = 200, variable = value_h, from_ = 4000.0, to = 50000.0, command = update_bytescale)

scroll_h.place(x=645,y=85)
scroll_h.set(cmax_global)

label_bytescale = Label(text='Bytescale:', fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12 bold').place(x = 580, y = 103)

# Define Our Images
#on = PhotoImage(file = "on.png")
#off = PhotoImage(file = "off.png")
# Create A Button
#on_button = Button(window, image = on, bd = 0, command = switch).place(x = 790, y = 90)


#on_button = Button(command=switch)
#on_button.place(x =860 , y =100)

on_button = Button(text="ON", width=6, fg = 'black', bg = 'green', command=switch)
on_button.place(x = 860, y = 103)


value_i = IntVar()
scroll_i = Scale(window, orient = HORIZONTAL, length = 600, variable = value_i, from_ = 0.0, to = len(path_list)-1, command = update_i)

scroll_i.place(x=100,y=642)
scroll_i.set(i)
#scroll_i.config(variable = i)
#------------------------------------------------------------------------------
window.mainloop()
