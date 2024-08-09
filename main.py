from PIL import Image, ImageTk, UnidentifiedImageError
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np

def encrypt_image(image, key):
    try:
        pixels = np.array(image, dtype=np.int16)  # Convert to higher bit-depth to prevent overflow
        encrypted_pixels = (pixels + key) % 256
        encrypted_image = Image.fromarray(encrypted_pixels.astype(np.uint8))
        return encrypted_image
    except Exception as e:
        messagebox.showerror("Encryption Error", f"An error occurred during encryption: {e}")
        return None

def decrypt_image(image, key):
    try:
        pixels = np.array(image, dtype=np.int16)  # Convert to higher bit-depth to prevent overflow
        decrypted_pixels = (pixels - key) % 256
        decrypted_image = Image.fromarray(decrypted_pixels.astype(np.uint8))
        return decrypted_image
    except Exception as e:
        messagebox.showerror("Decryption Error", f"An error occurred during decryption: {e}")
        return None

def select_image():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
        if file_path:
            global original_image
            original_image = Image.open(file_path)
            display_image(original_image, original_label)
            status_label.config(text="Image selected: " + file_path)
            
            # Enable the key entry field and the encrypt and decrypt buttons
            key_entry.config(state=tk.NORMAL)
            encrypt_button.config(state=tk.NORMAL)
            decrypt_button.config(state=tk.NORMAL)
    except UnidentifiedImageError:
        messagebox.showerror("File Error", "The selected file is not a valid image.")
    except Exception as e:
        messagebox.showerror("File Error", f"An error occurred while opening the image: {e}")

def save_image(image):
    try:
        if image is not None:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if save_path:
                image.save(save_path)
                messagebox.showinfo("Save Image", "Image saved as " + save_path)
    except Exception as e:
        messagebox.showerror("Save Error", f"An error occurred while saving the image: {e}")

def encrypt_button_clicked():
    try:
        key = int(key_entry.get())
        encrypted_image = encrypt_image(original_image, key)
        if encrypted_image:
            display_image(encrypted_image, encrypted_label)
            save_button.config(command=lambda: save_image(encrypted_image))
            status_label.config(text="Image encrypted. Click 'Save Image' to save the result.")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid integer for the key.")
    except Exception as e:
        messagebox.showerror("Encryption Error", f"An error occurred during encryption: {e}")

def decrypt_button_clicked():
    try:
        key = int(key_entry.get())
        decrypted_image = decrypt_image(original_image, key)
        if decrypted_image:
            display_image(decrypted_image, encrypted_label)
            save_button.config(command=lambda: save_image(decrypted_image))
            status_label.config(text="Image decrypted. Click 'Save Image' to save the result.")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid integer for the key.")
    except Exception as e:
        messagebox.showerror("Decryption Error", f"An error occurred during decryption: {e}")

def display_image(image, label):
    img = image.resize((250, 250))
    img = ImageTk.PhotoImage(img)
    label.config(image=img)
    label.image = img

# Create main window
root = tk.Tk()
root.title("Image Encryption Tool")

# Original image label
original_label = tk.Label(root)
original_label.pack(side=tk.LEFT, padx=10, pady=10)

# Encrypted/Decrypted image label
encrypted_label = tk.Label(root)
encrypted_label.pack(side=tk.RIGHT, padx=10, pady=10)

# Key input
key_frame = tk.Frame(root)
key_frame.pack(pady=10)
tk.Label(key_frame, text="Enter Key:").pack(side=tk.LEFT)
key_entry = tk.Entry(key_frame, state=tk.DISABLED)  # Start with disabled entry
key_entry.pack(side=tk.LEFT)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)
select_button = tk.Button(button_frame, text="Select Image", command=select_image)
select_button.pack(side=tk.LEFT, padx=5)

# Encrypt and Decrypt buttons are initially disabled
encrypt_button = tk.Button(button_frame, text="Encrypt Image", state=tk.DISABLED, command=encrypt_button_clicked)
encrypt_button.pack(side=tk.LEFT, padx=5)
decrypt_button = tk.Button(button_frame, text="Decrypt Image", state=tk.DISABLED, command=decrypt_button_clicked)
decrypt_button.pack(side=tk.LEFT, padx=5)

# Save Button
save_button = tk.Button(root, text="Save Image")
save_button.pack(pady=10)

# Status Label
status_label = tk.Label(root, text="Select an image to start.")
status_label.pack(pady=10)

root.mainloop()