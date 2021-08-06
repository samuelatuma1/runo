
from django.contrib.auth.models import User

class EmailAuth(object):
    def authenticate(self, request, username=None, password=None):
        user = User.objects.filter(email=username).first()
        if user is not None:
            if user.check_password(password):
                return user
            else:
                return None
        
        return None
    
    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user
        except:
            return None