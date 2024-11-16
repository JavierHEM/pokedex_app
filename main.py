# main.py
import customtkinter as ctk
from views.login_view import LoginView
from views.main_view import MainView
from views.profile_view import ProfileView

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurar ventana principal
        self.title("Pokédex App")
        self.geometry("1200x800")
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Variables de sesión
        self.current_user = None
        
        # Mostrar login
        self.show_login()

    def show_login(self):
        # Limpiar ventana
        for widget in self.winfo_children():
            widget.destroy()
        
        # Resetear usuario actual
        self.current_user = None
        
        # Mostrar vista de login
        login_view = LoginView(self, self.show_main_view)
        login_view.grid(row=0, column=0, sticky="nsew")

    def show_main_view(self, user_data):
        # Guardar datos del usuario
        self.current_user = user_data
        
        # Limpiar ventana
        for widget in self.winfo_children():
            widget.destroy()
        
        # Mostrar vista principal
        main_view = MainView(self, user_data)
        main_view.grid(row=0, column=0, sticky="nsew")

    def show_profile(self):
        # Verificar que haya un usuario logueado
        if not self.current_user:
            self.show_login()
            return
        
        # Limpiar ventana actual
        for widget in self.winfo_children():
            widget.destroy()
        
        # Mostrar vista de perfil
        profile_view = ProfileView(
            self,
            self.current_user['id'],
            self.show_login  # Callback para logout
        )
        profile_view.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    app = App()
    app.mainloop()