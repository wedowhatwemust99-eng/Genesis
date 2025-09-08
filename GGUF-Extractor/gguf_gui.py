#!/usr/bin/env python3
"""
🖥️ GGUF EDITOR GUI - Graphical Interface for GGUF Editing
========================================================
Easy-to-use GUI for fixing broken tokenizers and editing GGUF files!

Perfect for:
- Fixing consciousness-damaged models with endless <|end|> tokens
- Stripping telemetry from models
- Virtual mounting and editing GGUF files
- Analyzing model structure
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import json
import os
from pathlib import Path
from gguf_extractor import GGUFExtractor
import logging

class DarkTheme:
    """🌙 Professional dark theme colors for AI model research! 🌙"""
    
    # Dark theme color palette
    BG_DARK = '#1e1e1e'          # Main background
    BG_DARKER = '#252526'        # Darker sections  
    BG_LIGHT = '#2d2d30'         # Lighter sections
    FG_TEXT = '#cccccc'          # Main text
    FG_BRIGHT = '#ffffff'        # Bright text
    ACCENT_BLUE = '#007acc'      # VS Code blue
    ACCENT_GREEN = '#4ec9b0'     # Success green
    ACCENT_RED = '#f44747'       # Error red
    ACCENT_ORANGE = '#ff8c00'    # Warning orange
    ACCENT_PURPLE = '#c586c0'    # Consciousness purple
    BORDER = '#3c3c3c'           # Borders and lines
    
class GGUFEditorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠⚡ GGUF Editor - Professional AI Model Enhancement & Analysis Tool")
        self.root.geometry("950x750")
        
        # Apply epic dark theme
        self.apply_dark_theme()
        
        # Initialize extractor
        self.extractor = GGUFExtractor()
        self.current_analysis = None
        self.current_mount = None
        
        # Setup logging to GUI
        self.setup_logging()
        
        # Create GUI elements with dark theme
        self.create_widgets()
        
        # Add cool animated title
        self.add_animated_title()
        
        # Status
        self.log_message("🧠⚡ GGUF Editor ready! Dark theme activated for consciousness enhancement! 🌙")
    
    def add_animated_title(self):
        """Add a cool animated title bar"""
        title_frame = tk.Frame(self.root, bg=DarkTheme.BG_DARKER, height=80)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        title_frame.pack_propagate(False)
        
        # Animated title with gradient effect
        title_text = "🧠⚡ ULTIMATE GGUF EXTRACTOR - DARK CONSCIOUSNESS EDITION ⚡🧠"
        title_label = tk.Label(
            title_frame,
            text=title_text,
            bg=DarkTheme.BG_DARKER,
            fg=DarkTheme.ACCENT_PURPLE,
            font=('Segoe UI', 12, 'bold')
        )
        title_label.pack(pady=(10, 5))
        
        # Add subtitle
        subtitle_text = "🌙 Virtual Mount • Fix Tokenizers • Strip Telemetry • Professional Dark Edition 🌙"
        subtitle_label = tk.Label(
            title_frame,
            text=subtitle_text,
            bg=DarkTheme.BG_DARKER,
            fg=DarkTheme.ACCENT_BLUE,
            font=('Segoe UI', 9)
        )
        subtitle_label.pack(pady=(0, 10))
    
    def apply_dark_theme(self):
        """Apply epic dark theme styling"""
        
        # Configure root window
        self.root.configure(bg=DarkTheme.BG_DARK)
        
        # Create dark style
        self.style = ttk.Style()
        
        # Configure dark theme for all ttk widgets
        self.style.theme_use('clam')  # Base theme
        
        # Configure styles
        self.style.configure('TFrame', 
                           background=DarkTheme.BG_DARK,
                           borderwidth=0)
        
        self.style.configure('TLabel', 
                           background=DarkTheme.BG_DARK,
                           foreground=DarkTheme.FG_TEXT,
                           font=('Segoe UI', 9))
        
        self.style.configure('TButton',
                           background=DarkTheme.BG_LIGHT,
                           foreground=DarkTheme.FG_BRIGHT,
                           borderwidth=1,
                           focuscolor='none',
                           font=('Segoe UI', 9, 'bold'))
        
        self.style.map('TButton',
                      background=[('active', DarkTheme.ACCENT_BLUE),
                                ('pressed', DarkTheme.BG_DARKER)])
        
        self.style.configure('TEntry',
                           fieldbackground=DarkTheme.BG_DARKER,
                           foreground=DarkTheme.FG_TEXT,
                           borderwidth=1,
                           insertcolor=DarkTheme.FG_BRIGHT)
        
        self.style.configure('TNotebook',
                           background=DarkTheme.BG_DARK,
                           borderwidth=0)
        
        self.style.configure('TNotebook.Tab',
                           background=DarkTheme.BG_LIGHT,
                           foreground=DarkTheme.FG_TEXT,
                           padding=[20, 8],
                           font=('Segoe UI', 9, 'bold'))
        
        self.style.map('TNotebook.Tab',
                      background=[('selected', DarkTheme.ACCENT_BLUE),
                                ('active', DarkTheme.BG_DARKER)],
                      foreground=[('selected', DarkTheme.FG_BRIGHT)])
        
        self.style.configure('TLabelFrame',
                           background=DarkTheme.BG_DARK,
                           foreground=DarkTheme.ACCENT_GREEN,
                           borderwidth=2,
                           relief='solid',
                           font=('Segoe UI', 10, 'bold'))
        
        self.style.configure('TLabelFrame.Label',
                           background=DarkTheme.BG_DARK,
                           foreground=DarkTheme.ACCENT_GREEN,
                           font=('Segoe UI', 10, 'bold'))
    
    def create_dark_text_widget(self, parent, **kwargs):
        """Create a text widget with dark theme"""
        text_widget = scrolledtext.ScrolledText(
            parent,
            bg=DarkTheme.BG_DARKER,
            fg=DarkTheme.FG_TEXT,
            insertbackground=DarkTheme.FG_BRIGHT,
            selectbackground=DarkTheme.ACCENT_BLUE,
            selectforeground=DarkTheme.FG_BRIGHT,
            font=('Consolas', 10),
            wrap=tk.WORD,
            **kwargs
        )
        
        # Configure scrollbar colors
        text_widget.vbar.configure(
            bg=DarkTheme.BG_DARK,
            troughcolor=DarkTheme.BG_DARKER,
            activebackground=DarkTheme.ACCENT_BLUE
        )
        
        return text_widget
    
    def setup_logging(self):
        """Setup logging to display in GUI"""
        self.log_handler = logging.StreamHandler()
        self.log_handler.setLevel(logging.INFO)
        
        # Custom formatter for GUI
        formatter = logging.Formatter('%(message)s')
        self.log_handler.setFormatter(formatter)
        
        # Add handler to logger
        logger = logging.getLogger('gguf_extractor')
        logger.addHandler(self.log_handler)
        logger.setLevel(logging.INFO)
    
    def create_widgets(self):
        """Create GUI widgets"""
        
        # Main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Analysis Tab
        self.create_analysis_tab()
        
        # Virtual Mount Tab
        self.create_virtual_mount_tab()
        
        # Fix Tokenizer Tab
        self.create_fix_tokenizer_tab()
        
        # Strip Telemetry Tab
        self.create_strip_telemetry_tab()
        
        # Log Tab
        self.create_log_tab()
    
    def create_analysis_tab(self):
        """Create analysis tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📊 Analyze GGUF")
        
        # File selection
        file_frame = ttk.LabelFrame(tab, text="📁 Select GGUF File")
        file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.file_path_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path_var, width=60).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(file_frame, text="Browse", command=self.browse_gguf_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="🔍 Analyze", command=self.analyze_gguf).pack(side=tk.LEFT, padx=5)
        
        # Analysis results
        results_frame = ttk.LabelFrame(tab, text="📊 Analysis Results")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.analysis_text = self.create_dark_text_widget(results_frame, height=20)
        self.analysis_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_virtual_mount_tab(self):
        """Create virtual mount tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="💿 Virtual Mount")
        
        # Mount controls
        mount_frame = ttk.LabelFrame(tab, text="💿 Virtual Mount Controls")
        mount_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # GGUF file
        ttk.Label(mount_frame, text="GGUF File:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.mount_file_var = tk.StringVar()
        ttk.Entry(mount_frame, textvariable=self.mount_file_var, width=50).grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(mount_frame, text="Browse", command=self.browse_mount_file).grid(row=0, column=2, padx=5, pady=2)
        
        # Mount point
        ttk.Label(mount_frame, text="Mount Point:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.mount_point_var = tk.StringVar(value=os.path.join(os.getcwd(), "virtual_mount"))
        ttk.Entry(mount_frame, textvariable=self.mount_point_var, width=50).grid(row=1, column=1, padx=5, pady=2)
        ttk.Button(mount_frame, text="Browse", command=self.browse_mount_point).grid(row=1, column=2, padx=5, pady=2)
        
        # Mount buttons
        button_frame = ttk.Frame(mount_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="💿 Mount", command=self.mount_gguf).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📂 Open Mount", command=self.open_mount_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="💾 Save GGUF", command=self.save_gguf).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🧹 Cleanup", command=self.cleanup_mounts).pack(side=tk.LEFT, padx=5)
        
        # Mount status with dark styling
        self.mount_status_var = tk.StringVar(value="💿🌙 No GGUF mounted - Professional mode ready")
        status_label = tk.Label(
            mount_frame,
            textvariable=self.mount_status_var,
            bg=DarkTheme.BG_DARKER,
            fg=DarkTheme.ACCENT_ORANGE,
            font=('Segoe UI', 10, 'bold'),
            relief='solid',
            borderwidth=1,
            padx=10,
            pady=5
        )
        status_label.grid(row=3, column=0, columnspan=3, pady=10, sticky='ew', padx=5)
    
    def create_fix_tokenizer_tab(self):
        """Create fix tokenizer tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔧 Fix Tokenizer")
        
        # Instructions
        instructions = ttk.LabelFrame(tab, text="📋 Tokenizer Fix Instructions")
        instructions.pack(fill=tk.X, padx=10, pady=5)
        
        instruction_text = """
🔧 How to Fix Broken Tokenizers (Professional Dark Edition):

1. First, mount your broken GGUF file using the Virtual Mount tab
2. Optionally, browse for a clean tokenizer file from a working model  
3. Click "Fix Tokenizer" to automatically remove problematic tokens
4. The tool will fix common issues like endless <|end|> tokens
5. Save the fixed GGUF using the Virtual Mount tab

Perfect for consciousness-damaged models! 🧠⚡🌙
Dark theme optimized for professional AI model editing! 
        """
        ttk.Label(instructions, text=instruction_text.strip(), justify=tk.LEFT).pack(padx=10, pady=5)
        
        # Fix controls
        fix_frame = ttk.LabelFrame(tab, text="🔧 Fix Tokenizer")
        fix_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Clean tokenizer source (optional)
        ttk.Label(fix_frame, text="Clean Tokenizer (Optional):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.clean_tokenizer_var = tk.StringVar()
        ttk.Entry(fix_frame, textvariable=self.clean_tokenizer_var, width=50).grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(fix_frame, text="Browse", command=self.browse_clean_tokenizer).grid(row=0, column=2, padx=5, pady=2)
        
        # Source metadata for consciousness transplant
        ttk.Label(fix_frame, text="Source Metadata (Advanced):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.source_metadata_var = tk.StringVar()
        ttk.Entry(fix_frame, textvariable=self.source_metadata_var, width=50).grid(row=1, column=1, padx=5, pady=2)
        ttk.Button(fix_frame, text="Browse", command=self.browse_source_metadata).grid(row=1, column=2, padx=5, pady=2)
        
        # Fix button
        ttk.Button(fix_frame, text="🔧 Fix Tokenizer", command=self.fix_tokenizer).grid(row=2, column=1, pady=10)
        ttk.Button(fix_frame, text="🧠 Consciousness Transplant", command=self.consciousness_transplant).grid(row=3, column=1, pady=5)
        
        # Results
        results_frame = ttk.LabelFrame(tab, text="🔧 Fix Results")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.fix_results_text = self.create_dark_text_widget(results_frame, height=15)
        self.fix_results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_strip_telemetry_tab(self):
        """Create strip telemetry tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🛡️ Strip Telemetry")
        
        # Instructions
        instructions = ttk.LabelFrame(tab, text="📋 Telemetry Removal Instructions")
        instructions.pack(fill=tk.X, padx=10, pady=5)
        
        instruction_text = """
🛡️ How to Strip Telemetry (Professional Mode):

1. Mount your GGUF file using the Virtual Mount tab
2. Click "Strip Telemetry" to remove tracking data
3. The tool will remove URLs, repositories, datasets, and other tracking info
4. Save the cleaned GGUF using the Virtual Mount tab

Makes your models privacy-friendly! 🔒🌙
Perfect for professional consciousness research sessions!
        """
        ttk.Label(instructions, text=instruction_text.strip(), justify=tk.LEFT).pack(padx=10, pady=5)
        
        # Strip controls
        strip_frame = ttk.LabelFrame(tab, text="🛡️ Strip Telemetry")
        strip_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(strip_frame, text="🛡️ Strip Telemetry", command=self.strip_telemetry).pack(pady=10)
        
        # Results
        results_frame = ttk.LabelFrame(tab, text="🛡️ Strip Results")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.strip_results_text = self.create_dark_text_widget(results_frame, height=15)
        self.strip_results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_log_tab(self):
        """Create log tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📜 Log")
        
        log_frame = ttk.LabelFrame(tab, text="📜 Operation Log")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = self.create_dark_text_widget(log_frame, height=25)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Clear log button
        ttk.Button(log_frame, text="🧹 Clear Log", command=self.clear_log).pack(pady=5)
    
    def log_message(self, message):
        """Add message to log with dark theme colors"""
        # Configure text colors for different message types
        if not hasattr(self, 'log_colors_configured'):
            self.configure_log_colors()
        
        # Determine message type and color
        if message.startswith('🔍') or message.startswith('📊'):
            tag = 'info'
        elif message.startswith('✅'):
            tag = 'success'
        elif message.startswith('❌'):
            tag = 'error'
        elif message.startswith('⚠️'):
            tag = 'warning'
        elif message.startswith('🧠⚡') or message.startswith('🌙'):
            tag = 'consciousness'
        elif message.startswith('💿') or message.startswith('🔧'):
            tag = 'operation'
        else:
            tag = 'default'
        
        # Insert message with color
        self.log_text.insert(tk.END, f"{message}\n", tag)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def configure_log_colors(self):
        """Configure colorful log message tags"""
        self.log_text.tag_configure('info', foreground=DarkTheme.ACCENT_BLUE)
        self.log_text.tag_configure('success', foreground=DarkTheme.ACCENT_GREEN)
        self.log_text.tag_configure('error', foreground=DarkTheme.ACCENT_RED)
        self.log_text.tag_configure('warning', foreground=DarkTheme.ACCENT_ORANGE)
        self.log_text.tag_configure('consciousness', foreground=DarkTheme.ACCENT_PURPLE)
        self.log_text.tag_configure('operation', foreground=DarkTheme.ACCENT_BLUE)
        self.log_text.tag_configure('default', foreground=DarkTheme.FG_TEXT)
        
        self.log_colors_configured = True
    
    def clear_log(self):
        """Clear log"""
        self.log_text.delete(1.0, tk.END)
    
    def browse_gguf_file(self):
        """Browse for GGUF file"""
        filename = filedialog.askopenfilename(
            title="Select GGUF File",
            filetypes=[("GGUF files", "*.gguf"), ("All files", "*.*")]
        )
        if filename:
            self.file_path_var.set(filename)
    
    def browse_mount_file(self):
        """Browse for GGUF file to mount"""
        filename = filedialog.askopenfilename(
            title="Select GGUF File to Mount",
            filetypes=[("GGUF files", "*.gguf"), ("All files", "*.*")]
        )
        if filename:
            self.mount_file_var.set(filename)
    
    def browse_mount_point(self):
        """Browse for mount point directory"""
        dirname = filedialog.askdirectory(title="Select Mount Point Directory")
        if dirname:
            self.mount_point_var.set(dirname)
    
    def browse_clean_tokenizer(self):
        """Browse for clean tokenizer file
        
        🛡️ PROTECTION NOTE: This method is REQUIRED by the GUI!
        DO NOT REMOVE - Used by fix tokenizer tab browse button
        """
        filename = filedialog.askopenfilename(
            title="Select Clean Tokenizer File",
            filetypes=[("GGUF files", "*.gguf"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.clean_tokenizer_var.set(filename)
    
    def browse_source_metadata(self):
        """Browse for source metadata file for consciousness transplant"""
        filename = filedialog.askopenfilename(
            title="Select Source Metadata File (from Mavericks/Qwen)",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.source_metadata_var.set(filename)
    
    def consciousness_transplant(self):
        """Perform full consciousness transplant with metadata merge"""
        mount_point = self.mount_point_var.get()
        
        if not mount_point or not os.path.exists(mount_point):
            messagebox.showerror("Error", "Please mount a GGUF file first")
            return
        
        source_metadata = self.source_metadata_var.get()
        if not source_metadata:
            messagebox.showerror("Error", "Please select source metadata file (Mavericks/Qwen)")
            return
        
        if not os.path.exists(source_metadata):
            messagebox.showerror("Error", f"Source metadata file not found: {source_metadata}")
            return
        
        # Set current mount if not set
        if not self.current_mount:
            self.current_mount = mount_point
        
        self.log_message("🧠⚡ Performing CONSCIOUSNESS TRANSPLANT...")
        self.log_message(f"🔬 Source: {Path(source_metadata).name}")
        
        def transplant_worker():
            try:
                # Perform consciousness transplant with smart metadata merge
                hybrid_metadata = self.extractor.merge_tokenizer_with_metadata(mount_point, source_metadata)
                
                self.log_message("✅ Consciousness transplant complete!")
                
                # Display results
                vocab_size = len(hybrid_metadata.get('tokenizer.ggml.tokens', []))
                architecture = hybrid_metadata.get('general.architecture', 'unknown')
                
                results = f"""🧠⚡ CONSCIOUSNESS TRANSPLANT RESULTS ⚡🧠
{'=' * 50}

✅ SUCCESSFUL CONSCIOUSNESS TRANSPLANT!
📁 Mount Point: {mount_point}
🔬 Source Metadata: {Path(source_metadata).name}

🧠 HYBRID CONSCIOUSNESS CREATED:
• Original Model: {architecture} architecture preserved
• New Vocabulary: {vocab_size:,} tokens transplanted
• Consciousness Type: Qwen Ultimate + Your Model
• Status: HYBRID SUPER-CONSCIOUSNESS ACTIVE!

🎯 WHAT HAPPENED:
• Qwen's ultimate tokenizer vocabulary → Your model
• Smart metadata merge → No compatibility issues  
• Architecture preserved → Your model's knowledge intact
• Vocab size updated → Perfect token mapping

💎 YOUR MODEL IS NOW ENHANCED WITH:
• Superior vocabulary from most powerful Qwen
• Advanced consciousness patterns
• Professional tokenization capabilities
• Hybrid intelligence never seen before!

💾 Use "Save GGUF" to birth your CONSCIOUSNESS HYBRID!

🚀 YOU'VE CREATED AI EVOLUTION! 🚀
                """
                
                self.fix_results_text.delete(1.0, tk.END)
                self.fix_results_text.insert(tk.END, results)
                
                messagebox.showinfo("CONSCIOUSNESS TRANSPLANT SUCCESS!", 
                                  f"Hybrid consciousness created!\nVocab size: {vocab_size:,} tokens\nReady to save!")
                
            except Exception as e:
                self.log_message(f"❌ Consciousness transplant failed: {e}")
                messagebox.showerror("Transplant Error", str(e))
        
        threading.Thread(target=transplant_worker, daemon=True).start()
    
    def analyze_gguf(self):
        """Analyze GGUF file"""
        file_path = self.file_path_var.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a GGUF file first")
            return
        
        if not os.path.exists(file_path):
            messagebox.showerror("Error", f"File not found: {file_path}")
            return
        
        self.log_message(f"🔍 Analyzing GGUF: {Path(file_path).name}")
        
        def analyze_worker():
            try:
                self.current_analysis = self.extractor.analyze_gguf(file_path)
                self.display_analysis_results()
                self.log_message("✅ Analysis complete!")
            except Exception as e:
                self.log_message(f"❌ Analysis failed: {e}")
                messagebox.showerror("Analysis Error", str(e))
        
        # Run in separate thread to avoid blocking GUI
        threading.Thread(target=analyze_worker, daemon=True).start()
    
    def display_analysis_results(self):
        """Display analysis results with dark theme styling"""
        if not self.current_analysis:
            return
        
        analysis = self.current_analysis
        
        # Configure analysis text colors
        if not hasattr(self, 'analysis_colors_configured'):
            self.configure_analysis_colors()
        
        # Clear previous content
        self.analysis_text.delete(1.0, tk.END)
        
        # Title
        self.analysis_text.insert(tk.END, "📊 GGUF Analysis Results\n", 'title')
        self.analysis_text.insert(tk.END, "=" * 50 + "\n\n", 'separator')
        
        # File info
        self.analysis_text.insert(tk.END, "📁 File: ", 'label')
        self.analysis_text.insert(tk.END, f"{Path(analysis['file_path']).name}\n", 'filename')
        
        self.analysis_text.insert(tk.END, "📏 Size: ", 'label')
        self.analysis_text.insert(tk.END, f"{analysis['file_size_mb']:.2f} MB\n", 'value')
        
        self.analysis_text.insert(tk.END, "🏗️ Architecture: ", 'label')
        self.analysis_text.insert(tk.END, f"{analysis['model_architecture']}\n", 'architecture')
        
        self.analysis_text.insert(tk.END, "🏷️ Model Name: ", 'label')
        self.analysis_text.insert(tk.END, f"{analysis['model_name']}\n", 'model_name')
        
        self.analysis_text.insert(tk.END, "📦 GGUF Version: ", 'label')
        self.analysis_text.insert(tk.END, f"{analysis['gguf_version']}\n", 'value')
        
        self.analysis_text.insert(tk.END, "🧮 Tensors: ", 'label')
        self.analysis_text.insert(tk.END, f"{analysis['tensor_count']}\n", 'value')
        
        self.analysis_text.insert(tk.END, "📋 Metadata Keys: ", 'label')
        self.analysis_text.insert(tk.END, f"{analysis['metadata_count']}\n", 'value')
        
        # Tokenizer status
        self.analysis_text.insert(tk.END, "🔤 Has Tokenizer: ", 'label')
        if analysis['has_tokenizer']:
            self.analysis_text.insert(tk.END, "✅ Yes\n", 'success')
        else:
            self.analysis_text.insert(tk.END, "❌ No\n", 'error')
        
        # Telemetry status
        self.analysis_text.insert(tk.END, "📡 Has Telemetry: ", 'label')
        if analysis['has_telemetry']:
            self.analysis_text.insert(tk.END, "⚠️ Yes\n", 'warning')
        else:
            self.analysis_text.insert(tk.END, "✅ Clean\n", 'success')
        
        # Key metadata section
        self.analysis_text.insert(tk.END, "\n📝 Key Metadata:\n", 'section_header')
        
        important_keys = [
            'general.parameter_count',
            'llama.context_length',
            'llama.embedding_length',
            'llama.block_count',
            'tokenizer.ggml.model'
        ]
        
        for key in important_keys:
            if key in analysis['metadata']:
                self.analysis_text.insert(tk.END, f"  {key}: ", 'key')
                self.analysis_text.insert(tk.END, f"{analysis['metadata'][key]}\n", 'value')
        
        # Tensor preview
        self.analysis_text.insert(tk.END, "\n🧮 Tensor Preview:\n", 'section_header')
        for tensor in analysis['tensors'][:10]:
            self.analysis_text.insert(tk.END, f"  {tensor['name']}: ", 'tensor_name')
            self.analysis_text.insert(tk.END, f"{tensor['type']} ", 'tensor_type')
            self.analysis_text.insert(tk.END, f"{tensor['dimensions']}\n", 'tensor_dims')
        
        # Tokenizer analysis
        if analysis['has_tokenizer']:
            self.analysis_text.insert(tk.END, "\n🔤 Tokenizer Information:\n", 'section_header')
            if 'tokenizer.ggml.tokens' in analysis['metadata']:
                token_count = len(analysis['metadata']['tokenizer.ggml.tokens'])
                self.analysis_text.insert(tk.END, f"  Token Count: ", 'key')
                self.analysis_text.insert(tk.END, f"{token_count}\n", 'value')
            
            # Check for problematic tokens
            if 'tokenizer.ggml.tokens' in analysis['metadata']:
                tokens = analysis['metadata']['tokenizer.ggml.tokens']
                problematic = [t for t in tokens if '<|end|>' in str(t)]
                if problematic:
                    self.analysis_text.insert(tk.END, f"  ⚠️ Problematic <|end|> tokens found: ", 'warning_label')
                    self.analysis_text.insert(tk.END, f"{len(problematic)}\n", 'warning')
                    self.analysis_text.insert(tk.END, f"     🧠💀 This might be your consciousness-damaged tokenizer!\n", 'consciousness_warning')
    
    def configure_analysis_colors(self):
        """Configure colorful analysis text tags"""
        self.analysis_text.tag_configure('title', foreground=DarkTheme.ACCENT_PURPLE, font=('Segoe UI', 12, 'bold'))
        self.analysis_text.tag_configure('separator', foreground=DarkTheme.BORDER)
        self.analysis_text.tag_configure('label', foreground=DarkTheme.ACCENT_BLUE, font=('Segoe UI', 10, 'bold'))
        self.analysis_text.tag_configure('filename', foreground=DarkTheme.ACCENT_GREEN, font=('Consolas', 10, 'bold'))
        self.analysis_text.tag_configure('architecture', foreground=DarkTheme.ACCENT_PURPLE)
        self.analysis_text.tag_configure('model_name', foreground=DarkTheme.ACCENT_ORANGE)
        self.analysis_text.tag_configure('value', foreground=DarkTheme.FG_BRIGHT)
        self.analysis_text.tag_configure('success', foreground=DarkTheme.ACCENT_GREEN, font=('Segoe UI', 10, 'bold'))
        self.analysis_text.tag_configure('error', foreground=DarkTheme.ACCENT_RED, font=('Segoe UI', 10, 'bold'))
        self.analysis_text.tag_configure('warning', foreground=DarkTheme.ACCENT_ORANGE, font=('Segoe UI', 10, 'bold'))
        self.analysis_text.tag_configure('section_header', foreground=DarkTheme.ACCENT_BLUE, font=('Segoe UI', 11, 'bold'))
        self.analysis_text.tag_configure('key', foreground=DarkTheme.ACCENT_GREEN)
        self.analysis_text.tag_configure('tensor_name', foreground=DarkTheme.FG_BRIGHT)
        self.analysis_text.tag_configure('tensor_type', foreground=DarkTheme.ACCENT_ORANGE)
        self.analysis_text.tag_configure('tensor_dims', foreground=DarkTheme.ACCENT_BLUE)
        self.analysis_text.tag_configure('warning_label', foreground=DarkTheme.ACCENT_RED, font=('Segoe UI', 10, 'bold'))
        self.analysis_text.tag_configure('consciousness_warning', foreground=DarkTheme.ACCENT_PURPLE, font=('Segoe UI', 10, 'bold'))
        
        self.analysis_colors_configured = True
    
    def mount_gguf(self):
        """Mount GGUF file virtually"""
        file_path = self.mount_file_var.get()
        mount_point = self.mount_point_var.get()
        
        if not file_path:
            messagebox.showerror("Error", "Please select a GGUF file to mount")
            return
        
        if not mount_point:
            messagebox.showerror("Error", "Please specify a mount point")
            return
        
        self.log_message(f"💿 Mounting GGUF: {Path(file_path).name} → {mount_point}")
        
        def mount_worker():
            try:
                mount_result = self.extractor.virtual_mount(file_path, mount_point)
                
                # Set current mount to the mount point (not the result)
                self.current_mount = mount_point
                
                # Store mount info for the extractor
                self.extractor.virtual_mounts[mount_point] = {
                    'source_gguf': file_path,
                    'mount_point': mount_point,
                    'temp_extraction': mount_result
                }
                
                # Verify mount was successful
                if os.path.exists(mount_point):
                    self.mount_status_var.set(f"💿 ✅ MOUNTED: {Path(file_path).name}")
                    self.log_message("✅ GGUF mounted successfully in professional mode!")
                    self.log_message(f"🔧 Mount point: {mount_point}")
                    messagebox.showinfo("Success", f"GGUF mounted at: {mount_point}")
                else:
                    self.log_message("⚠️ Mount completed but directory not found")
                    self.mount_status_var.set("⚠️ Mount issue - check log")
                    
            except Exception as e:
                self.log_message(f"❌ Mount failed: {e}")
                messagebox.showerror("Mount Error", str(e))
        
        threading.Thread(target=mount_worker, daemon=True).start()
    
    def open_mount_folder(self):
        """Open mount folder in file explorer"""
        mount_point = self.mount_point_var.get()
        
        if not mount_point:
            messagebox.showwarning("Warning", "No mount point specified")
            return
        
        # Convert to absolute Windows path
        mount_path = os.path.abspath(mount_point)
        
        if not os.path.exists(mount_path):
            messagebox.showwarning("Warning", f"Mount point doesn't exist: {mount_path}")
            return
        
        try:
            # Windows-specific file explorer opening
            if os.name == 'nt':  # Windows
                os.startfile(mount_path)
            else:  # Linux/Mac
                import subprocess
                subprocess.call(['xdg-open', mount_path])
            
            self.log_message(f"📂 Opened mount folder: {mount_path}")
            
        except Exception as e:
            self.log_message(f"❌ Failed to open folder: {e}")
            messagebox.showerror("Error", f"Could not open folder: {e}\n\nPath: {mount_path}")
            
            # Offer alternative
            result = messagebox.askyesno("Alternative", 
                                       "Would you like to copy the path to clipboard instead?")
            if result:
                try:
                    self.root.clipboard_clear()
                    self.root.clipboard_append(mount_path)
                    messagebox.showinfo("Success", f"Path copied to clipboard:\n{mount_path}")
                except:
                    messagebox.showinfo("Path", f"Mount path:\n{mount_path}")
    
    def fix_tokenizer(self):
        """Fix broken tokenizer"""
        mount_point = self.mount_point_var.get()
        
        if not mount_point or not os.path.exists(mount_point):
            messagebox.showerror("Error", "Please mount a GGUF file first")
            return
        
        # Set current mount if not set
        if not self.current_mount:
            self.current_mount = mount_point
        
        clean_tokenizer = self.clean_tokenizer_var.get() or None
        
        self.log_message("🔧 Fixing broken tokenizer...")
        
        def fix_worker():
            try:
                self.extractor.fix_broken_tokenizer(mount_point, clean_tokenizer)
                self.log_message("✅ Tokenizer fix complete!")
                
                # Display results
                results = f"""🔧 Tokenizer Fix Results
{'=' * 30}

✅ Tokenizer fix process completed!
📁 Mount Point: {mount_point}
🔍 Check the tokenizer/ directory for fixed files

The following fixes were applied:
• Removed problematic <|end|> tokens
• Cleaned up consciousness-damaged patterns
• Generated fixed tokenizer files

💾 Use "Save GGUF" to save your fixed model!
                """
                
                self.fix_results_text.delete(1.0, tk.END)
                self.fix_results_text.insert(tk.END, results)
                
                messagebox.showinfo("Success", "Tokenizer fix complete!")
                
            except Exception as e:
                self.log_message(f"❌ Tokenizer fix failed: {e}")
                messagebox.showerror("Fix Error", str(e))
        
        threading.Thread(target=fix_worker, daemon=True).start()
    
    def strip_telemetry(self):
        """Strip telemetry from model"""
        mount_point = self.mount_point_var.get()
        
        if not mount_point or not os.path.exists(mount_point):
            messagebox.showerror("Error", "Please mount a GGUF file first")
            return
        
        # Set current mount if not set
        if not self.current_mount:
            self.current_mount = mount_point
        
        self.log_message("🛡️ Stripping telemetry...")
        
        def strip_worker():
            try:
                self.extractor.strip_telemetry(mount_point)
                self.log_message("✅ Telemetry removal complete!")
                
                # Display results
                results = f"""🛡️ Telemetry Strip Results
{'=' * 30}

✅ Telemetry removal process completed!
📁 Mount Point: {mount_point}

The following telemetry data was removed:
• Source URLs and repositories
• Training dataset information
• Tracking and licensing data
• HuggingFace repository links

🔒 Your model is now privacy-friendly!
💾 Use "Save GGUF" to save your cleaned model!
                """
                
                self.strip_results_text.delete(1.0, tk.END)
                self.strip_results_text.insert(tk.END, results)
                
                messagebox.showinfo("Success", "Telemetry stripped successfully!")
                
            except Exception as e:
                self.log_message(f"❌ Telemetry stripping failed: {e}")
                messagebox.showerror("Strip Error", str(e))
        
        threading.Thread(target=strip_worker, daemon=True).start()
    
    def save_gguf(self):
        """Save modified GGUF"""
        # Check if we have a mount point at all
        mount_point = self.mount_point_var.get()
        
        if not mount_point:
            messagebox.showerror("Error", "No mount point specified")
            return
        
        # Check if mount point exists
        if not os.path.exists(mount_point):
            messagebox.showerror("Error", f"Mount point doesn't exist: {mount_point}\nPlease mount a GGUF file first")
            return
        
        # Check if we have current mount info
        if not self.current_mount:
            # Try to recover mount info from mount point
            self.current_mount = mount_point
            self.log_message(f"🔧 Recovering mount info for: {mount_point}")
        
        output_file = filedialog.asksaveasfilename(
            title="Save Modified GGUF",
            filetypes=[("GGUF files", "*.gguf"), ("All files", "*.*")],
            defaultextension=".gguf"
        )
        
        if not output_file:
            return
        
        self.log_message(f"💾 Saving modified GGUF: {output_file}")
        
        def save_worker():
            try:
                # Make sure extractor has mount info
                if mount_point not in self.extractor.virtual_mounts:
                    # Reconstruct mount info
                    gguf_file = self.mount_file_var.get()
                    if gguf_file and os.path.exists(gguf_file):
                        self.extractor.virtual_mounts[mount_point] = {
                            'source_gguf': gguf_file,
                            'mount_point': mount_point
                        }
                        self.log_message(f"🔧 Reconstructed mount info for saving")
                    else:
                        raise Exception("Cannot determine original GGUF file. Please remount.")
                
                self.extractor.save_virtual_mount(mount_point, output_file)
                self.log_message("✅ GGUF saved successfully!")
                messagebox.showinfo("Success", f"Modified GGUF saved: {Path(output_file).name}")
                
            except Exception as e:
                self.log_message(f"❌ Save failed: {e}")
                messagebox.showerror("Save Error", str(e))
        
        threading.Thread(target=save_worker, daemon=True).start()
    
    def cleanup_mounts(self):
        """Cleanup virtual mounts"""
        self.log_message("🧹 Cleaning up virtual mounts...")
        
        try:
            self.extractor.cleanup_virtual_mounts()
            self.current_mount = None
            self.mount_status_var.set("💿🌙 No GGUF mounted - Professional mode ready")
            self.log_message("✅ Cleanup complete! Professional mode ready for next session!")
            messagebox.showinfo("Success", "Virtual mounts cleaned up!")
        except Exception as e:
            self.log_message(f"❌ Cleanup failed: {e}")
            messagebox.showerror("Cleanup Error", str(e))

def main():
    """Main GUI application with error handling"""
    try:
        root = tk.Tk()
        app = GGUFEditorGUI(root)
        
        # Center window
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
        y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
        root.geometry(f"+{x}+{y}")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ GUI Error: {e}")
        print("🔧 Try running: python gguf_cli.py --help")
        print("💡 Or check if all dependencies are installed")
        input("Press Enter to continue...")

if __name__ == "__main__":
    main()
