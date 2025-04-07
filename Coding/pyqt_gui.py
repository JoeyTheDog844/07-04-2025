import tkinter as tk
from PIL import Image, ImageTk  # Import Pillow for resizing images
import disable_services_gui
from tkinter import messagebox
import automate_rdp_services
import password_policy
import cache_manager
import automate_default_share
import logs_analysis
import export_logs_to_pdf
import threading
import pdf_generator
import random

def on_enter(e, button):
    button.config(bg='#d9d9d9', relief='raised')  # Lighten the button and add raised effect

def on_leave(e, button):
    button.config(bg='#2c3e50', relief='flat')  # Restore original color and flat style

def styled_button(parent, text, command, **kwargs):
    return tk.Button(
        parent,
        text=text,
        font=("Segoe UI", 11, "bold"),  # Change to your desired font
        bg="#2c3e50",  # Dark blue-gray
        fg="white",
        activebackground="#34495e",
        activeforeground="white",
        relief="flat",
        command=command,
        **kwargs
    )

# Load and Resize Image
image_path = r"C:\Users\amaan\Desktop\Work-on-gui-main\Coding\doggy.jpg"  # Ensure this is the correct path

root = tk.Tk()
root.geometry('900x640')
root.title('CyberSecurity Audit Application')

def show_automate_services(parent_frame):
    """ ✅ Display service statuses in the GUI """
    for widget in parent_frame.winfo_children():
        widget.destroy()

    service_statuses = disable_services_gui.check_all_services()

    # 🔹 Header
    header_font = ("Arial", 12, "bold")
    tk.Label(parent_frame, text="Service Name", font=header_font, bg="white").grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))
    tk.Label(parent_frame, text="Status", font=header_font, bg="white").grid(row=0, column=1, padx=10, pady=(10, 5))

    # 🔹 List services with status
    row_start = 1
    for i, (service, status) in enumerate(service_statuses.items()):
        tk.Label(parent_frame, text=service, font=("Arial", 12), bg="white", anchor="w").grid(row=row_start + i, column=0, sticky="w", padx=10, pady=4)
        tk.Label(parent_frame, text=status, font=("Arial", 12), fg="green" if status == "Running" else "red", bg="white").grid(row=row_start + i, column=1, padx=10, pady=4)

    # 🔹 Buttons
    button_font = ("Bold", 14)
    button_width = 20

    tk.Button(parent_frame, text="STOP ALL SERVICES", font=button_font, width=button_width,
              bg="red", fg="white", activebackground="#cc0000", command=stop_automate_services).grid(
        row=row_start + len(service_statuses) + 1, column=0, padx=10, pady=15
    )

    tk.Button(parent_frame, text="START ALL SERVICES", font=button_font, width=button_width,
              bg="green", fg="white", activebackground="#0f8c0f", command=start_automate_services).grid(
        row=row_start + len(service_statuses) + 1, column=1, padx=10, pady=15
    )

    tk.Button(parent_frame, text="DISABLE ALL SERVICES", font=button_font, width=button_width,
              bg="gray", fg="white", activebackground="#444", command=disable_automate_services).grid(
        row=row_start + len(service_statuses) + 2, column=0, columnspan=2, padx=10, pady=(5, 15)
    )

def stop_automate_services():
    """ ✅ Stop all running services """
    stopped_services, failed_services = disable_services_gui.stop_all_services()

    if stopped_services:
        messagebox.showinfo("Services Stopped", f"Successfully stopped:\n" + "\n".join(stopped_services))
    if failed_services:
        messagebox.showwarning("Failed to Stop", f"Could not stop:\n" + "\n".join(failed_services))

    show_automate_services(automateservices_inner_frame)

def start_automate_services():
    """ ✅ Start all stopped services """
    started_services, failed_services = disable_services_gui.start_all_services()

    if started_services:
        messagebox.showinfo("Services Started", f"Successfully started:\n" + "\n".join(started_services))
    if failed_services:
        messagebox.showwarning("Failed to Start", f"Could not start:\n" + "\n".join(failed_services))

    show_automate_services(automateservices_inner_frame)

def disable_automate_services():
    """ ✅ Disable all critical services """
    disabled_services, failed_services = disable_services_gui.disable_all_services()

    if disabled_services:
        messagebox.showinfo("Services Disabled", f"Successfully disabled:\n" + "\n".join(disabled_services))
    if failed_services:
        messagebox.showwarning("Failed to Disable", f"Could not disable:\n" + "\n".join(failed_services))

    show_automate_services(automateservices_inner_frame)

def automateservices_page():
    delete_pages()
    
    global automateservices_frame, automateservices_inner_frame
    automateservices_frame = tk.Frame(main_frame, bg="#f9f9f9")
    automateservices_frame.pack(pady=20, fill="both", expand=True)

    tk.Label(automateservices_frame, text="Disable Services", font=("Bold", 26), bg="#f9f9f9").pack(pady=(0, 20))

    # Save reference to inner_frame
    automateservices_inner_frame = tk.Frame(automateservices_frame, bd=3, relief="groove", bg="white", width=500, height=400)
    automateservices_inner_frame.pack(pady=10)
    automateservices_inner_frame.pack_propagate(False)

    show_automate_services(automateservices_inner_frame)

def show_rdp_services(parent_frame):
    """ ✅ Display RDP & Remote Services statuses in the GUI """
    for widget in parent_frame.winfo_children():
        widget.destroy()  # ✅ Clear old widgets

    service_statuses = automate_rdp_services.check_services_status()  # ✅ Fetch service statuses

    # 🔹 Title row
    header_font = ("Arial", 12, "bold")
    tk.Label(parent_frame, text="Service Name", font=header_font, bg="white").grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))
    tk.Label(parent_frame, text="Status", font=header_font, bg="white").grid(row=0, column=1, padx=10, pady=(10, 5))

    # 🔹 Services list
    row_start = 1
    for i, (service, status) in enumerate(service_statuses.items()):
        tk.Label(parent_frame, text=service, font=("Arial", 12), bg="white", anchor="w").grid(row=row_start + i, column=0, sticky="w", padx=10, pady=4)
        tk.Label(parent_frame, text=status, font=("Arial", 12), fg="green" if status == "Running" else "red", bg="white").grid(row=row_start + i, column=1, padx=10, pady=4)

    # 🔹 Buttons
    button_font = ("Bold", 14)
    button_width = 20

    tk.Button(parent_frame, text="STOP SERVICES", font=button_font, width=button_width,
              bg="red", fg="white", activebackground="#cc0000", command=stop_rdp_services).grid(
        row=row_start + len(service_statuses) + 1, column=0, padx=10, pady=15
    )

    tk.Button(parent_frame, text="ENABLE SERVICES", font=button_font, width=button_width,
              bg="green", fg="white", activebackground="#0f8c0f", command=enable_rdp_services).grid(
        row=row_start + len(service_statuses) + 1, column=1, padx=10, pady=15
    )

    tk.Button(parent_frame, text="DISABLE SERVICES", font=button_font, width=button_width,
              bg="gray", fg="white", activebackground="#444", command=disable_rdp_services).grid(
        row=row_start + len(service_statuses) + 2, column=0, columnspan=2, padx=10, pady=(5, 15)
    )

def stop_rdp_services():
    """ ✅ Stop all RDP & Remote Services (non-blocking) """
    def worker():
        try:
            stopped_services, failed_services = automate_rdp_services.stop_services()

            def update_ui():
                if stopped_services:
                    messagebox.showinfo("Services Stopped", "Successfully stopped:\n" + "\n".join(stopped_services))
                if failed_services:
                    messagebox.showwarning("Failed to Stop", "Could not stop:\n" + "\n".join(failed_services))

                show_rdp_services(rdp_inner_frame)

            root.after(0, update_ui)

        except Exception as e:
            root.after(0, lambda: messagebox.showerror("Error", f"Something went wrong:\n{e}"))

    threading.Thread(target=worker).start()

def enable_rdp_services():
    """ ✅ Enable all RDP & Remote Services """
    enabled_services, failed_services = automate_rdp_services.enable_services()

    if enabled_services:
        messagebox.showinfo("Services Enabled", f"Successfully enabled:\n" + "\n".join(enabled_services))
    if failed_services:
        messagebox.showwarning("Failed to Enable", f"Could not enable:\n" + "\n".join(failed_services))

    show_rdp_services(rdp_inner_frame)  # ✅ Refresh the GUI

def disable_rdp_services():
    """ ✅ Disable all RDP & Remote Services """
    disabled_services, failed_services = automate_rdp_services.disable_services()

    if disabled_services:
        messagebox.showinfo("Services Disabled", f"Successfully disabled:\n" + "\n".join(disabled_services))
    if failed_services:
        messagebox.showwarning("Failed to Disable", f"Could not disable:\n" + "\n".join(failed_services))

    show_rdp_services(rdp_inner_frame)  # ✅ Refresh the GUI

def rdp_services_page():
    """ ✅ Show the RDP & Remote Services page """
    delete_pages()

    global rdp_services_frame, rdp_inner_frame  # ← add this
    rdp_services_frame = tk.Frame(main_frame, bg="#f9f9f9")
    rdp_services_frame.pack(pady=20, fill="both", expand=True)

    tk.Label(rdp_services_frame, text="Disable REMOTE Services", font=("Bold", 26), bg="#f9f9f9").pack(pady=(0, 20))

    rdp_inner_frame = tk.Frame(rdp_services_frame, bd=3, relief="groove", bg="white", width=500, height=400)
    rdp_inner_frame.pack(pady=10)
    rdp_inner_frame.pack_propagate(False)

    show_rdp_services(rdp_inner_frame)  # ✅ Pass the inner frame

def show_password_policy():
    """ ✅ Display the current password policy in the GUI """
    delete_pages()

    global password_policy_frame
    password_policy_frame = tk.Frame(main_frame, bg="#f9f9f9")
    password_policy_frame.pack(pady=20, fill="both", expand=True)

    # 🔹 Heading
    tk.Label(password_policy_frame, text="Password Policy", font=("Bold", 26), bg="#f9f9f9").pack(pady=(0, 20))

    # 🔹 Inner frame like a card
    inner_frame = tk.Frame(password_policy_frame, bd=3, relief="groove", bg="white", width=500, height=400)
    inner_frame.pack(pady=10)
    inner_frame.pack_propagate(False)

    # 🔹 Fetch current policy
    policy_text = password_policy.get_current_policy()

    # 🔹 Display policy text
    policy_label = tk.Label(inner_frame, text="Current Password Policy:\n\n" + policy_text,
                            font=("Arial", 12), anchor="nw", justify="left", bg="white", wraplength=460)
    policy_label.pack(padx=15, pady=20, fill="both", expand=True)

    # 🔹 Apply button
    tk.Button(inner_frame, text="APPLY PASSWORD POLICY", font=("Bold", 14), width=30,
              bg="blue", fg="white", activebackground="#003e80", command=apply_password_policy).pack(pady=20)

def apply_password_policy():
    """ ✅ Ask for confirmation before applying new password policy """
    confirm = messagebox.askyesno("Confirm Policy Change", "Are you sure you want to apply the new password policy?")
    
    if confirm:  # Only proceed if the user clicks "Yes"
        result = password_policy.set_password_policy()
        messagebox.showinfo("Password Policy Updated", result)

        # ✅ Refresh to show the updated policy
        show_password_policy()

def show_cache_manager():
    delete_pages()

    global cache_manager_frame
    cache_manager_frame = tk.Frame(main_frame, bg="#f9f9f9")  # Light background
    cache_manager_frame.pack(pady=20, fill="both", expand=True)

    # Larger Title
    tk.Label(cache_manager_frame, text="Cache Management", font=("Bold", 26), bg="#f9f9f9").pack(pady=(0, 20))

    # Bigger inner frame
    inner_frame = tk.Frame(cache_manager_frame, bd=3, relief="groove", width=500, height=400, bg="white")
    inner_frame.pack(pady=10)
    inner_frame.pack_propagate(False)

    # Bigger status label
    status_label = tk.Label(inner_frame, text="", font=("Arial", 12), fg="green", bg="#f9f9f9", wraplength=460, justify="left")
    status_label.pack(pady=15)

    button_width = 35  # Wider buttons

    # Main action button with more padding
    tk.Button(inner_frame, text="CLEAR ALL CACHE", font=("Bold", 14), width=button_width,
              bg="#6a0dad", fg="white", activebackground="#5a009d", padx=10, pady=5,
              command=lambda: status_label.config(text=cache_manager.clear_all_caches())).pack(pady=8)

    # Looping other buttons
    for text, command in [
        ("CLEAR RECYCLE BIN", cache_manager.clear_recycle_bin),
        ("CLEAR TEMP FILES", cache_manager.clear_temp_files),
        ("CLEAR DNS CACHE", cache_manager.clear_dns_cache),
        ("CLEAR WINDOWS UPDATE CACHE", cache_manager.clear_windows_update_cache)
    ]:
        tk.Button(inner_frame, text=text, font=("Bold", 14), width=button_width,
                  bg="#007acc", fg="white", activebackground="#005a99", padx=10, pady=5,
                  command=lambda cmd=command: status_label.config(text=cmd())).pack(pady=8)

def default_share_page():
    """ ✅ Show the Default Admin Share Toggle page """
    delete_pages()

    global default_share_frame
    default_share_frame = tk.Frame(main_frame)
    default_share_frame.pack(pady=10, fill="both", expand=True)

    # Status label
    status_label = tk.Label(default_share_frame, font=("Arial", 12))
    status_label.pack(pady=10)

    # Toggle button (set text dynamically)
    toggle_button = tk.Button(default_share_frame, font=("Bold", 12), width=25)
    toggle_button.pack(pady=10)

    # Restart note
    note_label = tk.Label(default_share_frame, text="* Restart required to apply changes", font=("Arial", 9), fg="gray")
    note_label.pack(pady=5)

    def update_ui():
        is_disabled = automate_default_share.get_admin_share_status()
        if is_disabled:
            status_label.config(text="❌ Default Shares are Disabled", fg="red")
            toggle_button.config(text="Enable Default Shares")
        else:
            status_label.config(text="✅ Default Shares are Enabled", fg="green")
            toggle_button.config(text="Disable Default Shares")

    def toggle_share():
        current_status = automate_default_share.get_admin_share_status()
        success = automate_default_share.set_admin_share_status(disable=not current_status)
        if success:
            update_ui()
            messagebox.showinfo("Success", "Change applied. Please restart your PC to take full effect.")

    toggle_button.config(command=toggle_share)
    update_ui()

def show_logs_page():
    delete_pages()

    global logs_frame
    logs_frame = tk.Frame(main_frame)
    logs_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Title
    tk.Label(logs_frame, text="System Logs Viewer", font=("Bold", 20)).pack(pady=10)

    # Text widget with scrollbar
    text_scroll = tk.Scrollbar(logs_frame)
    text_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    log_text = tk.Text(logs_frame, wrap="word", font=("Consolas", 9), yscrollcommand=text_scroll.set)
    log_text.pack(fill="both", expand=True)

    text_scroll.config(command=log_text.yview)

    # Fetch logs
    log_text.insert(tk.END, "🔌 USB Logs:\n" + logs_analysis.get_usb_logs() + "\n\n")
    log_text.insert(tk.END, "🔐 Security Logs:\n" + logs_analysis.get_security_logs() + "\n\n")
    log_text.insert(tk.END, "🖥️ System Logs:\n" + logs_analysis.get_system_logs() + "\n\n")
    log_text.insert(tk.END, "📦 Application Logs:\n" + logs_analysis.get_application_logs() + "\n\n")
    log_text.insert(tk.END, "🌐 DNS Logs:\n" + logs_analysis.get_dns_logs() + "\n\n")

    log_text.config(state="disabled")  # Make read-only

    # Export Logs Button
    tk.Button(logs_frame, text="EXPORT LOGS TO PDF", font=("Bold", 12), bg="green", fg="white",
              command=export_logs).pack(pady=10)

def export_logs():
    try:
        path = export_logs_to_pdf.export_logs_to_pdf()
        messagebox.showinfo("Success", f"Logs exported to:\n{path}")
    except Exception as e:
        messagebox.showerror("Error", f"Export failed:\n{e}")

def home_page():
    delete_pages()

    global home_frame
    home_frame = tk.Frame(main_frame, bg="#ecf0f1")  # Softer background
    home_frame.pack(fill="both", expand=True)

    # 🔹 Centered container
    container = tk.Frame(home_frame, bg="#ecf0f1")
    container.place(relx=0.5, rely=0.5, anchor="center")

    # 🔹 Title
    tk.Label(container, text="CyberSecurity\nAudit Application", font=("Segoe UI", 28, "bold"),
             bg="#ecf0f1", fg="#2c3e50", justify="center").pack(pady=(0, 10))

    # 🔹 Subtitle
    tk.Label(container, text="Welcome to your personal system auditor.", font=("Arial", 13),
             bg="#ecf0f1", fg="#555").pack(pady=(0, 20))

    # 🔹 About "Card"
    about_card = tk.Frame(container, bg="white", bd=1, relief="solid", width=600, height=180)
    about_card.pack(pady=10)
    about_card.pack_propagate(False)

    about_text = (
        "🔐 This tool helps you harden your system:\n"
        "• Disable unnecessary services\n"
        "• Manage RDP and remote services\n"
        "• View and export system logs\n"
        "• Enforce password & lockout policies\n\n"
        "🧑‍💻 Developed by Amaan | Version 1.0"
    )

    tk.Label(about_card, text=about_text, font=("Arial", 11), justify="left",
             bg="white", anchor="nw", wraplength=560).pack(padx=15, pady=15, fill="both", expand=True)

    # 🔹 Tip Card
    tips = [
        "✅ Always use strong, unique passwords.",
        "🛡️ Disable unnecessary services to reduce attack surface.",
        "🔐 Enable lockout policies to prevent brute force attacks.",
        "🧼 Clear your system caches regularly.",
        "🚫 Disable default admin shares if unused.",
        "🧠 Don’t reuse passwords across platforms.",
    ]
    random_tip = random.choice(tips)

    tip_card = tk.Frame(container, bg="#dff9fb", bd=0, relief="ridge", width=600, height=60)
    tip_card.pack(pady=(20, 5))
    tip_card.pack_propagate(False)

    tk.Label(tip_card, text="💡 Tip of the Day", font=("Arial", 12, "bold"), bg="#dff9fb", fg="#130f40").pack()
    tk.Label(tip_card, text=random_tip, font=("Arial", 11), bg="#dff9fb", wraplength=580).pack()

def export_to_pdf_page():
    delete_pages()

    global export_pdf_frame
    export_pdf_frame = tk.Frame(main_frame)
    export_pdf_frame.pack(pady=20, fill="both", expand=True)

    # Title
    tk.Label(export_pdf_frame, text='CyberSecurity\nAudit Application', font=('Bold', 30)).pack(pady=20)

    # Subtitle
    tk.Label(export_pdf_frame, text='Generate Full Cyber Security Audit Report', font=('Arial', 14)).pack(pady=10)

    # Name Entry
    tk.Label(export_pdf_frame, text="Enter User Name:", font=("Arial", 12)).pack()
    name_entry = tk.Entry(export_pdf_frame, font=("Arial", 12), width=30)
    name_entry.pack(pady=5)

    # Lab Entry
    tk.Label(export_pdf_frame, text="Enter Lab Name:", font=("Arial", 12)).pack()
    lab_entry = tk.Entry(export_pdf_frame, font=("Arial", 12), width=30)
    lab_entry.pack(pady=5)

    # Status label
    status_label = tk.Label(export_pdf_frame, text="", font=("Arial", 11), fg="green")
    status_label.pack(pady=5)

    # Submit Button
    def generate_report():
        user_name = name_entry.get().strip()
        lab_name = lab_entry.get().strip()

        if not user_name or not lab_name:
            messagebox.showwarning("Input Required", "Please enter both Name and Lab.")
            return

        def run():
            try:
                status_label.config(text="Generating PDF, please wait...", fg="blue")
                pdf_generator.generate_pdf_report(user_name, lab_name)
                root.after(0, lambda: status_label.config(text="✅ Report generated successfully!", fg="green"))
                root.after(0, lambda: messagebox.showinfo("Done", "PDF Report has been generated."))
            except Exception as e:
                root.after(0, lambda: status_label.config(text="❌ Failed to generate report.", fg="red"))
                root.after(0, lambda: messagebox.showerror("Error", str(e)))

        threading.Thread(target=run).start()

    tk.Button(export_pdf_frame, text="GENERATE REPORT", font=('Bold', 14), bg="green", fg="white", command=generate_report).pack(pady=15)

def hide_indicators():
    home_indicate.config(bg='#c3c3c3')
    automateservices_indicate.config(bg='#c3c3c3')
    rdp_services_indicate.config(bg='#c3c3c3')
    password_policy_indicate.config(bg='#c3c3c3')
    cache_manager_indicate.config(bg='#c3c3c3')
    default_share_indicate.config(bg='#c3c3c3')
    logs_analysis_indicate.config(bg='#c3c3c3')
    export_pdf_indicate.config(bg='#c3c3c3')

def delete_pages():
    for frame in main_frame.winfo_children():
        frame.destroy()

def indicate(lb, page):
    hide_indicators()
    lb.config(bg='#2c3e50')
    delete_pages()
    page()

# Sidebar container frame (Now it does NOT restrict options_frame)
sidebar_frame = tk.Frame(root, bg='#c3c3c3')

# Options Frame (Manually set its width again)
options_frame = tk.Frame(sidebar_frame, bg='#c3c3c3', width=140, height=600)
options_frame.configure(width=140, height=600)  # Explicitly set size

# Load and Resize Logo (Separate from options_frame)
try:
    original_image = Image.open(image_path)
    resized_image = original_image.resize((95, 95), Image.LANCZOS)  # Resize to fit
    logo_img = ImageTk.PhotoImage(resized_image)  # Convert to Tkinter-compatible format

    logo_label = tk.Label(sidebar_frame, image=logo_img, bg='#c3c3c3')
    logo_label.pack(pady=10)  # Align properly
except Exception as e:
    print(f"Error loading logo: {e}")

# Create indicators first before buttons to avoid NameError
home_indicate = tk.Label(options_frame, text='', bg='#c3c3c3')
home_indicate.grid(row=0, column=0, sticky="w", padx=5)

automateservices_indicate = tk.Label(options_frame, text='', bg='#c3c3c3')
automateservices_indicate.grid(row=1, column=0, sticky="w", padx=5)

rdp_services_indicate = tk.Label(options_frame, text='', bg='#c3c3c3')
rdp_services_indicate.grid(row=2, column=0, sticky="w", padx=5)

password_policy_indicate = tk.Label(options_frame, text='', bg='#c3c3c3')
password_policy_indicate.grid(row=3, column=0, sticky="w", padx=5)

cache_manager_indicate = tk.Label(options_frame, text='', bg='#c3c3c3')
cache_manager_indicate.grid(row=4, column=0, sticky="w", padx=5)

default_share_indicate = tk.Label(options_frame, text='', bg='#c3c3c3')
default_share_indicate.grid(row=5, column=0, sticky="w", padx=5)

logs_analysis_indicate = tk.Label(options_frame, text='', bg='#c3c3c3')
logs_analysis_indicate.grid(row=6, column=0, sticky="w", padx=5)

export_pdf_indicate = tk.Label(options_frame, text='', bg='#c3c3c3')
export_pdf_indicate.grid(row=7, column=0, sticky="w", padx=5)

# Configure the options_frame for perfect alignment
options_frame.grid_columnconfigure(1, weight=1)  # Ensure buttons expand evenly

# Home Button
home_btn = styled_button(
    options_frame, text='🏠 HOME', width=20,
    command=lambda: indicate(home_indicate, home_page)
)
home_btn.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
home_btn.bind('<Enter>', lambda e: on_enter(e, home_btn))
home_btn.bind('<Leave>', lambda e: on_leave(e, home_btn))

# DISABLE Services Button
automateservices_btn = styled_button(
    options_frame, text='🚫 DISABLE\nSERVICES', width=20,
    command=lambda: indicate(automateservices_indicate, automateservices_page)
)
automateservices_btn.grid(row=1, column=1, sticky="ew", padx=10, pady=10)
automateservices_btn.bind('<Enter>', lambda e: on_enter(e, automateservices_btn))
automateservices_btn.bind('<Leave>', lambda e: on_leave(e, automateservices_btn))

# Automate RDP Services Button
rdp_services_btn = styled_button(
    options_frame, text='💻 RDP SERVICES', width=20,
    command=lambda: indicate(rdp_services_indicate, rdp_services_page)
)
rdp_services_btn.grid(row=2, column=1, sticky="ew", padx=10, pady=10)
rdp_services_btn.bind('<Enter>', lambda e: on_enter(e, rdp_services_btn))
rdp_services_btn.bind('<Leave>', lambda e: on_leave(e, rdp_services_btn))

# Password Policy Button
password_policy_btn = styled_button(
    options_frame, text='🔐 PASSWORD AND\nLOCKOUT POLICY', width=20,
    command=lambda: indicate(password_policy_indicate, show_password_policy)
)
password_policy_btn.grid(row=3, column=1, sticky="ew", padx=10, pady=10)
password_policy_btn.bind('<Enter>', lambda e: on_enter(e, password_policy_btn))
password_policy_btn.bind('<Leave>', lambda e: on_leave(e, password_policy_btn))

# Manage Cache
cache_manager_btn = styled_button(
    options_frame, text='🧹 MANAGE\nCACHE', width=20,
    command=lambda: indicate(cache_manager_indicate, show_cache_manager)
)
cache_manager_btn.grid(row=4, column=1, sticky="ew", padx=10, pady=10)
cache_manager_btn.bind('<Enter>', lambda e: on_enter(e, cache_manager_btn))
cache_manager_btn.bind('<Leave>', lambda e: on_leave(e, cache_manager_btn))

# Default Share
default_share_btn = styled_button(
    options_frame, text='🔁 DEFAULT\nSHARE', width=20,
    command=lambda: indicate(default_share_indicate, default_share_page)
)
default_share_btn.grid(row=5, column=1, sticky="ew", padx=10, pady=10)
default_share_btn.bind('<Enter>', lambda e: on_enter(e, default_share_btn))
default_share_btn.bind('<Leave>', lambda e: on_leave(e, default_share_btn))

# Logs
logs_analysis_btn = styled_button(
    options_frame, text='📄 LOGS', width=20,
    command=lambda: indicate(logs_analysis_indicate, show_logs_page)
)
logs_analysis_btn.grid(row=6, column=1, sticky="ew", padx=10, pady=10)
logs_analysis_btn.bind('<Enter>', lambda e: on_enter(e, logs_analysis_btn))
logs_analysis_btn.bind('<Leave>', lambda e: on_leave(e, logs_analysis_btn))

# Export to PDF Button
export_pdf_btn = styled_button(
    options_frame, text='📝 EXPORT TO PDF', width=20,
    command=lambda: indicate(export_pdf_indicate, export_to_pdf_page)
)
export_pdf_btn.grid(row=7, column=1, sticky="ew", padx=10, pady=10)
export_pdf_btn.bind('<Enter>', lambda e: on_enter(e, export_pdf_btn))
export_pdf_btn.bind('<Leave>', lambda e: on_leave(e, export_pdf_btn))

# Pack everything properly
options_frame.pack(fill="both", expand=False)  # Now it can be resized manually
sidebar_frame.pack(side=tk.LEFT, fill="y")  # Sidebar keeps full height

# Main content area
main_frame = tk.Frame(root, highlightbackground='black', highlightthickness=2)
main_frame.pack(side=tk.LEFT, fill="both", expand=True)

root.mainloop()
