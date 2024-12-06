from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import PaqueteForm
from .models import Paquete, EstadoPaquete,Cliente
from django.core.paginator import Paginator
from django.db.models import Sum


def home(request):
    return render(request, 'home.html')

def crear_paquete(request):
    if request.method == 'POST':
        form = PaqueteForm(request.POST, request.FILES)
        if form.is_valid():
            paquete = form.save(commit=False)  # No guardes aún en la base de datos
            paquete.empleado = request.user.empleado_profile  # Asigna el empleado como el usuario actual
            paquete.estado = EstadoPaquete.objects.get(nombre_estado='Recepcionado')  # Asigna el estado inicial
            paquete.save()  # Ahora guarda en la base de datos
            return redirect('listar_paquetes')  
    else:
        form = PaqueteForm()
    
    return render(request, 'registro/crear_envio.html', {'form': form})



def listar_paquetes(request):
    fecha_filtro = request.GET.get('fecha')  
    cliente_filtro = request.GET.get('cliente')
    paquetes = Paquete.objects.all()

   
    if fecha_filtro:
        paquetes = paquetes.filter(fecha_envio__date=fecha_filtro)

    if cliente_filtro:
        paquetes = paquetes.filter(
            cliente__user__first_name__icontains=cliente_filtro
        )

    total_ganancias = paquetes.aggregate(Sum('precio'))['precio__sum'] or 0

    paginator = Paginator(paquetes, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'registro/listar_paquetes.html', {
        'paquetes': page_obj,
        'total_ganancias': total_ganancias,
        'fecha_filtro': fecha_filtro,
        'cliente_filtro': cliente_filtro,
    })




def ver_detalle_paquete(request, paquete_id):
    paquete = get_object_or_404(Paquete, id=paquete_id)
    return render(request, 'ver_detalle_paquete.html', {'paquete': paquete})


def lista_paque(request):
   
    cliente = Cliente.objects.get(user=request.user)
    
    paquetes = Paquete.objects.filter(cliente=cliente)
    
    return render(request, 'registro/lista_paque.html', {'paquetes': paquetes})