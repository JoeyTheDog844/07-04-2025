import os
import subprocess
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

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.tooltip or not self.text:
            return
        x = y = 0
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("Arial", 9))
        label.pack(ipadx=1)

    def hide(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

def on_enter(e, button):
    button.config(bg="#1abc9c")  # Teal-like on hover

def on_leave(e, button):
    button.config(bg="#34495e")  # Back to dark blue-gray

def styled_button(parent, text, command, **kwargs):
    btn = tk.Button(
        parent,
        text=text,
        font=("Segoe UI", 11, "bold"),
        bg="#34495e",  # Dark slate blue
        fg="white",
        activebackground="#2c3e50",
        activeforeground="white",
        relief="flat",
        bd=0,
        padx=10,
        pady=6,
        wraplength=130,
        justify="center",
        command=command,
        **kwargs
    )
    return btn

# Load and Resize Image
image_path = r"C:\Users\amaan\Desktop\06-04-2025-main\Coding\doggy.jpg"  # Ensure this is the correct path

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

tooltips = {
    "Minimum password age (days)": "Number of days a user must wait before changing their password again.",
    "Maximum password age (days)": "Maximum number of days a password is valid before it must be changed.",
    "Minimum password length": "The least number of characters required in a password.",
    "Length of password history maintained": "Prevents reuse of previous passwords by remembering them.",
    "Lockout threshold": "Number of failed login attempts before account lockout.",
    "Lockout duration (minutes)": "How long the account stays locked after too many failed attempts.",
    "Lockout observation window (minutes)": "Time window in which failed logins are counted towards lockout.",
    "Force user logoff how long after time expires?": "Forces user logout when logon hours expire.",
    "Computer role": "Indicates whether this machine is a workstation or server."
}

def show_password_policy():
    """ ✅ Display the current password policy in the GUI """
    delete_pages()

    global password_policy_frame
    password_policy_frame = tk.Frame(main_frame, bg="#f9f9f9")
    password_policy_frame.pack(pady=20, fill="both", expand=True)

    # 🔹 Heading
    tk.Label(
        password_policy_frame,
        text="Password Policy",
        font=("Segoe UI", 24, "bold"),
        bg="#f9f9f9",
        fg="#333"
    ).pack(pady=(0, 20))

    # 🔹 Inner card-style frame
    inner_frame = tk.Frame(password_policy_frame, bg="white", bd=2, relief="ridge", width=600, height=400)
    inner_frame.pack(pady=10)
    inner_frame.pack_propagate(False)

    # 🔹 Fetch current policy as dict
    policy_dict = password_policy.get_current_policy()

    # 🔹 Scrollable area
    canvas = tk.Canvas(inner_frame, bg="white", highlightthickness=0)
    scrollbar = tk.Scrollbar(inner_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    scrollbar.pack(side="right", fill="y")

    # 🔹 Show each policy entry
    for key, value in policy_dict.items():
        row = tk.Frame(scrollable_frame, bg="white")
        row.pack(fill="x", pady=5, anchor="w")

        key_label = tk.Label(row, text=f"{key}:", font=("Segoe UI", 11, "bold"), bg="white", anchor="w", width=40)
        key_label.pack(side="left")

        value_label = tk.Label(row, text=value, font=("Segoe UI", 11), bg="white", anchor="w")
        value_label.pack(side="left")

        # 🧠 Attach tooltip if we have one for this key
        if key in tooltips:
            ToolTip(key_label, tooltips[key])
            ToolTip(value_label, tooltips[key])

    # 🔹 Apply button
    tk.Button(
        password_policy_frame,
        text="Apply Password Policy",
        font=("Segoe UI", 12, "bold"),
        width=30,
        bg="#0078D7",
        fg="white",
        activebackground="#005A9E",
        activeforeground="white",
        relief="flat",
        command=apply_password_policy
    ).pack(pady=20)

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
    cache_manager_frame = tk.Frame(main_frame, bg="#f9f9f9")
    cache_manager_frame.pack(pady=20, fill="both", expand=True)

    # 🔹 Title
    tk.Label(
        cache_manager_frame,
        text="🧹 Cache Management",
        font=("Segoe UI", 26, "bold"),
        bg="#f9f9f9",
        fg="#2c3e50"
    ).pack(pady=(0, 20))

    # 🔹 Inner card
    inner_frame = tk.Frame(cache_manager_frame, bd=2, relief="solid", width=520, height=410, bg="white")
    inner_frame.pack(pady=10)
    inner_frame.pack_propagate(False)

    # 🔹 Status label
    status_label = tk.Label(
        inner_frame, text="", font=("Segoe UI", 11),
        fg="green", bg="white", wraplength=460, justify="left"
    )
    status_label.pack(pady=15)

    # 🔹 Cache actions
    button_width = 34
    button_style = {
        "font": ("Segoe UI", 11, "bold"),
        "width": button_width,
        "fg": "white",
        "padx": 10,
        "pady": 5,
        "relief": "flat",
        "cursor": "hand2"
    }

    # 🔹 All Cache Button (Purple)
    tk.Button(
        inner_frame,
        text="🧹 CLEAR ALL CACHE",
        bg="#6a0dad",
        activebackground="#5a009d",
        command=lambda: status_label.config(text=cache_manager.clear_all_caches()),
        **button_style
    ).pack(pady=8)

    # 🔹 Individual Buttons (Blue)
    cache_tasks = [
        ("🗑️ CLEAR RECYCLE BIN", cache_manager.clear_recycle_bin),
        ("📂 CLEAR TEMP FILES", cache_manager.clear_temp_files),
        ("🌐 CLEAR DNS CACHE", cache_manager.clear_dns_cache),
        ("🔄 CLEAR WINDOWS UPDATE CACHE", cache_manager.clear_windows_update_cache)
    ]

    for text, command in cache_tasks:
        tk.Button(
            inner_frame,
            text=text,
            bg="#007acc",
            activebackground="#005a99",
            command=lambda cmd=command: status_label.config(text=cmd()),
            **button_style
        ).pack(pady=8)

    # 🔹 Footer Note
    tk.Label(
        cache_manager_frame,
        text="⚠️ Temporary files may reappear after reboot or system updates.",
        font=("Arial", 9),
        bg="#f9f9f9",
        fg="gray"
    ).pack(pady=(15, 0))

def default_share_page():
    """ ✅ Show the Default Admin Share Toggle page """
    delete_pages()

    global default_share_frame
    default_share_frame = tk.Frame(main_frame, bg="#f9f9f9")
    default_share_frame.pack(pady=20, fill="both", expand=True)

    # 🔹 Title
    tk.Label(default_share_frame, text="Default Admin Shares", font=("Segoe UI", 24, "bold"),
             bg="#f9f9f9", fg="#2c3e50").pack(pady=(0, 20))

    # 🔹 Card-style container
    card = tk.Frame(default_share_frame, bg="white", bd=2, relief="ridge", width=500, height=200)
    card.pack(pady=10)
    card.pack_propagate(False)

    # 🔹 Status label
    status_label = tk.Label(card, font=("Segoe UI", 12), bg="white")
    status_label.pack(pady=(20, 10))

    # 🔹 Toggle button
    toggle_button = tk.Button(card, font=("Segoe UI", 11, "bold"), width=25,
                              bg="#2c3e50", fg="white", activebackground="#34495e", relief="flat")
    toggle_button.pack(pady=10)

    # 🔹 Restart note
    tk.Label(card, text="⚠️ Restart required to apply changes", font=("Arial", 9),
             fg="gray", bg="white").pack(pady=(5, 10))

    def update_ui():
        is_disabled = automate_default_share.get_admin_share_status()
        if is_disabled:
            status_label.config(text="❌ Default Shares are Disabled", fg="red")
            toggle_button.config(text="Enable Default Shares", bg="#2c3e50")
        else:
            status_label.config(text="✅ Default Shares are Enabled", fg="green")
            toggle_button.config(text="Disable Default Shares", bg="#cc0000")

    def toggle_share():
        current_status = automate_default_share.get_admin_share_status()
        message = automate_default_share.set_admin_share_status(disable=not current_status)

        update_ui()
        if "successfully" in message.lower():
            messagebox.showinfo("Success", message + "\nPlease restart your PC to take full effect.")
        else:
            messagebox.showerror("Error", message)
    
    toggle_button.config(command=toggle_share)
    update_ui()

def show_logs_page():
    delete_pages()

    global logs_frame
    logs_frame = tk.Frame(main_frame, bg="#f9f9f9")
    logs_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # 🔹 Title
    tk.Label(logs_frame, text="📝 System Logs Viewer", font=("Segoe UI", 24, "bold"),
             bg="#f9f9f9", fg="#2c3e50").pack(pady=(0, 15))

    # 🔹 Card-like container
    card = tk.Frame(logs_frame, bg="white", bd=2, relief="ridge")
    card.pack(fill="both", expand=True)

    # 🔹 Scrollable Text Area
    text_scroll = tk.Scrollbar(card)
    text_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    log_text = tk.Text(card, wrap="word", font=("Consolas", 10),
                       yscrollcommand=text_scroll.set, bg="white", padx=10, pady=10)
    log_text.pack(side=tk.LEFT, fill="both", expand=True)

    text_scroll.config(command=log_text.yview)

    # 🔹 Load logs into text box
    log_text.insert(tk.END, "🔌 USB Logs:\n" + logs_analysis.get_usb_logs() + "\n\n")
    log_text.insert(tk.END, "🔐 Security Logs:\n" + logs_analysis.get_security_logs() + "\n\n")
    log_text.insert(tk.END, "🖥️ System Logs:\n" + logs_analysis.get_system_logs() + "\n\n")
    log_text.insert(tk.END, "📦 Application Logs:\n" + logs_analysis.get_application_logs() + "\n\n")
    log_text.insert(tk.END, "🌐 DNS Logs:\n" + logs_analysis.get_dns_logs() + "\n\n")

    log_text.config(state="disabled")  # Read-only

    # 🔹 Export Button
    tk.Button(logs_frame, text="EXPORT LOGS TO PDF", font=("Segoe UI", 12, "bold"),
              bg="#0078D7", fg="white", activebackground="#005A9E", relief="flat",
              command=export_logs).pack(pady=15)

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
    export_pdf_frame = tk.Frame(main_frame, bg="#f9f9f9")
    export_pdf_frame.pack(pady=30, fill="both", expand=True)

    # 🔹 Title
    tk.Label(
        export_pdf_frame,
        text='📄 CyberSecurity Audit Report',
        font=('Segoe UI', 28, 'bold'),
        bg="#f9f9f9",
        fg="#2c3e50"
    ).pack(pady=(0, 10))

    # 🔹 Subtitle
    tk.Label(
        export_pdf_frame,
        text='Generate a detailed system audit report in PDF format.',
        font=('Segoe UI', 13),
        bg="#f9f9f9",
        fg="#555"
    ).pack(pady=(0, 25))

    # 🔹 Card-style container
    card = tk.Frame(export_pdf_frame, bg="white", bd=1, relief="solid", width=520, height=270)
    card.pack()
    card.pack_propagate(False)

    # 🔹 Inside card content
    form = tk.Frame(card, bg="white")
    form.pack(pady=25)

    # Input: Name
    tk.Label(form, text="👤 User Name:", font=("Segoe UI", 11), bg="white").grid(row=0, column=0, sticky="e", padx=10, pady=8)
    name_entry = tk.Entry(form, font=("Segoe UI", 11), width=30, bd=1, relief="solid", highlightthickness=1)
    name_entry.grid(row=0, column=1, padx=10, pady=8)

    # Input: Lab
    tk.Label(form, text="🏢 Lab Name:", font=("Segoe UI", 11), bg="white").grid(row=1, column=0, sticky="e", padx=10, pady=8)
    lab_entry = tk.Entry(form, font=("Segoe UI", 11), width=30, bd=1, relief="solid", highlightthickness=1)
    lab_entry.grid(row=1, column=1, padx=10, pady=8)

    # Status label
    status_label = tk.Label(card, text="", font=("Segoe UI", 10), fg="green", bg="white")
    status_label.pack(pady=(0, 5))

    # 🔹 Generate Button
    def generate_report():
        user_name = name_entry.get().strip()
        lab_name = lab_entry.get().strip()

        if not user_name or not lab_name:
            messagebox.showwarning("Input Required", "Please enter both User Name and Lab Name.")
            return

        generate_btn.config(state="disabled", text="⏳ Generating...")

        def run():
            try:
                status_label.config(text="📄 Generating PDF, please wait...", fg="blue")
                pdf_generator.generate_pdf_report(user_name, lab_name)
                root.after(0, lambda: status_label.config(text="✅ Report generated successfully!", fg="green"))
                root.after(0, lambda: messagebox.showinfo("Done", "PDF Report has been generated."))
            except Exception as e:
                root.after(0, lambda: status_label.config(text="❌ Failed to generate report.", fg="red"))
                root.after(0, lambda: messagebox.showerror("Error", str(e)))
            finally:
                root.after(0, lambda: generate_btn.config(state="normal", text="📝 GENERATE REPORT"))

        threading.Thread(target=run).start()

    generate_btn = tk.Button(
        card,
        text="📝 GENERATE REPORT",
        font=('Segoe UI', 12, 'bold'),
        width=28,
        bg="#007BFF",
        fg="white",
        activebackground="#0056b3",
        relief="flat",
        cursor="hand2",
        command=generate_report
    )
    generate_btn.pack(pady=(10, 20))

    # 🔹 Footer note
    tk.Label(
        export_pdf_frame,
        text="🔒 Your data is processed locally. Nothing is uploaded.",
        font=("Arial", 9),
        bg="#f9f9f9",
        fg="gray"
    ).pack(pady=(15, 0))

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
    lb.config(bg='#1abc9c')  # Highlight with accent
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
