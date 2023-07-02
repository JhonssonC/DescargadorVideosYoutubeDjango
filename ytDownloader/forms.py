from django import forms
from ytDownloader.models import Video

class VideoForm(forms.Form):
    
    # def __init__(self, resoluciones=()):
    #     self.resluciones=forms.Field(
    #         widget=forms.widgets.Select(choices=resoluciones,
    #             attrs={
    #                 "class": "form-select"
    #             }
    #         ),
    #         label="Criterio de Búsqueda",
    #     )
    
    enlace = forms.CharField(
       max_length=120,
       required=True,
       widget=forms.widgets.Input (
           attrs={
               "class": "form-control form-control-lg"
           }
       ),
       label="Enlace"
       )

    titulo = forms.CharField(
       max_length=120,
       required=True,
       widget=forms.widgets.Input (
           attrs={
               "class": "form-control form-control-lg",
               "readonly": True
           }
       ),
       label="Titulo de Video"
       )

    resluciones = forms.Field(
       widget=forms.widgets.Select(choices=(),
           attrs={
            "class": "form-select form-select-lg mb-3"
           }
       ),
       label="Resoluciones Disponibles",
    )



    class Meta:
      model = Video
      exclude = ("user",)