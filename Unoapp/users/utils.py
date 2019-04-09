import uuid
import jwt,json
from django.http import HttpResponse
from rest_framework import views
import bleach
from django.core.mail import EmailMessage
from rest_framework_simplejwt.settings import api_settings

from Unoapp.settings import EMAIL_HOST_USER, SECRET_KEY
from users.models import Profile, UserConfirmation


class Register():

    def __init__(self):
        pass


    def register1(self,email,password,fname,lname):
        newuser , is_created = Profile.objects.get_or_create(
            email = email.strip().lower(),
            first_name = fname,
            last_name = lname,
            username = email.strip().lower().replace('@','-')
        )
        newuser.set_password(password)
        newuser.save()


        if is_created:

            token = str(uuid.uuid1())
            user = Profile.objects.get(email =email.strip().lower())
            user_confirmation , is_created =UserConfirmation.objects.get_or_create(
                user_id =user.id,
                token = token
            )

            msg = 'To verify your email click on the link = '+ '127.0.0.1:8000/users/verify-email'+email+'/token'+token.format(

            email=email,
            token=token
                )
            html = bleach.linkify(msg)
            msg =html
            subject = 'Welcome to Test project'
            email = EmailMessage(
            subject=subject,
            body=msg,
            to=[email],
            from_email=EMAIL_HOST_USER,)
            email.send()



# class  AuthenticationToken(object):
#     """
#     Takes user object and returns JW Token
#     """
#
#     def __new__(cls, user, *args, **kwargs):
#         jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
#         jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
#         payload = jwt_payload_handler(user)
#         token = jwt_encode_handler(payload)
#         return token

class AuthenticationToken():

    def __init__(self,user):
        self.user =user
        pass

    def authenticate(self,user):
        payload = {
                'id': user.id,
                'email': user.email,
            }
        jwt_token = {'token': jwt.encode(payload, SECRET_KEY)}

        return jwt_token

        # return HttpResponse(
        #           json.dumps(jwt_token),
        #           status=200,
        #           content_type="application/json"
        #         )
