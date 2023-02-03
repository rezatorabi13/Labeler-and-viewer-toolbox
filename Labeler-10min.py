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

def switch():
    # Define our switch function
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

def generate_child_path(path,child_num):
    path=str(path)
    path_list = path.split('\\')
    path_list_2 = path_list[-1].split('_')
    path_list_2[1]=path_list_2[1]+str(child_num)+'0'
    path_list[-1]='_'.join(path_list_2)
    path_child = '\\'.join(path_list) 
    return path_child

def show_label():
    global i
    global j
    n=(i*6)+j-1  #n starts from 0
    global label_info 
    
    #if labels[n]!='not_assigned':
        #label_info = Label(text=labels[n]+'                    ', fg = 'red', bg = 'SystemButtonFace', font = 'Aria -12 bold').place(x = 750, y = 40)
    #else:
        #label_info = Label(text='                                        ', fg = 'red', bg = 'SystemButtonFace', font = 'Aria -12 bold').place(x = 750, y = 40)

    if initializing==True:
        if labels[n]!='not_assigned':
            label_info = Label(text=labels[n]+'                    ', fg = 'red', bg = 'SystemButtonFace', font = 'Aria -13 bold')
            label_info.place(x = 750, y = 40)
        else:
            label_info = Label(text='                                        ', fg = 'red', bg = 'SystemButtonFace', font = 'Aria -13 bold')
            label_info.place(x = 750, y = 40)
            
    if initializing==False:
        if labels[n]!='not_assigned':
            label_info.configure(text=labels[n]+'                    ')
            label_info.place(x = 750, y = 40)
        else:
            label_info.configure(text='                                        ')
            label_info.place(x = 750, y = 40)


def load_labels():
    global names
    global labels
    global year_global
    
    filename = filedialog.askopenfile()
    #print(str(filename))
    f_n=str(filename.name).split('/')[-1].split('.')[0]
    #print(f_n+'_labeled')
    #print(type(f_n))
    if (f_n!=year_global and f_n!=year_global+'_labeled'):
        messagebox.showerror(title = 'Error', message = 'Select the right file for selected year')
        #print(messagebox.askyesno(title = 'Hungry?', message = 'Do you want SPAM?'))
        #tkinter.messagebox.showerror(title=None, message=None, **options)
    
    else:
        print("Please wait until the labeled data is loaded...")
        #data = pd.read_excel (year_global+'.xlsx') 
        data = pd.read_excel (str(filename.name))
        df = pd.DataFrame(data, columns= ['Name','Label'])
        names=df['Name']
        labels=df['Label']
        print("Labeled data has been loaded succesfully!")
        show_label()
    
def save_data():
    global names
    global labels
    global year_global
    #global df
    
    output_path= year_global+'.xlsx'
    df=pd.DataFrame(names, columns=['Name'])
    df['Label']=labels
    df.to_excel(output_path)
    print('The data has been saved')
    #print(df.head())
    #print(len(df))
    #print('The command is working')
    
def save_labeled_data():
    global names
    global labels
    global year_global
    
    output_path= year_global+'_labeled.xlsx'
    df=pd.DataFrame(names, columns=['Name'])
    df['Label']=labels
    df=df[df['Label']!='not_assigned']
    df.to_excel(output_path)
    print('The data has been saved')
    #print(df.head())
    #print(len(df))
    #print('The command is working')

def select_year():
    global year_global
    year_global = year_s.get()
    print('The data is loading...')
    yaer_Gui.destroy()

def find_fullsky_paths(path):
    YY=path.split('\\')[2]
    MM=path.split('\\')[3]
    DD=path.split('\\')[4]
    Site=path.split('\\')[5]
    UT=path.split('\\')[6][2:]
    path_fulls='D:\\stream0\\'+YY+'\\'+MM+'\\'+DD+'\\'+Site+'\\'
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

def show_figures():
    global i
    global j
    global filename1
    global filename2
    global filename3
    global filename4
    global filename5
    global filename6
    global panel
    global parent_info
    global child_info
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
    
    if j==1:
        img = cv2.rectangle(img, (0, 0), (100, 255), (255, 0, 0))
    if j==2:
        img = cv2.rectangle(img, (100, 0), (200, 255), (255, 0, 0))
    if j==3:
        img = cv2.rectangle(img, (200, 0), (300, 255), (255, 0, 0))
    if j==4:
        img = cv2.rectangle(img, (300, 0), (400, 255), (255, 0, 0))
    if j==5:
        img = cv2.rectangle(img, (400, 0), (500, 255), (255, 0, 0))
    if j==6:
        img = cv2.rectangle(img, (500, 0), (600, 255), (255, 0, 0))
    
    im = Image.fromarray(img)
    resized_image= im.resize((900,350), Image.ANTIALIAS)
    new_image = ImageTk.PhotoImage(image=resized_image)
               
    #resized_image= img.resize((900,350), Image.ANTIALIAS)
    #new_image= ImageTk.PhotoImage(resized_image)
        
    #The Label widget is a standard Tkinter widget used to display a text or image on the screen.
    #panel = Label(image = new_image)  #label is a better name than panel in here
    if initializing==True:
        panel = Label(image = new_image)
    else:
        panel.configure(image = new_image)
    panel.image = new_image        #keep a reference
    panel.place(x =10 , y =290)
        
    #Showing information relating to parrent path (1 hour keogram)
    #path_parent, path_child = find_parent_child_paths()
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
    #Show information about child path
    if initializing==True:
        child_title = Label(text='10 minute keogram:', fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12').place(x = 10, y = 40)
    
    if initializing==True:
        if j==1:
            if filename1!='':
                child_info = Label(text=filename1+'        ', fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12 bold')
                child_info.place(x = 160, y = 40)
            else:
                child_info = Label(text='                                                          '*3, fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12 bold')
                child_info.place(x = 160, y = 40)
        if j==2:
            if filename2!='':
                child_info = Label(text=filename2+'        ', fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12 bold')
                child_info.place(x = 160, y = 40)
            else:
                child_info = Label(text='                                                           '*3, fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12 bold')
                child_info.place(x = 160, y = 40)
        if j==3:
            if filename3!='':
                child_info = Label(text=filename3+'        ', fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12 bold')
                child_info.place(x = 160, y = 40)
            else:
                child_info = Label(text='                                                            '*3, fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12 bold')
                child_info.place(x = 160, y = 40)
        if j==4:
            if filename4!='':
                child_info = Label(text=filename4+'        ', fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12 bold')
                child_info.place(x = 160, y = 40)
            else:
                child_info = Label(text='                                                             '*3, fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12 bold')
                child_info.place(x = 160, y = 40)
        if j==5:
            if filename5!='':
                child_info = Label(text=filename5+'        ', fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12 bold')
                child_info.place(x = 160, y = 40)
            else:
                child_info = Label(text='                                                             '*3, fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12 bold')
                child_info.place(x = 160, y = 40)
        if j==6:
            if filename6!='':
                child_info = Label(text=filename6+'        ', fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12 bold')
                child_info.place(x = 160, y = 40)
            else:
                child_info = Label(text='                                                             '*3, fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12 bold')
                child_info.place(x = 160, y = 40) 
    
    if initializing==False:
        if j==1:
            if filename1!='':
                child_info.configure(text=filename1+'        ')#, fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12 bold').place(x = 160, y = 40)
            else:
                child_info.configure(text='                                                          '*3)#, fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12 bold').place(x = 160, y = 40)
        if j==2:
            if filename2!='':
                child_info.configure(text=filename2+'        ')#, fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12 bold').place(x = 160, y = 40)
            else:
                child_info.configure(text='                                                           '*3)#, fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12 bold').place(x = 160, y = 40)
        if j==3:
            if filename3!='':
                child_info.configure(text=filename3+'        ')#, fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12 bold').place(x = 160, y = 40)
            else:
                child_info.configure(text='                                                            '*3)#, fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12 bold').place(x = 160, y = 40)
        if j==4:
            if filename4!='':
                child_info.configure(text=filename4+'        ')#, fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12 bold').place(x = 160, y = 40)
            else:
                child_info.configure(text='                                                             '*3)#, fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12 bold').place(x = 160, y = 40)  
        if j==5:
            if filename5!='':
                child_info.configure(text=filename5+'        ')#, fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12 bold').place(x = 160, y = 40)
            else:
                child_info.configure(text='                                                             '*3)#, fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12 bold').place(x = 160, y = 40)   
        if j==6:
            if filename6!='':
                child_info.configure(text=filename6+'        ')#, fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12 bold').place(x = 160, y = 40)
            else:
                child_info.configure(text='                                                             '*3)#, fg = 'black', bg = 'SystemButtonFace', font = 'Aria -12 bold').place(x = 160, y = 40)   
           
    #Show full upper pannel images
    #plot_upper_images(filename1,filename2,filename3,filename4,filename5,filename6,alpha_global,beta_global)
    plot_upper_images(filename1,filename2,filename3,filename4,filename5,filename6,alpha_global,beta_global,cmax_global)    
   
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


def plot_full_sky(filename, alpha, beta ,xp, yp,cmax,t):
    global j
    global panel_im1
    global panel_im2
    global panel_im3
    global panel_im4
    global panel_im5
    global panel_im6
    #del panel_im
    #print('The path is: ',filename)
    #filename='D:\\stream0\\2008\\01\\01\\atha_themis02\\20080101_020000_021039_atha_themis02_full.png'
    #print('The modified path is: ',filename)
    
    # Read RGB image
    img=cv2.imread(filename, cv2.IMREAD_ANYDEPTH)
    #img=cv2.imread(filename)
    
    if is_on == True:
        adj_img=bytescale(img,cmax)
    else:
        adj_img=img  
    
    #print(adj_img.max())
        
    adj_img =(adj_img/(adj_img.max()))*255
    adj_img = cv2.convertScaleAbs(adj_img, alpha=alpha, beta=beta)
    
    #print(adj_img.max())
    
    im = Image.fromarray(adj_img)
    im= im.resize((150,150), Image.ANTIALIAS)
    imgtk = ImageTk.PhotoImage(image=im)
    
    #The label widget
    #panel_im = Label(image = imgtk)  #label is a better name than panel in here
    #panel_im.image = imgtk        #keep a reference
    #panel_im.place(x =xp , y =yp)
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
        
def update_i(number):
    global i
    
    i=int(number)
    show_figures()
    show_label()

def filter_site():
    global filter_list
    global filter_on
    global i
    global j
    i=0
    j=1
    
    if filter_on==False:
        filter_on=True
        select_site_button.config(bg='green')

    else:
        filter_on=False
        select_site_button.config(bg='SystemButtonFace')
        filter_label=Label(text='                                                                            ', bg = 'SystemButtonFace', font = 'Aria -12 bold').place(x = 235, y = 8)

    
    if filter_on==True:
        filter_var = site.get()
        for k in range(len(filter_list)):
            if str(path_list[k]).split('\\')[5]==filter_var:
                filter_list[k]="no"
            else:
                filter_list[k]="yes"
        filter_label=Label(text='Filter is on for site:  '+filter_var, fg = 'green', bg = 'SystemButtonFace', font = 'Aria -12 bold').place(x = 235, y = 8)


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
    plot_upper_images(filename1,filename2,filename3,filename4,filename5,filename6, alpha, beta_global, cmax_global)
    #plot_upper_images(alpha,beta_global)
    
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
    #plot_upper_images(alpha_global,beta)

def update_bytescale(cmax): #high is cmax
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
    global j
    global alpha_global
    global beta_global
    global cmax_global
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
           print('Reached to the end of the list')
    
    #panel.image=''
    show_figures()
    show_label()
    
def show_previous(): 
    global i
    global j
    global alpha_global
    global beta_global
    global cmax_global
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
    
def show_next_chunk():
    global i
    global j
    global filter_list
    

    filter_flag=True
    while filter_flag:
        j+=1
        if (i==len(filter_list)-1 and j>6):
            print('Reached to the end of the list')
            j=6
            break
        if (i<len(filter_list)-1 and j>6):
            j=1
            i+=1
            scroll_i.set(i)
        if filter_list[i]=='no':
            filter_flag=False 
 
    show_figures()
    show_label()
    
def show_previous_chunk():
    global i
    global j
    global filter_list
    
    filter_flag=True
    while filter_flag:
        j-=1
        if (i<=0 and j<1):  
            #print('Reached to the begining of the list')
            j=1
            break
        if (i>0 and j<1):
            j=6
            i-=1
            #break
        scroll_i.set(i)
        if filter_list[i]=='no':
            filter_flag=False 
                         
    show_figures()
    show_label()

def add_diffuse():
    global i
    global j
    n=(i*6)+j-1
    
    labels[n]='diffuse'
    #show_next()
    show_next_chunk()
    
def add_other_Aurora():
    global i
    global j
    n=(i*6)+j-1
    
    labels[n]='other Aurora'
    #show_next()
    show_next_chunk()
    
def add_cloudy():
    global i
    global j
    n=(i*6)+j-1
    
    labels[n]='cloudy'
    #show_next()
    show_next_chunk()
    
def add_other():
    global i
    global j
    n=(i*6)+j-1
    
    labels[n]='other'
    #show_next()
    show_next_chunk()
 
def Erase_label():
    global i
    global j
    n=(i*6)+j-1
    
    labels[n]='not_assigned'
    #show_next()
    show_next_chunk()
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#Initializing the program and global variables
i=0 #1hour keogram indicator
j=1 #10 minute keogram indicator
#n=0
path_list=[]  #i is its indicator
path_list_child=[]  #n is its indicator

alpha_global = 2 # Contrast control (1.0-3.0) --- This is the default contrast
beta_global = 10 # Brightness control (0-100) --- This is the default brightness
cmax_global = 10000 #255
is_on = True   #Global is_on for bytescale
filter_on=False #for filtering site
year_global = ''

#Create the first Gui to get the year information
yaer_Gui = Tk()
yaer_Gui.title("AuroraX labeler")
yaer_Gui.geometry("250x200+450+200")

Instruction = Label(text="Select a year and press Enter ", fg = 'black', font = 'Aria -15').place(x = 20, y = 20)
#text = Entry(textvariable = a).pack()
year_s = StringVar()
Spinbox(from_ = 2006, to = 2020, width=6, textvariable = year_s, font=12).place(x =85 , y =70)

#yearButton = Button(text='Enter', fg='black', bg='green',command = select_year, font=20).place(x =120 , y =180)#.pack()
yearButton = Button(text="Enter", relief= RAISED, width=6, height= 2,
                        bg='gray', fg='black', bd=7, activebackground='green', 
                        activeforeground='white',command = select_year, font=16).place(x =85 , y =110)
yaer_Gui.mainloop()


#Load the data for the selectwd year
#year_global = '2008'

for path in Path('E:\\Keograms\\'+year_global).rglob('*.jpg'):
    path_list.append(path)
    for child_num in range(6):
        path_c=generate_child_path(path,child_num)
        path_list_child.append(path_c)
    
names=path_list_child    #data are saved based on child lists
#print(names[0])
#print(names[1])
#print(len(names))
labels=len(names)*['not_assigned']
#h_num=len(path_list)
#print(h_num)
filter_list=len(path_list)*['no'] #filtering is based on argument i

print('The data has been loaded!')

#df=pd.DataFrame(names, columns=['Name'])
#df['Label']=labels
    
#------------------------------------------------------------------------------
#Creating main window
window = Tk()
window.geometry('1180x685+50+5')
window.title('Aurora Image Viewer and Keogram Labeling Toolbox v1')
#window.configure(background='grey')
#Welcome_label = Label(text="Welcome to Aurorax toolbox for labeling the Keogram data", fg = 'black').place(x = 0, y = 0)

#initialize upper panel paths (full sky image paths)
filename1,filename2,filename3,filename4,filename5,filename6 = find_fullsky_paths(str(path_list[i]))
#Show keogram and upper panel figures

initializing=True
show_figures()
show_label()
initializing=False
#create_rectangle(50, 50, 100, 100, fill="", outline = 'red') 
#------------------------------------------------------------------------------
#Designing Menu bar
menuBar = Menu(window)
window.config(menu=menuBar)

filemenu = Menu(menuBar)
menuBar.add_cascade(label="File", menu=filemenu)

filemenu.add_command(label="Open", command=load_labels)
filemenu.add_separator()
filemenu.add_command(label="Save", command=save_data)
filemenu.add_separator()
filemenu.add_command(label="Save labeled data", command=save_labeled_data)


helpMenu = Menu(menuBar)
menuBar.add_cascade(label="Help", menu=helpMenu)

helpMenu.add_command(label="About")
#------------------------------------------------------------------------------
#Designing site and data selection
site_info = Label(text="Site: ", fg = 'black', font = 'Aria -13 bold').place(x = 10, y = 10)
site = StringVar()
combobox = ttk.Combobox(window, textvariable = site)
combobox.place(x =50 , y =10)
combobox.config(values = ('atha_themis02', 'gbay_themis03', 'fsim_themis05', 'whit_themis07', 
                          'tpas_themis08', 'snkq_themis09', 'fsmi_themis10', 'snap_themis10',
                          'mcgr_themis11', 'rank_themis12', 'kuuj_themis13', 'fykn_themis14', 
                          'pgeo_themis15', 'chbg_themis16', 'inuv_themis17', 'pina_themis18',
                          'gill_themis19', 'gako_themis20', 'kapu_themis21', 'kian_themis22',
                          'nrsq'), width=13)
site.set('atha_themis02')

select_site_button = Button(text="Filter", relief= RAISED, width=7, height= 1,
                        bg='gray', fg='black', bd=3, command=filter_site)
select_site_button.place(x =170 , y =5)

#date_info = Label(text="Month: ", fg = 'black', font = 'Aria -13 bold').place(x = 460, y = 10)
#month = StringVar()
#Spinbox(window, from_ = 1, to = 12, width=7, textvariable = month).place(x =510 , y =10)
#month.set('1')

#select_month_button = Button(text="Filter", relief= RAISED, width=7, height= 1,
#                        bg='gray', fg='black', bd=3, activebackground='green', 
#                        activeforeground='white', command=filter_month)
#select_month_button.place(x =570 , y =5)
#------------------------------------------------------------------------------
#Designing labaling keys
diffuse_button = Button(text="diffuse", relief= RAISED, width=13, height= 3,
                        bg='green', fg='black', bd=7, activebackground='green', 
                        activeforeground='white', command=add_diffuse).place(x =1000 , y =150)
other_Aurora_button = Button(text="other Aurora", relief= RAISED, width=13, height= 3,
                        bg='#ADD8E6', fg='black', bd=7, activebackground='green', 
                        activeforeground='white',command=add_other_Aurora).place(x =1000 , y =225)
cloudy_button = Button(text="cloudy", relief= RAISED, width=13, height= 3,
                        bg='#FFFDD0', fg='black', bd=7, activebackground='green', 
                        activeforeground='white',command=add_cloudy).place(x =1000 , y =330)
other_button = Button(text="other", relief= RAISED, width=13, height= 3,
                        bg='#ff726f', fg='black', bd=7, activebackground='green', 
                        activeforeground='white',command=add_other).place(x =1000 , y =405)

forward = Button(command=show_next)
forward.place(x =1070 , y =50)

logof = PhotoImage(file = 'forward.png')
forward.config(image = logof, compound = LEFT)
small_logo_f = logof.subsample(4, 4)
forward.config(image = small_logo_f)


backward = Button(command=show_previous)
backward.place(x =980 , y =50)

logob = PhotoImage(file = 'backward.png')
backward.config(image = logob, compound = LEFT)
small_logo_b = logob.subsample(4, 4)
backward.config(image = small_logo_b)

Erase_button = Button(text="Erase", relief= RAISED, width=13, height= 2,
                        bg='gray', fg='black', bd=7, activebackground='green', 
                        activeforeground='white',command=Erase_label).place(x =1000 , y =600)
#------------------------------------------------------------------------------
#Designing forward and backward button for chunk keograms
forward_chunk = Button(command=show_next_chunk)
forward_chunk.place(x =1060 , y =500)

logofc = PhotoImage(file = 'forward.png')
forward_chunk.config(image = logofc, compound = LEFT)
small_logo_fc = logofc.subsample(5, 5)
forward_chunk.config(image = small_logo_fc)

backward_chunk = Button(command=show_previous_chunk)
backward_chunk.place(x =990 , y =500)

logobc = PhotoImage(file = 'backward.png')
backward_chunk.config(image = logobc, compound = LEFT)
small_logo_bc = logobc.subsample(5, 5)
backward_chunk.config(image = small_logo_bc)
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
