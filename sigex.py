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

btn_open = ttk.Button(text="Load", command=load)
btn_open.grid(row=0, column=0)

btn_write = ttk.Button(text="Write", command=save)
btn_write.grid(row=0, column=2)


signals_loaded = []
signals_loaded_var = tk.StringVar(root, signals_loaded)

signals_selected = []
signals_selected_var = tk.StringVar(root, signals_selected)

signals_loaded_filter = tk.StringVar(root)
signals_loaded_filter.trace_add('write', filter_signals_loaded)

tb_filter_signals_loaded = ttk.Entry(root, textvariable=signals_loaded_filter)
tb_filter_signals_loaded.grid(row=1, column=0)

lb_signals_loaded = tk.Listbox(listvariable=signals_loaded_var, selectmode=tk.MULTIPLE)
lb_signals_loaded.grid(row=2, column=0, rowspan=4)

lb_signals_selected = tk.Listbox(listvariable=signals_selected_var, selectmode=tk.MULTIPLE)
lb_signals_selected.grid(row=2, column=2, rowspan=4)

btn_select = ttk.Button(text=(">"), command=select_signal)
btn_select.grid(row=3, column=1, sticky="ns")

btn_deselect = ttk.Button(text=("<"), command=deselect_signal)
btn_deselect.grid(row=4, column=1, sticky="ns")

root.mainloop()


