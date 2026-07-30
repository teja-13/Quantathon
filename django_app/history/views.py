from django.shortcuts import redirect
from django.views import View

class HistoryRedirectView(View):
    def get(self, request):
        return redirect('reports:history')
