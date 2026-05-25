from django import forms
from django.contrib.auth.models import User, Group
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["phone_number", "address", "department", "position", "avatar"]
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-[13px] font-semibold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all',
                'placeholder': 'Số điện thoại...',
            }),
            'address': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-[13px] font-semibold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all',
                'placeholder': 'Địa chỉ...',
            }),
            'department': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-[13px] font-semibold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all',
                'placeholder': 'Phòng ban...',
            }),
            'position': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-[13px] font-semibold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all',
                'placeholder': 'Chức vụ...',
            }),
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'w-full px-3 py-1.5 text-[12px] text-gray-500 border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 transition-all',
            }),
        }
        labels = {
            'phone_number': 'Số điện thoại',
            'address': 'Địa chỉ',
            'department': 'Phòng ban',
            'position': 'Chức vụ',
            'avatar': 'Ảnh đại diện',
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "is_active", "groups"]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-[13px] font-semibold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all',
                'placeholder': 'Tên đăng nhập',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 text-[13px] font-semibold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all',
                'placeholder': 'Email...',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-[13px] font-semibold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all',
                'placeholder': 'Tên...',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-[13px] font-semibold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all',
                'placeholder': 'Họ và tên đệm...',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 w-4 h-4',
            }),
            'groups': forms.SelectMultiple(attrs={
                'class': 'w-full px-3 py-2 text-[13px] font-semibold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all min-h-[100px]',
            }),
        }
        labels = {
            'username': 'Tên đăng nhập',
            'email': 'Email',
            'first_name': 'Tên',
            'last_name': 'Họ và tên đệm',
            'is_active': 'Đang hoạt động',
            'groups': 'Phân vào nhóm',
        }


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name", "permissions"]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-[13px] font-semibold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all',
                'placeholder': 'Tên nhóm (VD: Kỹ thuật viên)',
            }),
            'permissions': forms.SelectMultiple(attrs={
                'class': 'w-full px-3 py-2 text-[13px] font-semibold border border-gray-100 bg-gray-50/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 focus:bg-white transition-all min-h-[200px]',
            }),
        }
        labels = {
            'name': 'Tên nhóm',
            'permissions': 'Quyền hạn',
        }
