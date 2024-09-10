from django.urls import path
from .views import make_production_directories,make_task_directories,liste_images,liste_scenes,lancer_scene,get_vignette

urlpatterns = [
    path('make_production_directories/<str:nameprod>',make_production_directories,name="make_directories"),
    path('make_task_directories/<str:nameprod>/<str:nametask>/<str:nametasktype>/<str:namecgartist>',make_task_directories,name="make_task_directories"),
    path('listei/<str:nameprod>/<str:nametask>/<str:nametasktype>',liste_images,name="liste_images"),
    path('listes/<str:nameprod>/<str:nametask>/<str:nametasktype>',liste_scenes,name="liste_scenes"),
    path('lancer_scene', lancer_scene, name='lancer_scene'),
    path('vignette/<str:nameprod>',get_vignette)

]
