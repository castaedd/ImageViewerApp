# Visor de Imágenes con Tkinter y PIL (Pillow)

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk, ImageEnhance
import os

class ImageViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visor de Imágenes")

        # Variables principales
        self.image_label = None
        self.image_path = None
        self.current_image = None
        self.image_index = 0
        self.image_list = []

        # Configuración de la interfaz
        self.setup_ui()

    def setup_ui(self):
        # Marco para los botones
        button_frame = ttk.Frame(self.root)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        # Botones de control
        self.open_button = ttk.Button(button_frame, text="Abrir Carpeta", command=self.open_folder)
        self.open_button.pack(side=tk.LEFT, padx=5)

        self.prev_button = ttk.Button(button_frame, text="< Anterior", command=self.show_previous_image, state=tk.DISABLED)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.next_button = ttk.Button(button_frame, text="Siguiente >", command=self.show_next_image, state=tk.DISABLED)
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.effect_button = ttk.Button(button_frame, text="Aplicar Efecto (Brillo)", command=self.apply_effect, state=tk.DISABLED)
        self.effect_button.pack(side=tk.LEFT, padx=5)

        # Área para mostrar la imagen
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def open_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.image_list = [os.path.join(folder_selected, f) for f in os.listdir(folder_selected) if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))]
            self.image_index = 0
            if self.image_list:
                self.load_image()
                self.update_buttons()

    def load_image(self):
        try:
            self.image_path = self.image_list[self.image_index]
            image = Image.open(self.image_path)
            self.current_image = image
            # Redimensionar la imagen para ajustarla a la ventana
            image.thumbnail((self.canvas.winfo_width(), self.canvas.winfo_height()), Image.ANTIALIAS)
            self.display_image(image)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")

    def display_image(self, image):
        tk_image = ImageTk.PhotoImage(image)
        self.canvas.delete("all")
        self.canvas.create_image(self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2, image=tk_image, anchor=tk.CENTER)
        self.canvas.image = tk_image

    def show_next_image(self):
        if self.image_list and self.image_index < len(self.image_list) - 1:
            self.image_index += 1
            self.load_image()
        self.update_buttons()

    def show_previous_image(self):
        if self.image_list and self.image_index > 0:
            self.image_index -= 1
            self.load_image()
        self.update_buttons()

    def apply_effect(self):
        if self.current_image:
            enhancer = ImageEnhance.Brightness(self.current_image)
            enhanced_image = enhancer.enhance(1.5)  # Incrementa el brillo
            self.display_image(enhanced_image)

    def update_buttons(self):
        if self.image_list:
            self.prev_button["state"] = tk.NORMAL if self.image_index > 0 else tk.DISABLED
            self.next_button["state"] = tk.NORMAL if self.image_index < len(self.image_list) - 1 else tk.DISABLED
            self.effect_button["state"] = tk.NORMAL
        else:
            self.prev_button["state"] = tk.DISABLED
            self.next_button["state"] = tk.DISABLED
            self.effect_button["state"] = tk.DISABLED

# Inicializar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewerApp(root)
    root.geometry("800x600")
    root.mainloop()
