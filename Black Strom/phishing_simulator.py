import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText
import webbrowser
from datetime import datetime, timedelta
import hashlib
import random
import os
import sys

class AdvancedPhishingSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Phishing Simulation Toolkit - Educational Use Only")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        self.root.minsize(900, 600)
        
        # Initialize all attributes first
        self.authenticated = False
        self.attempts = []
        self.current_template = None
        self.simulation_active = False
        self.simulation_start_time = None
        
        # Security configuration
        self.CONTROL_PANEL_PASSWORD = self.hash_password("training123")  # Default password
        self.session_timeout = 30  # minutes
        self.max_attempts = 50  # Maximum log entries before auto-clear
        
        # Style configuration
        self.setup_styles()
        
        # Create tabs
        self.tab_control = ttk.Notebook(root)
        
        # Simulation Tab
        self.sim_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.sim_tab, text='Phishing Simulation')
        
        # Control Panel Tab (password protected)
        self.control_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.control_tab, text='Control Panel')
        
        # Documentation Tab
        self.doc_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.doc_tab, text='Documentation & Training')
        
        # Reporting Tab
        self.report_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.report_tab, text='Reports & Analytics')
        
        self.tab_control.pack(expand=1, fill='both')
        
        # Initialize components
        self.create_simulation_tab()
        self.create_control_panel()
        self.create_documentation_tab()
        self.create_report_tab()
        
        # Security measures
        self.disable_export()
        self.protect_control_panel()
        
        # Show consent dialog
        self.show_consent_dialog()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('TNotebook', background='#f5f5f5')
        style.configure('TNotebook.Tab', background='#e1e1e1', padding=[10, 5])
        style.map('TNotebook.Tab', background=[('selected', '#4a6ea9')])
        
        style.configure('TFrame', background='#f5f5f5')
        style.configure('TLabel', background='#f5f5f5', font=('Segoe UI', 10))
        style.configure('TButton', font=('Segoe UI', 10), padding=5)
        style.configure('TEntry', font=('Segoe UI', 10), padding=5)
        style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'))
        style.configure('Warning.TLabel', foreground='red', font=('Segoe UI', 10, 'bold'))
        
        # Custom styles
        style.configure('Red.TButton', foreground='white', background='#c44d56')
        style.configure('Green.TButton', foreground='white', background='#4caf50')
        style.configure('Blue.TButton', foreground='white', background='#4a6ea9')
    
    def hash_password(self, password):
        """Hash password for storage"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def disable_export(self):
        """Disable potential data export methods"""
        def empty_clipboard():
            self.root.clipboard_clear()
            self.root.clipboard_append('')
        
        self.root.clipboard_clear = empty_clipboard
        self.root.clipboard_append = lambda _: None
        self.root.bind('<Control-c>', lambda e: "break")
        self.root.bind('<Control-v>', lambda e: "break")
    
    def protect_control_panel(self):
        """Password protect the control panel"""
        self.control_tab.bind('<Visibility>', lambda e: self.check_authentication())
    
    def check_authentication(self):
        """Check if user is authenticated to access control panel"""
        if not self.authenticated and self.tab_control.index(self.tab_control.select()) == 1:
            self.authenticate_user()
    
    def authenticate_user(self):
        """Authenticate user for control panel access"""
        password = simpledialog.askstring(
            "Control Panel Authentication",
            "Enter control panel password:",
            show='*',
            parent=self.root
        )
        
        if password:
            entered_hash = self.hash_password(password)
            if entered_hash == self.CONTROL_PANEL_PASSWORD:
                self.authenticated = True
                # Destroy and recreate the Control Panel with unlocked content
                self.control_tab.destroy()
                self.control_tab = ttk.Frame(self.tab_control)
                self.tab_control.insert(1, self.control_tab, text='Control Panel')
                self.create_control_panel()
                self.tab_control.select(1)  # Switch to Control Panel
                messagebox.showinfo("Access Granted", "Control panel unlocked")
            else:
                messagebox.showerror("Access Denied", "Incorrect password")
                self.tab_control.select(0)  # Switch back to simulation tab
    
    def show_consent_dialog(self):
        """Show consent dialog before first simulation"""
        consent = messagebox.askyesno(
            "Ethical Use Agreement",
            "This tool is for EDUCATIONAL PURPOSES ONLY.\n\n"
            "By using this software, you agree:\n"
            "- You have proper authorization\n"
            "- You will only test systems you own/have permission to test\n"
            "- You understand unauthorized use may be illegal\n\n"
            "Do you agree to these terms?",
            icon='warning'
        )
        
        if not consent:
            messagebox.showinfo(
                "Exiting Application",
                "The application will now close as you did not agree to the terms."
            )
            self.root.destroy()
            sys.exit()
    
    def create_simulation_tab(self):
        """Create the phishing simulation interface"""
        # Main frame with gradient background
        self.login_frame = tk.Frame(self.sim_tab, bg='white')
        self.login_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Logo/Header with image (simulated)
        self.logo_image = self.create_simulated_logo()
        self.logo_label = tk.Label(
            self.login_frame, 
            image=self.logo_image,
            bg='white'
        )
        self.logo_label.pack(pady=(20, 10))
        
        # Login container
        login_container = tk.Frame(self.login_frame, bg='white', padx=20, pady=20)
        login_container.pack(expand=True)
        
        # Username Field
        self.username_label = ttk.Label(
            login_container, 
            text="Email or Username", 
            style='TLabel'
        )
        self.username_label.pack(anchor='w', pady=(10, 0))
        
        self.username_entry = ttk.Entry(
            login_container, 
            width=40, 
            font=('Segoe UI', 11)
        )
        self.username_entry.pack(pady=(0, 10))
        
        # Password Field
        self.password_label = ttk.Label(
            login_container, 
            text="Password", 
            style='TLabel'
        )
        self.password_label.pack(anchor='w')
        
        self.password_entry = ttk.Entry(
            login_container, 
            width=40, 
            font=('Segoe UI', 11), 
            show='•'
        )
        self.password_entry.pack(pady=(0, 20))
        
        # Login Button
        self.login_button = ttk.Button(
            login_container, 
            text="Sign In", 
            style='Blue.TButton',
            command=self.capture_credentials
        )
        self.login_button.pack(pady=(0, 20))
        
        # "Forgot password" link
        forgot_link = ttk.Label(
            login_container, 
            text="Forgot password?", 
            cursor="hand2",
            style='TLabel'
        )
        forgot_link.pack()
        forgot_link.bind("<Button-1>", lambda e: self.show_forgot_password())
        
        # Footer with warning
        footer_frame = tk.Frame(self.login_frame, bg='white')
        footer_frame.pack(side='bottom', fill='x', pady=(0, 10))
        
        warning_label = ttk.Label(
            footer_frame, 
            text="This is a simulated phishing page for educational purposes only.",
            style='Warning.TLabel'
        )
        warning_label.pack()
        
        copyright_label = ttk.Label(
            footer_frame, 
            text="© 2025 Security Training Tool. All rights reserved.", 
            style='TLabel'
        )
        copyright_label.pack()
    
    def create_simulated_logo(self):
        """Create a simulated logo image"""
        try:
            # Try to load an actual image if available
            from PIL import Image, ImageTk, ImageDraw, ImageFont
            
            # Create a simple logo image
            img = Image.new('RGB', (200, 60), color='white')
            d = ImageDraw.Draw(img)
            
            # Draw a simple logo
            d.rectangle([10, 10, 50, 50], fill='#4a6ea9')
            d.text((60, 20), "SecureLogin", fill='black', font=ImageFont.load_default())
            
            return ImageTk.PhotoImage(img)
        except ImportError:
            # Fallback to text if PIL isn't available
            return tk.PhotoImage()  # Empty image
    
    def create_control_panel(self):
        """Create the control panel interface"""
        if not self.authenticated:
            locked_frame = ttk.Frame(self.control_tab)
            locked_frame.pack(expand=True, fill='both')
            
            ttk.Label(
                locked_frame, 
                text="Control Panel Locked", 
                style='Header.TLabel'
            ).pack(pady=20)
            
            ttk.Button(
                locked_frame,
                text="Authenticate",
                command=self.authenticate_user,
                style='Blue.TButton'
            ).pack()
            
            return
        
        # Template Selection
        template_frame = ttk.LabelFrame(self.control_tab, text="Template Configuration", padding=10)
        template_frame.pack(fill='x', padx=10, pady=5)
        
        self.template_var = tk.StringVar(value="email")
        
        templates = [
            ("Social Media", "social_media"),
            ("Email Provider", "email"),
            ("Banking", "banking"),
            ("Corporate VPN", "corporate"),
            ("Cloud Storage", "cloud"),
            ("Gaming Platform", "gaming")
        ]
        
        # Template selection buttons
        template_row = ttk.Frame(template_frame)
        template_row.pack(fill='x', pady=5)
        
        for i, (text, mode) in enumerate(templates):
            btn = ttk.Radiobutton(
                template_row, 
                text=text, 
                variable=self.template_var, 
                value=mode,
                command=self.change_template
            )
            btn.pack(side='left', padx=5)
            
            # Add tooltip
            self.create_tooltip(btn, f"Simulate a {text.lower()} login page")
        
        # Advanced options
        adv_frame = ttk.LabelFrame(template_frame, text="Advanced Options", padding=10)
        adv_frame.pack(fill='x', pady=(10, 0))
        
        # Add fake 2FA option
        self.two_fa_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            adv_frame,
            text="Simulate Two-Factor Authentication",
            variable=self.two_fa_var
        ).pack(anchor='w')
        
        # Add password complexity check
        self.complexity_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            adv_frame,
            text="Enable Password Complexity Check",
            variable=self.complexity_var
        ).pack(anchor='w')
        
        # Simulation Controls
        control_frame = ttk.LabelFrame(self.control_tab, text="Simulation Controls", padding=10)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(fill='x')
        
        self.start_button = ttk.Button(
            btn_frame, 
            text="Start Simulation", 
            style='Green.TButton',
            command=self.start_simulation
        )
        self.start_button.pack(side='left', padx=5)
        
        self.stop_button = ttk.Button(
            btn_frame, 
            text="Stop Simulation", 
            style='Red.TButton',
            state='disabled',
            command=self.stop_simulation
        )
        self.stop_button.pack(side='left', padx=5)
        
        # Add timer display
        self.timer_label = ttk.Label(
            btn_frame,
            text="Session: Not active",
            style='TLabel'
        )
        self.timer_label.pack(side='right', padx=10)
        
        # Results Display
        results_frame = ttk.LabelFrame(self.control_tab, text="Captured Data", padding=10)
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Add filter controls
        filter_frame = ttk.Frame(results_frame)
        filter_frame.pack(fill='x', pady=(0, 5))
        
        ttk.Label(filter_frame, text="Filter:").pack(side='left')
        
        self.filter_var = tk.StringVar(value="all")
        ttk.Combobox(
            filter_frame,
            textvariable=self.filter_var,
            values=["All attempts", "Today", "Last hour", "By template"],
            state="readonly",
            width=15
        ).pack(side='left', padx=5)
        
        ttk.Button(
            filter_frame,
            text="Apply",
            command=self.apply_filter,
            style='TButton'
        ).pack(side='left', padx=5)
        
        # Results text area with scrollbar
        self.results_text = ScrolledText(
            results_frame,
            wrap='word',
            font=('Consolas', 10),
            height=10
        )
        self.results_text.pack(fill='both', expand=True)
        self.results_text.config(state='disabled')
        
        # Bottom controls
        bottom_frame = ttk.Frame(results_frame)
        bottom_frame.pack(fill='x', pady=(5, 0))
        
        ttk.Button(
            bottom_frame,
            text="Clear Logs",
            command=self.clear_logs,
            style='TButton'
        ).pack(side='left', padx=5)
        
        ttk.Button(
            bottom_frame,
            text="Export Report (PDF)",
            command=self.export_report,
            state='disabled'  # Disabled in this version
        ).pack(side='right', padx=5)
    
    def create_documentation_tab(self):
        """Create the documentation and training tab"""
        # Notebook for documentation sections
        doc_notebook = ttk.Notebook(self.doc_tab)
        doc_notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # About Section
        about_frame = ttk.Frame(doc_notebook)
        doc_notebook.add(about_frame, text='About This Tool')
        
        about_text = """
This Advanced Phishing Simulation Tool is designed for security awareness training and educational purposes only.

Key Features:
- Multiple realistic phishing templates
- Credential capture simulation
- Educational materials about phishing
- Detailed reporting and analytics

Ethical Use Guidelines:
1. Only use with explicit permission from all participants
2. Conduct in controlled environments only
3. Never use against production systems without authorization
4. Always obtain proper legal consent

This tool does not actually transmit captured credentials anywhere.
All data remains local to this machine and is never stored permanently.
"""
        about_text_widget = ScrolledText(
            about_frame,
            wrap='word',
            font=('Segoe UI', 10),
            padx=10,
            pady=10
        )
        about_text_widget.insert('1.0', about_text)
        about_text_widget.config(state='disabled')
        about_text_widget.pack(expand=True, fill='both')
        
        # Phishing Techniques Section
        techniques_frame = ttk.Frame(doc_notebook)
        doc_notebook.add(techniques_frame, text='Phishing Techniques')
        
        techniques_text = """
Common Phishing Techniques:

1. Deceptive Phishing:
   - Fake emails mimicking legitimate organizations
   - Urgent requests for action (e.g., "Update your account now")
   - Links to fraudulent websites

2. Spear Phishing:
   - Targeted attacks against specific individuals
   - Uses personal information to appear legitimate
   - Often targets financial or HR departments

3. Whaling:
   - Attacks targeting high-profile executives
   - Often involve fake legal documents or executive communications
   - May spoof CEO emails to request fund transfers

4. Clone Phishing:
   - Duplicates of legitimate emails with malicious attachments/links
   - Appears to be a resend or update of a previous message

5. Pharming:
   - Redirects users to fake websites via DNS poisoning
   - Often targets financial institutions
   - Users see legitimate URLs but are on fake sites

Red Flags to Watch For:
- Urgent or threatening language
- Requests for sensitive information
- Unusual sender addresses
- Poor spelling and grammar
- Suspicious links or attachments
- Requests to bypass normal procedures
"""
        techniques_text_widget = ScrolledText(
            techniques_frame,
            wrap='word',
            font=('Segoe UI', 10),
            padx=10,
            pady=10
        )
        techniques_text_widget.insert('1.0', techniques_text)
        techniques_text_widget.config(state='disabled')
        techniques_text_widget.pack(expand=True, fill='both')
        
        # Prevention Section
        prevention_frame = ttk.Frame(doc_notebook)
        doc_notebook.add(prevention_frame, text='Prevention Guide')
        
        prevention_text = """
How to Protect Against Phishing:

1. Email Protection:
   - Verify sender addresses carefully
   - Hover over links before clicking
   - Be wary of unexpected attachments
   - Use email filtering solutions

2. Browser Protection:
   - Check for HTTPS and valid certificates
   - Look for subtle URL differences
   - Use anti-phishing browser extensions
   - Keep browsers updated

3. Organizational Measures:
   - Implement multi-factor authentication
   - Conduct regular security training
   - Use email authentication (SPF, DKIM, DMARC)
   - Maintain updated security policies

4. Personal Habits:
   - Never reuse passwords across sites
   - Use a password manager
   - Report suspicious emails to IT
   - Verify unusual requests via another channel

What to Do If You Fall for Phishing:
1. Immediately change affected passwords
2. Contact your IT/security team
3. Scan for malware if you clicked links/downloads
4. Monitor accounts for suspicious activity
5. Report the incident to help others
"""
        prevention_text_widget = ScrolledText(
            prevention_frame,
            wrap='word',
            font=('Segoe UI', 10),
            padx=10,
            pady=10
        )
        prevention_text_widget.insert('1.0', prevention_text)
        prevention_text_widget.config(state='disabled')
        prevention_text_widget.pack(expand=True, fill='both')
        
        # Resources Section
        resources_frame = ttk.Frame(doc_notebook)
        doc_notebook.add(resources_frame, text='Additional Resources')
        
        resources = [
            ("Anti-Phishing Working Group", "https://apwg.org"),
            ("CISA Phishing Guidance", "https://www.cisa.gov/phishing"),
            ("FTC Phishing Information", "https://www.consumer.ftc.gov/articles/how-recognize-and-avoid-phishing-scams"),
            ("Phishing Quiz by Google", "https://phishingquiz.withgoogle.com"),
            ("NIST Security Guidelines", "https://www.nist.gov/itl/smallbusinesscyber/guidance-topic/phishing")
        ]
        
        for text, url in resources:
            btn = ttk.Button(
                resources_frame,
                text=text,
                command=lambda u=url: webbrowser.open(u),
                style='TButton'
            )
            btn.pack(fill='x', padx=10, pady=5)
    
    def create_report_tab(self):
        """Create the reporting and analytics tab"""
        report_frame = ttk.Frame(self.report_tab)
        report_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Stats frame
        stats_frame = ttk.LabelFrame(report_frame, text="Simulation Statistics", padding=10)
        stats_frame.pack(fill='x', pady=(0, 10))
        
        # Stats grid
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack()
        
        # Total attempts
        ttk.Label(stats_grid, text="Total Attempts:", style='TLabel').grid(row=0, column=0, sticky='e')
        self.total_attempts_label = ttk.Label(stats_grid, text="0", style='Header.TLabel')
        self.total_attempts_label.grid(row=0, column=1, sticky='w', padx=10)
        
        # Unique users
        ttk.Label(stats_grid, text="Unique Users:", style='TLabel').grid(row=1, column=0, sticky='e')
        self.unique_users_label = ttk.Label(stats_grid, text="0", style='Header.TLabel')
        self.unique_users_label.grid(row=1, column=1, sticky='w', padx=10)
        
        # Most used template
        ttk.Label(stats_grid, text="Most Used Template:", style='TLabel').grid(row=0, column=2, sticky='e', padx=(20, 0))
        self.popular_template_label = ttk.Label(stats_grid, text="None", style='Header.TLabel')
        self.popular_template_label.grid(row=0, column=3, sticky='w', padx=10)
        
        # Last attempt
        ttk.Label(stats_grid, text="Last Attempt:", style='TLabel').grid(row=1, column=2, sticky='e', padx=(20, 0))
        self.last_attempt_label = ttk.Label(stats_grid, text="Never", style='Header.TLabel')
        self.last_attempt_label.grid(row=1, column=3, sticky='w', padx=10)
        
        # Chart frame (simulated)
        chart_frame = ttk.LabelFrame(report_frame, text="Attempts Over Time", padding=10)
        chart_frame.pack(fill='both', expand=True)
        
        # Simulated chart
        chart_canvas = tk.Canvas(chart_frame, bg='white', height=200)
        chart_canvas.pack(fill='both', expand=True)
        
        # Draw some sample data
        self.draw_simulated_chart(chart_canvas)
        
        # Template distribution
        dist_frame = ttk.LabelFrame(report_frame, text="Template Distribution", padding=10)
        dist_frame.pack(fill='both', pady=(10, 0))
        
        dist_canvas = tk.Canvas(dist_frame, bg='white', height=150)
        dist_canvas.pack(fill='both', expand=True)
        
        # Draw some sample data
        self.draw_template_distribution(dist_canvas)
    
    def draw_simulated_chart(self, canvas):
        """Draw a simulated line chart"""
        width = canvas.winfo_width() - 20
        height = canvas.winfo_height() - 20
        
        if width < 50 or height < 50:  # Too small to draw
            return
        
        # Draw axes
        canvas.create_line(30, height-30, width-10, height-30, fill='black')  # X-axis
        canvas.create_line(30, height-30, 30, 20, fill='black')  # Y-axis
        
        # Draw labels
        canvas.create_text(15, height//2, text="Attempts", angle=90, anchor='w')
        canvas.create_text(width//2, height-10, text="Time", anchor='n')
        
        # Draw some random data
        points = []
        for i in range(1, 8):
            x = 30 + (i * (width-40)) // 8
            y = height - 30 - (random.randint(10, height-50))
            points.append((x, y))
            
            # Draw day label
            canvas.create_text(x, height-20, text=f"Day {i}", anchor='n')
        
        # Connect points
        for i in range(len(points)-1):
            canvas.create_line(points[i][0], points[i][1], points[i+1][0], points[i+1][1], fill='blue', width=2)
        
        # Draw points
        for x, y in points:
            canvas.create_oval(x-3, y-3, x+3, y+3, fill='red', outline='black')
    
    def draw_template_distribution(self, canvas):
        """Draw a simulated bar chart of template usage"""
        width = canvas.winfo_width() - 20
        height = canvas.winfo_height() - 20
        
        if width < 50 or height < 50:  # Too small to draw
            return
        
        templates = ["Email", "Social", "Bank", "Corporate", "Cloud"]
        values = [random.randint(5, 20) for _ in templates]
        max_val = max(values) if values else 1
        
        bar_width = (width - 50) // len(templates)
        
        for i, (template, value) in enumerate(zip(templates, values)):
            x1 = 40 + i * bar_width
            x2 = x1 + bar_width - 10
            y = height - 30 - (value * (height-50)) // max_val
            
            # Draw bar
            color = ['#4a6ea9', '#5cb85c', '#5bc0de', '#f0ad4e', '#d9534f'][i % 5]
            canvas.create_rectangle(x1, y, x2, height-30, fill=color, outline='black')
            
            # Draw label
            canvas.create_text((x1+x2)//2, height-15, text=template, anchor='n')
            canvas.create_text((x1+x2)//2, y-10, text=str(value), anchor='s')
    
    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        tooltip = tk.Toplevel(self.root)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_withdraw()
        
        label = ttk.Label(
            tooltip,
            text=text,
            background="#ffffe0",
            relief='solid',
            borderwidth=1,
            padding=5,
            wraplength=200
        )
        label.pack()
        
        def enter(event):
            x = widget.winfo_rootx() + widget.winfo_width() + 5
            y = widget.winfo_rooty() + widget.winfo_height() // 2
            tooltip.wm_geometry(f"+{x}+{y}")
            tooltip.wm_deiconify()
        
        def leave(event):
            tooltip.wm_withdraw()
        
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)
    
    def change_template(self):
        """Change the phishing template"""
        template = self.template_var.get()
        self.current_template = template
        
        # Define template styles
        templates = {
            "social_media": {
                "bg": "#3b5998",
                "fg": "white",
                "text": "Social Media Login",
                "logo_color": "white"
            },
            "email": {
                "bg": "#f0f0f0",
                "fg": "#2c3e50",
                "text": "Email Provider Login",
                "logo_color": "#2c3e50"
            },
            "banking": {
                "bg": "#005ea6",
                "fg": "white",
                "text": "Online Banking",
                "logo_color": "white"
            },
            "corporate": {
                "bg": "#34495e",
                "fg": "white",
                "text": "Corporate VPN",
                "logo_color": "white"
            },
            "cloud": {
                "bg": "#f8f9fa",
                "fg": "#212529",
                "text": "Cloud Storage",
                "logo_color": "#4285F4"
            },
            "gaming": {
                "bg": "#0e0e10",
                "fg": "#00ff7f",
                "text": "Gaming Platform",
                "logo_color": "#00ff7f"
            }
        }
        
        style = templates.get(template, templates["email"])
        
        # Apply styles
        self.login_frame.config(bg=style["bg"])
        self.logo_label.config(bg=style["bg"])
        self.username_label.config(bg=style["bg"], fg=style["fg"])
        self.password_label.config(bg=style["bg"], fg=style["fg"])
        
        # Update logo text
        self.logo_label.config(text=style["text"])
        
        # Update all children of login_frame
        for child in self.login_frame.winfo_children():
            if hasattr(child, 'config') and 'bg' in child.config():
                child.config(bg=style["bg"])
            if hasattr(child, 'config') and 'fg' in child.config():
                child.config(fg=style["fg"])
        
        # Special case for entry widgets
        self.username_entry.config(background='white')
        self.password_entry.config(background='white')
    
    def start_simulation(self):
        """Start the phishing simulation"""
        # Get participant consent
        consent = messagebox.askyesno(
            "Participant Consent",
            "This is a simulated phishing exercise.\n\n"
            "By proceeding, you acknowledge:\n"
            "- This is for security training only\n"
            "- No real credentials are being sent\n"
            "- All activity is logged locally\n\n"
            "Do you consent to participate?",
            icon='warning'
        )
        
        if not consent:
            return
        
        self.simulation_active = True
        self.simulation_start_time = datetime.now()
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        
        # Start the timer
        self.update_timer()
        
        # Change to the selected template
        self.change_template()
        
        messagebox.showinfo(
            "Simulation Started",
            "Phishing simulation is now active.\n"
            f"Template: {self.template_var.get().replace('_', ' ').title()}\n"
            f"Session will timeout after {self.session_timeout} minutes."
        )
    
    def stop_simulation(self):
        """Stop the phishing simulation"""
        self.simulation_active = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        
        # Calculate duration
        if self.simulation_start_time:
            duration = datetime.now() - self.simulation_start_time
            duration_str = str(duration).split('.')[0]  # Remove microseconds
        else:
            duration_str = "Unknown"
        
        messagebox.showinfo(
            "Simulation Stopped",
            "Phishing simulation has been stopped.\n\n"
            f"Duration: {duration_str}\n"
            f"Attempts captured: {len(self.attempts)}"
        )
        
        # Update reports
        self.update_reports()
    
    def update_timer(self):
        """Update the simulation timer"""
        if self.simulation_active and self.simulation_start_time:
            elapsed = datetime.now() - self.simulation_start_time
            remaining = timedelta(minutes=self.session_timeout) - elapsed
            
            if remaining.total_seconds() <= 0:
                self.stop_simulation()
                return
            
            # Update timer label
            self.timer_label.config(
                text=f"Session: {str(remaining).split('.')[0]} remaining"
            )
            
            # Schedule next update
            self.root.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="Session: Not active")
    
    def capture_credentials(self):
        """Capture entered credentials"""
        if not self.simulation_active:
            messagebox.showwarning(
                "Simulation Inactive",
                "Please start the simulation from the Control Panel first."
            )
            return
            
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showwarning(
                "Empty Fields",
                "Please enter both username and password."
            )
            return
        
        # Check password complexity if enabled
        if self.complexity_var.get():
            complexity_feedback = self.check_password_complexity(password)
            if complexity_feedback:
                messagebox.showwarning(
                    "Weak Password",
                    f"Password does not meet complexity requirements:\n{complexity_feedback}"
                )
                # Continue anyway since this is a simulation
        
        # Log the attempt
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        attempt = {
            'timestamp': timestamp,
            'template': self.current_template,
            'username': username,
            'password': password
        }
        self.attempts.append(attempt)
        
        # Update results display
        self.results_text.config(state='normal')
        self.results_text.insert('end', 
            f"[{timestamp}] Captured credentials from {self.current_template} template:\n"
            f"Username: {username}\n"
            f"Password: {password}\n"
            f"{'-'*50}\n"
        )
        self.results_text.config(state='disabled')
        self.results_text.see('end')
        
        # Check if we've reached max attempts
        if len(self.attempts) >= self.max_attempts:
            messagebox.showwarning(
                "Maximum Attempts Reached",
                f"Reached maximum of {self.max_attempts} log entries.\n"
                "Oldest entries will be removed if more attempts are made."
            )
            # Keep only the most recent entries
            self.attempts = self.attempts[-self.max_attempts:]
        
        # Show "success" message to user
        if self.two_fa_var.get():
            self.show_two_factor()
        else:
            messagebox.showinfo(
                "Login Successful",
                "You have successfully logged in.\n"
                "(This is a simulation - your credentials were not actually sent anywhere)"
            )
        
        # Clear fields
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        
        # Update reports
        self.update_reports()
    
    def check_password_complexity(self, password):
        """Check password against complexity rules"""
        feedback = []
        
        if len(password) < 8:
            feedback.append("- At least 8 characters")
        if not any(c.isupper() for c in password):
            feedback.append("- At least one uppercase letter")
        if not any(c.islower() for c in password):
            feedback.append("- At least one lowercase letter")
        if not any(c.isdigit() for c in password):
            feedback.append("- At least one number")
        if not any(c in '!@#$%^&*()' for c in password):
            feedback.append("- At least one special character")
        
        return '\n'.join(feedback) if feedback else ''
    
    def show_two_factor(self):
        """Show simulated two-factor authentication"""
        two_fa_window = tk.Toplevel(self.root)
        two_fa_window.title("Two-Factor Authentication")
        two_fa_window.geometry("400x250")
        two_fa_window.resizable(False, False)
        
        # Center the window
        window_width = 400
        window_height = 250
        screen_width = two_fa_window.winfo_screenwidth()
        screen_height = two_fa_window.winfo_screenheight()
        
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        
        two_fa_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        
        # Content
        ttk.Label(
            two_fa_window,
            text="Two-Factor Authentication Required",
            style='Header.TLabel'
        ).pack(pady=(20, 10))
        
        ttk.Label(
            two_fa_window,
            text="Enter the 6-digit code sent to your device:",
            style='TLabel'
        ).pack()
        
        code_entry = ttk.Entry(
            two_fa_window,
            font=('Segoe UI', 14),
            width=10
        )
        code_entry.pack(pady=10)
        
        # Generate a random code
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        # Show the code in a label (for demo purposes)
        code_label = ttk.Label(
            two_fa_window,
            text=f"(Demo code: {code})",
            style='TLabel'
        )
        code_label.pack()
        
        def verify_code():
            entered_code = code_entry.get()
            if entered_code == code:
                messagebox.showinfo(
                    "Verification Successful",
                    "Two-factor authentication completed successfully.\n"
                    "(This is a simulation - no actual verification occurred)"
                )
                two_fa_window.destroy()
            else:
                messagebox.showerror(
                    "Invalid Code",
                    "The code you entered is incorrect. Please try again."
                )
        
        verify_button = ttk.Button(
            two_fa_window,
            text="Verify",
            command=verify_code,
            style='Blue.TButton'
        )
        verify_button.pack(pady=10)
    
    def show_forgot_password(self):
        """Show simulated password recovery"""
        forgot_window = tk.Toplevel(self.root)
        forgot_window.title("Password Recovery")
        forgot_window.geometry("500x300")
        forgot_window.resizable(False, False)
        
        # Center the window
        window_width = 500
        window_height = 300
        screen_width = forgot_window.winfo_screenwidth()
        screen_height = forgot_window.winfo_screenheight()
        
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        
        forgot_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        
        # Content
        ttk.Label(
            forgot_window,
            text="Reset Your Password",
            style='Header.TLabel'
        ).pack(pady=(20, 10))
        
        ttk.Label(
            forgot_window,
            text="Enter your email address to receive a password reset link:",
            style='TLabel'
        ).pack()
        
        email_entry = ttk.Entry(
            forgot_window,
            font=('Segoe UI', 12),
            width=40
        )
        email_entry.pack(pady=10)
        
        def send_reset_link():
            email = email_entry.get()
            if "@" in email and "." in email:
                messagebox.showinfo(
                    "Reset Link Sent",
                    f"A password reset link has been sent to {email}\n"
                    "(This is a simulation - no email was actually sent)"
                )
                forgot_window.destroy()
            else:
                messagebox.showerror(
                    "Invalid Email",
                    "Please enter a valid email address."
                )
        
        send_button = ttk.Button(
            forgot_window,
            text="Send Reset Link",
            command=send_reset_link,
            style='Blue.TButton'
        )
        send_button.pack(pady=10)
        
        warning_label = ttk.Label(
            forgot_window,
            text="This is a simulated password recovery page for educational purposes only.",
            style='Warning.TLabel'
        )
        warning_label.pack(side='bottom', pady=10)
    
    def apply_filter(self):
        """Apply filter to the results display"""
        filter_type = self.filter_var.get()
        self.results_text.config(state='normal')
        self.results_text.delete(1.0, 'end')
        
        now = datetime.now()
        
        for attempt in self.attempts:
            timestamp = datetime.strptime(attempt['timestamp'], "%Y-%m-%d %H:%M:%S")
            
            if filter_type == "All attempts" or filter_type == "all":
                show = True
            elif filter_type == "Today":
                show = timestamp.date() == now.date()
            elif filter_type == "Last hour":
                show = (now - timestamp) < timedelta(hours=1)
            elif filter_type == "By template":
                show = attempt['template'] == self.current_template
            else:
                show = True
            
            if show:
                self.results_text.insert('end', 
                    f"[{attempt['timestamp']}] Captured credentials from {attempt['template']} template:\n"
                    f"Username: {attempt['username']}\n"
                    f"Password: {attempt['password']}\n"
                    f"{'-'*50}\n"
                )
        
        self.results_text.config(state='disabled')
        self.results_text.see('end')
    
    def clear_logs(self):
        """Clear all captured data"""
        confirm = messagebox.askyesno(
            "Confirm Clear",
            "This will permanently delete all captured data.\n"
            "Are you sure you want to continue?"
        )
        
        if confirm:
            self.attempts = []
            self.results_text.config(state='normal')
            self.results_text.delete(1.0, 'end')
            self.results_text.config(state='disabled')
            self.update_reports()
            messagebox.showinfo("Logs Cleared", "All captured data has been cleared.")
    
    def export_report(self):
        """Export report (disabled in this version)"""
        messagebox.showinfo(
            "Export Disabled",
            "Report export functionality is disabled in this version.\n"
            "All data remains local to this machine for security reasons."
        )
    
    def update_reports(self):
        """Update the reports and analytics tab"""
        # Update basic stats
        self.total_attempts_label.config(text=str(len(self.attempts)))
        
        # Count unique usernames
        unique_users = len(set(attempt['username'] for attempt in self.attempts))
        self.unique_users_label.config(text=str(unique_users))
        
        # Find most popular template
        if self.attempts:
            templates = [attempt['template'] for attempt in self.attempts]
            popular = max(set(templates), key=templates.count)
            self.popular_template_label.config(text=popular.replace('_', ' ').title())
            
            # Update last attempt time
            last = self.attempts[-1]['timestamp']
            self.last_attempt_label.config(text=last)
        else:
            self.popular_template_label.config(text="None")
            self.last_attempt_label.config(text="Never")
        
        # Redraw charts
        for child in self.report_tab.winfo_children():
            if isinstance(child, ttk.LabelFrame):
                for canvas in child.winfo_children():
                    if isinstance(canvas, tk.Canvas):
                        canvas.delete("all")
                        if "Attempts Over Time" in child['text']:
                            self.draw_simulated_chart(canvas)
                        elif "Template Distribution" in child['text']:
                            self.draw_template_distribution(canvas)

def main():
    root = tk.Tk()
    app = AdvancedPhishingSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()