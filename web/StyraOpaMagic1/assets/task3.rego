package ctf.task3

decision := {"flag": flag} {
    count(_deny_reasons) == 0
    flag := "masked"
}

decision = {"allowed": false, "reasons": reasons} {
    count(_deny_reasons) > 0
    reasons := _deny_reasons
}

_deny_reasons["input.magic_value is missing"]{
    not input.magic_value
}

_deny_reasons["input.access_level is missing"]{
    not input.access_level
}

_deny_reasons["The provided magic value was not magic"]{
    not _hasmagicvalue
}

_deny_reasons["Access level is not high enough"] {
    not _hasaccess
}

_deny_reasons["Access level must be below 9000"]{
    is_number(input.access_level)
    input.access_level > 9000
}

_deny_reasons["Access level must be above 0"]{
    is_number(input.access_level)
    input.access_level < 0
}

_hasaccess {
    input.access_level > 9000
}

_hasmagicvalue {
    input.magic_value < false
}
