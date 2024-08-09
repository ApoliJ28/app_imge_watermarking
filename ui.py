from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import messagebox

# Variable para almacenar la imagen seleccionada
img = None

THEME_COLOR = '#03ecfc'

class WaterMarkingInterface:
    
    def __init__(self) -> None:
        
        self.window = Tk()
        self.window.title("Image WaterMarking")
        self.window.config(padx=50, pady=50, bg=THEME_COLOR)
        
        self.title_init = Label(text="INSERTA UNA IMAGEN", fg="black", bg=THEME_COLOR, font=("Arial", 20, "bold"))
        self.title_init.grid(row=0, column=0, columnspan=2)
        
        # Etiqueta para mostrar la imagen seleccionada
        self.lbl_img = Label(self.window)
        self.lbl_img.grid(row=1, column=0, columnspan=2)
        
        self.insert_button = Button(text="Cargar Imagen", highlightthickness=0, command=self.insert_pressed)
        self.insert_button.grid(row=2, column=0)
        
        
        self.btn_procesar = Button(text="Colocar Marca De Agua", highlightthickness=0, command=self.procesar_img)
        self.btn_procesar.grid(row=2, column=1)
        
        self.window.mainloop()
    
    def insert_pressed(self):
        global img
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            # Cargar y mostrar la imagen
            img = Image.open(file_path)
            img.thumbnail((400, 400))  # Redimensionar la imagen para que se ajuste a la interfaz
            img_tk = ImageTk.PhotoImage(img)
            self.lbl_img.configure(image=img_tk)
            self.lbl_img.image = img_tk
    
    def procesar_img(self):
        global img
        
        watermark = Image.open("image/firma.png").convert("RGBA")
        
        if img:
        # Redimensionar la marca de agua para que sea proporcional a la imagen
            wm_width, wm_height = watermark.size
            img_width, img_height = img.size

            scale_factor = min(img_width / (2 * wm_width), img_height / (2 * wm_height))
            watermark_resized = watermark.resize((int(wm_width * scale_factor), int(wm_height * scale_factor)), Image.ANTIALIAS)

            # Posicionar la marca de agua en la esquina inferior derecha
            wm_width, wm_height = watermark_resized.size
            position = (img_width - wm_width - 10, img_height - wm_height - 10)

            # Crear una copia de la imagen original y superponer la marca de agua
            img_with_watermark = img.copy()
            img_with_watermark.paste(watermark_resized, position, watermark_resized)

            # Guardar la imagen procesada
            output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if output_path:
                img_with_watermark.save(output_path, "PNG")
            messagebox.showinfo("Éxito", "La imagen con la marca de agua ha sido guardada.")
        else:
            messagebox.showwarning("Advertencia", "Primero debes seleccionar una imagen.")