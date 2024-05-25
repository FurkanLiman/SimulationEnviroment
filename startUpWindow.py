import tkinter as tk
from tkinter import ttk

startUpConfigurations = {
"startPopulation" : 10,
"startFood" : 10,
"envSizes" : [100,1,100]
}
def StartUp():
    
    root = tk.Tk()
    root.title("Slider ve Text Box Örneği")
    root.geometry("600x350")


    sliderPop_value = tk.StringVar(value="60")
    sliderFood_value = tk.StringVar(value="10")
    sliderX_value = tk.StringVar(value="60")
    sliderY_value = tk.StringVar(value="60")

    def update_sliders_value(event):
        sliderPop_value.set(int(sliderPop.get()))
        sliderFood_value.set(int(sliderFood.get()))
        sliderX_value.set(int(sliderX.get()))
        sliderY_value.set(int(sliderY.get()))
    
    
    frame = tk.Frame(root)
    frame.pack(pady=20)
    label1 = ttk.Label(frame, text="Population Number:")
    label1.pack(side=tk.LEFT, padx=10)
    sliderPop = ttk.Scale(frame, from_=1, to=150, orient='horizontal', length=250,variable=sliderPop_value,command=update_sliders_value)
    sliderPop.pack(side=tk.LEFT, padx=10)
    value_label1 = ttk.Label(frame, textvariable=sliderPop_value)
    value_label1.pack(side=tk.LEFT, padx=10)

    frame2 = tk.Frame(root)
    frame2.pack(pady=10)
    label2 = ttk.Label(frame2, text="Food Number:")
    label2.pack(side=tk.LEFT, padx=10)
    sliderFood = ttk.Scale(frame2, from_=1, to=250, orient='horizontal', length=250, variable=sliderFood_value,command=update_sliders_value)
    sliderFood.pack(side=tk.LEFT, padx=10)
    value_label2 = ttk.Label(frame2, textvariable=sliderFood_value)
    value_label2.pack(side=tk.LEFT, padx=10)

    frame3 = tk.Frame(root)
    frame3.pack(pady=20)
    label3 = ttk.Label(frame3, text="X length:")
    label3.pack(side=tk.LEFT, padx=10)
    sliderX = ttk.Scale(frame3, from_=5, to=150, orient='horizontal', length=250, variable=sliderX_value,command=update_sliders_value)
    sliderX.pack(side=tk.LEFT, padx=10)
    value_label3 = ttk.Label(frame3, textvariable=sliderX_value)
    value_label3.pack(side=tk.LEFT, padx=10)

    frame4 = tk.Frame(root)
    frame4.pack(pady=20)
    label4 = ttk.Label(frame4, text="Y length:")
    label4.pack(side=tk.LEFT, padx=10)
    sliderY = ttk.Scale(frame4, from_=5, to=150, orient='horizontal', length=250,variable=sliderY_value, command=update_sliders_value)
    sliderY.pack(side=tk.LEFT, padx=10)
    value_label4 = ttk.Label(frame4, textvariable=sliderY_value)
    value_label4.pack(side=tk.LEFT, padx=10)
    
    def Start():
        global startUpConfigurations
        startUpConfigurations["startPopulation"] = int(sliderPop.get())
        startUpConfigurations["startFood"] = int(sliderFood.get())
        startUpConfigurations["envSizes"][0] = int(sliderX.get())
        startUpConfigurations["envSizes"][2] = int(sliderY.get())        
        root.destroy()

    buton = ttk.Button(root, text="Start", command=Start)
    buton.pack(pady=20)

    root.mainloop()

