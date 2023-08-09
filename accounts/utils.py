
def detectUser(user):
    if user.role == 1:
        redirectUrl = 'ownerDashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'tenantDashboard'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl
    
