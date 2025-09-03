from django.db import models
import bcrypt

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150,unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)

    def set_password(self,raw_password):
        hashed = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
        self.password = hashed.decode('utf-8')

    def check_password(self,raw_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'),self.password.encode('utf-8'))
    
    def __str__(self):
        return self.username
