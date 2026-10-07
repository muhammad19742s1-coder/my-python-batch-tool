import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageDraw, ImageFont

class ProfessionalBatchProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Batch Image Resizer & Watermarker Pro")
        self.root.geometry("560x780")
        self.root.resizable(True, True)
        self.root.configure(bg="#1E1E24")

        self.input_folder = ""
        self.output_folder = ""
        self.logo_path = ""

        self.presets = {
            "Custom": (None, None),
            "Shopify / Amazon (2000x2000)": (2000, 2000),
            "Instagram Story / Reel (1080x1920)": (1080, 1920),
            "YouTube Thumbnail (1280x720)": (1280, 720),
            "Web Banner (1920x1080)": (1920, 1080)
        }

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure("TFrame", background="#1E1E24")
        self.style.configure("TLabelframe", background="#2B2D42", foreground="#F8F9FA", borderwidth=1, relief="solid")
        self.style.configure("TLabelframe.Label", background="#2B2D42", foreground="#60A5FA", font=("Segoe UI", 10, "bold"))
        self.style.configure("TLabel", background="#2B2D42", foreground="#F8F9FA", font=("Segoe UI", 9))
        self.style.configure("TCheckbutton", background="#2B2D42", foreground="#F8F9FA", font=("Segoe UI", 9))
        self.style.configure("TRadiobutton", background="#2B2D42", foreground="#F8F9FA", font=("Segoe UI", 9))
        
        self.style.configure("TButton", background="#3D405B", foreground="#FFFFFF", font=("Segoe UI", 9, "bold"), borderwidth=0, padding=4)
        self.style.map("TButton", background=[("active", "#4A4E69")])

        self.style.configure("Accent.TButton", background="#3A86FF", foreground="#FFFFFF", font=("Segoe UI", 11, "bold"), padding=8)
        self.style.map("Accent.TButton", background=[("active", "#2563EB")])

        self.style.configure("TEntry", fieldbackground="#1E1E24", foreground="#FFFFFF", insertcolor="white")
        self.style.configure("TCombobox", fieldbackground="#1E1E24", foreground="#FFFFFF", background="#3D405B", darkcolor="#1E1E24", lightcolor="#1E1E24")
        self.style.map("TCombobox", fieldbackground=[("readonly", "#1E1E24")], foreground=[("readonly", "#FFFFFF")])

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=12)
        main_frame.pack(fill="both", expand=True)

        title_lbl = tk.Label(main_frame, text="Batch Image Processor", bg="#1E1E24", fg="#FFFFFF", font=("Segoe UI", 15, "bold"))
        title_lbl.pack(anchor="w", pady=(0, 6))

        # 1. Folders
        frame_folders = ttk.LabelFrame(main_frame, text=" 1. Select Folders ", padding=8)
        frame_folders.pack(fill="x", pady=4)

        ttk.Button(frame_folders, text="Select Input Folder", command=self.select_input).pack(fill="x", pady=2)
        self.lbl_input = ttk.Label(frame_folders, text="No folder selected", wraplength=480, foreground="#A0AAB8")
        self.lbl_input.pack(fill="x", pady=1)

        ttk.Button(frame_folders, text="Select Output Folder", command=self.select_output).pack(fill="x", pady=(4, 2))
        self.lbl_output = ttk.Label(frame_folders, text="No folder selected", wraplength=480, foreground="#A0AAB8")
        self.lbl_output.pack(fill="x", pady=1)

        # 2. Resize
        frame_resize = ttk.LabelFrame(main_frame, text=" 2. Resize & Presets ", padding=8)
        frame_resize.pack(fill="x", pady=4)

        self.var_resize = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame_resize, text="Enable Resizing", variable=self.var_resize).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 2))

        ttk.Label(frame_resize, text="Preset Target:").grid(row=1, column=0, sticky="w", pady=2)
        self.cb_presets = ttk.Combobox(frame_resize, values=list(self.presets.keys()), state="readonly", width=28)
        self.cb_presets.current(0)
        self.cb_presets.grid(row=1, column=1, sticky="w", pady=2, padx=8)
        self.cb_presets.bind("<<ComboboxSelected>>", self.apply_preset)

        ttk.Label(frame_resize, text="Max Width (px):").grid(row=2, column=0, sticky="w", pady=2)
        self.ent_width = ttk.Entry(frame_resize, width=12)
        self.ent_width.insert(0, "1920")
        self.ent_width.grid(row=2, column=1, sticky="w", pady=2, padx=8)

        ttk.Label(frame_resize, text="Max Height (px):").grid(row=3, column=0, sticky="w", pady=2)
        self.ent_height = ttk.Entry(frame_resize, width=12)
        self.ent_height.insert(0, "1080")
        self.ent_height.grid(row=3, column=1, sticky="w", pady=2, padx=8)

        # 3. Watermark Options
        frame_wm = ttk.LabelFrame(main_frame, text=" 3. Watermark Options ", padding=8)
        frame_wm.pack(fill="x", pady=4)

        self.var_wm_type = tk.StringVar(value="text")
        ttk.Radiobutton(frame_wm, text="Text Watermark", value="text", variable=self.var_wm_type).grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(frame_wm, text="PNG Logo Overlay", value="logo", variable=self.var_wm_type).grid(row=0, column=1, sticky="w")

        ttk.Label(frame_wm, text="Text:").grid(row=1, column=0, sticky="w", pady=2)
        self.ent_wm_text = ttk.Entry(frame_wm, width=30)
        self.ent_wm_text.insert(0, "Copyright © My Brand")
        self.ent_wm_text.grid(row=1, column=1, sticky="w", pady=2, padx=8)

        ttk.Button(frame_wm, text="Choose PNG Logo", command=self.select_logo).grid(row=2, column=0, pady=2, sticky="w")
        self.lbl_logo = ttk.Label(frame_wm, text="No logo chosen", foreground="#A0AAB8")
        self.lbl_logo.grid(row=2, column=1, sticky="w", pady=2, padx=8)

        # 4. Format Options
        frame_opts = ttk.LabelFrame(main_frame, text=" 4. Format Options ", padding=8)
        frame_opts.pack(fill="x", pady=4)

        self.var_webp = tk.BooleanVar(value=False)
        ttk.Checkbutton(frame_opts, text="Convert images to WebP format", variable=self.var_webp).pack(anchor="w")

        # Action & Status
        self.btn_process = ttk.Button(main_frame, text="Start Batch Processing", style="Accent.TButton", command=self.process_images)
        self.btn_process.pack(fill="x", pady=(10, 4))

        self.lbl_status = tk.Label(main_frame, text="Ready", bg="#1E1E24", fg="#A0AAB8", font=("Segoe UI", 9, "italic"))
        self.lbl_status.pack()

    def apply_preset(self, event):
        selected = self.cb_presets.get()
        w, h = self.presets[selected]
        if w and h:
            self.ent_width.delete(0, tk.END)
            self.ent_width.insert(0, str(w))
            self.ent_height.delete(0, tk.END)
            self.ent_height.insert(0, str(h))

    def select_input(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_folder = folder
            self.lbl_input.config(text=folder)

    def select_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder = folder
            self.lbl_output.config(text=folder)

    def select_logo(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png")])
        if file_path:
            self.logo_path = file_path
            self.lbl_logo.config(text=os.path.basename(file_path))

    def process_images(self):
        if not self.input_folder or not self.output_folder:
            messagebox.showerror("Error", "Please select both input and output folders.")
            return

        supported_exts = ('.jpg', '.jpeg', '.png', '.webp', '.bmp')
        file_paths = [os.path.join(self.input_folder, f) for f in os.listdir(self.input_folder) if f.lower().endswith(supported_exts)]

        if not file_paths:
            messagebox.showinfo("No Images Found", "No supported image files found in input folder.")
            return

        max_w = int(self.ent_width.get()) if self.var_resize.get() and self.ent_width.get().isdigit() else None
        max_h = int(self.ent_height.get()) if self.var_resize.get() and self.ent_height.get().isdigit() else None
        wm_type = self.var_wm_type.get()
        wm_text = self.ent_wm_text.get()

        processed_count = 0

        for img_path in file_paths:
            file_name = os.path.basename(img_path)
            self.lbl_status.config(text=f"Processing: {file_name}")
            self.root.update()

            try:
                img = Image.open(img_path).convert("RGBA")

                if self.var_resize.get() and max_w and max_h:
                    img.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)

                if wm_type == "text" and wm_text:
                    draw = ImageDraw.Draw(img)
                    font = ImageFont.load_default()
                    bbox = draw.textbbox((0, 0), wm_text, font=font)
                    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
                    x, y = img.width - text_w - 15, img.height - text_h - 15
                    draw.text((x+1, y+1), wm_text, font=font, fill=(0, 0, 0, 255))
                    draw.text((x, y), wm_text, font=font, fill=(255, 255, 255, 255))

                elif wm_type == "logo" and self.logo_path:
                    logo = Image.open(self.logo_path).convert("RGBA")
                    logo_w = int(img.width * 0.15)
                    aspect_ratio = logo.height / logo.width
                    logo_h = int(logo_w * aspect_ratio)
                    logo = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
                    pos = (img.width - logo_w - 15, img.height - logo_h - 15)
                    img.paste(logo, pos, mask=logo)

                base_name = os.path.splitext(file_name)[0]
                if self.var_webp.get():
                    save_path = os.path.join(self.output_folder, f"{base_name}.webp")
                    img.convert("RGB").save(save_path, "WEBP", quality=90)
                else:
                    save_path = os.path.join(self.output_folder, file_name)
                    if file_name.lower().endswith(('.jpg', '.jpeg')):
                        img.convert("RGB").save(save_path, quality=95)
                    else:
                        img.save(save_path)

                processed_count += 1
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

        self.lbl_status.config(text="Complete!")
        messagebox.showinfo("Success", f"Successfully processed {processed_count} images!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProfessionalBatchProcessorApp(root)
    root.mainloop()