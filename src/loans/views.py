
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import permission_classes

from .models import LoanRequest
from .serializers import LoanRequestSerializer, LoanRequestUpdateStatusSerializer
from treyd.permissions import IsOwner
from django.http import HttpResponse
from openpyxl import load_workbook
from django.conf import settings
from django.shortcuts import get_object_or_404


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
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance and instance.status == 'pending' and not request.user.is_staff:
            return Response({'status': 'cannot view pending loan request'}, status=status.HTTP_400_BAD_REQUEST)
        return super().get(request, *args, **kwargs)

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


@permission_classes([permissions.IsAuthenticated])
def loan_amortization_schedule(request):
    # Get the user’s loan data from the database
    loan_data = get_object_or_404(LoanRequest, user_id=request.user.id)

    # Load the template workbook
    template_path = settings.BASE_DIR / 'templates' / 'loan-amortization-schedule_template.xlsx'
    workbook = load_workbook(template_path)
    sheet = workbook.active

    # Fill the template with loan data from the database
    # Example: assuming columns in template are B2, B3, etc.
    sheet['D5'] = loan_data.amount
    sheet['D6'] = loan_data.term
    sheet['D7'] = '7%'

    # Add any other necessary data to fill in the template

    # Set the HTTP response for file download
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=loan_schedule_{request.user.id}.xlsx'

    # Save the workbook to the response
    workbook.save(response)

    return response
