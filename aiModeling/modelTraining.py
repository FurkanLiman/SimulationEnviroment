import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


import json
import os



import matplotlib.pyplot as plt
import pandas as pd

# Veriyi tanımlama

def ciz(veri):
    
    # Veriyi bir DataFrame'e dönüştürme
    df = pd.DataFrame(veri)

    # Günleri tanımlama (indeks)
    days = range(1, len(df) + 1)

    # Her bir kategoriyi çizme
    plt.figure(figsize=(14, 8))

    for column in df.columns:
        plt.plot(days, df[column], marker='o', label=column)

    # Grafiği özelleştirme
    plt.title('Veri Zaman Serisi Grafiği')
    plt.xlabel('Gün')
    plt.ylabel('Değerler')
    plt.legend()
    plt.grid(True)

    # Grafiği gösterme
    plt.show()





folder_path = 'results\\aiData'
# Örnek JSON verileri
combined_data = {
    "Day": [],
    "Population": [],
    "Winners": [],
    "Losers": [],
    "DisasterType": [],
    "speed": [],
    "vision": [],
    "visionRadius": [],
    "immunity": [],
    "durability": [],
    "mutationRate": []
}
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as file:
            data = json.load(file)
            for key in combined_data:
                combined_data[key].extend(data[key])

# Birleştirilen verileri yeni bir JSON dosyasına kaydedin
output_file_path = os.path.join(folder_path, 'combined_data.json')
with open(output_file_path, 'w') as output_file:
    json.dump(combined_data, output_file, indent=4)
    
    
    
# 1. JSON verilerini pandas DataFrame'e yükleme
data = pd.DataFrame(combined_data)

# 2. Özellikler ve hedef değişkenleri ayırma
X = data[['Day', 'mutationRate']]
y = data.drop(columns=['Day', 'mutationRate'])

# 3. Verileri eğitim ve test olarak ayırma
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Model eğitimi
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Model değerlendirme
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

import tkinter as tk
from tkinter import ttk

new_data_json = {
"mutation" : 10,
"day":5
}
result= {
        "Population": [],
        "Winners": [],
        "Losers": [],
        "DisasterType": [],
        "speed": [],
        "vision": [],
        "visionRadius": [],
        "immunity": [],
        "durability": [],
        }
def StartUp():
    
    root = tk.Tk()
    root.title("Slider ve Text Box Örneği")
    root.geometry("600x400")

    sliderPop_value = tk.StringVar(value="60")
    sliderDay_value = tk.StringVar(value="5")

    def update_sliders_value(event):
        sliderPop_value.set(int(sliderPop.get()))
        sliderDay_value.set(int(sliderDay.get()))
    
    
    frame = tk.Frame(root)
    frame.pack(pady=20)
    label1 = ttk.Label(frame, text="Mutation Rate:")
    label1.pack(side=tk.LEFT, padx=10)
    sliderPop = ttk.Scale(frame, from_=1, to=100, orient='horizontal', length=250,variable=sliderPop_value,command=update_sliders_value)
    sliderPop.pack(side=tk.LEFT, padx=10)
    value_label1 = ttk.Label(frame, textvariable=sliderPop_value)
    value_label1.pack(side=tk.LEFT, padx=10)

    frame5 = tk.Frame(root)
    frame5.pack(pady=20)
    label5 = ttk.Label(frame5, text="Day Limit:")
    label5.pack(side=tk.LEFT, padx=10)
    sliderDay = ttk.Scale(frame5, from_=2, to=50, orient='horizontal', length=250,variable=sliderDay_value, command=update_sliders_value)
    sliderDay.pack(side=tk.LEFT, padx=10)
    value_label5 = ttk.Label(frame5, textvariable=sliderDay_value)
    value_label5.pack(side=tk.LEFT, padx=10)
    def show_result():
    # Yeni bir pencere oluştur
        global result
        print(result)
        
        ciz(result)
        """
        result_label = tk.Label(result_window, text=f"Population: {int(result['Population'])}")
        result_label.pack()
        result_label1 = tk.Label(result_window, text=f"Winners: {int(result['Winners'])}")
        result_label1.pack()
        result_label2 = tk.Label(result_window, text=f"Losers: {int(result['Losers'])}")
        result_label2.pack()
        result_label3 = tk.Label(result_window, text=f"DisasterType: {round(result['DisasterType'],2)}")
        result_label3.pack()
        result_label4 = tk.Label(result_window, text=f"Speed: {round(result['speed'],3)}")
        result_label4.pack()
        result_label5 = tk.Label(result_window, text=f"vision: {round(result['vision'],3)}")
        result_label5.pack()
        result_label6 = tk.Label(result_window, text=f"visionRadius: {round(result['visionRadius'],3)}")
        result_label6.pack()
        result_label7 = tk.Label(result_window, text=f"immunity: {int(result['immunity'])}")
        result_label7.pack()
        result_label8 = tk.Label(result_window, text=f"durability: {round(result['durability'],3)}")
        result_label8.pack()
        """
    def Start():
        global new_data_json
        new_data_json["mutation"] = int(sliderPop.get()) /100
        new_data_json["day"] = int(sliderDay.get())   
        global result
        for i in range(new_data_json["day"]):
            new_data = pd.DataFrame({'Day': [i], 'mutationRate': [new_data_json["mutation"]]})  # örnek veri
            predictions = model.predict(new_data)
            result["Population"].append(predictions[0][0])   
            result["Winners"].append(predictions[0][1])
            result["Losers"].append(predictions[0][2])
            result["DisasterType"].append(predictions[0][3])
            result["speed"].append(predictions[0][4])
            result["vision"].append(predictions[0][5])
            result["visionRadius"].append(predictions[0][6])
            result["immunity"].append(predictions[0][7])
            result["durability"].append(predictions[0][8])
            """
            result= {
        "Population": predictions[0][0],
        "Winners": predictions[0][1],
        "Losers": predictions[0][2],
        "DisasterType": predictions[0][3],
        "speed": predictions[0][4],
        "vision": predictions[0][5],
        "visionRadius": predictions[0][6],
        "immunity": predictions[0][7],
        "durability": predictions[0][8],
        }
            """
        print(f'Tahminler: {predictions}')
        show_result()
        
        
        

    buton = ttk.Button(root, text="Start", command=Start)
    buton.pack(pady=20)

    root.mainloop()

    
StartUp() 

# 6. Yeni verilerle tahmin
