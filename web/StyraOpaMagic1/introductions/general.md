# Introduction to OPA and Rego
OPA stands for "Open Policy Agent" and is a program that accepts JSON as input and produces a JSON response based on a policy and data.
The policy is written in a language called Rego: https://www.openpolicyagent.org/docs/latest/policy-language/

Each task is viewed on a website where there is an input field, the policy and optional data. There is also a submit button that sends the input to the OPA and displays the response from OPA.

The goal of each task is to make the `decision` rule that contains the flag to evaluate to true.

## Introduction to common rules in Rego
A Rego file consists of rules and below is three examples of common structures of rules.

### Example 1
```
decision = {"allowed": "true"} {
    //statement1
    //statement2
}
```
the `decision` rule will be equal to `{"allowed": "true"}` if all the statements in the body evaluate to true.

### Example 2
```
my_rule {
    //statement1
    //statement2
}
```

the `my_rule` rule will be equal to `true` if the statements evaluate to true. If the statements does not evaluate to true the value of `my_rule` is undefined.

### Example 3
```
_deny_reasons["reason for not getting access"]{
    //statement1
    //statement2
}
```

in this case the `_deny_reasons` rule is a map. It will contain the key "reason for not getting access" if statements evaluate to true. 

