from django.db import models

# Create your models here.
class ActivationCode(models.Model):
    serial_number = models.CharField(max_length=50, unique=True)
    activation_code = models.CharField(max_length=16)
    activation_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.serial_number} - {self.activation_code}"
    
    def calculate_activation_key(self):
        numero_serie = str(self.serial_number)
        TCle = "MAZBNCYDOEWHQIVJRKULST"  # Clé principale
        TCle1 = TCle  # Utilisé pour compléter si nécessaire

        # Étape 1 : On enlève les espaces du numéro de série
        TNoSerie = numero_serie.replace(" ", "")

        # Étape 2 : On inverse les caractères (le dernier devient le premier)
        TXT = TNoSerie[::-1]

        # Étape 3 : On code les caractères
        TCodeActivation = ""
        for L in range(0, len(TXT), 2):
            # Je prends un double
            T1 = TXT[L:L + 2]

            # Je prends le premier caractère du double pour trouver la lettre à utiliser
            premier_caractere = T1[0]
            if premier_caractere.isdigit():
                index = int(premier_caractere)  # Convertit le premier caractère en entier
                if index == 0:
                    index += 1
            else:
                index = ord(premier_caractere.upper()) - ord('A') + 1  # Convertit les lettres en index (A=1, B=2...)

            # Si l'index est valide, on récupère la lettre correspondante
            T2 = TCle[index - 1] if 1 <= index <= len(TCle) else ""

            # J'assemble les 3 caractères trouvés
            T3 = T2 + T1

            # Je recompose la clé d'activation
            TCodeActivation += T3

        # Étape 4 : Ajuster la longueur à 16 caractères
        if len(TCodeActivation) < 16:
            TCodeActivation += TCle1[:16 - len(TCodeActivation)]
        elif len(TCodeActivation) > 16:
            TCodeActivation = TCodeActivation[:16]

        self.activation_code= TCodeActivation
