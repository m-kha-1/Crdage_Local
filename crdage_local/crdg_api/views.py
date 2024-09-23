from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import os
import shutil
import subprocess
# Create your views here.


# organization="C:/CORD"
organization="C:\cordage_service\crdage_local\media"
nameProd="testtestProd"
# @csrf_exempt
# def make_production_directories(request,nameprod):
   
#    try: 
#         path= os.path.join(organization,nameprod)
#         os.makedirs(path)
#         return JsonResponse({"dossiers": f"créés {path}"},status=200)
#    except Exception as e:
#         return JsonResponse({"erreur": str(e)},status=500)
   
   
   
@csrf_exempt
def make_production_directories(request,nameprod):
     subfolders = ["presentation","lighting", "animation", "modelling","fx","compositing","surfacing","rigging"]

     try: 
        path= os.path.join(organization,nameprod)
        os.makedirs(path)
        for subfolder in subfolders:
             os.makedirs(os.path.join(path, subfolder), exist_ok=True)
             
        
        
        return JsonResponse({"dossiers": f"créés {path}"},status=200)
     except Exception as e:
        return JsonResponse({"erreur": str(e)},status=500)
   
   
   
@csrf_exempt
   
def make_task_directories(request,nameprod,nametask,nametasktype,namecgartist):
        print("données=",nameprod,nametask,nametasktype,namecgartist)
        
        pathTask_work=os.path.join(organization,nameprod,nametasktype,nametask,"WORK",namecgartist,"scenes")
        pathTask_publish=os.path.join(organization,nameprod,nametasktype,nametask,"PUBLISH","scenes") 
        pathTask_publish_images=os.path.join(organization,nameprod,nametasktype,nametask,"PUBLISH","images","V01")
        
        if not os.path.exists(pathTask_work):
             os.makedirs(pathTask_work)
        if not os.path.exists(pathTask_publish):
             os.makedirs(pathTask_publish)
        if not os.path.exists(pathTask_publish_images):
             os.makedirs(pathTask_publish_images)
        fileName=nametasktype+"_"+nametask+"_V001"
        print("fileName:", fileName)
        shutil.copy("C:\\CORD\\scripts\\empty.blend",pathTask_publish+"\\"+nametasktype+"_"+nametask+"_V01.blend")
        shutil.copy("C:\\CORD\\empty.png",pathTask_publish_images+"\\"+nametasktype+"_"+nametask+"_V01.png")
        
      
        
        
        return JsonResponse({"données":  [nameprod,nametask]},status=200)
   
   
   
   
   

@api_view(['GET'])
# def liste_images(request,organization, nameprod, nametask, nametasktype,namecgartist):
def liste_images(request, nameprod, nametask, nametasktype):
   
#     stockage=Stockage.objects.get(name=organization)
    
    stockage="C:\cordage_service\crdage_local\media"
#     base_dir = os.path.join(stockage.media_root, np, tt, nt, 'PUBLISH')
    base_dir = os.path.join(stockage, nameprod, nametask, nametasktype, 'PUBLISH')
    
    
    try :
        if not os.path.exists(base_dir):
            return JsonResponse({'message': str(base_dir)+'Directory does not exist'},status=404)
        
        all_files = [os.path.join(root, file)
                    for root, dirs, files in os.walk(base_dir)
                    for file in files
                    if file.endswith('.png')]
        
        return Response(all_files, status=200)
          

    except Exception as e:
        return Response({'message':str(e)},status=500)
   
   
   
   
   
@api_view(['GET'])
def liste_scenes(request, nameprod, nametask, nametasktype):
    
    # organization="dev"
#     stockage=Stockage.objects.get(name=organization)
     stockage="C:\cordage_service\crdage_local\media"
     
     base_dir = os.path.join(stockage, nameprod, nametask, nametasktype, 'PUBLISH')

     try:
        # Vérifier si le répertoire existe
        if not os.path.exists(base_dir):
            return JsonResponse({'message': 'Directory does not exist'}, status=404)

        
        all_files = [os.path.join(root, file)
                     for root, dirs, files in os.walk(base_dir)
                     for file in files
                     if file.endswith('.blend')]

        return JsonResponse(all_files, safe=False)
   
     except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
    
    
    

@csrf_exempt

@api_view(['POST'])
def lancer_scene(request):
    # Extraire le chemin du fichier .blend des données POST
    blend_file_path = request.data.get('blend_file_path')

    # Vérifier si le chemin du fichier est fourni et valide
    if not blend_file_path or not os.path.exists(blend_file_path):
        return JsonResponse({'message': 'Invalid or non-existent file path'}, status=400)

    # Chemin vers l'exécutable Blender
    blender_path = r"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe"
    
    try:
        # Lancer Blender avec le fichier .blend
        subprocess.Popen([blender_path, blend_file_path])
        return JsonResponse({'message': 'Scene launched successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
    
    
    
    
@api_view(['GET'])
def get_vignette(request, nameprod):
    try:
        vignettes=os.listdir(f"C:\cordage_service\crdage_local\media\{nameprod}\presentation")
        if vignettes:
            dict={"vignette":vignettes[0]}
            return JsonResponse(dict,status=200)
        else:
            return JsonResponse({"vignette":"imageParDefaut"},status=200)
    except Exception as e:
        return JsonResponse({"error":str(e)},status=500)