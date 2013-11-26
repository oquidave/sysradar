from django.shortcuts import render, render_to_response
from django.http import HttpResponse 
from django.template import Context
from radar.server_radar.checkserver import Radar
from monitor.models import Box, Service


# Create your views here.

def check_serverip(request):
    ip = request.GET.get('ip', '')
    radar = Radar()
    box_status = radar.box_alive(ip)
    return HttpResponse("The Box with IP: %s is %s" % (ip, box_status))
    
def check_service(request):
    service = request.GET.get('service', '')
    port = request.GET.get('port', '')
    port = int(port)
    ip = request.GET.get('ip', '')
    if not ip:
        ip = "127.0.0.1"
    radar = Radar()
    service_status = radar.service_check(ip, port)
    return HttpResponse("Service running on port %s on box with IP: %s is %s" % (port, ip, service_status))
    
def add_box(request):
    ip = request.GET.get('ip', '')
    box_name =  request.GET.get('box_name', '')
    "add a new box"
    try:
        box = Box(ip=ip, box_name=box_name)
        print("ip: "+ ip + " box_name: "+box_name)
        box.save()
        return HttpResponse("added the box %s with name %s " % (ip, box_name))
    except:
        return HttpResponse('There was an error')
        
def update_box(request):
    theproperty = request.GET.get("theproperty", "")
    oldvalue = request.GET.get("oldvalue", "")
    newvalue = request.GET.get("newvalue", "")
    if theproperty != "ip" or theproperty != "box_name":
        return HttpResponse("There was a error updating a box")
    else:
        box = Box.objects.get(theproperty=oldvalue)
        box.theproperty = newvalue
        box.save()
        return HttpResponse("The property %s has been updated: " % theproperty)
        
def get_boxes(request):
    boxes = Box.objects.all()
    #{"boxes_ip":boxes.ip, "boxes_name":boxes.box_name})
    return render_to_response("show_boxes.html", 
                              {"boxes":boxes})
        

def get_box_id(box_name):
    try:
        box_id = Box.objects.get(box_name=box_name)
        return box_id
    except : 
        print("there was error")
        return False
                    
def add_service(request):
    box_name = request.GET.get("box_name", "")
    service_name = request.GET.get("service_name", "")
    service_port = request.GET.get("service_port", "")
    try:
        service = Service(service_name=service_name, service_port=service_port, box=Box.objects.get(box_name=box_name))
        service.save()
        return True
    except :
        print("there was an error")
        return False
 
def update_service(request):
    theproperty = request.GET.get("theproperty", "")
    oldvalue = request.GET.get("oldvalue", "")
    newvalue = request.GET.get("newvalue", "")
    if theproperty != "service_name" or theproperty != "service_port":
        return False
    else:
        #Service.objects.filter(service_name="apache").update(service_name="apachee")
        service = Service.objects.get(theproperty=oldvalue)
        service.theproperty = newvalue
        service.save()


def get_box_services(request):
    box_id = request.GET.get("box_id", "")
    box_services = Service.objects.filter(box_id=box_id).values()
    return render_to_response("box_services.html", 
                       {"box_services":box_services})
    
def check_box_services(request):
    r = Radar()
    box_id = request.GET.get("box_id", "")
    ip = request.GET.get("ip", "")
    box_services = Service.objects.filter(box_id=box_id)
    services = []
    for box_service in box_services:
        service = {}
        service_port = box_service.service_port
        service_name = box_service.service_name
        service_status = r.service_check(ip, service_port)
        service["service_port"] = service_port
        service["service_name"] = service_name
        service["service_status"] = service_status
        service["daemon"] = box_service.daemon
        
        print ('service_name %s service_port %s service_status %s ' % (service_name, service_port, service_status))
        print service
        services.append(service)
        
    print services
    return render_to_response("box_services_status.html", 
                               {"box_services":services})

def service_control(request):
    r = Radar()
    action = request.GET.get("action", "")
    daemon = request.GET.get("daemon", "")
    password = "davesuse"
    status = r.service_control(daemon, action, password)
    #check_box_services(request)
    return HttpResponse("action %s taken for daemon %s " % (action, daemon))
        
    
    
    
    
    
    
            
