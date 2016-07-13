from django import forms

from .models import Join

# class EmailForm(forms.Form):
# 	name = forms.CharField(required=False)
# 	email = forms.EmailField()

class AptForm(forms.Form):
	listing_type_text = forms.CharField(max_length = 10, required = False)
	name = forms.CharField(required=False)
	email = forms.EmailField(required=False)
	neighborhood = forms.CharField(required = False)
	bedroom = forms.CharField(max_length = 6, required = False)
	bathroom = forms.CharField(max_length = 3, required = False)


class SearchForm(forms.Form):
	listing_type_text = forms.CharField(max_length = 10, required = False)
	neighborhood = forms.CharField(max_length = 100, required = False)
	bedroom = forms.IntegerField(required = False)
	bathroom = forms.IntegerField(required = False)
	minprice = forms.IntegerField(required = False)
	maxprice = forms.IntegerField(required = False)



class JoinForm(forms.ModelForm):
	class Meta:
		model = Join
		fields = ["listing_type_text", "email", "neighborhood", "price", "bedroom", "bathroom"]


