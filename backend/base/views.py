from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

import io
from PIL import Image as im
from django.conf import settings

from .modelsDjango import Conclusion, Data, Manual
from django.core.files.base import ContentFile


from .serializers import *

# ------for calculations------
import math
# ------endfor calculations-----

# -----for yolo----------
from pathlib import Path
import torch
import torch.backends.cudnn as cudnn
import numpy
import json
import base64
# -------endfor yolo-------


# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView

# # Create your views here.

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Add custom claims
#         token['username'] = user.username
#         # ...

#         return token

# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer


def haversine(lon1, lat1, lon2, lat2):

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))

    r = 6371
    return round(c * r * 100, 2)


@api_view(['GET'])
def updator(request):
    data = Data.objects.all()
    for i in data:
        count = 0
        viable = []
        for j in data:
            if haversine(i.longitude, i.latitude, j.longitude, j.latitude) < 3:
                count += 1
                viable.append(j)
                ("http://127.0.0.1:8000/static/images/503.jpg")
        if count >= 1:
            allPreds = []
            f_name = []
            for k in viable:
                f_name.append(str(k.capture))
            for f in f_name:
                torch.hub.download_url_to_file(
                    'http://127.0.0.1:8000/static/images/' + f, f)
                img = im.open(f)
                width, height = img.size

            path_hubconfig = 'D:/Renaissance/projectPorthole/backend/yolov5'
            path_weightfile = 'D:/Renaissance/projectPorthole/backend/yolov5/models/last.pt'

            model = torch.hub.load(
                path_hubconfig, 'custom', path=path_weightfile, source='local')

            results = model(img, size=640)
            df = results.pandas().xyxy[0]
            print(df)
            results.show()
            allPreds = df.to_numpy()

            res = [0] * 9
            if len(allPreds) > 0:
                for m in allPreds:
                    x = (m[0]+m[2])/2
                    y = (m[1]+m[3])/2
                    if x < width/3:
                        if y < (0.5*height):
                            res[6] += 1
                        elif y > (0.5*height) and y <= (0.8*height):
                            res[3] += 1
                        elif y > 400 and y < height:
                            res[0] += 1
                    if x > width/3 and x <= 2*(width/3):
                        if y < (0.5*height):
                            res[7] += 1
                        elif y > (0.5*height) and y <= (0.8*height):
                            res[4] += 1
                        elif y > (0.8*height) and y < height:
                            res[1] += 1
                    if x > 2*(width/3) and x <= width:
                        if y < (0.5*height):
                            res[8] += 1
                        elif y > (0.5*height) and y <= (0.8*height):
                            res[5] += 1
                        elif y > (0.8*height) and y < height:
                            res[2] += 1

            print(res)

            c = Conclusion(
                latitude=i.latitude,
                longitude=i.longitude,
                v1=res[0],
                v2=res[1],
                v3=res[2],
                v4=res[3],
                v5=res[4],
                v6=res[5],
                v7=res[6],
                v8=res[7],
                v9=res[8],
            )
            c.save()

    return Response("Updation Successful")


@api_view(['POST'])
def getConclusion(request):
    data = request.data
    print("/////////", data)
    allConclusions = Conclusion.objects.all()
    for i in allConclusions:
        if haversine(float(data['lon']), float(data['lat']), i.longitude, i.latitude) <= 3:
            serializer = ConclusionSerializer(i, many=False)
            return Response(serializer.data)
    return Response("Nothing found")


@api_view(['POST'])
def uploadImage(request):
    data = request.data
    format, imgstr = data['image'].split(';base64,')
    ext = format.split('/')[-1]

    # You can save this as file instance.
    imageData = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
    user = User.objects.get(username='admin')
    adder = Data.objects.create(
        user=user,
        latitude=float(data['lat']),
        longitude=float(data['lon']),
        capture=imageData
    )
    serializer = DataSerializer(adder, many=False)

    # arr = ['image', 'secImage']
    # count = 0
    # for i in arr:
    #     count += 1
    #     if isinstance(request.FILES.get(i), type(None)) != 1:
    #         if count == 1:
    #             product.image = request.FILES.get(i)
    #         if count == 2:
    #             product.secImage = request.FILES.get(i)
    # product.save()
    

    return Response(serializer.data)