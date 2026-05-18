from django import forms
from .models import MaterialTest

class MaterialTestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if 'tester' in self.fields:
            self.fields['tester'].empty_label = "Chọn người thực hiện..."
        if 'reviewer' in self.fields:
            self.fields['reviewer'].empty_label = "Chọn người kiểm tra..."

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        reviewer = cleaned_data.get('reviewer')
        
        if status == 'completed':
            if not self.user or reviewer != self.user:
                self.add_error('status', 'Chỉ có người kiểm tra được phân công mới có thể chuyển trạng thái thành Hoàn tất.')
                
        return cleaned_data

    class Meta:
        model = MaterialTest
        fields = ["test_code", "content", "material_type", "quantity", "unit", "test_date", "result_date", "tester", "reviewer", "status"]
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
            'tester': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-[13px] font-semibold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all',
            }),
            'reviewer': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-[13px] font-semibold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all',
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-[13px] font-semibold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all',
            }),
        }
