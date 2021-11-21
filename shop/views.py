from django.shortcuts import render, get_object_or_404
from .models import Product, Brand, Category
from django.core.paginator import Paginator
from django.db.models import Avg, Max, Min

def homepage(request):
	products = Product.objects.filter(available=True)
	new_product = products.order_by('-id')[:5]
	return render(request, 'pages/index.html', {'new_product': new_product})


def store(request, category_slug=None):
	category = None
	categories = Category.objects.all()

	category_id_list = []
	for i in categories:
		if request.POST.get(f"category-{i.id}", False) == 'on':
			category_id_list.append(i.id)

	brand = None
	brands = Brand.objects.all()

	brand_id_list = []
	for i in brands:
		if request.POST.get(f"brand-{i.id}", False) == 'on':
			brand_id_list.append(i.id)

	products = Product.objects.filter(available=True)
	min_price = products.aggregate(Min('price'))

	if category_id_list:
		products = products.filter(available=True, category__in=category_id_list)

	if brand_id_list:
		products = products.filter(available=True, brand__in=brand_id_list)

	if category_slug:
		category = get_object_or_404(Category, slug=category_slug)
		products = products.filter(category=category)

	paginator = Paginator(products, 9)
	page_number = request.GET.get('page')
	products = paginator.get_page(page_number)

	return render(request, 'pages/store.html', {'category': category,
												'categories': categories,
												'brands': brands,
												'brand_id_list': brand_id_list,
												'min_price': min_price,
												'products': products,
												'category_id_list': category_id_list})


def checkout(request):
	return render(request, 'pages/checkout.html')


def product(request, pk):
	product = get_object_or_404(Product, pk=pk)
	return render(request, 'pages/product.html', {'product': product})
