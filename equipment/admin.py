from django.contrib import admin
from django import forms

import base.admin
from equipment.models import *

class GearAdmin(base.admin.EntryAdmin):  
  list_display = ('name', 'price', 'encumbrance', 'rarity', 'indexes')
  fields = ['name', ('price', 'restricted'), 'encumbrance', 'rarity', 'category', 'notes', 'image']
  inlines = [base.admin.IndexInline]
  
  def formfield_for_foreignkey(self, db_field, request, **kwargs):
    if db_field.name == 'category':
      kwargs['queryset'] = Category.objects.filter(model=1)
    return super(GearAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

  def queryset(self, request):
    qs = super(GearAdmin, self).queryset(request)
    return qs.filter(model='Gear')

  
class WeaponAdmin(GearAdmin):
  fields = ['name', 'weapon_skill', 'damage', 'critical', 'weapon_range', 'encumbrance', 'hard_points', ('price', 'restricted'), 'rarity', 'special', 'category', 'notes', 'image']

  def formfield_for_choice_field(self, db_field, request, **kwargs):
    if db_field.name == "weapon_skill":
      kwargs['choices'] = (
        (1, 'Brawl'),
        (2, 'Melee'),
        (3, 'Ranged [Light]'),
        (4, 'Ranged [Heavy]'),
        (5, 'Gunnery'),
        (6, 'Lightsaber'),
        (7, 'Brawl - Non Brawn'), # These are for items that do not add
        (8, 'Melee - Non Brawn'), # To the Brawn Characteristic
      )
    return super(WeaponAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)
      
  def formfield_for_dbfield(self, db_field, **kwargs):
    formfield = super(WeaponAdmin, self).formfield_for_dbfield(db_field, **kwargs)
    if db_field.name == 'special':
      formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
    return formfield
          
  def formfield_for_foreignkey(self, db_field, request, **kwargs):
    if db_field.name == 'category':
      kwargs['queryset'] = Category.objects.filter(model=2)
    return super(GearAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
  def queryset(self, request):
    qs = super(GearAdmin, self).queryset(request)
    return qs.filter(category__model=2)
    
class ArmorAdmin(GearAdmin):
  fields = ['name', 'defense', 'soak', ('price', 'restricted'), 'encumbrance', 'hard_points', 'rarity', 'category', 'notes', 'image']

  def formfield_for_foreignkey(self, db_field, request, **kwargs):
    if db_field.name == 'category':
      kwargs['queryset'] = Category.objects.filter(model=3)
    return super(GearAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

  def queryset(self, request):
    qs = super(GearAdmin, self).queryset(request)
    return qs.filter(category__model=3)
  
class CategoryAdmin(admin.ModelAdmin):
  list_display = ('model', 'name')
  
  def queryset(self, request):
    qs = super(CategoryAdmin, self).queryset(request)
    return qs.filter(model__in=[x[0] for x in Category.MODEL_CHOICES])
  
class AttachmentAdmin(GearAdmin):
  fields = ['name', ('price', 'restricted'), 'encumbrance', 'hard_points', 'rarity', 'category', 'notes', 'image']

  def formfield_for_foreignkey(self, db_field, request, **kwargs):
    if db_field.name == 'category':
      kwargs['queryset'] = Category.objects.filter(model=4)
    return super(GearAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

  def queryset(self, request):
    qs = super(GearAdmin, self).queryset(request)
    return qs.filter(category__model=4)



admin.site.register(Gear, GearAdmin)
admin.site.register(Weapon, WeaponAdmin)
admin.site.register(Armor, ArmorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Attachment, AttachmentAdmin)
