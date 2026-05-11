from django import forms
from django.contrib.auth.models import User
from .models import Request, MaterialTest


class RequestForm(forms.ModelForm):
    # Field ẩn cho participants
    participants = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={':value': 'JSON.stringify(list)'})
    )

    # Các trường riêng lẻ cho project_information
    project_name = forms.CharField(
        label="Tên dự án", required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 text-[13px] font-semibold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all',
            'x-model': 'projectData.project_name'
        })
    )
    work_package = forms.CharField(
        label="Gói thầu", required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 text-[13px] font-semibold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all',
            'x-model': 'projectData.work_package'
        })
    )
    location = forms.CharField(
        label="Địa điểm", required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 text-[13px] font-semibold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all',
            'x-model': 'projectData.location'
        })
    )

    # Các trường riêng lẻ cho requesting_unit
    unit_address = forms.CharField(
        label="Địa chỉ đơn vị", required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 text-[13px] font-semibold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all',
            'x-model': 'unitData.address'
        })
    )
    unit_telephone = forms.CharField(
        label="Số điện thoại", required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 text-[13px] font-semibold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all',
            'x-model': 'unitData.telephone'
        })
    )

    class Meta:
        model = Request
        fields = [
            "title", "type", "status", "content", "created_by", "participants",
            "project_information", "requesting_unit"
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-[13px] font-semibold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all',
                'placeholder': 'Ví dụ: Hợp đồng tháng 5',
            }),
            'type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-[13px] font-bold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all appearance-none cursor-pointer',
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-[13px] font-bold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all appearance-none cursor-pointer',
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-3 py-3 text-[13px] font-medium border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white placeholder-gray-300 resize-none transition-all',
                'rows': 4,
                'placeholder': 'Mô tả nội dung...',
            }),
            'created_by': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-[13px] font-bold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all appearance-none cursor-pointer',
            }),
            'project_information': forms.HiddenInput(attrs={':value': 'JSON.stringify(projectData)'}),
            'requesting_unit': forms.HiddenInput(attrs={':value': 'JSON.stringify(unitData)'}),
        }

    def __init__(self, *args, **kwargs):
        import json
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Load data từ JSON vào các trường riêng lẻ
            if self.instance.participants:
                self.initial['participants'] = json.dumps(self.instance.participants)
            
            p_info = self.instance.project_information or {}
            self.initial['project_name'] = p_info.get('project_name', '')
            self.initial['work_package'] = p_info.get('work_package', '')
            self.initial['location'] = p_info.get('location', '')

            r_unit = self.instance.requesting_unit or {}
            self.initial['unit_address'] = r_unit.get('address', '')
            self.initial['unit_telephone'] = r_unit.get('telephone', '')

    def clean(self):
        cleaned_data = super().clean()
        
        # Pack project_information
        cleaned_data['project_information'] = {
            'project_name': cleaned_data.get('project_name', ''),
            'work_package': cleaned_data.get('work_package', ''),
            'location': cleaned_data.get('location', ''),
        }

        # Pack requesting_unit
        cleaned_data['requesting_unit'] = {
            'address': cleaned_data.get('unit_address', ''),
            'telephone': cleaned_data.get('unit_telephone', ''),
        }

        return cleaned_data

    def clean_participants(self):
        import json
        data = self.cleaned_data.get('participants')
        if not data:
            return []
        try:
            return json.loads(data)
        except (ValueError, TypeError):
            return []


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
