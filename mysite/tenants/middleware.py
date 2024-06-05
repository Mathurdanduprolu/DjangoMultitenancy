from django.http import HttpResponseForbidden, HttpResponse
from .models import Tenant

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        domain = request.get_host().split(':')[0]
        print("middleware call was made")
        print(f"Debug: domain={domain}")
        try:
            tenant = Tenant.objects.get(domain=domain)
            request.tenant = tenant
            print(f"Debug: Found tenant: {tenant.name}")
        except Tenant.DoesNotExist:
            print("Debug: Tenant not found")
            return HttpResponseForbidden('Tenant not found')
        except Exception as e:
            print(f"Debug: Exception occurred: {e}")
            return HttpResponse(f"Error: {str(e)}", status=500)

        response = self.get_response(request)
        return response