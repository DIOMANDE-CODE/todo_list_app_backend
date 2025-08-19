from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.

def default_photo_profil():
    return 'default/photo-profil-defaut.jpg'

class UtilisateurManager(BaseUserManager):
    def create_user(self, account_email, password=None, **extra_fields):
        if not account_email:
            raise ValueError("Veuillez entrer votre email")
        
        account_email = self.normalize_email(account_email)
        user = self.model(account_email=account_email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, account_email,password=None, **extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_active",True)
        extra_fields.setdefault("is_superuser",True)
        return self.create_user(account_email,password,**extra_fields)  
    

class Utilisateur(AbstractBaseUser, PermissionsMixin):
    account_email = models.EmailField(unique=True, verbose_name="Votre email")
    account_name = models.CharField(max_length=200, verbose_name="Votre nom et prenoms")
    account_image = models.ImageField(upload_to='photo_profil/', default=default_photo_profil) # Ajout de photo de profil 
    account_created = models.DateTimeField(auto_now_add=True) # Date création
    account_updated = models.DateTimeField(auto_now=True) # Date modification   
    
    # Role
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'account_email'
    REQUIRED_FIELDS = []

    objects = UtilisateurManager()

    def __str__(self):
        return self.account_email