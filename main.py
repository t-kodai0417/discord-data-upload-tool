import requests,pyperclip,os,json,threading,sys
import tkinter as tk
from tkinter import ttk,messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD



#https://rikoubou.hatenablog.com/entry/2022/01/21/174800
def get_icon_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        
        base_path = os.path.abspath(os.path.dirname(sys.argv[0]))

    
    return os.path.join(base_path, relative_path)



def main_thread(acc_data:dict,path:str):
    try:
        path=path.replace("{","").replace("}","")
        send_pic_data=main(acc_data["token"],acc_data["ch_id"],path)
        try:
            with open("./data.json","w")as f:
                f.write(json.dumps(acc_data))
        except:
            None
        messagebox.showinfo("送信成功",send_pic_data)
        pyperclip.copy(send_pic_data)
    except:
        messagebox.showerror("送信失敗","")




def main(token:str,channel_id:str,path:str):
    headers = {
        'host': 'discord.com',
        'connection': 'keep-alive',
        'authorization': token,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.1.9 Chrome/83.0.4103.122 Electron/9.4.4 Safari/537.36',
    }

    
    basename = os.path.basename(path)
    
    with open(path, 'rb') as f:
        file_bin = f.read()

    files_qiita = {
        "favicon" : ( basename, file_bin),
    }
    payload = {
        "content": ""
    }


    response = requests.post(f'https://discord.com/api/v9/channels/{channel_id}/messages',headers=headers, data=payload,files=files_qiita)
    return(response.json()["attachments"][0]["url"])



class MyApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        
        
        width = 300
        height = 150
        self.geometry(f'{width}x{height}')
        self.minsize(width, height)
        self.maxsize(width, height)
        self.title(f'データうｐツール')
        self.iconbitmap(default=get_icon_path('icon.ico'))

        
        self.frame_drag_drop = frameDragAndDrop(self)

        self.frame_drag_drop.grid(column=0, row=0, padx=0, pady=0, sticky=(tk.E, tk.W, tk.S, tk.N))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


class frameDragAndDrop(tk.LabelFrame):
    
    def __init__(self, parent):
        super().__init__(parent)
        
        #https://qiita.com/bassan/items/0094379024a3e88d4d23
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.funcDragAndDrop)
        label1=ttk.Label(self, text='ここにファイルをD&D')
        label1.pack()
        label = tk.Label(self, text='Token')
        label.pack()
        global entry,entry2
        entry = tk.Entry(self, show="*")
        entry.pack()
        label1=ttk.Label(self, text='ChannelID')
        label1.pack()
        entry2 = tk.Entry(self)
        entry2.pack()
        button_execute = ttk.Button(self, text="以前のデータを読み込む", command=config_load)
        button_execute.pack()
    
    global config_load
    def config_load():
        try:
            with open("./data.json","r")as f:
                acc_data=json.loads(f.read())
            entry.delete(0,tk.END)
            entry2.delete(0,tk.END)
            entry.insert(tk.END,acc_data["token"])
            entry2.insert(tk.END,acc_data["ch_id"])
            messagebox.showinfo("成功","以前のデータの読み込みに成功しました。")
        except:
            messagebox.showinfo("失敗","以前のデータの読み込みに失敗しました。")

    def funcDragAndDrop(self, e):
        acc_data={"token":entry.get(),"ch_id":entry2.get()}
        thread_1 = threading.Thread(target=main_thread, args=(acc_data,e.data,))
        thread_1.start()
        
        
        


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
