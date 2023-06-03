import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
from asammdf import MDF
from pathlib import Path


def load():
    file = filedialog.askopenfilename()
    if file:   
        global signals_loaded, signals_selected
        signals_loaded = []
        signals_selected = [] 
        signals_selected_var.set(signals_selected)

        global mdf 
        mdf = MDF(file)   

        channels = mdf.iter_channels()
        for channel in channels:
            signals_loaded.append(channel.name)
        signals_loaded_var.set(signals_loaded)
        

def save():
    if signals_selected:
        file = filedialog.asksaveasfilename(initialfile=Path(mdf.name).stem + "_extracted")
        if file:
            mdf.filter(signals_selected).save(file, overwrite=True)
   

def select_signal():
    idx_selection = lb_signals_loaded.curselection()
    for idx in idx_selection:
        if signals_loaded[idx] not in signals_selected:
            signals_selected.append(signals_loaded[idx])
    signals_selected_var.set(signals_selected)

def deselect_signal():
    idx_selection = lb_signals_selected.curselection()
    for idx in sorted(idx_selection, reverse=True):
        del signals_selected[idx]
    signals_selected_var.set(signals_selected)



    
root = tk.Tk()
root.title("Signal Extractor")

btn_open = ttk.Button(text="Load", command=load)
btn_open.grid(row=0, column=0)

btn_write = ttk.Button(text="Write", command=save)
btn_write.grid(row=0, column=2)


signals_loaded = []
signals_loaded_var = tk.StringVar(root, signals_loaded)

signals_selected = []
signals_selected_var = tk.StringVar(root, signals_selected)

lb_signals_loaded = tk.Listbox(listvariable=signals_loaded_var, selectmode=tk.MULTIPLE)
lb_signals_loaded.grid(row=1, column=0, rowspan=4)

lb_signals_selected = tk.Listbox(listvariable=signals_selected_var, selectmode=tk.MULTIPLE)
lb_signals_selected.grid(row=1, column=2, rowspan=4)

btn_select = ttk.Button(text=(">"), command=select_signal)
btn_select.grid(row=2, column=1, sticky="ns")

btn_deselect = ttk.Button(text=("<"), command=deselect_signal)
btn_deselect.grid(row=3, column=1, sticky="ns")

root.mainloop()


