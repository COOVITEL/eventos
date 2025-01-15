from django.shortcuts import render, redirect
from .utils import getUsers
from .models import EntregaObsequio, Sucursal, Asesor
from django.contrib import messages

def index(request):
    asociado = None
    sucursales = Sucursal.objects.all().order_by("nombre")
    asesores = Asesor.objects.all().order_by("nombre")
    if request.method == 'POST':
        form = request.POST.get("form_id")
        if form == "form-consulta":
            asesor = request.POST.get("quien_entrega", "").strip()
            request.session['asesor'] = asesor
            
            lugar = request.POST.get("medio_entrega", "").strip()
            request.session['lugar'] = lugar
            
            cedula = request.POST.get("cedula", "").strip()
            request.session['cedula'] = cedula
            
            if EntregaObsequio.objects.filter(documento=cedula):
                messages.info(request, "Ya se realizo la entrega del obsequio al Asociado.")
                return render(request, 'index.html', {'sucursales': sucursales, 'asesores': asesores})
            
            
            asociado = getUsers(int(cedula))
            if asociado['state'] == False:
                messages.error(request, "No se encontro ningun asociado con ese numero de identificación.")
                return render(request, 'index.html', {'sucursales': sucursales, 'asesores': asesores})
                
            if asociado:
                request.session['name'] = asociado['asociado']['name']
                request.session['state'] = asociado['asociado']['state']
                request.session['description'] = asociado['asociado']['description']
            
        if form == "form_entrega":
            if request.POST.get("razon"):
                razon = request.POST.get("razon")
            else:
                razon = ""
            cedula = request.session.get('cedula', None)
            lugar = request.session.get('lugar', None)
            asesor = request.session.get('asesor', None)
            name = request.session.get('name', None)
            state = request.session.get('state', None)
            description = request.session.get('description', None)
            registro = EntregaObsequio(
                nombre=name,
                documento=cedula,
                sucursal=lugar,
                estado=state,
                obsequio=description,
                asesor=asesor,
                razonDeEntrega=razon
            )
            registro.save()
            
            messages.success(request, "Se ha registrado con éxito la entrega.")
            
            return render(request, 'index.html', {'sucursales': sucursales, 'asesores': asesores})

        return render(request, 'index.html', {
                'asociado': asociado,
                })
    return render(request, 'index.html', {'sucursales': sucursales, 'asesores': asesores})

def close(request):
    return redirect ('index')