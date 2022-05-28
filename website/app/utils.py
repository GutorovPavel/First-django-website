from .models import *

menu = [
    {'title': 'Новая статья', 'url_name': 'addpost'},
]

main = 'RAP NEWS:  '


class DataMixin:

    def get_user_context(self, **kwargs):
        user_menu = menu.copy()
        if not self.request.user.is_authenticated or not self.request.user.role == 'Editor':
            user_menu.pop(0)

        context = kwargs
        context['cats'] = Category.objects.all()
        context['menu'] = user_menu
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
