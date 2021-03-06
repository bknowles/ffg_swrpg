from django.db import models
import base.models

class Category(models.Model):
  MODEL_CHOICES = (
    (1, 'Gear'),
    (2, 'Weapon'),
    (3, 'Armor'),
    (4, 'Attachment'),
  )

  model = models.IntegerField(choices=MODEL_CHOICES)
  name = models.CharField(max_length=50)

  @classmethod
  def model_hash(cls):
    return { v[1]:v[0] for i,v in enumerate(cls.MODEL_CHOICES) }

  @classmethod
  def model_numbers(cls):
    mhash = cls.model_hash()
    return [mhash[i] for i in mhash.keys()]

  def model_info(self):
    return {'id': int(self.model), 'name': self.get_model_display() }

  def __init__(self, *args, **kwargs):
    super(Category, self).__init__(*args, **kwargs)
    self._meta.get_field_by_name('model')[0]._choices = self.__class__.MODEL_CHOICES

  def __unicode__(self):
    return self.name

  class Meta:
    ordering = ['name']

  def _weapon_set(self):
    if self.model == 2:
      return Weapon.objects.filter(gear_ptr_id__in=[x.id for x in self.gear_set.all()])
  weapon_set = property(_weapon_set)

  def _attachment_set(self):
    if self.model == 4:
      return Attachment.objects.filter(gear_ptr_id__in=[x.id for x in self.gear_set.all()])
  attachment_set = property(_attachment_set)

class GearManager(models.Manager):
  def get_queryset(self):
    return super(GearManager, self).get_queryset()

class Gear(base.models.Entry):
  price = models.IntegerField()
  restricted = models.BooleanField()
  encumbrance = models.IntegerField()
  rarity = models.IntegerField()
  category = models.ForeignKey(Category)
  
  def __unicode__(self):
    return self.name
    
  def _display_price(self):
    if self.restricted:
      res = "(R) "
    else:
      res = ""
    if self.price:
      rprice = "{0:,d}".format(self.price)
    else:
      rprice = "-"
    return '{0}{1}'.format(res, rprice)

  def _display_encum(self):
    if self.price or self.encumbrance:
      return str(self.encumbrance)
    else:
      return "-"

  def _display_rarity(self):
    if self.price or self.rarity:
      return str(self.rarity)
    else:
      return "-"
      
  def _equipment_display(self):
    if self.model == 'Weapon':
      return "{name} ({skill}; Damage {damage}; Critical {critical}; Range ({range}); {special})".format(name=self.name_link(), skill=self.weapon.get_weapon_skill_display(), damage=self.weapon.display_damage, critical=self.weapon.display_crit, range=self.weapon.get_weapon_range_display(), special=self.weapon.special)
    else:
      return self.name_link()
  equipment_display = property(_equipment_display)
          
  display_price = property(_display_price)
  display_encum = property(_display_encum)
  display_rarity = property(_display_rarity)
  
  class Meta:
    ordering = ['name']

class Weapon(Gear):
  SKILL_CHOICES = (
    (1, 'Brawl'),
    (2, 'Melee'),
    (3, 'Ranged [Light]'),
    (4, 'Ranged [Heavy]'),
    (5, 'Gunnery'),
    (6, 'Lightsaber'),
    (7, 'Brawl'), # These are for items that do not add
    (8, 'Melee'), # To the Brawn Characteristic
  )
  RANGE_CHOICES = (  
    (1, 'Engaged'),
    (2, 'Short'),
    (3, 'Medium'),
    (4, 'Long'),
    (5, 'Extreme'),
  )
  weapon_skill = models.IntegerField(choices=SKILL_CHOICES)
  damage = models.IntegerField()
  critical = models.IntegerField()
  weapon_range = models.IntegerField(choices=RANGE_CHOICES)
  hard_points = models.IntegerField()
  special = models.CharField(max_length=200)
  
  def _display_damage(self):
    if (self.weapon_skill in [1, 2]):
      return "{0:+d}".format(self.damage)
    else:
      return self.damage
  
  def _display_crit(self):
    if self.critical:
      return str(self.critical)
    else:
      return "-"

  def _display_hp(self):
    if self.price or self.hard_points:
      return str(self.hard_points)
    else:
      return "-"
      
  display_crit = property(_display_crit)
  display_hp = property(_display_hp)
  display_damage = property(_display_damage)
  
    
class Armor(Gear):
  defense = models.IntegerField()
  soak = models.IntegerField()
  hard_points = models.IntegerField()

  def _display_hp(self):
    if self.price or self.hard_points:
      return str(self.hard_points)
    else:
      return "-"
      
  display_hp = property(_display_hp)
    
class Attachment(Gear):
  hard_points = models.IntegerField()
  
  def _display_encum(self):
    if self.price and self.encumbrance:
      return "{0:+d}".format(self.encumbrance)
    else:
      return "-"

  display_encum = property(_display_encum)

  
