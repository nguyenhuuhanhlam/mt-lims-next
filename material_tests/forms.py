from django import forms
from .models import MaterialTest

class MaterialTestForm(forms.ModelForm):
    class Meta:
        model = MaterialTest
        fields = ["test_code", "content", "material_type", "quantity", "unit", "test_date", "result_date"]
        widgets = {
            'test_code': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-[13px] font-semibold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all',
                'placeholder': 'Mã số (VD: MT-001)',
                'required': True
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 text-[13px] font-medium border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white resize-none transition-all',
                'rows': 3,
                'placeholder': 'Nội dung yêu cầu...',
                'required': True
            }),
            'material_type': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-[13px] font-semibold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all',
                'placeholder': 'Bê tông, thép...',
                'required': True
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-[13px] font-semibold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all',
                'step': '0.01',
                'required': True
            }),
            'unit': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-[13px] font-semibold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all',
                'placeholder': 'Mẫu, Kg...',
                'required': True
            }),
            'test_date': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 text-[13px] font-semibold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all',
                'type': 'date'
            }),
            'result_date': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 text-[13px] font-semibold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all',
                'type': 'date'
            }),
        }
