""" Supabase Authenticator. """

import streamlit as st
from supabase import create_client, Client
from pydantic.dataclasses import dataclass
from pydantic import ConfigDict
from dotenv import load_dotenv

load_dotenv()


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class SupabaseAuth:

    supabase: Client

    def __post_init__(self) -> None:
        self.supabase = create_client(
            supabase_url=st.secrets.supabase.PROJECT_URL,
            supabase_key=st.secrets.supabase.ANON_PUBLIC,
        )

    def init_session(self) -> None:
        if "logged_in" not in st.session_state:
            st.session_state["logged_in"] = False

    # def register_user(self, email: str, password: str) -> None:
    #     try:
    #         user = self.supabase.auth.sign_up({"email": email, "password": password})
    #         return f"User {email} registered successfully"
    #     except Exception as e:
    #         return f"An error occurred:\n{e}"

    def register_user(
        self, email: str, password: str, first_name: str, last_name: str, username: str
    ) -> str:
        try:
            # Register the user
            user = self.supabase.auth.sign_up({"email": email, "password": password})
            user_id = user.user.id

            # Insert into profiles table
            self.supabase.from_("profiles").insert(
                {
                    "user_id": user_id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "username": username,
                }
            ).execute()

            return True, f"User {email} registered successfully with profile"
        except Exception as e:
            return False, f"An error occurred:\n{e}"

    def login(self, email: str, password: str) -> None:
        try:
            user = self.supabase.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
            if user and user.get("access_token"):
                st.session_state["logged_in"] = True
                st.session_state["email"] = email
                return True, f"User {email} logged in successfully"
            return False, f"User {email} not logged in"
        except Exception as e:
            return False, f"An error occurred:\n{e}"

    def logout(self) -> None:
        st.session_state["logged_in"] = False
        st.session_state["email"] = None
        self.supabase.auth.sign_out()

    def is_logged_in(self) -> bool:
        return st.session_state.get("logged_in", False)

    def set_username(self, username: str) -> str:
        try:
            existing_user = (
                self.supabase.from_("profiles")
                .select("id")
                .eq("username", username)
                .execute()
            )
            if existing_user.data:
                return f"Username {username} already exists, please choose another one."

            self.supabase.from_("profiles").insert(
                {"email": st.session_state["email"], "username": username}
            ).execute()

            return f"Username {username} set successfully"
        except Exception as e:
            return f"An error occurred:\n{e}"

    # def get_user_info(self):
    #     user = self.supabase.auth.get_user()
    #     if user:
    #         return user
    #     return {"error": "User not found"}
    def get_user_profile(self):
        user = self.supabase.auth.get_user()
        if user:
            profile = (
                self.supabase.from_("profiles")
                .select("*")
                .eq("user_id", user.user.id)
                .execute()
            )
            return profile.data[0] if profile.data else None
        return None

    def update_user_profile(
        self, first_name: str, last_name: str, username: str
    ) -> str:
        try:
            user = self.supabase.auth.get_user()
            if user:
                self.supabase.from_("profiles").update(
                    {
                        "first_name": first_name,
                        "last_name": last_name,
                        "username": username,
                    }
                ).eq("user_id", user.user.id).execute()

                return "Profile updated successfully"
            return "User not found"
        except Exception as e:
            return f"An error occurred:\n{e}"
