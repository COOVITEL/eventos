from django.shortcuts import render, redirect
from .models import EntregaObsequio, Sucursal, Asesor, Asociados
from django.contrib import messages
from django.utils.timezone import localtime
from .utils import setValue
from django.core.cache import cache
from django.db import transaction

def index(request):
    # Usa caché para reducir consultas repetitivas
    sucursales = cache.get('sucursales')

    if not sucursales:
        sucursales = list(Sucursal.objects.all().order_by("nombre"))
        cache.set('sucursales', sucursales, 3600)  # 1 hora

    asesores = cache.get('asesores')
    if not asesores:
        asesores = list(Asesor.objects.all().order_by("nombre"))
        cache.set('asesores', asesores, 3600)  # 1 hora
    
    entregasTotales = [
        {
            'nombre': registro.nombre,
            'numero_entregas': EntregaObsequio.objects.filter(sucursal=registro.nombre).count()
        }
        for registro in sucursales
    ]
    if request.method == 'POST':
        form = request.POST.get("form_id")
        
        if form == "form-consulta":
            cedula = request.POST.get("cedula", "").strip()
            request.session.update({
                'asesor': request.POST.get("quien_entrega"),
                'lugar': request.POST.get("medio_entrega", "").strip(),
                'cedula': cedula
            })
            
            entrega = EntregaObsequio.objects.filter(documento=cedula).first()
            if entrega:
                fecha_local = str(localtime(entrega.fecha)).split(".")[0]
                messages.info(request, f"Ya se realizó la entrega a {entrega.nombre} el día {fecha_local} en {entrega.sucursal} por {entrega.asesor}.")
                return render(request, 'index.html', {'sucursales': sucursales, 'asesores': asesores})
            
            asociado = Asociados.objects.only('documento', 'nombre', 'tipo', 'obsequio', 'causa', 'state', 'preaprobado', 'cuota', 'plazo').filter(documento=cedula).first()
            if not asociado:
                messages.error(request, "No se encontró ningún asociado con ese número de identificación.")
            elif asociado.tipo == "EMPRESA":
                messages.error(request, f"Lo sentimos {asociado.nombre}, los obsequios de fidelización no aplican para empresas.")
            elif asociado.obsequio == "NO CUMPLE ANTIGÜEDAD" and asociado.causa == "NO CUMPLE ANTIGÜEDAD":
                messages.error(request, f"Lo sentimos {asociado.nombre}, no cumples con la antigüedad mínima para aplicar a un obsequio.")
            else:
                request.session.update({
                    'name': asociado.nombre,
                    'state': asociado.state,
                    'description': asociado.obsequio
                })
                preaprobado = {
                    'prestamo': int(asociado.preaprobado) > 0,
                    'monto': setValue(asociado.preaprobado),
                    'cuota': setValue(asociado.cuota),
                    'plazo': asociado.plazo
                }
                return render(request, 'index.html', {
                    'asociado': asociado,
                    'prestamo': preaprobado
                })
            
        elif form == "form_entrega":
            try:
                with transaction.atomic():
                    EntregaObsequio.objects.create(
                        nombre=request.session.get('name'),
                        documento=request.session.get('cedula'),
                        sucursal=request.session.get('lugar'),
                        estado=request.session.get('state'),
                        obsequio=request.session.get('description'),
                        asesor=request.session.get('asesor'),
                        razonDeEntrega=request.POST.get("razon", "")
                    )
                messages.success(request, "Se ha registrado con éxito la entrega.")
            except Exception as e:
                messages.error(request, f"Ocurrió un error al registrar la entrega: {str(e)}")
            
    return render(request, 'index.html', {'sucursales': sucursales, 'asesores': asesores, 'entregas': entregasTotales})
# def index(request):
#     asociado = None
#     sucursales = Sucursal.objects.all().order_by("nombre")
#     asesores = Asesor.objects.all().order_by("nombre")
#     # entregasTotales = [
#     #     {
#     #         'nombre': registro.nombre,
#     #         'numero_entregas': EntregaObsequio.objects.filter(sucursal=registro.nombre).count()
#     #     }
#     #     for registro in sucursales
#     # ]
    
#     if request.method == 'POST':
#         form = request.POST.get("form_id")
#         if form == "form-consulta":
#             asesor = request.POST.get("quien_entrega")
#             request.session['asesor'] = asesor
            
#             lugar = request.POST.get("medio_entrega", "").strip()
#             request.session['lugar'] = lugar
            
#             cedula = request.POST.get("cedula", "").strip()
#             request.session['cedula'] = cedula
            
#             entrega = EntregaObsequio.objects.filter(documento=cedula)
#             if entrega:
#                 fecha_local = str(localtime(entrega[0].fecha)).split(".")

#                 messages.info(request, f"Ya se realizo la entrega a {entrega[0].nombre} el dia {fecha_local[0]} en {entrega[0].sucursal} por {entrega[0].asesor}.")
#                 return render(request, 'index.html', {'sucursales': sucursales, 'asesores': asesores})
            
#             asociado = Asociados.objects.filter(documento=cedula)
#             if len(asociado) == 0:
#                 messages.error(request, "No se encontro ningun asociado con ese numero de identificación.")
#                 return render(request, 'index.html', {'sucursales': sucursales, 'asesores': asesores})
            
#             if asociado[0].tipo == "EMPRESA":
#                 messages.error(request, f"Lo sentimos {asociado[0].nombre}, los obsequios de fidelización no aplican para empresas.")
#                 return render(request, 'index.html', {'sucursales': sucursales, 'asesores': asesores})

#             if asociado[0].obsequio == "NO CUMPLE ANTIGÜEDAD" and asociado[0].causa == "NO CUMPLE ANTIGÜEDAD":
#                 messages.error(request, f"Lo sentimos {asociado[0].nombre}, no cumples con la antigüedad  mínima para aplicar a un obsequio.")
#                 return render(request, 'index.html', {'sucursales': sucursales, 'asesores': asesores})
            
#             if asociado:
#                 request.session['name'] = asociado[0].nombre
#                 request.session['state'] = asociado[0].state
#                 request.session['description'] = asociado[0].obsequio
            
#         if form == "form_entrega":
#             if request.POST.get("razon"):
#                 razon = request.POST.get("razon")
#             else:
#                 razon = ""
#             cedula = request.session.get('cedula', None)
#             lugar = request.session.get('lugar', None)
#             asesor = request.session.get('asesor', None)
#             name = request.session.get('name', None)
#             state = request.session.get('state', None)
#             description = request.session.get('description', None)
#             registro = EntregaObsequio(
#                 nombre=name,
#                 documento=cedula,
#                 sucursal=lugar,
#                 estado=state,
#                 obsequio=description,
#                 asesor=asesor,
#                 razonDeEntrega=razon
#             )
#             registro.save()
            
#             messages.success(request, "Se ha registrado con éxito la entrega.")
            
#             return render(request, 'index.html', {'sucursales': sucursales, 'asesores': asesores})
#         preaprobado = {
#             'prestamo': int(asociado[0].preaprobado) > 0,
#             'monto': setValue(asociado[0].preaprobado),
#             'cuota': setValue(asociado[0].cuota),
#             'plazo': asociado[0].plazo
#         }
#         return render(request, 'index.html', {
#                 'asociado': asociado[0],
#                 'prestamo': preaprobado
#                 })
#     return render(request, 'index.html', {'sucursales': sucursales, 'asesores': asesores})
#     # return render(request, 'index.html', {'sucursales': sucursales, 'asesores': asesores, 'entregas': entregasTotales})


def close(request):
    return redirect ('index')