package ctf.task1

decision := {"flag": flag} {
    count(_deny_reasons) == 0
    not _banneduser
    flag := "CTF{NOT_UNDEFINED_IS_TRUE}"
}

decision = {"allowed": false, "reasons": reasons} {
    count(_deny_reasons) > 0
    reasons := _deny_reasons
}

_deny_reasons["index must be a number"]{
    not is_number(input.index)
}

_deny_reasons["input.index is missing"]{
    not input.index
}

_banneduser {
    data.task1.bannedusers[input.index]
} 
