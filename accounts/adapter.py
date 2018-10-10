from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.signals import pre_social_login
from allauth.account.models import EmailAddress
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class MyLoginAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        """ 
        """
        if request.user.is_authenticated:
            return settings.LOGIN_REDIRECT_URL.format(
                id=request.user.id)
        else:
            return "/"


class MySocialAccountAdapter(DefaultSocialAccountAdapter):

#     def pre_social_login(self, request, sociallogin):
#         pass    # TODOFuture: To perform some actions right after successful login

# @receiver(pre_social_login)
    def pre_social_login(self, request, sociallogin):
        # Ignore existing social accounts, just do this stuff for new ones
        if sociallogin.is_existing:
            return

        # some social logins don't have an email address, e.g. facebook accounts
        # with mobile numbers only, but allauth takes care of this case so just
        # ignore it
        if 'email' not in sociallogin.account.extra_data:
            return

        # check if given email address already exists.
        # Note: __iexact is used to ignore cases
        try:
            email = sociallogin.account.extra_data['email'].lower()
            email_address = EmailAddress.objects.get(email__iexact=email)

        # if it does not, let allauth take care of this new social account
        except EmailAddress.DoesNotExist:
            return

        # if it does, connect this new social login to the existing user
        user = email_address.user
        sociallogin.connect(request, user)