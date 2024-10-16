from django.middleware.csrf import CsrfViewMiddleware

class CustomCsrfMiddleware(CsrfViewMiddleware):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        # Try to read the CSRF token from 'X-CSRF-Token'
        # Custom header with additional dash after CSRF
        # Going with the Rails format, as happen to have implemented front-end for that first
        if 'HTTP_X_CSRF_TOKEN' in request.META:
            request.META['HTTP_X_CSRFTOKEN'] = request.META['HTTP_X_CSRF_TOKEN']

        # Call the default CSRF middleware process
        return super().process_view(request, callback, callback_args, callback_kwargs)