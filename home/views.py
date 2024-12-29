from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from home.forms import *
from cart.forms import CartForm
from home.models import Product, DietCategory, MainMenu, Comment, Image, MenuItem, Variant, Size, Views
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Max, Min, Avg
from .filters import ProductFilter
from django.core.paginator import Paginator
from urllib.parse import urlencode


class HomeView(View):
    form_class = SearchForm

    def get(self, request):
        products = Product.objects.all()
        diet_list = DietCategory.objects.all()
        main_menu = MainMenu.objects.all()
        menu_item = MenuItem.objects.all()
        comments = Comment.objects.filter(rate__gte=4)

        if search := request.GET.get('search'):
            minimum = Product.objects.aggregate(unit_price=Min('unit_price'))
            min_price = int(minimum['unit_price'])
            maximum = Product.objects.aggregate(unit_price=Max('unit_price'))
            max_price = int(maximum['unit_price'])
            my_filter = ProductFilter(request.GET, queryset=products)
            products = my_filter.qs
            products = products.filter(Q(name__icontains=search)
                                       | Q(description__icontains=search)
                                       | Q(unit_price__icontains=search))
            paginator = Paginator(products, 6)
            page_num = request.GET.get('page')
            products = paginator.get_page(page_num)
            page_url_data = request.GET.copy()

            if 'page' in page_url_data:
                del page_url_data['page']

            ctx = {
                'search_form': self.form_class(),
                'products': products,
                'page_num': page_num,
                'filter': my_filter,
                'max': max_price,
                'min': min_price,
                'page_url_data': page_url_data,
            }
            return render(request, 'home/products.html', ctx)
        # best_pro = Product.objects.filter(average__gte=4)

        ctx = {
            'products': products,
            'diet_list': diet_list,
            'main_menu': main_menu,
            'menu_item': menu_item,
            'comments': comments,

            # 'best_pro': best_pro,

        }

        return render(request, 'home/home.html', ctx)


class ProductView(View):
    form_class = SearchForm

    def get(self, request, id=None, slug=None):
        # print(request.session.get('cart'))
        products = Product.objects.all()
        # var = Variant.objects.filter(available=True)
        minimum = Product.objects.aggregate(unit_price=Min('unit_price'))
        min_price = int(minimum['unit_price'])
        maximum = Product.objects.aggregate(unit_price=Max('unit_price'))
        max_price = int(maximum['unit_price'])
        my_filter = ProductFilter(request.GET, queryset=products)
        products = my_filter.qs
        diet_list = DietCategory.objects.filter(available=True)

        # sizes = Size.objects.all()
        if id and slug:
            products = products.filter(diet_category__id=id, diet_category__slug=slug)
            # diet_list = DietCategory.objects.filter(available=True)
        # if size:
        #     products = products.filter(size__name=size)

        if search := request.GET.get('search'):
            products = products.filter(Q(name__icontains=search)
                                       | Q(description__icontains=search)
                                       | Q(unit_price__icontains=search))

        paginator = Paginator(products, 6)
        page_num = request.GET.get('page')
        data = request.GET.copy()
        products = paginator.get_page(page_num)
        if 'page' in data:
            del data['page']

        ctx = {
            'products': products,
            'diet_list': diet_list,
            'search_form': self.form_class(),
            'page_num': page_num,
            'filter': my_filter,
            'max': max_price,
            'min': min_price,
            'data': urlencode(data),
            # 'var': var,
            # 'sizes':sizes
        }
        return render(request, 'home/products.html', ctx)


class MenuView(View):
    form_class = SearchForm

    def get(self, request, id=None, slug=None):
        diet_list = DietCategory.objects.filter(available=True)
        products = Product.objects.all()
        menus = MainMenu.objects.all()
        minimum = Product.objects.aggregate(unit_price=Min('unit_price'))
        min_price = int(minimum['unit_price'])
        maximum = Product.objects.aggregate(unit_price=Max('unit_price'))
        max_price = int(maximum['unit_price'])
        my_filter = ProductFilter(request.GET, queryset=products)
        products = my_filter.qs

        if id and slug:
            products = products.filter(main_menu__id=id, main_menu__slug=slug)
            # diet_list = MainMenu.objects.filter(available=True)

        if search := request.GET.get('search'):
            products = products.filter(Q(name__icontains=search)
                                       | Q(description__icontains=search)
                                       | Q(unit_price__icontains=search))
        paginator = Paginator(products, 6)
        page_num = request.GET.get('page')
        products = paginator.get_page(page_num)
        page_url_data = request.GET.copy()
        if 'page' in page_url_data:
            del page_url_data['page']

        ctx = {
            'products': products,
            'main_menu': menus,
            'diet_list': diet_list,
            'search_form': self.form_class(),
            'page_num': page_num,
            'filter': my_filter,
            'max': max_price,
            'min': min_price,
            'page_url_data': page_url_data,

        }
        return render(request, 'home/products.html', ctx)


class MenuItemView(View):
    form_class = SearchForm

    def get(self, request, id=None, slug=None):
        diet_list = DietCategory.objects.filter(available=True)
        products = Product.objects.all()
        menu_item = MenuItem.objects.all()
        minimum = Product.objects.aggregate(unit_price=Min('unit_price'))
        min_price = int(minimum['unit_price'])
        maximum = Product.objects.aggregate(unit_price=Max('unit_price'))
        max_price = int(maximum['unit_price'])
        my_filter = ProductFilter(request.GET, queryset=products)
        products = my_filter.qs

        if id and slug:
            products = products.filter(menu_item__id=id, menu_item__slug=slug)
            # diet_list = MenuItem.objects.filter(available=True)
        if search := request.GET.get('search'):
            products = products.filter(Q(name__icontains=search)
                                       | Q(description__icontains=search)
                                       | Q(unit_price__icontains=search))

        paginator = Paginator(products, 6)
        page_num = request.GET.get('page')
        products = paginator.get_page(page_num)
        page_url_data = request.GET.copy()
        if 'page' in page_url_data:
            del page_url_data['page']

        ctx = {
            'products': products,
            'menu_item': menu_item,
            'diet_list': diet_list,
            'search_form': self.form_class(),
            'page_num': page_num,
            'filter': my_filter,
            'max': max_price,
            'min': min_price,
            'page_url_data': page_url_data,

        }
        return render(request, 'home/products.html', ctx)


class ProductDetailsView(View):
    template_name = 'home/details.html'
    form_class = SearchForm

    def setup(self, request, *args, **kwargs):
        self.product_instance = get_object_or_404(Product, id=kwargs['id'], slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        product = self.product_instance
        ip = request.META.get('REMOTE_ADDER')
        view = Views.objects.filter(product_id=product.id, ip=ip)
        if not view.exists():
            Views.objects.create(product_id=product.id, ip=ip)
            product.num_views += 1
            product.save()
        if request.user.is_authenticated:
            product.view.add(request.user)
        products = Product.objects.all().order_by('-discount')[:3]

        product_images = Image.objects.filter(product=self.product_instance)
        similar = product.tags.similar_objects()[:6]
        comment = Comment.objects.filter(product=product, is_reply=False).order_by('-created')
        selected_var = None
        if product.status != 'none':
            selected_var = Variant.objects.filter(product=product).first()

        if var_id := request.GET.get('select_var'):
            selected_var = Variant.objects.filter(id=var_id).first()

        if search := request.GET.get('search'):
            products = products.filter(Q(name__icontains=search) | Q(description__icontains=search))
            return render(request, 'home/products.html', {'search_form': self.form_class(), 'products': products, })
        is_favourite = False
        if product.favourite.filter(id=request.user.id).exists():
            # messages.success(request, 'Your product add/remove to your favourite.', "success")
            is_favourite = True

        ctx = {
            'product': product,
            'comment_form': CommentForm(),
            'comments': comment,
            'product_images': product_images,
            'products': products,
            'diet_list': DietCategory.objects.all(),
            'selected_var': selected_var,
            'cart_form': CartForm(),
            'similar': similar,
            'like_class': product.like_checkers(request.user),
            'is_favourite': is_favourite,



        }
        return render(request, self.template_name, ctx)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        url = request.META.get('HTTP_REFERER')
        _type = request.GET.get('type')
        product = self.product_instance
        # similar = product.tags.similar_objects()[:2]
        form = CommentForm(request.POST)
        rep_form = ReplyForm(request.POST)

        if not _type:
            if form.is_valid():
                cm = form.save(commit=False)
                cm.user = request.user
                cm.product = product
                cm.save()
                messages.success(request, 'Your comment has been submitted.', "success")
                return redirect('home:details', product.id, product.slug)
                # cd = form.cleaned_data
                # cm=Comment.objects.create(body=cd['body'],rate=cd['rate'],user_id=request.user.id,product_id=product.id)
                # cm.save()
                # return redirect(url)
            ctx = {

                'comment_form': CommentForm(),
                # 'similar': similar

            }

            return render(request, self.template_name, ctx)
        else:

            if rep_form.is_valid():
                rep_to_comment = Comment.objects.filter(id=kwargs.get('com_id')).first()
                rep = rep_form.save(commit=False)
                rep.user = request.user
                rep.product = product
                rep.reply_to = rep_to_comment
                rep.is_reply = True
                rep.save()
                messages.success(request, 'Your Reply has been submitted.', "success")
                # return redirect('home:details', product.id, product.slug)
                return redirect(url)
            ctx = {

                'comment_form': ReplyForm(),
                # 'similar': similar

            }
            return render(request, self.template_name, ctx)


# class FeaturedProductView(View):
#     def get(self, request):
#
#         products = Product.objects.all().order_by('-discount')
#
#         return render(request,'home/details.html',{'products': products})


class ProductLikeView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            data = {
                'login_required': True
            }
            return JsonResponse(data)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        product = get_object_or_404(Product, id=request.GET.get('product_id'))
        if product.like_product.filter(id=request.user.id).exists():
            product.like_product.remove(request.user)
            p_liked = False

        else:
            product.like_product.add(request.user)
            p_liked = True

        product.save()
        data = {
            'p_liked': p_liked,
            'p_liker_count': product.likes_count
        }
        # messages.success(request, 'Your product add to your favourite.', "success")
        return JsonResponse(data)


class CommentLikeView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            data = {
                'login_required': True
            }
            return JsonResponse(data)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        # url = request.META.get('HTTP_REFERER')
        cm = get_object_or_404(Comment, id=request.GET.get('com_id'))

        if cm.disliked_comment.filter(id=request.user.id).exists():
            cm.disliked_comment.remove(request.user)
            liked = False

        if cm.liked_comment.filter(id=request.user.id).exists():
            cm.liked_comment.remove(request.user)
            liked = False

        else:
            cm.liked_comment.add(request.user)
            liked = True

        cm.save()
        data = {
            'liked': liked,
            'like_counter': cm.like_count,
            'dislike_counter': cm.dislike_count

        }
        messages.success(request, 'Your like has been submitted.', "success")

        return JsonResponse(data)


class CommentDislikeView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            data = {
                'login_required': True
            }
            return JsonResponse(data)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        # url = request.META.get('HTTP_REFERER')
        cm = get_object_or_404(Comment, id=request.GET.get('com_id'))
        if cm.liked_comment.filter(id=request.user.id).exists():
            cm.liked_comment.remove(request.user)
            disliked = False

        if cm.disliked_comment.filter(id=request.user.id).exists():
            cm.disliked_comment.remove(request.user)
            disliked = False

        else:
            cm.disliked_comment.add(request.user)
            disliked = True

        cm.save()
        data = {

            'disliked': disliked,
            'like_counter': cm.like_count,
            'dislike_counter': cm.dislike_count
        }
        messages.success(request, 'Your dislike has been submitted.', "success")

        return JsonResponse(data)


class FavouriteProductsView(View):
    def get(self,request, id):
        url = request.META.get('HTTP_REFERER')
        product = get_object_or_404(Product, id=id)
        is_favourite = False
        if product.favourite.filter(id=request.user.id).exists():
            product.favourite.remove(request.user)
            is_favourite = False
            product.total_favourite -= 1
            messages.success(request, 'Your product remove of your favourite.', "success")

        else:
            product.favourite.add(request.user)
            is_favourite = True
            product.total_favourite += 1
            messages.success(request, 'Your product add to your favourite.', "success")

        return redirect(url)


