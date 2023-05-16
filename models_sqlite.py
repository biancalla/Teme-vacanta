"""Modulul care contine clasele aferente entitatilor din DB. 
Models face maparea dintre datele din DB si codul nostru Python"""
import bcrypt

class User:
    def __init__(self, id, name, password, email, is_logged=0):
        self.id = id
        self.name = name
        self.email = email
        self.password = self.hash_password(password)   # TODO: trebuie ascunsa parola (HASH)
        self.is_logged = is_logged

    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed

    def validate(self):
        """Metoda care valideaza un User, asigurandu-se ca are field-urile potrivite, cu tipurile 
        de date potrivite, ca email-ul e valid, etc..
        return: True/False
        Validarea presupune verificarea tipului de date pentru fiecare field (id, name, password, ...)
        Validarea structurii email-ului, respectand urmatoarele:
        1. email-ul tre sa contina exact un @
        2. email-ul tre sa contina minim un .
        3. nu are voie sa contina niciun caracter special dintre urmatoarele:  !#$%^&*()+=`~/?:;<>,\\|\"\'|țșăîâÂÎȚȘĂ
        4. domeniul email-ului poate sa contina intre 2 is 3 caractere (ex: ro, com, org, net, ...)
        """

        if not all([
            isinstance(self.id, str),
            isinstance(self.name, str),
            isinstance(self.email, str),
            isinstance(self.password, bytes),
            isinstance(self.is_logged, int),
        ]):
            return False

        invalid_special_symbols = "!#$%^&*()+=`~/?<>,\\|\"\'|țșăîâÂÎȚȘĂ"
        if any(char in self.email for char in invalid_special_symbols):
            return False

        email_parts = self.email.split("@")
        if len(email_parts) != 2:
            return False

        local_part, domain_part = email_parts

        if "." not in domain_part:
            return False

        domain_parts = domain_part.split(".")
        if not (2 <= len(domain_parts[-1]) <= 3):
            return False

        return True

    def __str__(self):
        return f"User(name={self.name}, email={self.email}, is_logged={self.is_logged})"


class Book:
    # TODO: de implementat similar cu User
    def __init__(self, id, title, author, pages, category):
        self.id = id
        self.title = title
        self.author = author
        self.pages = pages
        self.category = category

    def validate(self):
        if not all([
            isinstance(self.id, str),
            isinstance(self.title, str),
            isinstance(self.author, str),
            isinstance(self.pages, int),
            isinstance(self.category, str),
        ]):
            return False