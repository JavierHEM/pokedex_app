# views/profile_view.py
import customtkinter as ctk
from models.user_model import UserModel
import re
from datetime import datetime

class ProfileView(ctk.CTkFrame):
    def __init__(self, master, user_data):
        super().__init__(master)
        self.user_data = user_data
        self.user_model = UserModel()
        self.profile_data = None
        self.setup_ui()
        self.load_profile_data()

    def setup_ui(self):
        # Configurar grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Panel izquierdo (información del perfil)
        self.setup_profile_panel()

        # Panel derecho (estadísticas y configuración)
        self.setup_stats_panel()

    def setup_profile_panel(self):
        profile_frame = ctk.CTkFrame(self)
        profile_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Título
        title = ctk.CTkLabel(
            profile_frame,
            text="Mi Perfil",
            font=("Roboto", 24, "bold")
        )
        title.pack(pady=20)

        # Form container
        form_frame = ctk.CTkFrame(profile_frame)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Campos de usuario
        self.setup_user_fields(form_frame)

        # Campos de entrenador
        self.setup_trainer_fields(form_frame)

        # Botón de guardar
        save_btn = ctk.CTkButton(
            profile_frame,
            text="Guardar Cambios",
            command=self.save_profile
        )
        save_btn.pack(pady=20)

        # Label para mensajes
        self.message_label = ctk.CTkLabel(
            profile_frame,
            text="",
            text_color="green"
        )
        self.message_label.pack(pady=10)

    def setup_user_fields(self, parent):
        # Frame para datos de usuario
        user_frame = ctk.CTkFrame(parent)
        user_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            user_frame,
            text="Información de Usuario",
            font=("Roboto", 16, "bold")
        ).pack(pady=10)

        # Username (no editable)
        ctk.CTkLabel(user_frame, text="Nombre de usuario:").pack()
        self.username_label = ctk.CTkLabel(
            user_frame,
            text="",
            font=("Roboto", 12, "bold")
        )
        self.username_label.pack(pady=(0, 10))

        # Email
        ctk.CTkLabel(user_frame, text="Email:").pack()
        self.email_entry = ctk.CTkEntry(user_frame)
        self.email_entry.pack(pady=(0, 10), padx=20)

        # Cambiar contraseña
        password_btn = ctk.CTkButton(
            user_frame,
            text="Cambiar Contraseña",
            command=self.show_change_password_dialog
        )
        password_btn.pack(pady=10)

    def setup_trainer_fields(self, parent):
        # Frame para datos de entrenador
        trainer_frame = ctk.CTkFrame(parent)
        trainer_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            trainer_frame,
            text="Información de Entrenador",
            font=("Roboto", 16, "bold")
        ).pack(pady=10)

        # Nombre de entrenador
        ctk.CTkLabel(trainer_frame, text="Nombre:").pack()
        self.trainer_name_entry = ctk.CTkEntry(trainer_frame)
        self.trainer_name_entry.pack(pady=(0, 10), padx=20)

        # Edad
        ctk.CTkLabel(trainer_frame, text="Edad:").pack()
        self.trainer_age_entry = ctk.CTkEntry(trainer_frame)
        self.trainer_age_entry.pack(pady=(0, 10), padx=20)

        # Región
        ctk.CTkLabel(trainer_frame, text="Región:").pack()
        self.trainer_region_entry = ctk.CTkEntry(trainer_frame)
        self.trainer_region_entry.pack(pady=(0, 10), padx=20)

    def setup_stats_panel(self):
        stats_frame = ctk.CTkFrame(self)
        stats_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Título
        title = ctk.CTkLabel(
            stats_frame,
            text="Estadísticas",
            font=("Roboto", 24, "bold")
        )
        title.pack(pady=20)

        # Contenedor de estadísticas
        self.stats_container = ctk.CTkFrame(stats_frame)
        self.stats_container.pack(fill="both", expand=True, padx=20, pady=10)

    def load_profile_data(self):
        # Cargar datos del perfil
        self.profile_data = self.user_model.get_user_profile(self.user_data['id'])
        if self.profile_data:
            # Actualizar campos de usuario
            self.username_label.configure(text=self.profile_data['username'])
            self.email_entry.delete(0, 'end')
            self.email_entry.insert(0, self.profile_data['email'])

            # Actualizar campos de entrenador
            if self.profile_data['trainer_name']:
                self.trainer_name_entry.insert(0, self.profile_data['trainer_name'])
            if self.profile_data['trainer_age']:
                self.trainer_age_entry.insert(0, str(self.profile_data['trainer_age']))
            if self.profile_data['trainer_region']:
                self.trainer_region_entry.insert(0, self.profile_data['trainer_region'])

        # Cargar estadísticas
        self.load_stats()

    def load_stats(self):
        # Limpiar contenedor de estadísticas
        for widget in self.stats_container.winfo_children():
            widget.destroy()

        # Obtener estadísticas
        stats = self.user_model.get_user_stats(self.user_data['id'])

        # Crear tarjetas de estadísticas
        self.create_stat_card("Fecha de registro", 
                            stats['join_date'].strftime('%d/%m/%Y') 
                            if stats['join_date'] else "N/A")
        
        self.create_stat_card("Total de búsquedas", 
                            str(stats['total_searches']))
        
        self.create_stat_card("Pokémon en equipo", 
                            f"{stats['total_pokemon']}/10")
        
        self.create_stat_card("Última búsqueda", 
                            stats['last_search'].strftime('%d/%m/%Y %H:%M') 
                            if stats['last_search'] else "N/A")

    def create_stat_card(self, title: str, value: str):
        card = ctk.CTkFrame(self.stats_container)
        card.pack(fill="x", pady=5, padx=5)

        ctk.CTkLabel(
            card,
            text=title,
            font=("Roboto", 12)
        ).pack(pady=(5,0))

        ctk.CTkLabel(
            card,
            text=value,
            font=("Roboto", 16, "bold")
        ).pack(pady=(0,5))

    def validate_profile_data(self, data: dict) -> bool:
        # Validar email
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', data['email']):
            self.show_error("Email inválido")
            return False

        # Validar edad (si se proporciona)
        if data['trainer_age']:
            try:
                age = int(data['trainer_age'])
                if age < 10 or age > 100:
                    self.show_error("La edad debe estar entre 10 y 100 años")
                    return False
            except ValueError:
                self.show_error("La edad debe ser un número")
                return False

        return True

    def save_profile(self):
        # Recopilar datos
        data = {
            'email': self.email_entry.get(),
            'trainer_name': self.trainer_name_entry.get(),
            'trainer_age': self.trainer_age_entry.get(),
            'trainer_region': self.trainer_region_entry.get()
        }

        # Validar datos
        if not self.validate_profile_data(data):
            return

        # Convertir edad a int si existe
        if data['trainer_age']:
            data['trainer_age'] = int(data['trainer_age'])

        # Guardar cambios
        success, message = self.user_model.update_user_profile(
            self.user_data['id'], 
            data
        )

        if success:
            self.show_message(message)
            self.load_profile_data()  # Recargar datos
        else:
            self.show_error(message)

    def show_change_password_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Cambiar Contraseña")
        dialog.geometry("400x300")
        dialog.resizable(False, False)

        # Centrar en la pantalla
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        # Campos
        ctk.CTkLabel(dialog, text="Contraseña actual:").pack(pady=(20,5))
        current_password = ctk.CTkEntry(dialog, show="*")
        current_password.pack(pady=(0,10), padx=20)

        ctk.CTkLabel(dialog, text="Nueva contraseña:").pack(pady=(10,5))
        new_password = ctk.CTkEntry(dialog, show="*")
        new_password.pack(pady=(0,10), padx=20)

        ctk.CTkLabel(dialog, text="Confirmar nueva contraseña:").pack(pady=(10,5))
        confirm_password = ctk.CTkEntry(dialog, show="*")
        confirm_password.pack(pady=(0,10), padx=20)

        # Label para mensajes de error
        error_label = ctk.CTkLabel(dialog, text="", text_color="red")
        error_label.pack(pady=10)

        def change_password():
            if new_password.get() != confirm_password.get():
                error_label.configure(text="Las contraseñas no coinciden")
                return

            if len(new_password.get()) < 8:
                error_label.configure(text="La contraseña debe tener al menos 8 caracteres")
                return

            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", new_password.get()):
                error_label.configure(text="La contraseña debe contener al menos un carácter especial")
                return

            success, message = self.user_model.change_password(
                self.user_data['id'],
                current_password.get(),
                new_password.get()
            )

            if success:
                dialog.destroy()
                self.show_message(message)
            else:
                error_label.configure(text=message)

        # Botón de cambiar
        ctk.CTkButton(
            dialog,
            text="Cambiar Contraseña",
            command=change_password
        ).pack(pady=20)

    def show_message(self, message: str):
        self.message_label.configure(text=message, text_color="green")

    def show_error(self, message: str):
        self.message_label.configure(text=message, text_color="red")