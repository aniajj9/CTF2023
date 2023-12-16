package ctf.task4

decision = {"allowed": true, "flag": flag} {
    count(_deny_reasons) == 0
    flag := "CTF{THAT_WAS_EASY}"
}

decision = {"allowed": false, "reasons": reasons} {
    count(_deny_reasons) > 0
    reasons := _deny_reasons
}

_deny_reasons["input.password not provided"] {
    not input.password
}

_deny_reasons["input.password must be a string"] {
    not is_string(input.password)
}

_deny_reasons["password was not correct"] {
    not _correct_password
}

_correct_password {
    #warming up the RAM
    100000000 > 1000000
    warmup1(100) == true
    warmup2(20, 400) == true
    warmup2(20, 401) == false
    not randomrule
    
    space_splitted_password := regex.split("\\s+", input.password)
    
    #hint for number of element in password
    number_of_parts := { index | value := space_splitted_password[index]; is_string(value)}
    count(number_of_parts) == 6 
    
    #hint for element 3 of password
    list_of_objects := [{"key1": "value1", "key11": "value11"}, {"key2": "value2"}, {"key31": "value31"}]
    good_keys_and_values := { [key, value] | list_of_objects[_][key]; contains(key, "1"); value := list_of_objects[_][key]}      
    some i, j   
    space_splitted_password[i] == good_keys_and_values[j][_]    
    
    #hint for element 2 of password
    list := ["value6541", "value2234", "value1233", "12983", "515123"]
    some k
    space_splitted_password[k] == list[k]
    
    #hint for element 5 and 6 of password
    filter := [ res | res := list[_]; contains(res, "123")]
    concat_string := concat(" ", filter)
    contains(input.password, concat_string)
    
    #hint for element 4
    password_as_map := { value: key | value := space_splitted_password[key] }
    password_as_map["value5"] == 3
       
    #random and almost useless hint
    password_contains_1234 := {part | part := space_splitted_password[_]; part == "1234"}
    count(password_contains_1234) == 0
    
    #hint for element 1 of password
    numbers_string := regex.split("_", space_splitted_password[0])
    [item1, item2, item3, item4, item5] := [ number | number_string := numbers_string[_]; number := to_number(number_string); number < 6]
    set := {item1, item2, item3, item4, item5}
    set == {5,1,3,4,2}  
}

warmup1(x) := success{
    success := 100 == x
}

warmup2(x,y) := success{
    success := x*2 == y/10
}

randomrule {
    input.password == "1234"
}
