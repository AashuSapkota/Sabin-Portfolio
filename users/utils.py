from .models import User, UserRolePrevilegeModel, UserRoleModel

def checkUserPrevilege(user, menu_code, action):
    user = User.objects.get(pk=user)
    if user.user_role != -1:
        usr_role = int(user.user_role)
        print(usr_role)
        usr_role = UserRoleModel.objects.get(pk=usr_role).role_name
        print(usr_role)
        if usr_role == 'super admin':
            print('True')
            return True
        else:
            try:
                if action == 'create_rights':
                    role_previlege = UserRolePrevilegeModel.objects.get(role_id=user.user_role, menu_code=menu_code, create_rights=True)
                    if role_previlege:
                        return True
                    else:
                        return False
                elif action == 'delete_rights':
                    role_previlege = UserRolePrevilegeModel.objects.get(role_id=user.user_role, menu_code=menu_code, delete_rights=True)
                    if role_previlege:
                        return True
                    else:
                        return False
                elif action == 'retrieve_rights':
                    print(user.user_role)
                    print(menu_code)
                    print('here')
                    role_previlege = UserRolePrevilegeModel.objects.get(role_id=user.user_role, menu_code=menu_code, retrieve_rights=True)
                    if role_previlege:
                        return True
                    else:
                        return False
                elif action == 'update_rights':
                    role_previlege = UserRolePrevilegeModel.objects.get(role_id=user.user_role, menu_code=menu_code, update_rights=True)
                    if role_previlege:
                        return True
                    else:
                        return False
            except Exception as e:
                print(e)
                return False
    if user.user_role == -1:
        try:
            if action == 'create_rights':
                user_previlege = UserRolePrevilegeModel.objects.get(user_id=user.pk, menu_code=menu_code, create_rights=True)
                if user_previlege:
                    return True
                else:
                    return False
            elif action == 'delete_rights':
                user_previlege = UserRolePrevilegeModel.objects.get(user_id=user.pk, menu_code=menu_code, delete_rights=True)
                if user_previlege:
                    return True
                else:
                    return False
            elif action == 'retrieve_rights':
                user_previlege = UserRolePrevilegeModel.objects.get(user_id=user.pk, menu_code=menu_code, retrieve_rights=True)
                if user_previlege:
                    return True
                else:
                    return False
            elif action == 'update_rights':
                user_previlege = UserRolePrevilegeModel.objects.get(user_id=user.pk, menu_code=menu_code, update_rights=True)
                if user_previlege:
                    return True
                else:
                    return False
        except Exception as e:
            return False