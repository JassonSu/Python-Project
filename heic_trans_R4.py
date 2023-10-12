import tkinter as tk
from tkinter import *
from PIL import ImageTk , Image
from tkinter import ttk
from tkinter import filedialog
import os
import pillow_heif
from pillow_heif import register_heif_opener
register_heif_opener()

def search_heic_files(folder_path):
        heic_files = []
        for root, dirs, files in os.walk(folder_path):
           for file in files:
               if file.lower().endswith('.heic'):
                   heic_files.append(file.split('.')[0])
        return heic_files

def search_jpg_files(folder_path):
        jpg_files = []
        for root, dirs, files in os.walk(folder_path):
           for file in files:
               if file.lower().endswith('.jpg'):
                   jpg_files.append(file.split('.')[0])
        return jpg_files

def open_dir():
    global folder_path , heic_files
    file_path = filedialog.askdirectory(parent=root,initialdir='../')
    dir_entry.insert(0, file_path)
    folder_path=file_path
    heic_files = search_heic_files(folder_path)
    if heic_files==[]:
        c.set(f'這個目錄沒有HEIC檔，請更換目錄')
    else:
        c.set(f'這個目錄找到{len(heic_files)}個 HEIC 檔案')

def clear():
    b.set('')
    c.set('')  
#    dir_entry.delete('0','end')   # 清空輸入欄位內容

# 使用範例
def heic_trans_jpg():
    target_path=f'{folder_path}/trans-jpg'
    
    if not os.path.exists(target_path):
        os.makedirs(target_path)
        c.set(f'建立{target_path}資料夾')

    jpg_dataset=search_jpg_files(target_path)
    heic_dataset=search_heic_files(folder_path)

    def heic_gen():             # my_generator 是一个生成器函数，它会在每次迭代时产生一个值，并在下一次迭代时继续执行。
        global files_hg
        for files_hg in heic_dataset:
            heic_image_o=Image.open(f'{folder_path}/{files_hg}.heic')            
            yield heic_image_o

    if jpg_dataset==[]:
        for heic_image_s in heic_gen():
            heic_image_s.save(f"{target_path}/{files_hg}.jpg",format="jpeg")
            jpg_dataset.append(files_hg)
            c.set(f'轉檔{files_hg}')    
            
    else:
        im_rest_dataset=list(set(heic_dataset)-set(jpg_dataset))
        def heic_rest_gen():             # my_generator 是一个生成器函数，它会在每次迭代时产生一个值，并在下一次迭代时继续执行。
            global files_rest_hg
            for files_rest_hg in im_rest_dataset:
                heic_image_r=Image.open(f'{folder_path}/{files_rest_hg}.heic')
                yield heic_image_r
        for heic_image_r in heic_rest_gen():          
            heic_image_r.save(f"{target_path}/{files_rest_hg}.jpg",format="jpeg")
            c.set(f'轉檔{files_rest_hg}')
    c.set(f'已轉{len(im_rest_dataset)}個heic檔完成!\n檔案存在{target_path}')

root = tk.Tk()
root.title('HEIC 轉 JPG 程式--Y.Y.Su')

frame_1 = tk.Frame(root)
frame_1.pack(side='top') 

widgets_frame = tk.LabelFrame(frame_1, text="輸入HEIC圖片的檔案目錄")
widgets_frame.grid(row=0, column=0, padx=20, pady=(10,0),sticky="ew")

frame_2 = tk.Frame(root)
frame_2.pack(side='bottom') 

widgets_frame_2 = tk.LabelFrame(frame_2, text="Information")
widgets_frame_2.grid(row=0, column=0,padx=10, pady=(15,20), ipadx=250, ipady=20,sticky="ew")

#輸入名字輸入框

b = tk.StringVar()
dir_entry = ttk.Entry(widgets_frame,width=10,textvariable=b,font=('微軟正黑體',12,'bold'))
dir_entry.insert(0, "目錄路徑")
dir_entry.bind("<FocusIn>", lambda e: dir_entry.delete('0', 'end'))     # bind函數讓<FocusIn>時觸發dir_entry.delete('0', 'end')
dir_entry.grid(row=1, column=0, padx=5, pady=(10, 5), sticky="ew")

button_s = tk.Button(widgets_frame, text="選取目錄", command=open_dir, font=('微軟正黑體',12,'bold'),bg='#40E0D0')
button_s.bind("<Button-1>", lambda e: dir_entry.delete('0', 'end')) 
button_s.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")


button_c = tk.Button(widgets_frame, text="清除", command=clear, font=('微軟正黑體',12,'bold'),bg='#00DD00')
button_c.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

#separator = ttk.Separator(widgets_frame)
#separator.grid(row=2, column=0, padx=(20, 10), pady=0, sticky="ew")

button = tk.Button(widgets_frame, text="將選取目錄下的HEIC檔轉換成jpg檔", 
                   command=heic_trans_jpg, 
                   font=('微軟正黑體',12,'bold'),
                    activeforeground='#FFFFBB',
                    activebackground='#008888',
                    foreground='#FFFFFF',
                    background='#880000')

button.grid(row=2, column=0,padx=120, pady=10, ipadx=10, ipady=5, sticky="nsew")

separator = ttk.Separator(widgets_frame)
separator.grid(row=3, column=0, padx=(20, 10), pady=10, sticky="ew")


c = tk.StringVar()
c.set('')
info_label=tk.Label(frame_2,textvariable=c,font=('微軟正黑體',12,'bold'),fg='#4B0082')    #在frame欄顯示路徑
info_label.grid(row=0, column=0)

separator = ttk.Separator(widgets_frame_2)
separator.grid(row=1, column=0, padx=(10, 10), pady=5, sticky="ew")

root.mainloop()


