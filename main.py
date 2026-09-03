"""
Main application - GUI for launching local scripts.
"""
import subprocess
import threading
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import messagebox, ttk
from typing import Callable, Dict, Optional

import theme
from config import Config
from script_runner import ScriptRunner


class ScriptLauncherApp:
    """Main GUI application for launching scripts."""

    def __init__(self, root: tk.Tk, config_path: Optional[Path] = None):
        """
        Initialize the application.
        
        Args:
            root: Tkinter root window
            config_path: Path to config.json file
        """
        self.root = root
        self.runner = ScriptRunner()
        self.last_status = {}
        self.logs_widget = None
        
        # Load configuration
        try:
            self.config = Config(config_path)
        except Exception as e:
            messagebox.showerror("Configuration Error", f"Failed to load config: {e}")
            root.destroy()
            return

        # Configure root window
        self.root.title(self.config.app_title)
        self.root.geometry(f"{self.config.window_width}x{self.config.window_height}")
        self.root.minsize(600, 400)
        
        # Apply theme
        theme.apply_theme(self.root)

        # Set icon if provided
        if self.config.app_icon and self.config.app_icon.exists():
            try:
                self.root.iconbitmap(str(self.config.app_icon))
            except Exception:
                pass

        # Build UI
        self._build_ui()
        self._load_scripts()

    def _build_ui(self):
        """Build the user interface."""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Header
        self._build_header(main_frame)

        # Separator
        ttk.Separator(main_frame, orient="horizontal").pack(
            fill="x", padx=0, pady=10
        )

        # Content area: scripts on left, logs on right
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Left side: Scripts area (scrollable)
        self._build_scripts_area(content_frame)

        # Right side: Logs area
        self._build_logs_area(content_frame)

        # Status bar
        self._build_status_bar(main_frame)

    def _build_header(self, parent: ttk.Frame):
        """Build the header section."""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill="x", padx=20, pady=(15, 5))

        title_label = ttk.Label(
            header_frame,
            text=self.config.app_title,
            style="Title.TLabel"
        )
        title_label.pack(anchor="w")

        desc_label = ttk.Label(
            header_frame,
            text="Click any button below to launch a script",
            style="Dim.TLabel"
        )
        desc_label.pack(anchor="w")

    def _build_scripts_area(self, parent: ttk.Frame):
        """Build the scrollable scripts area on the left."""
        # Container for scripts
        scripts_container = ttk.Frame(parent)
        scripts_container.pack(side="left", fill="both", expand=True, padx=20, pady=10)

        # Canvas with scrollbar for scrolling
        canvas = tk.Canvas(
            scripts_container,
            bg=theme.BG,
            highlightthickness=0,
            relief="flat"
        )
        scrollbar = ttk.Scrollbar(scripts_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.scripts_frame = scrollable_frame

    def _build_logs_area(self, parent: ttk.Frame):
        """Build the logs/output textarea on the right."""
        # Container for logs
        logs_container = ttk.Frame(parent)
        logs_container.pack(side="right", fill="both", expand=True, padx=(0, 20), pady=10)

        # Title
        logs_title = ttk.Label(
            logs_container,
            text="Execution Logs",
            style="Accent.TLabel"
        )
        logs_title.pack(anchor="w", pady=(0, 5))

        # Logs textarea with scrollbar
        logs_frame = ttk.Frame(logs_container)
        logs_frame.pack(fill="both", expand=True)

        self.logs_widget = tk.Text(
            logs_frame,
            bg=theme.BG_INPUT,
            fg=theme.FG,
            font=theme.FONT_MONO,
            relief="flat",
            borderwidth=1,
            wrap="word"
        )
        logs_scrollbar = ttk.Scrollbar(
            logs_frame,
            orient="vertical",
            command=self.logs_widget.yview
        )

        self.logs_widget.config(yscrollcommand=logs_scrollbar.set)
        self.logs_widget.pack(side="left", fill="both", expand=True)
        logs_scrollbar.pack(side="right", fill="y")

        # Clear button
        clear_btn = ttk.Button(
            logs_container,
            text="Clear Logs",
            command=self._clear_logs
        )
        clear_btn.pack(pady=(5, 0))

    def _build_status_bar(self, parent: ttk.Frame):
        """Build the status bar."""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill="x", padx=20, pady=(5, 15))

        ttk.Separator(status_frame, orient="horizontal").pack(fill="x", pady=(0, 10))

        self.status_label = ttk.Label(
            status_frame,
            text="Ready",
            style="Dim.TLabel"
        )
        self.status_label.pack(anchor="w")

    def _load_scripts(self):
        """Load scripts from configuration and create buttons."""
        scripts = self.config.get_scripts()
        script_paths = self.config.get_script_paths()

        if not scripts:
            no_scripts_label = ttk.Label(
                self.scripts_frame,
                text="No scripts configured",
                style="Dim.TLabel"
            )
            no_scripts_label.pack(pady=20)
            return

        for i, script in enumerate(scripts):
            link_name = script["link_name"]
            script_path = script_paths[link_name]
            description = script.get("description", "No description")

            # Check if script can run
            can_run = self.runner.can_run(script_path)

            self._create_script_button(
                link_name,
                script_path,
                description,
                can_run,
                i == 0  # Is first item
            )

    def _create_script_button(
        self,
        link_name: str,
        script_path: Path,
        description: str,
        can_run: bool,
        is_first: bool
    ):
        """
        Create a script button.
        
        Args:
            link_name: Name/label for the button
            script_path: Path to the script
            description: Description of what the script does
            can_run: Whether the script can be run on this system
            is_first: Whether this is the first button
        """
        # Container for button and info
        button_frame = ttk.Frame(self.scripts_frame, style="Card.TFrame")
        button_frame.pack(
            fill="x",
            pady=(0 if is_first else 8, 0),
            padx=0
        )

        # Left side - button
        left_frame = ttk.Frame(button_frame, style="Card.TFrame")
        left_frame.pack(side="left", fill="both", expand=True, padx=12, pady=12)

        # Script name label
        name_label = ttk.Label(
            left_frame,
            text=link_name,
            style="Accent.TLabel"
        )
        name_label.pack(anchor="w")

        # Description label
        desc_label = ttk.Label(
            left_frame,
            text=description,
            style="Dim.TLabel"
        )
        desc_label.pack(anchor="w", pady=(2, 0))

        # Path label
        path_label = ttk.Label(
            left_frame,
            text=f"📁 {script_path.name}",
            style="Mono.TLabel"
        )
        path_label.pack(anchor="w", pady=(6, 0))

        # Right side - button
        right_frame = ttk.Frame(button_frame, style="Card.TFrame")
        right_frame.pack(side="right", padx=12, pady=12)

        if can_run:
            btn_style = "Accent.TButton"
            btn_text = "▶ Launch"
            btn_command = lambda: self._on_script_launch(link_name, script_path)
        else:
            btn_style = "Danger.TButton"
            btn_text = "⊘ Unavailable"
            btn_command = lambda: self._on_script_unavailable(script_path)

        button = ttk.Button(
            right_frame,
            text=btn_text,
            style=btn_style,
            command=btn_command,
            width=15
        )
        button.pack()

    def _on_script_launch(self, link_name: str, script_path: Path):
        """Handle script launch button click."""
        self._update_status(f"Launching: {link_name}...")
        self._append_log(f"\n{'='*60}")
        self._append_log(f"[{self._get_timestamp()}] Starting: {link_name}")
        self._append_log(f"Script: {script_path}")
        self._append_log(f"{'='*60}\n")

        # Run in a thread to keep UI responsive
        def run_script():
            success, message = self.runner.run(script_path)
            self.last_status[link_name] = (success, message)
            
            # Log the result
            status_icon = "✓" if success else "✗"
            status_color = "green" if success else "red"
            
            # Update status in main thread
            self.root.after(
                0,
                lambda: self._on_script_complete(link_name, success, message, status_icon)
            )

        thread = threading.Thread(target=run_script, daemon=True)
        thread.start()

    def _on_script_complete(self, link_name: str, success: bool, message: str, status_icon: str):
        """Handle script completion."""
        self._update_status(message, is_error=not success)
        
        # Log completion
        self._append_log(f"[{self._get_timestamp()}] {status_icon} {message}")
        
        if success:
            print(f"✓ {message}")
        else:
            print(f"✗ {message}")
            messagebox.showerror(link_name, message)

    def _on_script_unavailable(self, script_path: Path):
        """Handle click on unavailable script."""
        supported = self.runner.get_supported_extensions()
        suffix = script_path.suffix.lower()
        
        message = f"Cannot run {script_path.name}\n\n"
        message += f"File type: {suffix if suffix else '(no extension)'}\n"
        message += "Supported file types on this system:\n"
        
        for ext, available in supported.items():
            status = "✓ Available" if available else "✗ Not available"
            message += f"  {ext}: {status}\n"

        messagebox.showwarning("Script Unavailable", message)

    def _append_log(self, message: str):
        """Append message to the logs textarea."""
        if self.logs_widget:
            self.logs_widget.config(state="normal")
            self.logs_widget.insert("end", message + "\n")
            self.logs_widget.see("end")  # Auto-scroll to bottom
            self.logs_widget.config(state="normal")
            self.root.update_idletasks()

    def _clear_logs(self):
        """Clear the logs textarea."""
        if self.logs_widget:
            self.logs_widget.config(state="normal")
            self.logs_widget.delete("1.0", "end")
            self.logs_widget.config(state="normal")

    @staticmethod
    def _get_timestamp() -> str:
        """Get current timestamp string."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _update_status(self, message: str, is_error: bool = False):
        """Update the status bar."""
        style = "Danger.TLabel" if is_error else "Success.TLabel"
        self.status_label.configure(text=message, style=style)


def main():
    """Main entry point."""
    root = tk.Tk()
    app = ScriptLauncherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
