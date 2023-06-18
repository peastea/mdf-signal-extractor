import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import tkinter.ttk as ttk
from asammdf import MDF
from pathlib import Path
import json


def load_from_mdf():
    load((("mf4","*.mf4"),))

def load_from_json():
    load((("json","*.json"),))

def load(filetypes):
    global signals_loaded
    file = filedialog.askopenfilename(filetypes = filetypes)
    if file:           
        reset_selection() 

        if file.endswith('.mf4'):
            mdf = MDF(file)   
            channels = mdf.iter_channels()
            for channel in channels:                
                signals_loaded.append(channel.name)

        elif file.endswith('.json'):
            with open(file, 'r') as f:
                signals_loaded = json.load(f)
        
        signals_loaded_var.set(signals_loaded)

def reset_selection():
    global signals_loaded, signals_selected
    signals_loaded = []
    signals_selected = [] 
    signals_loaded_var.set(signals_loaded)
    signals_selected_var.set(signals_selected)
        

def extract_file():
    if signals_selected:
        file = filedialog.askopenfilename(filetypes = (("mf4","*.mf4"),))
        if file:
            mdf_to_extract = MDF(file)
            extract_path = filedialog.asksaveasfilename(defaultextension='mf4',initialfile=Path(mdf_to_extract.name).stem + "_extracted")
            if extract_path:
                mdf_to_extract.filter(signals_selected).save(extract_path, overwrite=True)

def extract_dir():
    if signals_selected:
        
        dir = filedialog.askdirectory(title='Select MDF dir')
        if dir:
            dirpath = Path(dir)
            list_mdf = []
            for file_to_load in dirpath.rglob('*.mf4'):
                list_mdf.append(MDF(file_to_load))

            destination_path = filedialog.askdirectory(title='Select destination dir')
            if destination_path:
                for mdf in list_mdf:
                    print(destination_path + '/'+  Path(mdf.name).stem + 'extracted')
                    #mdf.filter(signals_selected).save(destination_path + '/'+ Path(mdf.name).stem + '_extracted', overwrite=True)
                    try: 
                        mdf.filter(signals_selected).save(destination_path + '/'+ Path(mdf.name).stem + '_extracted', overwrite=True)
                    except Exception as e:
                        errormsg = str(e) + ' at ' + destination_path + '/'+ Path(mdf.name).stem
                        messagebox.showerror(message=errormsg )

            
            

def save_to_json():
    if signals_selected:
        file = filedialog.asksaveasfilename(defaultextension=".json", filetypes = (("json","*.json"),))
        if file: 
            with open(file, 'w') as f:
                json.dump(signals_selected, f, indent=2)


def select_signal():
    idx_selection = lb_signals_loaded.curselection()
    
    for idx in idx_selection:
        if lb_signals_loaded.get(idx) not in signals_selected:
            signals_selected.append(lb_signals_loaded.get(idx))
    signals_selected_var.set(signals_selected)

def deselect_signal():
    idx_selection = lb_signals_selected.curselection()
    for idx in sorted(idx_selection, reverse=True):
        del signals_selected[idx]
    signals_selected_var.set(signals_selected)

def filter_signals_loaded(*args):
    filter_entry = signals_loaded_filter.get()
    list_to_display = signals_loaded
    if filter_entry:
        list_to_display = []
        for signal in signals_loaded:
            if filter_entry.lower() in signal.lower():
                list_to_display.append(signal)
    signals_loaded_var.set(list_to_display)





    
root = tk.Tk()
root.title("Signal Extractor")

menubar = tk.Menu(root)
root.config(menu=menubar)
root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=0)
for i in range(2,5):
    root.grid_rowconfigure(i, weight=1)
root.grid_rowconfigure(6, weight=0)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)
root.grid_columnconfigure(2, weight=1)
   

file_menu = tk.Menu(menubar)
file_menu.add_command(label="Load from mdf", command=load_from_mdf)
file_menu.add_command(label="Load from json", command=load_from_json)
file_menu.add_command(label="Save Selected Signals", command=save_to_json)
menubar.add_cascade(label="File", menu=file_menu)

btn_open = ttk.Button(text="Load", command=lambda: load((("json","*.json"),("mf4","*.mf4"))))
btn_open.grid(row=0, column=0)

btn_write = ttk.Button(text="Save", command=save_to_json)
btn_write.grid(row=0, column=2)

btn_extract = ttk.Button(text="Extract", command=extract_dir)
btn_extract.grid(row=6, column=0, columnspan=3, sticky='nesw')



signals_loaded = []
signals_loaded_var = tk.StringVar(root, signals_loaded)

signals_selected = []
signals_selected_var = tk.StringVar(root, signals_selected)

signals_loaded_filter = tk.StringVar(root)
signals_loaded_filter.trace_add('write', filter_signals_loaded)

tb_filter_signals_loaded = ttk.Entry(root, textvariable=signals_loaded_filter)
tb_filter_signals_loaded.grid(row=1, column=0, sticky='ew')

lb_signals_loaded = tk.Listbox(listvariable=signals_loaded_var, selectmode=tk.MULTIPLE)
lb_signals_loaded.grid(row=2, column=0, rowspan=4, sticky='nesw')

lb_signals_selected = tk.Listbox(listvariable=signals_selected_var, selectmode=tk.MULTIPLE)
lb_signals_selected.grid(row=2, column=2, rowspan=4, sticky='nesw')

btn_select = ttk.Button(text=(">"), command=select_signal)
btn_select.grid(row=3, column=1, sticky="ns")

btn_deselect = ttk.Button(text=("<"), command=deselect_signal)
btn_deselect.grid(row=4, column=1, sticky="ns")

root.mainloop()


