# Punto de entrada de la aplicacion

# main.py
import customtkinter as ctk
from views.login_view import LoginView

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Pokédex App")
        self.geometry("800x600")
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Show login view
        self.show_login()

    def show_login(self):
        # Clear current view if exists
        for widget in self.winfo_children():
            widget.destroy()
        
        # Show login view
        login_view = LoginView(self, self.show_main_view)
        login_view.grid(row=0, column=0, sticky="nsew")

    def show_main_view(self, user):
        # Clear login view
        for widget in self.winfo_children():
            widget.destroy()
        
        # Here we'll add the main view later
        # For now, just show a welcome label
        welcome = ctk.CTkLabel(
            self,
            text=f"Bienvenido {user['username']}!",
            font=("Roboto", 24)
        )
        welcome.grid(row=0, column=0, pady=20)

if __name__ == "__main__":
    app = App()
    app.mainloop()