import numpy as np

def text_to_numbers(text):
    """
    Mengubah teks menjadi list angka A=0, B=1, ..., Z=25
    Hanya huruf A-Z yang diolah.
    """
    return [ord(char) - ord('A') for char in text.upper() if char.isalpha()]

def numbers_to_text(numbers):
    """
    Mengubah list angka menjadi string huruf A-Z.
    """
    return ''.join([chr(num + ord('A')) for num in numbers])

def encrypt(plaintext, key_matrix):
    """
    Enkripsi teks dengan Hill Cipher.
    - plaintext: teks asli (string)
    - key_matrix: matriks kunci (numpy array)
    """
    P = text_to_numbers(plaintext)

    # Padding jika panjang tidak kelipatan n (n = ordo matriks)
    while len(P) % key_matrix.shape[0] != 0:
        P.append(ord('X') - ord('A'))

    # Bentuk matriks kolom
    P = np.array(P).reshape(-1, key_matrix.shape[0]).T

    # Enkripsi: C = K * P mod 26
    C = np.dot(key_matrix, P) % 26

    return numbers_to_text(C.T.flatten())

def decrypt(ciphertext, key_matrix):
    """
    Dekripsi teks dengan Hill Cipher.
    - ciphertext: teks terenkripsi (string)
    - key_matrix: matriks kunci (numpy array)
    """
    C = text_to_numbers(ciphertext)
    C = np.array(C).reshape(-1, key_matrix.shape[0]).T

    # Hitung determinan & invers determinan mod 26
    det = int(round(np.linalg.det(key_matrix)))
    det_inv = mod_inverse(det, 26)

    # Invers matriks kunci mod 26
    key_matrix_inv = (
        det_inv * np.round(det * np.linalg.inv(key_matrix)).astype(int)
    ) % 26

    # Dekripsi: P = K_inv * C mod 26
    P = np.dot(key_matrix_inv, C) % 26

    return numbers_to_text(P.T.flatten())

def mod_inverse(a, m):
    """
    Mencari invers modulo (untuk determinan).
    """
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    raise ValueError(f"Tidak ada invers mod untuk {a} dengan modulo {m}")
