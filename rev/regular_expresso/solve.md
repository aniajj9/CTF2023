# Regular Expresso
Author: k4rt0fl3r

If we break down the regex string in public.txt by the delimeter `|` (OR operator), we can spot in the various results the following string `(563243)54(467b)75(5f)(6b)6(e)3(077)(5f7)93(0)(75725f7265)67657(85f)(695f7)333(337d)`.

This should draw our attention as its format is different from the rest of the expression.

Also, we know that our flag starts with `V2CTF{`, and the hex value of that is `56324354467b` which matches the start of the specific regex string.

If we take the specified regex string and:
1. we remove the parenthesis
2. use that with "From Hex" in CyberChef
3. profit, you got your flag