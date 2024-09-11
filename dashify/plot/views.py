from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import csv
import os.path


#import aus Übung

class ReadData:
    """ Konstruktor """
    def __init__(self, plot_button):
        self.filename = ""
        self.plot_button = plot_button  # Referenz auf den Plot-Button

    def select_file(self) -> None:
        """ Öffnet einen Dialog, um eine JSON- oder CSV-Datei auszuwählen, und speichert den Dateinamen. """
        self.filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv")],
            title="Select a JSON or CSV file"
        )
        if self.filename:
            print(f"Ausgewählte Datei: {self.filename}")
            self.plot_button.config(state=tk.NORMAL)
        else:
            self.plot_button.config(state=tk.DISABLED)

    def read_data(self) -> tuple:
        """ Liest die Daten aus der ausgewählten JSON- oder CSV-Datei. """
        if self.filename:
            f_name, f_ext = os.path.splitext(self.filename)
            if f_ext == ".json":
                return self._read_json_data()
            elif f_ext == ".csv":
                return self._read_csv_data()
            else:
                print("Unsupported file type")
                return [], []
        else:
            print("No file selected")
            return [], []

    def _read_json_data(self) -> tuple:
        """ Liest die Daten aus einer JSON-Datei. """
        with open(self.filename) as f:
            all_eq_data = json.load(f)
        all_eq_dicts = all_eq_data['features']
        lons, lats = [], []
        for eq_dict in all_eq_dicts:
            lon = eq_dict['geometry']['coordinates'][0]
            lat = eq_dict['geometry']['coordinates'][1]
            lons.append(lon)
            lats.append(lat)
        return lons, lats

    def _read_csv_data(self) -> tuple:
        """ Liest die Daten aus einer CSV-Datei und gibt sie in Form von Listen zurück. """
        x, y1, y2, y3 = [], [], [], []

        with open(self.filename, mode='r') as csvfile:
            csv_reader = csv.reader(csvfile)

            header = next(csv_reader)
            legend_entries = header[1:4]

            for row in csv_reader:
                x.append(float(row[0]))
                y1.append(float(row[1]))
                y2.append(float(row[2]))
                y3.append(float(row[3]))

        return x, y1, y2, y3, legend_entries


class PlotWindow:
    """ Konstruktor """
    def __init__(self, masterframe, size):
        self.figure, self.axes = plt.subplots(figsize=size, dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=masterframe)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        # Anpassung des Layouts im Masterframe
        masterframe.grid_rowconfigure(0, weight=1)
        masterframe.grid_columnconfigure(0, weight=1)

    def plotxy(self, x, y, label="") -> None:
        """ Erstellt ein Streudiagramm mit den gegebenen x- und y-Werten. """
        self.axes.scatter(x, y, color="blue", marker="o", label=label)
        if label:
            self.axes.legend()
        self.canvas.draw()

    def plot_multiple(self, x, y1, y2, y3, legend_entries) -> None:
        """ Erstellt ein Liniendiagramm mit mehreren Y-Datensätzen. """
        self.axes.plot(x, y1, label=legend_entries[0], color="blue")
        self.axes.plot(x, y2, label=legend_entries[1], color="green")
        self.axes.plot(x, y3, label=legend_entries[2], color="red")
        self.axes.legend()
        self.canvas.draw()

    def clearplot(self) -> None:
        """ Löscht den aktuellen Plot. """
        self.axes.cla()
        self.canvas.draw()


class App:
    """ Konstruktor """
    def __init__(self, root):
        self.root = root
        self.root.title("Earthquake Data Plotter")

        # Hauptframe für die Anordnung der Frames
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20)

        # Frame für die Buttons
        self.frame_buttons = self.setup_buttons_frame()
        self.create_widgets()

        # Frame für den Plot
        self.frame_plot = self.setup_plot_frame()

        # Initialisiere die Plot- und Datenklassen
        self.plot_w = PlotWindow(self.frame_plot, (5, 4))  # Kleinere Plotgröße (5x4 Inch)
        self.data_reader = ReadData(self.plot_button)  # Übergebe die Referenz auf den Plot-Button

        # Deaktiviere den Plot-Button initial
        self.plot_button.config(state=tk.DISABLED)

    """ Methoden """
    def create_widgets(self) -> None:
        """Erstellt und platziert die Widgets im gegebenen Frame."""

        # Label title
        label0 = tk.Label(self.frame_buttons, text="Was möchtest du plotten?")
        label0.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Buttons und Label
        self.label = tk.Label(self.frame_buttons, text="Select a JSON file and plot the data")
        self.label.grid(row=1, column=0, padx=10, pady=5)

        self.file_button = tk.Button(self.frame_buttons, text="Select File", command=self.select_file)
        self.file_button.grid(row=2, column=0, sticky="nsew")

        self.plot_button = tk.Button(self.frame_buttons, text="Plot", command=self.plot_data)
        self.plot_button.grid(row=3, column=0, sticky="nsew")

        self.clear_button = tk.Button(self.frame_buttons, text="Clear", command=self.clear_plot)
        self.clear_button.grid(row=4, column=0, sticky="nsew")

        self.close_button = tk.Button(self.frame_buttons, text="Close", command=self.close_app)
        self.close_button.grid(row=5, column=0, sticky="nsew")

    def select_file(self) -> None:
        """ Öffnet einen Dialog zum Auswählen einer Datei und speichert den Dateinamen. """
        self.data_reader.select_file()

    def setup_buttons_frame(self) -> tk.Frame:
        """Erstellt und gibt das Frame für die Buttons zurück."""
        frame = tk.Frame(self.main_frame, padx=20, pady=20)
        frame.pack(side=tk.LEFT, fill=tk.Y)  # Packe die Buttons links und lasse sie in der Höhe wachsen

        return frame

    def setup_plot_frame(self) -> tk.Frame:
        """Erstellt und gibt das Frame für den Plot zurück."""
        frame = tk.Frame(self.main_frame)
        frame.pack(side=tk.RIGHT, padx=20, pady=20)  # Packe den Plot rechts

        return frame

    def plot_data(self) -> None:
        """ Liest die Daten aus der ausgewählten Datei und plottet sie auf das Diagramm. """
        data = self.data_reader.read_data()

        if len(data) == 2:
            x, y = data
            if x and y:
                self.plot_w.plotxy(x, y)
        elif len(data) == 5:
            x, y1, y2, y3, legend_entries = data
            if x and y1 and y2 and y3:
                self.plot_w.plot_multiple(x, y1, y2, y3, legend_entries)
        else:
            print("Unbekanntes Datenformat")

    def clear_plot(self) -> None:
        """ Löscht den aktuellen Plot. """
        self.plot_w.clearplot()

    def close_app(self) -> None:
        """ Fragt den Benutzer, ob er die Anwendung schließen möchte. """
        if messagebox.askokcancel("Schließen", "Möchten Sie die Anwendung wirklich schließen?"):
            self.root.quit()
            self.root.destroy()


def main(request) -> None:
    root = tk.Tk()
    App(root)
    root.mainloop()
    return redirect("../plot/")

if __name__ == '__main__':
    main()


def plot(request):
    return render(request, "plot/plot.html")
