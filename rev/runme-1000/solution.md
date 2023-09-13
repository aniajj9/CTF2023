# Writeup

Steps:
1) Running the script gives a random number between 1 and 1000. If we manage to hit the value 1000, we get the flag. 
2) On the first run, the script outputs an XML file with counter and the Base64 encoded (and reversed) flag. 
3) Comment out line 36 and 38 - run lines 29-37, the flag is written to console
4) If <Counter>Thousand<Counter> is set in the XML, the flag is written to the console
If the printFlag function is run, the flag isn't printed ;)