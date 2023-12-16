package ctf.task0

#Get the flag by making this rule evaluate to true
decision = {"allowed": true, "flag": flag} {
    count(_deny_reasons) == 0
    flag := "masked"
}

decision = {"allowed": false, "reasons": reasons} {
    count(_deny_reasons) > 0
    reasons := _deny_reasons
}

#Input existence checking
_deny_reasons["input.user not provided"] {
    not input.user
}

#Input existence checking
_deny_reasons["input.access_level not provided"] {
    not input.access_level
}

#Input existence checking
_deny_reasons["input.path not provided"] {
    not input.path
}

#Input type checking
_deny_reasons["input.user must be a string"] {
    not is_string(input.user)
}

#Input type checking
_deny_reasons["input.access_level must be a number"] {
    not is_number(input.access_level)
}

#Input type checking
_deny_reasons["input.path must be a string"] {
     not is_string(input.path)
}

_deny_reasons[sprintf("%v with access level of %v does not have access to %v", [input.user, input.access_level, input.path])] {
    not _access_to_path_is_allowed
}

_deny_reasons[sprintf("%v is not in the list of admin users", [input.user])]{
    not _user_is_admin
}

_access_to_path_is_allowed {
    _user_is_admin
    input.path == "/admins"
    input.access_level > 9000
}

_user_is_admin {
    data.task0.admins[_] == input.user
}
