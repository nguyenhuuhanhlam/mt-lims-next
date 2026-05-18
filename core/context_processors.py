def user_roles(request):
    """
    Inject biến phân quyền vào toàn bộ template context.
    - is_manager:    True nếu user thuộc nhóm Managers hoặc là superuser.
    - is_technician: True nếu user thuộc nhóm Technicians (và không phải Manager/superuser).
    """
    is_manager = False
    is_technician = False
    if request.user.is_authenticated:
        is_manager = (
            request.user.is_superuser
            or request.user.groups.filter(name="Managers").exists()
        )
        if not is_manager:
            is_technician = request.user.groups.filter(name="Technicians").exists()
    return {
        "is_manager": is_manager,
        "is_technician": is_technician,
    }
