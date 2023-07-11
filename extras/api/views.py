from django.http import Http404
from facts.models import Fact
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import FactSerializer


class FactList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        facts = Fact.objects.all()
        serializer = FactSerializer(facts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FactDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_fact(self, id):
        try:
            return Fact.objects.get(id=id)
        except Fact.DoesNotExist:
            raise Http404

    def get(self, request, id):
        fact = self.get_fact(id)
        serializer = FactSerializer(fact)
        return Response(serializer.data)

    def put(self, request, id):
        fact = self.get_fact(id)
        serializer = FactSerializer(fact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        fact = self.get_fact(id)
        fact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
