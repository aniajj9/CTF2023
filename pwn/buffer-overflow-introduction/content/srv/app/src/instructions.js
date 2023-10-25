const instructions = [
    {
        title: "Hello world!",
        description: "In the textbox in the middle, try entering `Hello World!`. Observe which variable within the code takes the value."
    },
    {
        title: "Overflow!",
        description: "What happens if you write more than 16 characters into the buffer? Can you make the secret change?"
    },
    {
        title: "Take control",
        description: "Can you make secret take the value `1633771873 (0x61616161)`. Note that strings are stored in <a href='https://simple.wikipedia.org/wiki/ASCII' target='_blank'>ASCII</a>, and in ASCII, character number `0x61` is `a`.",
        hint: {
            text: "`0x61` is the ASCII representation of `a`, so enter any 16 characters to overflow into the value `secret`, and then enter `a` 4 times to fill it with the bytes `0x61`",
            cost: 50
        }
    },
    {
        title: "Little endian",
        description: "In most architectures, integers are read in reverse byte order from memory, in a method which is called <a href='https://simple.wikipedia.org/wiki/Endianness' target='_blank'>Little endian</a>. Can you make the secret take the value `1633837924 (0x61626364)`?",
        hint: {
            text: "Reading from the ASCII table, `0x61` is the ASCII representation of `a`, `0x62` is `b`, and so on. As the bytes are read in reverse order, we input `dcba`, which when read backwards will result in `0x61626364`",
            cost: 50
        }
    },
    {
        title: "Escape from ASCII",
        description: "As you may see in the code, to get past the restrictions and retrieve the flag, `secret` needs to have a value of `0xcafebabe`. However not all these characters are in ASCII! What will you do?",
        hint: {
            text: "You can use `\xab` to insert character `0xab`.",
            cost: 75
        }
    }
]

export {
    instructions
}
