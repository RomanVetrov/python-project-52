from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Главная страница с приветствием и меню."""
    template_name = "index.html"
