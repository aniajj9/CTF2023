const cProgram = `<pre class="hljs" style="display: block; overflow-x: auto; padding: 1em 0.5em 0.5em 2.5em; margin: 0; background: rgb(240, 240, 240); color: rgb(68, 68, 68);"><span class="hljs-meta" style="color: rgb(31, 113, 153);">#<span class="hljs-meta-keyword" style="font-weight: 700;">define</span> _GNU_SOURCE</span>
<span class="hljs-meta" style="color: rgb(31, 113, 153);">#<span class="hljs-meta-keyword" style="font-weight: 700;">include</span> <span class="hljs-meta-string" style="color: rgb(77, 153, 191);">&lt;stdio.h&gt;</span></span>
<span class="hljs-meta" style="color: rgb(31, 113, 153);">#<span class="hljs-meta-keyword" style="font-weight: 700;">include</span> <span class="hljs-meta-string" style="color: rgb(77, 153, 191);">&lt;stdlib.h&gt;</span></span>
<span class="hljs-meta" style="color: rgb(31, 113, 153);">#<span class="hljs-meta-keyword" style="font-weight: 700;">include</span> <span class="hljs-meta-string" style="color: rgb(77, 153, 191);">&lt;string.h&gt;</span></span>
<span class="hljs-meta" style="color: rgb(31, 113, 153);">#<span class="hljs-meta-keyword" style="font-weight: 700;">include</span> <span class="hljs-meta-string" style="color: rgb(77, 153, 191);">&lt;unistd.h&gt;</span></span>
<span class="hljs-meta" style="color: rgb(31, 113, 153);">#<span class="hljs-meta-keyword" style="font-weight: 700;">include</span> <span class="hljs-meta-string" style="color: rgb(77, 153, 191);">&lt;sys/types.h&gt;</span></span>

<span class="hljs-keyword" style="font-weight: 700;">const</span> <span class="hljs-keyword" style="font-weight: 700;">char</span>* FLAG = <span class="hljs-string" style="color: rgb(136, 0, 0);">"&lt;REDACTED&gt;"</span>

<span class="hljs-keyword" style="font-weight: 700;">void</span> flag() {
    <span class="hljs-built_in" style="color: rgb(57, 115, 0);">printf</span>(<span class="hljs-string" style="color: rgb(136, 0, 0);">"FLAG: %s\\n"</span>, FLAG);
}

<span class="hljs-function"><span class="hljs-keyword" style="font-weight: 700;">void</span> <span class="hljs-title" style="color: rgb(136, 0, 0); font-weight: 700;">message</span><span class="hljs-params">(<span class="hljs-keyword" style="font-weight: 700;">char</span> *input)</span> </span>{
    <span class="hljs-comment" style="color: rgb(136, 136, 136);">/// LIVE CODE</span>
    <span class="hljs-keyword" style="font-weight: 700;">char</span> buf[<span class="hljs-number" style="color: rgb(136, 0, 0);">16</span>] = <span class="hljs-string" style="color: rgb(136, 0, 0);">""</span>;
    <span class="hljs-comment" style="color: rgb(136, 136, 136);">/// END LIVE CODE</span>


    <span class="hljs-comment" style="color: rgb(136, 136, 136);">/// LIVE CODE</span>
    <span class="hljs-keyword" style="font-weight: 700;">int</span> secret = <span class="hljs-number" style="color: rgb(136, 0, 0);">0</span>;
    <span class="hljs-comment" style="color: rgb(136, 136, 136);">/// END LIVE CODE</span>
    <span class="hljs-built_in" style="color: rgb(57, 115, 0);">strcpy</span>(buf, input);

    <span class="hljs-built_in" style="color: rgb(57, 115, 0);">printf</span>(<span class="hljs-string" style="color: rgb(136, 0, 0);">"You said: %s\\n"</span>, buf);

    <span class="hljs-keyword" style="font-weight: 700;">if</span> (secret == <span class="hljs-number" style="color: rgb(136, 0, 0);">0xcafebabe</span>) {
        flag();
    } <span class="hljs-keyword" style="font-weight: 700;">else</span> {
        <span class="hljs-built_in" style="color: rgb(57, 115, 0);">printf</span>(<span class="hljs-string" style="color: rgb(136, 0, 0);">"The secret is 0x%x\\n"</span>, secret);
    }
}

<span class="hljs-function"><span class="hljs-keyword" style="font-weight: 700;">int</span> <span class="hljs-title" style="color: rgb(136, 0, 0); font-weight: 700;">main</span><span class="hljs-params">(<span class="hljs-keyword" style="font-weight: 700;">int</span> argc, <span class="hljs-keyword" style="font-weight: 700;">char</span> **argv)</span> </span>{
    <span class="hljs-keyword" style="font-weight: 700;">if</span> (argc &gt; <span class="hljs-number" style="color: rgb(136, 0, 0);">1</span>){
        message(argv[<span class="hljs-number" style="color: rgb(136, 0, 0);">1</span>]);
    } <span class="hljs-keyword" style="font-weight: 700;">else</span> {
        <span class="hljs-built_in" style="color: rgb(57, 115, 0);">printf</span>(<span class="hljs-string" style="color: rgb(136, 0, 0);">"Usage: ./overflow &lt;message&gt;\\n"</span>);
    }
    <span class="hljs-keyword" style="font-weight: 700;">return</span> <span class="hljs-number" style="color: rgb(136, 0, 0);">0</span>;
}

</pre>`

export {
    cProgram
}