# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from django.shortcuts import render, HttpResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *

from django.forms.models import model_to_dict


# Create your views here.

class TurkUserViewSet(viewsets.ModelViewSet):
    queryset = TurkUser.objects.all()
    serializer_class = TurkUserSerializer


class LoadTurkUserViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    queryset = TurkUser.objects.all()
    serializer_class = TurkUserSerializer


class LoginTurkUserViewSet(viewsets.ModelViewSet):
    # queryset = TurkUser.objects.all()
    # serializer_class = TurkUserSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (AllowAny,)

    def create(self, request, format=None):

        email = request.data.get('email', None)
        password = request.data.get('password', None)

        if TurkUser.objects.filter(email=email, password=password).exists():
            requested_user = TurkUser.objects.get(email=email, password=password)
            returned_user = model_to_dict(requested_user)
            del returned_user['password']
            returned_dict = {
                'user': returned_user
            }
            return Response(returned_dict, status=status.HTTP_202_ACCEPTED)
        else:
            requested_user = {'error': 'invalid credentials'}
            return Response(requested_user, status=status.HTTP_404_NOT_FOUND)


class LogoutTurkUserViewSet(viewsets.ModelViewSet):
    def create(self, request, format=None):
        response_dict = {'logout': 'succesfully'}
        return Response(response_dict, status=status.HTTP_202_ACCEPTED)


# ========================================================================================================================
# ========================================================================================================================
# ================================================ ROHAN =================================================================
# ========================================================================================================================
# ========================================================================================================================


class SysDemandViewSet(viewsets.ModelViewSet):
    queryset = SystemDemand.objects.all()
    serializer_class = SysDemandSerializer

    # def create(self, request, format=None):
    #     # this doesn't make sense just for testing
    #     if SystemDemand.objects.all():
    #         systemDemans = SystemDemand.objects.all()
    #         return Response(systemDemans, status=status.HTTP_202_ACCEPTED)

class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer


# ========================================================================================================================
# ========================================================================================================================
# ================================================ SAMMIE ================================================================
# ========================================================================================================================
# ========================================================================================================================










# ========================================================================================================================
# ========================================================================================================================
# ================================================ ENZO ==================================================================
# ========================================================================================================================
# ========================================================================================================================



class RegisterViewSet(viewsets.ModelViewSet):
    def create(self, request, format=None):
        print("\nREQUEST:::\n")
        print(request)
        print(request.data)
        TurkUsers = TurkUser.objects.all()
        name = request.data.get('firstname', None)
        lastname = request.data.get('lastname', None)
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        registerdata = {
            'name': name,
            'lastname': lastname,
            'email': email,
            'password': password
        }

        if TurkUsers.filter(email=email).exists():
            response = {'error': 'There already exists a user associated with this email'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        else:
            if BlackList.objects.filter(user__email=email).exists():
                reason = BlackList.objects.get(user__email=email).reason
                response = {'error': reason}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = RegisterSerializer(data=registerdata)
                if serializer.is_valid():

                    register_information = serializer.create(serializer.validated_data)
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    print(serializer.errors)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)