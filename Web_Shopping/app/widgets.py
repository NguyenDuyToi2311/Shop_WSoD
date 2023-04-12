from django.forms.widgets import SelectMultiple

class CustomCategoryWidget(SelectMultiple):
    def render(self, name, value, attrs=None, renderer=None):
        choices = self.choices
        html = super().render(name, value, attrs, renderer)
        html += '<input type="text" name="new_category" placeholder="Add new category">'
        return html