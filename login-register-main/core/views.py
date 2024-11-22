from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from .models import Post
from .forms import PostForm

# Create your views here.
def home(request):
    return render(request, 'core/home.html')

@login_required
def ofertas(request):
    return render(request, 'core/ofertas.html')

def register(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user_creation_form.save()

            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)
            return redirect('home')
        else:
            data['form'] = user_creation_form

    return render(request, 'registration/register.html', data)


def salir(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('home')  # Redirige a la página home

# Vista para publicaciones (requiere autenticación)
@login_required
def publicaciones(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Asigna el usuario actual al post
            post.save()
            return redirect('publicaciones')  # Redirige tras guardar el post
    else:
        form = PostForm()

    posts = Post.objects.all().order_by('-created_at')  # Ordena posts por fecha
    return render(request, 'core/publicaciones.html', {'posts': posts, 'form': form})