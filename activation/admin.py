from django.contrib import admin

# Register your models here.
from .models import ActivationCode

class ActivationCodeAdmin(admin.ModelAdmin):
    # Colonnes à afficher dans la liste
    list_display = ('serial_number', 'activation_code', 'activation_date', 'description')

    # Colonnes par lesquelles vous pouvez filtrer les données
    list_filter = ('activation_date',)

    # Champs recherchables
    search_fields = ('serial_number', 'activation_code', 'description')

    # Champs à éditer directement dans la liste (optionnel)
    list_editable = ('description',)

    # Afficher les détails dans le formulaire d'ajout/modification
    fields = ('serial_number', 'activation_code', 'description', 'activation_date')
    readonly_fields = ('activation_code', 'activation_date')  # Champs non modifiables

    # Méthode pour calculer automatiquement l'activation_code si le numéro de série change
    def save_model(self, request, obj, form, change):
        if not change or 'serial_number' in form.changed_data:
            obj.calculate_activation_key()
        super().save_model(request, obj, form, change)

# Enregistrer le modèle avec la classe personnalisée
admin.site.register(ActivationCode, ActivationCodeAdmin)

