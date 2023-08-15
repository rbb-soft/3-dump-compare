import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def format_to_hexadecimal(event):
    value = event.widget.get()

    try:
        decimal_value = int(value, 16)
        formatted_hex = f"0x{decimal_value:08X}"
        event.widget.delete(0, tk.END)
        event.widget.insert(0, formatted_hex)
    except ValueError:
        tk.messagebox.showerror("Error", "Valor no válido")

def on_closing():
    global root
    root.quit()

def disable_editing(event):
    return "break"

def load_files():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal de tkinter

    file_paths = filedialog.askopenfilenames()

    file_contents = []
    for file_path in file_paths:
        with open(file_path, 'rb') as file:
            file_contents.append(file.read())

    return file_contents

def compare_files():
    # Obtiene el valor de "start" en formato hexadecimal
    start_offset = int(start_entry.get(), 16)
    # Tamaño máximo del buffer en bytes (4 KB)
    max_buffer_size_bytes = 4 * 1024
    # Calcula el valor de end_offset sumando start_offset y el tamaño máximo del buffer
    end_offset = start_offset + max_buffer_size_bytes
    
    file_contents = load_files()
    
    if len(file_contents) < 3:
        messagebox.showerror("Error", "You need to load all three files to compare.")
        return

    file1_data = file_contents[0][start_offset:end_offset]
    file2_data = file_contents[1][start_offset:end_offset]
    file3_data = file_contents[2][start_offset:end_offset]

    if file1_data is None or file2_data is None or file3_data is None:
        return

    hex_view.delete('1.0', tk.END)
    differences1 = []
    differences2 = []
    differences3 = []

    for i in range(0, max(len(file1_data), len(file2_data), len(file3_data)), 16):
        chunk1 = file1_data[i:i+16]
        chunk2 = file2_data[i:i+16]
        chunk3 = file3_data[i:i+16]

        for j, (byte1, byte2, byte3) in enumerate(zip(chunk1, chunk2, chunk3)):
            if byte1 != byte2 or byte1 != byte3:
                differences1.append(i + j)
                differences2.append(i + j)
                differences3.append(i + j)

        buffer1 = " ".join(f"{byte:02X}" for byte in chunk1)
        buffer2 = " ".join(f"{byte:02X}" for byte in chunk2)
        buffer3 = " ".join(f"{byte:02X}" for byte in chunk3)

        buffer1 = buffer1.ljust(48)
        buffer2 = buffer2.ljust(48)
        buffer3 = buffer3.ljust(48)

        hex_view.insert(tk.END, f"{buffer1}  |  {buffer2}  |  {buffer3}\n")

    for diff1, diff2, diff3 in zip(differences1, differences2, differences3):
        line_number1 = diff1 // 16
        char_offset1 = (diff1 % 16) * 3
        hex_view.tag_add(
            "different", f"{line_number1+1}.{char_offset1}", f"{line_number1+1}.{char_offset1+2}")

        line_number2 = diff2 // 16
        char_offset2 = (diff2 % 16) * 3
        hex_view.tag_add(
            "different", f"{line_number2+1}.{char_offset2+53}", f"{line_number2+1}.{char_offset2+55}")

        line_number3 = diff3 // 16
        char_offset3 = (diff3 % 16) * 3
        hex_view.tag_add(
            "different", f"{line_number3+1}.{char_offset3+106}", f"{line_number3+1}.{char_offset3+108}")

def show_offset(event):
    offset_label.config(text="Offset: ----------")
    # Obtener la posición del cursor dentro del widget hex_view
    cursor_position = hex_view.index(tk.CURRENT)
    # Parsear la posición para obtener la línea y el carácter
    line, charColumn = cursor_position.split('.')
    if 0 < int(charColumn) <= 46:
        byte_offset = (int(line) - 1) * 16 + int(charColumn) // 3
        offset_label.config(text=f"Offset: 0x{byte_offset:08X}")
    elif 52 < int(charColumn) < 100:
        byte_offset = (int(line) - 1) * 16 + (int(charColumn) - 52) // 3
        offset_label.config(text=f"Offset: 0x{byte_offset:08X}")
    elif 105 < int(charColumn) < 153:
        byte_offset = (int(line) - 1) * 16 + (int(charColumn) - 105) // 3
        offset_label.config(text=f"Offset: 0x{byte_offset:08X}")


ancho = 1230
alto = 600
root = tk.Tk()
root.title("Three dump comparator")
root.minsize(ancho, alto)
root.protocol("WM_DELETE_WINDOW", on_closing)

frame = tk.Frame(root)
frame.pack(pady=10)

load_button = tk.Button(frame, text="load dumps", command=compare_files)
load_button.pack(side=tk.LEFT)

offset = ""
offset_label = tk.Label(frame, text=offset)
offset_label.pack(side=tk.LEFT, padx=5)

# Etiquetas "start" y "end"
start_label = tk.Label(frame, text="Start:")
start_label.pack(side=tk.LEFT, padx=5)
start_entry = tk.Entry(frame)
start_entry.insert(0, "0x00000000")  # Valor por defecto para "start"
start_entry.pack(side=tk.LEFT, padx=5)
start_entry.bind("<FocusOut>", format_to_hexadecimal) 

end_label = tk.Label(frame, text="End:")
end_label.pack(side=tk.LEFT, padx=5)
end_entry = tk.Entry(frame)
end_entry.insert(0, "0x00001000")  # Valor por defecto para "end"
end_entry.pack(side=tk.LEFT, padx=5)
end_entry.bind("<FocusOut>", format_to_hexadecimal) 

hex_view = tk.Text(root, wrap=tk.NONE)
hex_view.pack(fill=tk.BOTH, expand=True)

hex_view.tag_configure("different", background="yellow")

hex_view.bind("<Key>", disable_editing)
hex_view.bind("<Motion>", show_offset)

root.mainloop()
