import random
import string
import secrets
from django.utils import timezone
from users.models import MailAuth

def verification_code():
    """6 haneli rastgele bir kod üreten fonksiyon"""
    characters = string.ascii_letters + string.digits
    code = ''
    for i in range(6):
        code += random.choice(characters)
    return code 

def verification_token(length=128):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))

def create_mail_auth(username,temptoken,verifycode):
    mailauth = MailAuth(username=username, temptoken=temptoken, verifycode=verifycode, logintime=timezone.now())
    mailauth.save()


def is_mailauth_valid(mailauth, seconds):
    creation_time = mailauth.logintime
    current_time = timezone.now()
    elapsed_time = current_time - creation_time
    return elapsed_time.seconds < seconds