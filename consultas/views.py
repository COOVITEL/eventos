from django.shortcuts import render, redirect
from .models import EntregaObsequio, Sucursal, Asesor, Asociados
from django.contrib import messages
from django.utils.timezone import localtime
import pandas as pd
from django.http import HttpResponse
from .utils import setValue

def index(request):
    asociado = None
    sucursales = Sucursal.objects.all().order_by("nombre")
    asesores = Asesor.objects.all().order_by("nombre")
    if request.method == 'POST':
        form = request.POST.get("form_id")
        if form == "form-consulta":
            asesor = request.POST.get("quien_entrega")
            request.session['asesor'] = asesor
            
            lugar = request.POST.get("medio_entrega", "").strip()
            request.session['lugar'] = lugar
            
            cedula = request.POST.get("cedula", "").strip()
            request.session['cedula'] = cedula
            
            entrega = EntregaObsequio.objects.filter(documento=cedula)
            if entrega:
                fecha_local = str(localtime(entrega[0].fecha)).split(".")

                messages.info(request, f"Ya se realizo la entrega a {entrega[0].nombre} el dia {fecha_local[0]} en {entrega[0].sucursal} por {entrega[0].asesor}.")
                return render(request, 'index.html', {'sucursales': sucursales, 'asesores': asesores})
            
            asociado = Asociados.objects.filter(documento=cedula)
            if len(asociado) == 0:
                messages.error(request, "No se encontro ningun asociado con ese numero de identificación.")
                return render(request, 'index.html', {'sucursales': sucursales, 'asesores': asesores})
            
            if asociado[0].tipo == "EMPRESA":
                messages.error(request, f"Lo sentimos {asociado[0].nombre}, los obsequios de fidelización no aplican para empresas.")
                return render(request, 'index.html', {'sucursales': sucursales, 'asesores': asesores})

            if asociado[0].obsequio == "NO CUMPLE ANTIGÜEDAD" and asociado[0].causa == "NO CUMPLE ANTIGÜEDAD":
                messages.error(request, f"Lo sentimos {asociado[0].nombre}, no cumples con la antigüedad  mínima para aplicar a un obsequio.")
                return render(request, 'index.html', {'sucursales': sucursales, 'asesores': asesores})
            
            if asociado:
                request.session['name'] = asociado[0].nombre
                request.session['state'] = asociado[0].state
                request.session['description'] = asociado[0].obsequio
            
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
        preaprobado = {
            'prestamo': int(asociado[0].preaprobado) > 0,
            'monto': setValue(asociado[0].preaprobado),
            'cuota': setValue(asociado[0].cuota),
            'plazo': asociado[0].plazo
        }
        return render(request, 'index.html', {
                'asociado': asociado[0],
                'prestamo': preaprobado
                })
    return render(request, 'index.html', {'sucursales': sucursales, 'asesores': asesores})

def close(request):
    return redirect ('index')

def seedUserus(request):
    df = pd.read_excel('base.xlsx', sheet_name='Base Plataforma 15012024', skiprows=1)
    asociados = df.values.tolist()
    for asociado in asociados:
        exist = Asociados.objects.filter(documento=asociado[0]).exists()
        if not exist:
            aso = Asociados(
                documento=asociado[0],
                nombre=asociado[1],
                tipo=asociado[2],
                obsequio=asociado[4],
                state=asociado[5],
                causa=asociado[6],
                preaprobado=asociado[7],
                cuota=asociado[8],
                plazo=asociado[9]
            )
            aso.save()
    return HttpResponse("Se crearon de forma correcta")

