from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Producto, Publicacion, Bicycle, BicycleImage, Mensaje
from .forms import PublicacionForm, BicycleForm, BicycleImageForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import get_messages

def home(request):
    bicicletas_destacadas = Bicycle.objects.order_by('-id')[:6]
    return render(request, 'bicicletas/home.html', {
        'bicicletas_destacadas': bicicletas_destacadas
    })


def productos_view(request):
    query = request.GET.get('q')
    orden = request.GET.get('orden')

    # Filtro
    bicicletas = Bicycle.objects.all()
    if query:
        bicicletas = bicicletas.filter(titulo__icontains=query)
    if orden == 'precio_asc':
        bicicletas = bicicletas.order_by('precio')
    elif orden == 'precio_desc':
        bicicletas = bicicletas.order_by('-precio')

    context = {
        'bicicletas': bicicletas,
        'query': query,
        'orden': orden,
    }
    return render(request, 'bicicletas/productos.html', context)


def acerca_de(request):
    return render(request, 'bicicletas/acerca_de.html', {'title': 'Acerca de Nosotros'})


def contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')

        Mensaje.objects.create(
            nombre=nombre,
            email=email,
            asunto=asunto,
            mensaje=mensaje
        )
        storage = get_messages(request)
        list(storage)  
        messages.success(request, '¡Tu mensaje ha sido enviado con éxito!')

        return redirect('bicicletas:contacto')  

    return render(request, 'bicicletas/contacto.html')



def producto_detalle(request, producto_id):
    bicicleta = get_object_or_404(Bicycle, id=producto_id)
    if bicicleta.precio == int(bicicleta.precio):  
        precio_formateado = f"{int(bicicleta.precio):,}".replace(",", ".")
    else:  
        precio_formateado = f"{bicicleta.precio:,.2f}".replace(",", ".")
    
    return render(request, 'bicicletas/producto_detalle.html', {
        'bicicleta': bicicleta,
        'precio_formateado': precio_formateado,
    })


@login_required
def gestionar_publicacion(request, publicacion_id=None):
    if publicacion_id:
        publicacion = get_object_or_404(Publicacion, id=publicacion_id)
        form = PublicacionForm(request.POST or None, instance=publicacion)
    else:
        form = PublicacionForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        publicacion = form.save(commit=False)
        publicacion.usuario = request.user
        publicacion.save()
        return redirect('productos_view')  

    return render(request, 'bicicletas/nueva_publicacion.html', {'form': form})


def lista_publicaciones(request):
    publicaciones = Publicacion.objects.all()
    return render(request, 'bicicletas/publicaciones.html', {'publicaciones': publicaciones})


@login_required
def publish_bicycle(request):
    ImageFormSet = modelformset_factory(BicycleImage, form=BicycleImageForm, extra=5, max_num=5)
    if request.method == 'POST':
        form = BicycleForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=BicycleImage.objects.none())
        if form.is_valid() and formset.is_valid():
            bicycle = form.save(commit=False)
            bicycle.usuario = request.user
            bicycle.save()
            for image_form in formset:
                if image_form.cleaned_data.get('image'):
                    image = image_form.save(commit=False)
                    image.bicycle = bicycle
                    image.save()
            return redirect('profile')
    else:
        form = BicycleForm()
        formset = ImageFormSet(queryset=BicycleImage.objects.none())
    return render(request, 'bicicletas/publish_bicycle.html', {'form': form, 'formset': formset})


@login_required
def mis_publicaciones(request):
    publicaciones = Bicycle.objects.filter(usuario=request.user)
    return render(request, 'bicicletas/mis_publicaciones.html', {'publicaciones': publicaciones})


@login_required
def gestionar_publicacion(request, publicacion_id=None):
    if publicacion_id:
        publicacion = get_object_or_404(Bicycle, id=publicacion_id, usuario=request.user)
        form = BicycleForm(request.POST or None, request.FILES or None, instance=publicacion)
        images = publicacion.images.all()  
    else:
        publicacion = None
        form = BicycleForm(request.POST or None, request.FILES or None)
        images = []

    if request.method == 'POST' and form.is_valid():
        publicacion = form.save(commit=False)
        publicacion.usuario = request.user
        publicacion.save()

        if 'new_photos' in request.FILES:
            for image in request.FILES.getlist('new_photos'):
                BicycleImage.objects.create(bicycle=publicacion, image=image)

        return redirect('bicicletas:mis_publicaciones')

    return render(request, 'bicicletas/gestionar_publicacion.html', {
        'form': form,
        'images': images,
    })


@login_required
def eliminar_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Bicycle, id=publicacion_id, usuario=request.user)
    publicacion.delete()
    return HttpResponseRedirect(reverse('bicicletas:mis_publicaciones'))


@login_required
def delete_photo(request, image_id):
    image = get_object_or_404(BicycleImage, id=image_id, bicycle__usuario=request.user)
    bicycle_id = image.bicycle.id
    image.delete()
    return redirect('bicicletas:editar_publicacion', publicacion_id=bicycle_id)