from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import login
from .forms import SignupForm
# Create your views here.

from django.contrib.auth.decorators import login_required
from .models import ActivationCode

@login_required
def generate_activation_code(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Vous devez être connecté pour accéder à cette page.")
        return redirect('login')
    if request.method == 'POST':
        serial_number = request.POST.get('serial_number')
        description = request.POST.get('description')

        # Créer un nouveau code d'activation
        activation = ActivationCode.objects.create(serial_number=serial_number, description=description)
        activation.calculate_activation_key()
        # Sauvegarder l'objet dans la base de données
        activation.save()

        return render(request, 'activation/activation_code_generated.html', {'activation': activation, 'user': request.user})

    return render(request, 'activation/generate_activation_code.html', {
        'user': request.user,
    })

class CustomLoginView(LoginView):
    template_name = 'activation/login.html'  # Indique le template de connexion

def welcome(request):
    return render(request, 'activation/welcome.html')  
  
@login_required
def activation_history(request):
    activations = ActivationCode.objects.all()  # Récupérer toutes les clés générées
    return render(request, 'activation/history.html', {'activations': activations})

def logout_view(request):
    logout(request)
    return redirect('login')  # Rediriger vers la page de connexion après déconnexion


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # Connecter l'utilisateur automatiquement après inscription
            return redirect('generate_activation_code')  # Rediriger vers la page de génération de clé
    else:
        form = SignupForm()
    return render(request, 'activation/signup.html', {'form': form})

