from django.db import models
from django.urls import reverse
from utils.base_model import BaseModel
from home.model_field_validations import unit_price_validation
from django.db.models import Avg,Max,Min,Count
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField


class Product(BaseModel):
    class Meta:
        ordering = ('-created',)

    STATUS = (
        ('none', 'None'),
        ('size', 'Size'),


    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    image = models.ImageField(upload_to='products/')
    description = RichTextField(blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0,validators=[unit_price_validation])
    available_products = models.BooleanField()
    stock = models.IntegerField(default=0)
    tags = TaggableManager(blank=True)
    like_product = models.ManyToManyField('accounts.User', related_name='liked_products', blank=True)
    diet_category = models.ForeignKey('DietCategory', on_delete=models.PROTECT, related_name='diet_category', null=True)
    main_menu = models.ForeignKey('MainMenu', on_delete=models.PROTECT, related_name='main_menu', null=True)
    menu_item = models.ForeignKey('MenuItem', on_delete=models.PROTECT, related_name='menu_item', null=True)
    status = models.CharField(choices=STATUS, max_length=6, default='none')
    discount = models.PositiveIntegerField(default=0)
    size = models.ManyToManyField('Size', related_name='size', blank=True)
    sell = models.IntegerField(default=0)
    favourite = models.ManyToManyField('accounts.User', related_name='fav_user', blank=True)
    total_favourite = models.IntegerField(default=0)
    view = models.ManyToManyField('accounts.User', related_name='product_view', blank=True)
    num_views = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:details', args=(self.id, self.slug))

    @property
    def final_price(self):
        final_price = self.unit_price
        if self.discount:
            final_price = (100 - self.discount) * final_price / 100

        return final_price

    @property
    def average(self):
        data = Comment.objects.filter(product=self, is_reply=False).aggregate(avg=Avg('rate'))
        star = 0
        if data['avg'] is not None:
            star = round(data['avg'], 1)
        return star

    @property
    def num_comments(self):
        data = Comment.objects.filter(product=self,is_reply=False).aggregate(counts=Count('body'))
        star = 0
        if data['counts'] is not None:
            star = int(data['counts'])
        return star

    @property
    def likes_count(self):
        return self.like_product.count()

    def like_checkers(self,user):
        if self.like_product.filter(id=user.id).exists():
            return 'fa-solid'
        return 'fa-regular'

    # def reply_count(self):
    #     data = Comment.objects.filter(is_reply=True,product=self).aggregate(counts=Count('body'))
    #     star = 0
    #     if data['counts'] is not None:
    #         star = int(data['counts'])
    #     return star


class DietCategory(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    image = models.ImageField(upload_to='products/')
    available = models.BooleanField()

    def __str__(self):
        return self.name


class MainMenu(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True,null=True)
    available = models.BooleanField()

    def __str__(self):
        return self.name


class MenuItem(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    available = models.BooleanField(default=False)
    main_menu = models.ForeignKey('MainMenu',on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    name = models.CharField(max_length=255,blank=True)
    image = models.ImageField(upload_to='products/product_images/')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='product_images')


class Comment(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='user_comment')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_cms')
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE,related_name='replies', null=True,blank=True)
    liked_comment = models.ManyToManyField('accounts.User', 'liked_comments', blank=True)
    disliked_comment= models.ManyToManyField('accounts.User', 'disliked_comments', blank=True)
    rate = models.IntegerField(null=True,blank=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    # verified = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name

    @property
    def like_count(self):
        return self.liked_comment.count()

    @property
    def dislike_count(self):
        return self.disliked_comment.count()


    # def like_checker(self, user):
    #     if self.liked_comment.filter(id=user.id).exists():
    #         return 'fa-solid'
    #
    #     return 'fa-regular'

    # @property
    # def comment_count(self):
    #     return self.body.count()
class PriceChange(models.Model):
    product = models.ForeignKey('Product', models.CASCADE, 'changes', null=True)
    variant = models.ForeignKey('Variant', models.CASCADE, 'var_changes', null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0,validators=[unit_price_validation])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if not self.variant:
            return self.product.name

        return self.variant.product.name


class Size(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CookedSteak(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Variant(BaseModel):
    product = models.ForeignKey('Product', models.CASCADE, 'p_variants')
    size = models.ForeignKey('Size', models.SET_NULL, null=True, related_name='s_variants')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0,validators=[unit_price_validation])
    discount = models.PositiveIntegerField(default=0)
    available = models.BooleanField()
    stock = models.PositiveIntegerField()
    sell = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.product.name} - {self.size.name}'

    @property
    def final_price(self):
        final_p = self.unit_price
        if self.discount:
            final_p = (100 - self.discount) * final_p / 100

        return final_p


class Views(models.Model):
    ip = models.CharField(max_length=255,null=True,blank=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='views')
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name
