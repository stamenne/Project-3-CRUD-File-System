import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
from pathlib import Path
import shutil
import errno

root_directory = (Path(__file__).parent / "file_manager_root").resolve()
#FILE MANAGEMENT CODE
class FileManager:
    #manage file & directory operations within a root path
    def __init__(self, root_path):
        self.root = Path(root_path).resolve() #resolve making sure it is a root path
        self.current_path = self.root
        self.root.mkdir(parents= True, exist_ok= True) #create root directory

#CRUD METHODS
    #create new file in current directory
    def create_file(self, name, content=""):
        path = self.current_path / name
        #error if file with that name already exists
        if path.exists():
            raise Exception("A file or folder with that name already exists")

        with open(path, 'w') as f:
            f.write(content) #writing to new file

    #read file method that returns the content of selected file
    def read_file(self, path):
        path = Path(path)
        if not path.exists(): #error if file doesn't exist
            raise Exception("File not found")
        if path.is_dir(): #error if file is not selected
            raise Exception("Please select a file. Cannot open a directory as a file")

        with open(path, 'r') as f:
            return f.read() #reading and returning file

    #method that updates content of a selected file
    def update_file(self, path, new_content):
        path = Path(path)
        if not path.exists():
            raise Exception("File not found") #error if file doesn't exist
        if path.is_dir(): #error if file is not selected
            raise Exception("Please select a file. Cannot write to a directory")

        with open(path, 'w') as f:
            f.write(new_content)

    #deletes a file or directory
    def delete(self, path):
        path = Path(path)
        if not path.exists():
            raise Exception("File/Directory not found")

        #delete directory (even if not empty)
        if path.is_dir():
            try:
                shutil.rmtree(path)
            except OSError as e:
                raise Exception(f"Cannot delete directory: {e}")
        else:
            os.remove(path)

    #method to make a copy of a file in a new folder
    def copy(self, source, destination_folder):
        source = Path(source)

        #file exists?
        if not source.exists():
            raise Exception("File not found")
        #can't copy directory
        if source.is_dir():
            raise Exception("You can only copy files, not folders")

        #treat destination folder as being inside the main folder
        destination_dir = Path(destination_folder)
        if not destination_dir.is_absolute():
            destination_dir = self.root / destination_dir

        #verify destination folder exists
        if not destination_dir.exists() or not destination_dir.is_dir():
            raise Exception("Destination folder selected does not exist")

        #building final file path
        destination = destination_dir / source.name

        #warning if file already exists in this directory
        if destination.exists():
            raise Exception("A file with that name already exists in this directory")
        shutil.copy2(str(source), str(destination)) #copy the file
        return destination

    #method to move a file into another folder
    def move(self, source, destination_folder):
        source = Path(source)

        #make sure file exists
        if not source.exists():
            raise Exception("File not Found")

        #treat destination path as being inside the main folde
        destination_dir = Path(destination_folder)
        if not destination_dir.is_absolute():
            destination_dir = self.root / destination_dir

        #make sure destination folder exists & is a directory
        if not destination_dir.exists() or not destination_dir.is_dir():
            raise Exception("Destination folder selected does not exist")

        #build destination
        destination = destination_dir / source.name
        #warning if file already exists in this directory
        if destination.exists():
            raise Exception("A file with that name already exists in this directory")

        #move file
        shutil.move(str(source), str(destination))
        return destination

#NAVIGATION METHODS
    #method to rename a file/folder
    def rename(self, current, new_name):
        old = Path(current)
        if not old.exists():
            raise Exception("File/Directory not found")

        new = old.with_name(new_name) #new target path
        if new.exists():
            raise Exception("A file/folder with that name already exists")

        #rename
        os.rename(old, new)
        return new

    #create new folder/directory method
    def create_directory(self, name):
        path = self.current_path / name
        if path.exists():
            raise Exception("A file/folder with that name already exists")

        os.mkdir(path)

    #method that returns the sorted list of all objects in this path
    def directory_list(self):
        items = os.listdir(self.current_path)
        paths = []
        for item in items:
            full_path = self.current_path / item
            paths.append(full_path)

        #sorting items with folders first then files in alphabetical order
        paths.sort(key= lambda p: (not p.is_dir(), p.name.lower()))
        return paths

    #method to update current path to the new directory selected
    def navigate_into(self, path):
        path = Path(path)
        if not path.exists() or not path.is_dir():
            raise Exception("The selected item is not a directory")
        self.current_path = path

    #method going back up the path one level
    def navigate_back(self):
        if self.current_path == self.root:
            return
        self.current_path = self.current_path.parent

#GUI BUILDING
#starting with blank window
file_manager = FileManager(root_directory)
root = tk.Tk()
root.title("OwlTech CRUD File Manager")
root.geometry("1000x500")

current_path_open = None
display_items = []

#display to show current path
current_path_label = tk.Label(root, text= "Path:", anchor= "w")
current_path_label.pack(fill= "x") #place label to stretch horizontally

#main area of page
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand= True) #stretched horizontally & physically and will continue to expand if window is resized

#right side of main frame: the directory and list of files
f_list = tk.Listbox(main_frame)
f_list.pack(side="left", fill= "both", expand= True)

#left side of main frame: file content
file_content = tk.Text(main_frame)
file_content.pack(side="right", fill= "both", expand= True)


#BUTTONS
button_frame = tk.Frame(root)
button_frame.pack(fill= "x")

#create file button
create_file_button = tk.Button(button_frame, text= "Create a File")
create_file_button.pack(side= "left", padx= 5, pady= 5)

#create folder button
create_folder_button = tk.Button(button_frame, text= "Create a Folder")
create_folder_button.pack(side= "left", padx= 5, pady= 5)

#open button
open_button = tk.Button(button_frame, text= "Open")
open_button.pack(side= "left", padx= 5, pady= 5)

#rename button
rename_button = tk.Button(button_frame, text= "Rename")
rename_button.pack(side= "left", padx= 5, pady= 5)

#delete button
delete_button = tk.Button(button_frame, text= "Delete")
delete_button.pack(side= "left", padx= 5, pady= 5)

#save button
save_button = tk.Button(button_frame, text= "Save")
save_button.pack(side= "left", padx= 5, pady= 5)

#up button
back_button = tk.Button(button_frame, text= "Up")
back_button.pack(side= "left", padx= 5, pady= 5)

move_button = tk.Button(button_frame, text= "Move File")
move_button.pack(side= "left", padx= 5, pady= 5)

copy_button = tk.Button(button_frame, text= "Copy To Other Folder")
copy_button.pack(side= "left", padx= 5, pady= 5)
#status area
status_label = tk.Label(root, text="Status: Ready", anchor= "w")
status_label.pack(fill= "x")


#HELPER FUNCTIONS
#updates status message (bottom left of screen)
def update_status(message: str):
    status_label.config(text=f"Status: {message}")

#updates current path label at the top of the window
def update_path():
    current_path_label.config(text=f"Path: {file_manager.current_path}")

#method to update the Listbox with the current directory's content
def refresh_file_list():
    global display_items
    f_list.delete(0, tk.END)

    try:
        items = file_manager.directory_list()
        display_items = items

        for entry in items:
            name = entry.name + "/" if entry.is_dir() else entry.name
            f_list.insert(tk.END, name)

        update_path()
        update_status("Directory opened")
    except Exception as e:
        display_items = []
        messagebox.showerror("Error", str(e))
        update_status(f"Error: {e}")

#method that returns the selected item from the list
def get_path():
    selected_path = f_list.curselection()
    if not selected_path:
        return None
    index = selected_path[0] #create index
    #use index to look up path object from list
    for i in range(len(display_items)):
        if i == index:
            return display_items[i]

    return None

#method that clears the editor and forgets which file was opened
def clear_history():
    global current_path_open
    current_path_open = None
    file_content.delete("1.0", tk.END)

#method to make error messages more user-friendly
def error_message(e):
    message = str(e)

    #no permission
    if isinstance(e, PermissionError):
        message = "You do not have permission to access or modify this file"

    #file in use error
    elif isinstance(e, OSError) and e.errno == errno.EACCES:
        message = "This file is currently in use by another system"

    #disk full error
    elif isinstance(e, OSError) and e.errno == errno.ENOSPC:
        message = "There is not enough space on the disk"

    #invalid file/path name
    elif isinstance(e, OSError) and e.errno == errno.EINVAL:
        message = "Invalid file name or path"

    #network drive disconnected
    elif isinstance(e, OSError) and e.errno == errno.ENODEV:
        message = "Network drive unavailable"

    messagebox.showerror("Error", message)
    update_status(f"Error: {message}")

#BUTTON HANDLERS
#logic behind create file button
def create_file_handle():
    #store entered name
    name = simpledialog.askstring("Create New File", "Enter File Name: ")
    if not name:
        return


    #store entered content
    content = simpledialog.askstring("Create New File", "(Optional) Enter content: ")
    if content is None:
        content = ""

    try:
        file_manager.create_file(name, content) #call file manager method
        refresh_file_list()
        update_status(f"New File Created: {name}")
    except Exception as e:
        error_message(e)

#logic behind create folder button
def create_folder_handle():
    #store name entered
    name = simpledialog.askstring("Create New Folder", "Enter Folder Name: ")
    if not name:
        return

    try:
        file_manager.create_directory(name) #call file manager method
        refresh_file_list()
        update_status(f"New Folder Created: {name}")
    except Exception as e:
        error_message(e)

#logic behind open file button
def open_handle(event= None):
    global current_path_open

    path = get_path() #get current path
    if path is None:
        messagebox.showinfo("Information", "Please select a file/folder")
        return

    try:
        if path.is_dir(): #if directory is selected, navigate into and refresh list
            file_manager.navigate_into(path)
            clear_history()
            refresh_file_list()
            update_status(f"Entered folder: {path.name}")
        else:
            #if file is selected, read and show the content
            file_text = file_manager.read_file(path)
            clear_history()
            file_content.insert("1.0", file_text)
            current_path_open = path
            update_status(f"Opened file: {path.name}")

    except Exception as e:
        error_message(e)

#logic behind rename of files/folders
def rename_handle():
    path = get_path() #get current path
    if path is None:
        messagebox.showinfo("Information", "Please select a file/folder")
        return

    #store new name
    new = simpledialog.askstring("Rename", f"Enter the new name for {path.name}: ")
    if not new:
        return

    try:
        #replace old name and refresh the file list
        new = file_manager.rename(path, new)
        refresh_file_list()
        update_status(f"File/Folder has been renamed to: {new.name}")
    except Exception as e:
        error_message(e)

#logic behind delete button
def delete_handle():
    path = get_path() #get current path
    if path is None:
        messagebox.showinfo("Information", "Please select a file/folder")
        return

    #ask user to confirm
    if not messagebox.askyesno("Delete Confirmation", f"Delete '{path.name}'?"):
        return

    try:
        file_manager.delete(path) #call file manager function
        clear_history()
        refresh_file_list()
        update_status(f"Deleted: {path.name}")
    except Exception as e:
        error_message(e)

#logic behind save button
def save_handle():
    global current_path_open
    if current_path_open is None:
        messagebox.showinfo("Information", "No file is currently open")
        return

    #store current content of file
    new_content = file_content.get("1.0", tk.END)

    try:
        file_manager.update_file(current_path_open, new_content) #save using file manager method
        update_status(f"Saved: {current_path_open}")
    except Exception as e:
        error_message(e)

#logic behind back button
def back_handle():
    try:
        before_move = file_manager.current_path #store current path
        file_manager.navigate_back() #call file manager method
        if file_manager.current_path == before_move:
            update_status("Cannot go back any further")
        else:
            clear_history()
            refresh_file_list()
            update_status(f"Moved up to: {file_manager.current_path}")

    except Exception as e:
        error_message(e)

#logic beind copy button
def copy_handle():
    path = get_path()

    if path is None:
        messagebox.showinfo("Information", "Please select file you would like to copy")
        return
    if path.is_dir():
        messagebox.showinfo("Information", "You cannot copy a directory. Please select a file")

    #ask for destination folder
    destination_folder = simpledialog.askstring("Copy File", "Enter destination folder path relative to the root path \n")
    if not destination_folder:
        return
    try:
        new_path = file_manager.copy(path, destination_folder)
        refresh_file_list()
        update_status(f"Copied to: {new_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        update_status(f"Error: {e}")

#logic behind move button
def move_handle():
    path = get_path()
    if path is None:
        messagebox.showinfo("Information", "Please select file you would like to copy")
        return
    if path.is_dir():
        messagebox.showinfo("Information", "You cannot move a directory. Please select a file")

    destination_folder = simpledialog.askstring("Move File", "Enter destination folder path relative to the root path \n")
    if not destination_folder:
        return
    try:
        new_path = file_manager.move(path, destination_folder)
        clear_history()
        refresh_file_list()
        update_status(f"Moved to: {new_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        update_status(f"Error: {e}")


#CONNECTING BUTTONS TO HANDLERS
create_file_button.config(command= create_file_handle)
create_folder_button.config(command= create_folder_handle)
open_button.config(command= open_handle)
rename_button.config(command= rename_handle)
delete_button.config(command= delete_handle)
save_button.config(command= save_handle)
back_button.config(command= back_handle)
copy_button.config(command= copy_handle)
move_button.config(command= move_handle)
f_list.bind("<Double-Button-1>", open_handle) #select a file when it is double clicked

refresh_file_list()
root.mainloop()



