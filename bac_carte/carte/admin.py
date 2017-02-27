import os, tempfile

import time
from django.contrib import admin
from django import forms
from django.contrib.admin import widgets
from django.forms import ModelForm
from django.http import HttpResponse
from django.template import Context
from django.template import engines
from django.template import Template
from django.template.loader import get_template, render_to_string
from subprocess import Popen

from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from bac_carte.carte.models import Carte, TissuImage, Composant, Marque, \
    Utilisation, Composition


class MySelectWidget(widgets.FilteredSelectMultiple):
    def render_option(self, selected_choices, option_value, option_label):
        print("hhhh")
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        return format_html('<option value="{}"{}>lolololl</option>', option_value, selected_html, force_text(option_label))


class CompositionInline(admin.TabularInline):
    model = Composition
    extra = 1


def export_to_pdf(cartes, show_price=False):
    context = Context({
        'cartes': cartes,
        'show_price': show_price
    }, autoescape=False)
    template_text = r"""
    {% autoescape off %}
    \documentclass[a5paper,11pt]{article}
    \usepackage[a6paper, landscape, margin=1cm]{geometry}
    \usepackage[utf8x]{inputenc}
    \usepackage{libertine} % or \usepackage{fourier} or \usepackage[utopia]{mathdesign}
    \usepackage{graphicx}
    \usepackage{tabularx}
    \usepackage{array}
    \newcolumntype{L}{>{\raggedright\arraybackslash}X} % left multiline alignment
    \newcolumntype{R}{>{\raggedleft\arraybackslash}X}  % right multiline alignment
    \renewcommand{\arraystretch}{1.2}
    \pagenumbering{gobble}

    \begin{document}
    {% for carte in cartes %}
    \begin{tabularx}{0.90\textwidth}{|@{}p{0.25\linewidth} R|}
    \hline
    \multicolumn{2}{|l|}{\large\textbf{ {{ carte.marque }}  } }        \\ \hline
    Ref:                          & {{ carte.ref }}               \\ \hline
    {% if show_price %}
    Prix:                         & {% if carte.price %} {{ carte.price }} € {% endif %}               \\ \hline
    {% endif %}
    Largeur:                      & {% if carte.largeur %} {{ carte.largeur }} cm {% endif %}           \\ \hline
    Raccord:                      & {% if carte.raccord %} {{ carte.raccord }} cm {% endif %}             \\ \hline
    Composition:                  &                  \\
    \multicolumn{2}{|r|}{ {{ carte.compositions.all| join:" - " }} }                         \\ \hline
    Utilisation:                  &                  \\
    \multicolumn{2}{|r|}{ {{ carte.utilisations.all| join:" - " }} }                         \\ \hline
    Pictogramme:                  &                  \\
    \multicolumn{2}{|r|}{ {{ carte.images_latex }} }                         \\ \hline
    \end{tabularx}
    \clearpage
    {% endfor %}
    \end{document}
    {% endautoescape %}
    """
    rendered_tpl = Template(template_text).render(context)
    with tempfile.TemporaryDirectory() as tempdir:
        with open(os.path.join(tempdir, 'texput.tex'), 'w') as w:
            w.write(rendered_tpl)
        for i in range(2):
            command = "pdflatex -output-directory {} {}".format(tempdir, os.path.join(tempdir, 'texput.tex'))
            cmd = Popen([command], shell=True)
            cmd.communicate()
        with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
            pdf = f.read()
    r = HttpResponse(content_type='application/pdf')
    r.write(pdf)
    return r


def export_card_to_pdf(modeladmin, request, queryset):
    return export_to_pdf(queryset.all())


export_card_to_pdf.short_description = "Exporter les cartes en " \
                                                  "pdf sans les prix"


def export_card_to_pdf_with_price(modeladmin, request, queryset):
    return export_to_pdf(queryset.all(), True)


export_card_to_pdf_with_price.short_description = "Exporter les cartes en " \
                                                  "pdf avec les prix"



class CarteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CarteForm, self).__init__(*args, **kwargs)
        # self.fields['images'].widget = MySelectWidget(verbose_name="Pictogrammes", is_stacked=False)


@admin.register(Carte)
class CarteAdmin(admin.ModelAdmin):
    inlines = [CompositionInline, ]
    filter_vertical = ['utilisations', 'images']
    list_display = ['ref', 'marque', 'largeur', 'raccord', 'price']
    actions = [export_card_to_pdf, export_card_to_pdf_with_price]
    form = CarteForm


@admin.register(TissuImage)
class TissuImageAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_tag']


admin.site.register(Marque)
admin.site.register(Composant)
admin.site.register(Utilisation)
