package ctf.task2

decision := {"flag": flag} {
    count(_deny_reasons) == 0
    not _banneduser
    flag := "CTF{CHECK_FOR_INPUT_EXISTENCE}"
}

decision = {"allowed": false, "reasons": reasons} {
    count(_deny_reasons) > 0
    reasons := _deny_reasons
}

_deny_reasons["key must be a number"]{
    not is_number(input.key)
}

_deny_reasons["key must be less than 1"]{
    not input.key < 1
}

_deny_reasons["key must be bigger than 1"]{
    not input.key > 1
}

_banneduser {
    data.bannedusers[input.key]
} 
