from django.db import models

# Create your models here.
class Users(models.Model):
    uphone = models.CharField(max_length=30, verbose_name='手機號')
    upass = models.CharField(max_length=50)
    uemail = models.EmailField(verbose_name='信箱')
    uname = models.CharField(max_length=30, null=True, verbose_name='用戶名')
    isActive = models.BooleanField(default=True, verbose_name='啟用')

    def __str__(self):
        return self.uname

    class Meta:
        db_table = 'users'
        verbose_name = '用戶名'
        # 將用戶名s去掉
        verbose_name_plural = verbose_name