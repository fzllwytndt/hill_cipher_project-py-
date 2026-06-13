import customtkinter as ctk
from tkinter import filedialog, messagebox
import numpy as np

from hill_cipher import encrypt, decrypt
from file_handler import read_docx, save_docx, read_ciphertext, save_ciphertext

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class HillCipherApp:
    def __init__(self, master):
        self.master = master
        master.title("Hill Cipher - Pengamanan Dokumen ")

        self.file_path = ""

        # ======== Judul =========
        self.title_label = ctk.CTkLabel(
            master, text="🔒 Sistem Pengamanan Dokumen ", 
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.title_label.pack(pady=40)

        # ======== Frame Utama ========
        self.main_frame = ctk.CTkFrame(master)
        self.main_frame.pack(pady=20, padx=40, fill="both", expand=True)

        # Label pilih file
        self.label = ctk.CTkLabel(
            self.main_frame, text="1️. Pilih File (.docx)", font=ctk.CTkFont(size=16)
        )
        self.label.pack(pady=10)

        # Tombol Browse
        self.browse_button = ctk.CTkButton(
            self.main_frame, text="Browse File", command=self.browse_file, width=200
        )
        self.browse_button.pack(pady=10)

        # Label input matriks kunci
        self.key_label = ctk.CTkLabel(
            self.main_frame, 
            text="2️. Masukkan Matriks Kunci 2x2 (contoh: 3 3 2 5)",
            font=ctk.CTkFont(size=16)
        )
        self.key_label.pack(pady=10)

        # Entry matriks kunci
        self.key_entry = ctk.CTkEntry(self.main_frame, width=300)
        self.key_entry.pack(pady=10)

        # Tombol Enkripsi
        self.encrypt_button = ctk.CTkButton(
            self.main_frame, text="🔒 Enkripsi", command=self.encrypt_file, width=200
        )
        self.encrypt_button.pack(pady=20)

        # Tombol Dekripsi
        self.decrypt_button = ctk.CTkButton(
            self.main_frame, text="🔓 Dekripsi", command=self.decrypt_file, width=200
        )
        self.decrypt_button.pack(pady=10)

    def browse_file(self):
        self.file_path = filedialog.askopenfilename(
            filetypes=[("Word Documents", "*.docx")]
        )
        if self.file_path:
            messagebox.showinfo("File Terpilih", f"File: {self.file_path}")

    def encrypt_file(self):
        if not self.file_path:
            messagebox.showwarning("File Tidak Ditemukan", "Pilih file skripsi terlebih dahulu.")
            return

        try:
            key_values = list(map(int, self.key_entry.get().split()))
            key_matrix = np.array(key_values).reshape(2, 2)
        except:
            messagebox.showerror("Kesalahan Kunci", "Format matriks kunci salah.\nContoh: 3 3 2 5")
            return

        plaintext = read_docx(self.file_path)
        ciphertext = encrypt(plaintext, key_matrix)
        save_ciphertext(ciphertext, "ciphertext.txt")

        messagebox.showinfo("Sukses", "✅ Enkripsi berhasil!\nHasil: ciphertext.txt")

    def decrypt_file(self):
        try:
            key_values = list(map(int, self.key_entry.get().split()))
            key_matrix = np.array(key_values).reshape(2, 2)
        except:
            messagebox.showerror("Kesalahan Kunci", "Format matriks kunci salah.")
            return

        ciphertext = read_ciphertext("ciphertext.txt")
        decrypted_text = decrypt(ciphertext, key_matrix)
        save_docx(decrypted_text, "decrypted.docx")

        messagebox.showinfo("Sukses", "✅ Dekripsi berhasil!\nHasil: decrypted.docx")

if __name__ == "__main__":
    root = ctk.CTk()
    root.attributes('-fullscreen', True)
    root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))
    app = HillCipherApp(root)
    root.mainloop()
