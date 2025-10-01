import os
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox

def xapk_to_apk(xapk_path, output_dir="output"):
    # Make sure paths exist
    if not os.path.exists(xapk_path):
        raise FileNotFoundError(f"{xapk_path} not found")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Extract XAPK (ZIP format)
    with zipfile.ZipFile(xapk_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)

    # Look for APK files
    apk_files = [f for f in os.listdir(output_dir) if f.endswith(".apk")]

    if not apk_files:
        raise FileNotFoundError("No APK file found inside the XAPK")

    # Take the first APK (usually the main one)
    main_apk = apk_files[0]
    apk_path = os.path.join(output_dir, main_apk)

    return apk_path


def select_file():
    xapk_path = filedialog.askopenfilename(
        title="Select XAPK file",
        filetypes=[("XAPK files", "*.xapk"), ("All files", "*.*")]
    )
    if not xapk_path:
        return

    try:
        # Extract XAPK and get all APK files
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        with zipfile.ZipFile(xapk_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
        
        # Find all APK files
        apk_files = [f for f in os.listdir(output_dir) if f.endswith(".apk")]
        
        if not apk_files:
            raise FileNotFoundError("No APK file found inside the XAPK")
        
        # Create success message with all APK files
        apk_list = "\n".join([f"• {apk}" for apk in apk_files])
        messagebox.showinfo("Success", f"APK files extracted to 'output' folder:\n\n{apk_list}\n\nTotal files: {len(apk_files)}")
        
    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI setup
root = tk.Tk()
root.title("XAPK to APK Converter")
root.geometry("400x200")

label = tk.Label(root, text="Convert .XAPK to .APK", font=("Arial", 14))
label.pack(pady=20)

btn = tk.Button(root, text="Select XAPK File", command=select_file, font=("Arial", 12))
btn.pack(pady=10)

root.mainloop()

