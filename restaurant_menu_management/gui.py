import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import subprocess
import webbrowser


def run_etl_process():
    try:
        subprocess.run(["python", "manage.py", "etl_process"], check=True)
        messagebox.showinfo("Success", "ETL process completed successfully!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to run the ETL process.")


def open_query_window():
    # Create a new window for query options
    query_window = tk.Toplevel(root)
    query_window.title("Run Queries")

    tk.Label(query_window, text="Choose a Query:", font=("Arial", 12)).pack(pady=10)

    query_options = {
        1: "Retrieve Complete Menu Information",
        2: "Filter Items by Dietary Restrictions",
        3: "Track PDF Processing Status",
        4: "Generate Reports on Menu Items and Prices",
        5: "Handle Menu Updates and Versioning",
    }

    output_label = tk.Label(query_window, text="Query Output:", font=("Arial", 12))
    output_label.pack(pady=5)

    # Add a text box to display query results
    output_text = scrolledtext.ScrolledText(query_window, wrap=tk.WORD, width=80, height=20)
    output_text.pack(pady=10)

    def display_output(output):
        output_text.delete(1.0, tk.END)  # Clear existing text
        output_text.insert(tk.END, output)  # Insert new output

    def run_selected_query(query_choice):
        try:
            command = ["python", "manage.py", "run_queries", f"--query={query_choice}"]

            if query_choice == 2:  # Dietary restrictions query
                restriction_type = simpledialog.askstring(
                    "Dietary Restriction",
                    "Enter the dietary restriction (e.g., Gluten-Free):",
                )
                if restriction_type:
                    restaurant_id = simpledialog.askinteger(
                        "Restaurant ID",
                        "Enter the Restaurant ID:",
                    )
                    if restaurant_id:
                        command.extend(
                            [f"--restaurant_id={restaurant_id}", f"--restriction_type={restriction_type}"]
                        )
                    else:
                        messagebox.showerror("Error", "Restaurant ID is required!")
                        return
                else:
                    messagebox.showerror("Error", "Dietary restriction is required!")
                    return

            # Run the query command and capture the output
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            display_output(result.stdout)

        except subprocess.CalledProcessError as e:
            display_output(e.stderr or "An error occurred while executing the query.")
        except Exception as e:
            display_output(f"An unexpected error occurred: {e}")

    for key, value in query_options.items():
        btn_query = tk.Button(
            query_window,
            text=value,
            command=lambda k=key: run_selected_query(k),
            width=40,
            height=2,
        )
        btn_query.pack(pady=5)


def start_server():
    try:
        subprocess.Popen(["python", "manage.py", "runserver"])
        webbrowser.open("http://127.0.0.1:8000/admin/")
        messagebox.showinfo("Server Started", "Server is running and the admin page has been opened.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start the server: {e}")


def open_search_page():
    try:
        webbrowser.open("http://127.0.0.1:8000/menu_manager/search/")
        messagebox.showinfo("Search Page", "Search page opened in browser.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open search page: {e}")


# Create the main tkinter window
root = tk.Tk()
root.title("Restaurant Menu Management GUI")

# Add buttons for each option
tk.Label(root, text="Choose an Option:", font=("Arial", 14)).pack(pady=10)

btn_etl = tk.Button(root, text="1) Insert a Menu (ETL Process)", command=run_etl_process, width=40, height=2)
btn_etl.pack(pady=5)

btn_queries = tk.Button(root, text="2) Run Queries", command=open_query_window, width=40, height=2)
btn_queries.pack(pady=5)

btn_server = tk.Button(root, text="3) Start Server and Open Admin Page", command=start_server, width=40, height=2)
btn_server.pack(pady=5)

btn_search = tk.Button(root, text="4) Go to Full Search Page", command=open_search_page, width=40, height=2)
btn_search.pack(pady=5)

# Start the tkinter event loop
root.mainloop()
