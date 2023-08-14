import tkinter as tk
from tkinter import filedialog
import binascii


def load_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'rb') as file:
            return file.read()
    return None


def compare_files():
    file1_data = load_file()
    file2_data = load_file()

    if file1_data is None or file2_data is None:
        return

    hex_view.delete('1.0', tk.END)
    differences1 = []
    differences2 = []

    for i in range(0, max(len(file1_data), len(file2_data)), 16):
        chunk1 = file1_data[i:i+16]
        chunk2 = file2_data[i:i+16]

        for j, (byte1, byte2) in enumerate(zip(chunk1, chunk2)):
            if byte1 != byte2:
                differences1.append(i + j)
                differences2.append(i + j)

        line1 = " ".join(f"{byte:02X}" for byte in chunk1)
        line2 = " ".join(f"{byte:02X}" for byte in chunk2)

        line1 = line1.ljust(48)
        line2 = line2.ljust(48)

        hex_view.insert(tk.END, f"{line1}  |  {line2}\n")

    for diff1, diff2 in zip(differences1, differences2):
        line_number1 = diff1 // 16
        char_offset1 = (diff1 % 16) * 3
        hex_view.tag_add(
            "different", f"{line_number1+1}.{char_offset1}", f"{line_number1+1}.{char_offset1+2}")

        line_number2 = diff2 // 16
        char_offset2 = (diff2 % 16) * 3
        hex_view.tag_add(
            "different", f"{line_number2+1}.{char_offset2+53}", f"{line_number2+1}.{char_offset2+55}")


# Crear la ventana
root = tk.Tk()
root.title("Visor Hexadecimal de Diferencias")

# Botón para cargar archivos
load_button = tk.Button(root, text="Cargar Archivos", command=compare_files)
load_button.pack(pady=10)

# Área de texto para mostrar el visor hexadecimal
hex_view = tk.Text(root, wrap=tk.NONE)
# El visor se expandirá al cambiar el tamaño de la ventana
hex_view.pack(fill=tk.BOTH, expand=True)

# Estilo para resaltar las diferencias
hex_view.tag_configure("different", background="yellow")

# Iniciar el bucle de la GUI
root.mainloop()
