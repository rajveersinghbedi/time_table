import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime

class DataCollectionTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Academic Data Collection Tool")
        self.root.geometry("800x600")
        
        # Data storage
        self.data = {
            "streams": [],
            "semesters": [],
            "majors": [],
            "minors": [],
            "subjects": {},  # {major_name: [subjects]}
            "teachers": {},  # {subject_name: [teachers]}
            "connections": []  # [(major, minor), ...]
        }
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_stream_semester_tab()
        self.create_major_minor_tab()
        self.create_subject_teacher_tab()
        self.create_connection_tab()
        
        # Menu bar
        self.create_menu()
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Data", command=self.save_data)
        file_menu.add_command(label="Load Data", command=self.load_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
    
    def create_stream_semester_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Streams & Semesters")
        
        # Stream section
        stream_frame = ttk.LabelFrame(tab, text="Streams")
        stream_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(stream_frame, text="Stream Name:").grid(row=0, column=0, padx=5, pady=5)
        self.stream_entry = ttk.Entry(stream_frame)
        self.stream_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.add_stream_btn = ttk.Button(stream_frame, text="Add Stream", command=self.add_stream)
        self.add_stream_btn.grid(row=0, column=2, padx=5, pady=5)
        
        self.streams_listbox = tk.Listbox(stream_frame, height=5)
        self.streams_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        stream_frame.grid_columnconfigure(1, weight=1)
        
        # Semester section
        semester_frame = ttk.LabelFrame(tab, text="Semesters")
        semester_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(semester_frame, text="Semester Name:").grid(row=0, column=0, padx=5, pady=5)
        self.semester_entry = ttk.Entry(semester_frame)
        self.semester_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.add_semester_btn = ttk.Button(semester_frame, text="Add Semester", command=self.add_semester)
        self.add_semester_btn.grid(row=0, column=2, padx=5, pady=5)
        
        self.semesters_listbox = tk.Listbox(semester_frame, height=5)
        self.semesters_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        semester_frame.grid_columnconfigure(1, weight=1)
    
    def create_major_minor_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Majors & Minors")
        
        # Major section
        major_frame = ttk.LabelFrame(tab, text="Majors")
        major_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(major_frame, text="Major Name:").grid(row=0, column=0, padx=5, pady=5)
        self.major_entry = ttk.Entry(major_frame)
        self.major_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.add_major_btn = ttk.Button(major_frame, text="Add Major", command=self.add_major)
        self.add_major_btn.grid(row=0, column=2, padx=5, pady=5)
        
        self.majors_listbox = tk.Listbox(major_frame, height=5)
        self.majors_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        major_frame.grid_columnconfigure(1, weight=1)
        
        # Minor section
        minor_frame = ttk.LabelFrame(tab, text="Minors")
        minor_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(minor_frame, text="Minor Name:").grid(row=0, column=0, padx=5, pady=5)
        self.minor_entry = ttk.Entry(minor_frame)
        self.minor_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.add_minor_btn = ttk.Button(minor_frame, text="Add Minor", command=self.add_minor)
        self.add_minor_btn.grid(row=0, column=2, padx=5, pady=5)
        
        self.minors_listbox = tk.Listbox(minor_frame, height=5)
        self.minors_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        minor_frame.grid_columnconfigure(1, weight=1)
        
        # Add default "Core" major
        if "Core" not in self.data["majors"]:
            self.data["majors"].append("Core")
            self.majors_listbox.insert(tk.END, "Core")
    
    def create_subject_teacher_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Subjects & Teachers")
        
        # Subject section
        subject_frame = ttk.LabelFrame(tab, text="Subjects")
        subject_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Major selection for subjects
        ttk.Label(subject_frame, text="Select Major/Minor:").grid(row=0, column=0, padx=5, pady=5)
        self.major_subject_var = tk.StringVar()
        self.major_subject_combo = ttk.Combobox(subject_frame, textvariable=self.major_subject_var)
        self.major_subject_combo.grid(row=0, column=1, padx=5, pady=5)
        self.major_subject_combo.bind("<<ComboboxSelected>>", self.update_subject_list)
        
        ttk.Label(subject_frame, text="Subject Name:").grid(row=1, column=0, padx=5, pady=5)
        self.subject_entry = ttk.Entry(subject_frame)
        self.subject_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.add_subject_btn = ttk.Button(subject_frame, text="Add Subject", command=self.add_subject)
        self.add_subject_btn.grid(row=1, column=2, padx=5, pady=5)
        
        self.subjects_listbox = tk.Listbox(subject_frame, height=5)
        self.subjects_listbox.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        subject_frame.grid_columnconfigure(1, weight=1)
        
        # Teacher section
        teacher_frame = ttk.LabelFrame(tab, text="Teachers")
        teacher_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Subject selection for teachers
        ttk.Label(teacher_frame, text="Select Subject:").grid(row=0, column=0, padx=5, pady=5)
        self.subject_teacher_var = tk.StringVar()
        self.subject_teacher_combo = ttk.Combobox(teacher_frame, textvariable=self.subject_teacher_var)
        self.subject_teacher_combo.grid(row=0, column=1, padx=5, pady=5)
        self.subject_teacher_combo.bind("<<ComboboxSelected>>", self.update_teacher_list)
        
        ttk.Label(teacher_frame, text="Teacher Name:").grid(row=1, column=0, padx=5, pady=5)
        self.teacher_entry = ttk.Entry(teacher_frame)
        self.teacher_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.add_teacher_btn = ttk.Button(teacher_frame, text="Add Teacher", command=self.add_teacher)
        self.add_teacher_btn.grid(row=1, column=2, padx=5, pady=5)
        
        self.teachers_listbox = tk.Listbox(teacher_frame, height=5)
        self.teachers_listbox.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        teacher_frame.grid_columnconfigure(1, weight=1)
    
    def create_connection_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Connections")
        
        # Connection section
        connection_frame = ttk.LabelFrame(tab, text="Major-Minor Connections")
        connection_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Major selection
        ttk.Label(connection_frame, text="Select Major:").grid(row=0, column=0, padx=5, pady=5)
        self.connection_major_var = tk.StringVar()
        self.connection_major_combo = ttk.Combobox(connection_frame, textvariable=self.connection_major_var)
        self.connection_major_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Minor selection
        ttk.Label(connection_frame, text="Select Minor:").grid(row=1, column=0, padx=5, pady=5)
        self.connection_minor_var = tk.StringVar()
        self.connection_minor_combo = ttk.Combobox(connection_frame, textvariable=self.connection_minor_var)
        self.connection_minor_combo.grid(row=1, column=1, padx=5, pady=5)
        
        self.add_connection_btn = ttk.Button(connection_frame, text="Add Connection", command=self.add_connection)
        self.add_connection_btn.grid(row=2, column=0, columnspan=2, pady=5)
        
        # List of connections
        self.connections_listbox = tk.Listbox(connection_frame, height=10)
        self.connections_listbox.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        connection_frame.grid_rowconfigure(3, weight=1)
        connection_frame.grid_columnconfigure(1, weight=1)
    
    # Stream and Semester methods
    def add_stream(self):
        stream_name = self.stream_entry.get().strip()
        if stream_name and stream_name not in self.data["streams"]:
            self.data["streams"].append(stream_name)
            self.streams_listbox.insert(tk.END, stream_name)
            self.stream_entry.delete(0, tk.END)
            self.update_comboboxes()
        else:
            messagebox.showwarning("Warning", "Stream already exists or is empty!")
    
    def add_semester(self):
        semester_name = self.semester_entry.get().strip()
        if semester_name and semester_name not in self.data["semesters"]:
            self.data["semesters"].append(semester_name)
            self.semesters_listbox.insert(tk.END, semester_name)
            self.semester_entry.delete(0, tk.END)
            self.update_comboboxes()
        else:
            messagebox.showwarning("Warning", "Semester already exists or is empty!")
    
    # Major and Minor methods
    def add_major(self):
        major_name = self.major_entry.get().strip()
        if major_name and major_name not in self.data["majors"]:
            self.data["majors"].append(major_name)
            self.majors_listbox.insert(tk.END, major_name)
            self.major_entry.delete(0, tk.END)
            self.update_comboboxes()
        else:
            messagebox.showwarning("Warning", "Major already exists or is empty!")
    
    def add_minor(self):
        minor_name = self.minor_entry.get().strip()
        if minor_name and minor_name not in self.data["minors"]:
            self.data["minors"].append(minor_name)
            self.minors_listbox.insert(tk.END, minor_name)
            self.minor_entry.delete(0, tk.END)
            self.update_comboboxes()
        else:
            messagebox.showwarning("Warning", "Minor already exists or is empty!")
    
    # Subject and Teacher methods
    def add_subject(self):
        major = self.major_subject_var.get()
        subject_name = self.subject_entry.get().strip()
        
        if not major:
            messagebox.showwarning("Warning", "Please select a major/minor!")
            return
        
        if not subject_name:
            messagebox.showwarning("Warning", "Subject name cannot be empty!")
            return
        
        if major not in self.data["subjects"]:
            self.data["subjects"][major] = []
        
        if subject_name not in self.data["subjects"][major]:
            self.data["subjects"][major].append(subject_name)
            self.subjects_listbox.insert(tk.END, subject_name)
            self.subject_entry.delete(0, tk.END)
            self.update_comboboxes()
        else:
            messagebox.showwarning("Warning", "Subject already exists for this major/minor!")
    
    def add_teacher(self):
        subject = self.subject_teacher_var.get()
        teacher_name = self.teacher_entry.get().strip()
        
        if not subject:
            messagebox.showwarning("Warning", "Please select a subject!")
            return
        
        if not teacher_name:
            messagebox.showwarning("Warning", "Teacher name cannot be empty!")
            return
        
        if subject not in self.data["teachers"]:
            self.data["teachers"][subject] = []
        
        if teacher_name not in self.data["teachers"][subject]:
            self.data["teachers"][subject].append(teacher_name)
            self.teachers_listbox.insert(tk.END, teacher_name)
            self.teacher_entry.delete(0, tk.END)
            self.update_comboboxes()
        else:
            messagebox.showwarning("Warning", "Teacher already exists for this subject!")
    
    # Connection methods
    def add_connection(self):
        major = self.connection_major_var.get()
        minor = self.connection_minor_var.get()
        
        if not major or not minor:
            messagebox.showwarning("Warning", "Please select both major and minor!")
            return
        
        connection = (major, minor)
        if connection not in self.data["connections"]:
            self.data["connections"].append(connection)
            self.connections_listbox.insert(tk.END, f"{major} + {minor}")
            self.update_comboboxes()
        else:
            messagebox.showwarning("Warning", "Connection already exists!")
    
    # Update comboboxes and listboxes
    def update_comboboxes(self):
        # Update major/minor combobox for subjects
        all_majors_minors = self.data["majors"] + self.data["minors"]
        self.major_subject_combo['values'] = all_majors_minors
        
        # Update subject combobox for teachers
        all_subjects = []
        for subjects in self.data["subjects"].values():
            all_subjects.extend(subjects)
        self.subject_teacher_combo['values'] = list(set(all_subjects))  # Remove duplicates
        
        # Update connection comboboxes
        self.connection_major_combo['values'] = self.data["majors"]
        self.connection_minor_combo['values'] = self.data["minors"]
    
    def update_subject_list(self, event=None):
        major = self.major_subject_var.get()
        self.subjects_listbox.delete(0, tk.END)
        if major in self.data["subjects"]:
            for subject in self.data["subjects"][major]:
                self.subjects_listbox.insert(tk.END, subject)
    
    def update_teacher_list(self, event=None):
        subject = self.subject_teacher_var.get()
        self.teachers_listbox.delete(0, tk.END)
        if subject in self.data["teachers"]:
            for teacher in self.data["teachers"][subject]:
                self.teachers_listbox.insert(tk.END, teacher)
    
    # Data persistence methods
    def save_data(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, 'w') as f:
                json.dump(self.data, f, indent=2)
            messagebox.showinfo("Success", f"Data saved to {filename}")
    
    def load_data(self):
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    self.data = json.load(f)
                
                # Update UI with loaded data
                self.streams_listbox.delete(0, tk.END)
                for stream in self.data["streams"]:
                    self.streams_listbox.insert(tk.END, stream)
                
                self.semesters_listbox.delete(0, tk.END)
                for semester in self.data["semesters"]:
                    self.semesters_listbox.insert(tk.END, semester)
                
                self.majors_listbox.delete(0, tk.END)
                for major in self.data["majors"]:
                    self.majors_listbox.insert(tk.END, major)
                
                self.minors_listbox.delete(0, tk.END)
                for minor in self.data["minors"]:
                    self.minors_listbox.insert(tk.END, minor)
                
                self.connections_listbox.delete(0, tk.END)
                for connection in self.data["connections"]:
                    self.connections_listbox.insert(tk.END, f"{connection[0]} + {connection[1]}")
                
                self.update_comboboxes()
                messagebox.showinfo("Success", f"Data loaded from {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {str(e)}")


def main():
    root = tk.Tk()
    app = DataCollectionTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()