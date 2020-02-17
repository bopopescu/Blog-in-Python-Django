from django.db import models

# Create your models here.
class tb_address_book(models.Model):
   class Meta:
        db_table = 'tb_address_book'
   id = models.AutoField(primary_key=True)
   #or id = models.PositiveIntegerField(primary_key=True) or id = models.BigIntegerField(primary_key=True)
   First_Name = models.CharField(max_length = 50)
   Surname  = models.CharField(max_length = 50)
   Address = models.CharField(max_length = 250)

class userRecord(models.Model):
   class Meta:
        db_table = 'userRecord'
   id = models.AutoField(primary_key=True)
   FullName = models.CharField(max_length = 250)
   userID  = models.CharField(max_length = 250)
   userPassword = models.CharField(max_length = 250)
   
class postRecord(models.Model):
  class Meta:
       db_table = 'postRecord'
  id = models.AutoField(primary_key=True)
  author = models.CharField(max_length = 250)
  postId = models.CharField(max_length = 250)
  postTitle  = models.CharField(max_length = 250)
  postBody = models.TextField()
  postType = models.CharField(max_length = 50)
  postDate = models.DateTimeField()
  del_status = models.CharField(max_length = 10)