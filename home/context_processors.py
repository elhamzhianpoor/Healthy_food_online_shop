from home.models import MainMenu, DietCategory, MenuItem, Product


def main_menu_cp(request):
    return {
        'main_menu': MainMenu.objects.filter(available=True)

    }


def menu_item_cp(request):
    return {

        'menu_item': MenuItem.objects.filter(available=True)
    }


def diet_category_cp(request):
    return {
        'diet_cat': DietCategory.objects.filter(available=True)
    }

