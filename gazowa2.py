#!/usr/bin/env python3
#coding:utf-8

import os
import sys
from tkinter import Tk, Label, Button, filedialog, Frame, StringVar
from PIL import Image, ImageTk

class ImageViewer:
    def __init__(self, root):
        self.direction = "NORMAL"
        self.image_list = []
        self.current_index = -1
        self.folder = ""

        self.root = root
        self.root.title("gazowa2")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

        # クロージャ使用する準備
        self.fullscreen_toggle = self.change_fullscreen()

        # ラベルを中央に配置するために行と列の重み付けをする
        for i in range(5):  # 必要な列数分を設定
            self.root.grid_columnconfigure(i, weight=1)
        self.root.grid_rowconfigure(0, weight=1) 
        
        COLOR_GRAY = "#252525"
        self.label = Label(root, bg="black")
        self.label.grid(row=0, column=0, rowspan = 100, columnspan=100, sticky="nsew")

        list = [
            {
                "text" : "全画面:f",
                "command" : self.fullscreen_toggle,
                "row" : 0, "column" : 5, "sticky" : "sw",
            },
            {
                "text" : "回転:r",
                "command" : self.rotate,
                "row" : 1, "column" : 5, "sticky" : "sw",
            },
            {
                "text" : "開く:o",
                "command" : self.open_folder,
                "row" : 5, "column" : 5, "sticky" : "sw",
            }
        ]
        self.widget_list = []
        for i, option in enumerate(list):
            self.widget_list.append(Button(self.root, text = option["text"], command = option["command"], bg="black", fg=COLOR_GRAY, relief="flat", bd="0", highlightbackground="black"))
            self.widget_list[i].grid(row = option["row"], column = option["column"], sticky = option["sticky"])

        # キーバインド
        keybind_list = {
            "<Up>" : self.prev_image,
            "<Left>" : self.prev_image,
            "<Down>" : self.next_image,
            "<Right>" : self.next_image,
            "<space>" : self.next_image,
            "o" : self.open_folder,
            "q" : lambda event: sys.exit(),
            "f" : self.fullscreen_toggle,
            "r" : self.rotate,
            "<Button-4>" : self.prev_image,
            "<Button-5>" : self.next_image,
            #"<MouseWheel>" : self.on_mouse_wheel,
            "<Button-1>" : self.next_image,
            "<Button-2>" : self.rotate,
            "<Double-Button-3>" : lambda event: sys.exit(),
        }
        for key, value in keybind_list.items():
            self.root.bind(key, value)

    def open_folder(self, event=None):
        folder = filedialog.askdirectory(title="フォルダを選択")
        self.open_image(folder, False)

    def open_image(self, folder, image_name):
        self.folder = folder #folderを記憶
        if folder:
            self.image_list = [os.path.join(folder, file) for file in os.listdir(folder) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp'))]
            self.image_list.sort()
            if image_name:
                image_index = self.image_list.index(os.path.join(folder, image_name))
            else:
                image_index = 0
            if self.image_list:
                self.current_index = image_index
                self.update()

    def show_image(self):
        if not self.image_list:
            return

        image_path = self.image_list[self.current_index]
        image = Image.open(image_path)

        image_ratio = image.width / image.height  # 変数image_ratioに再代入することになるのが少し気になる？
        if self.direction == "NORMAL" or image_ratio >= 1.0:
            pass
        elif self.direction == "RIGHT":
            image = image.rotate(-90, expand=True)
        else:
            image = image.rotate(90, expand=True)

        # 画像をウィンドウサイズに合わせてリサイズ（縦横比維持）
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        window_ratio = window_width / window_height
        image_ratio = image.width / image.height

        if window_ratio > image_ratio:
            # ウィンドウが横に広い場合、高さを基準にリサイズ
            new_height = window_height
            new_width = int(new_height * image_ratio)
        else:
            # ウィンドウが縦に広い場合、幅を基準にリサイズ
            new_width = window_width
            new_height = int(new_width / image_ratio)

        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)  # Image.Resampling.LANCZOS : リサイズ時の補完方法 LANCZOSフィルター
        photo = ImageTk.PhotoImage(image)

        self.label.config(image=photo)
        self.label.image = photo

    def next_image(self, event=None):
        self.image_list = [os.path.join(self.folder, file) for file in os.listdir(self.folder) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp'))]
        self.image_list.sort()

        if not self.image_list:
            return
        if self.current_index < len(self.image_list) - 1:
            self.current_index += 1
        else:
            self.current_index = 0
        self.update()

    def prev_image(self, event=None):
        self.image_list = [os.path.join(self.folder, file) for file in os.listdir(self.folder) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp'))]
        self.image_list.sort()
        
        if not self.image_list:
            return
        if self.current_index > 0:
            self.current_index -= 1
        else:
            self.current_index = len(self.image_list) - 1
        self.update()

    def update(self):
        self.show_image()

    def change_fullscreen(self, event=None):
        #クロージャを使用
        flag = True
        self.root.attributes("-fullscreen", True)
        def change(event=None):
            nonlocal flag
            if flag:
                self.root.attributes("-fullscreen", False)
                flag = not flag
                self.root.config(cursor="arrow")
            else:
                self.root.attributes("-fullscreen", True)
                flag = not flag
                self.root.config(cursor="none")
            self.root.after(100, self.update)
            return flag
        return change
    
    def rotate(self, event=None):
        if self.direction == "NORMAL":
            self.direction = "RIGHT"
        elif self.direction == "RIGHT":
            self.direction = "LEFT"
        else:
            self.direction = "NORMAL"
        self.update()
    
    def delete_image(self, event=None):
        pass
        
if __name__ == "__main__":
    root = Tk()
    app = ImageViewer(root)

    def delay():
        if len(sys.argv) > 1:
            path = sys.argv[1]
            file_name = os.path.basename(path)
            folder_path = os.path.dirname(path)
            print(f"フォルダ名:{folder_path}")
            print(f"ファイル名:{file_name}")
            app.open_image(folder_path, file_name)

    root.after(100, delay)
    root.mainloop()
