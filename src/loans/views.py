
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework import generics

from .models import LoanRequest
from .serializers import LoanRequestSerializer, LoanRequestUpdateStatusSerializer
from treyd.permissions import IsOwner


class LoanRequestList(generics.ListCreateAPIView):
    queryset = LoanRequest.objects.all()
    serializer_class = LoanRequestSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoanRequestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LoanRequest.objects.all()
    serializer_class = LoanRequestSerializer
    permission_classes = [IsOwner]
    http_method_names = ['get', 'patch', 'delete']

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [permissions.IsAdminUser|IsOwner]
        return super().get_permissions()

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != 'pending':
            return Response({'status': 'cannot update loan request that is not pending'}, status=status.HTTP_400_BAD_REQUEST)
        return super().patch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != 'pending':
            return Response({'status': 'cannot delete loan request that is not pending'}, status=status.HTTP_400_BAD_REQUEST)
        return super().delete(request, *args, **kwargs)

class LoanRequestStatusUpdate(generics.UpdateAPIView):
    queryset = LoanRequest.objects.all()
    serializer_class = LoanRequestUpdateStatusSerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ['patch']