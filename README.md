<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/marked/0.7.0/marked.min.js"></script>
    <script>
        document.addEventListener("DOMContentLoaded", function(){
            document.body.innerHTML = marked(document.body.innerHTML)
        })
    </script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css" />
    <style>
        form {border: 1px outset; padding: 1em; max-width: 30em; display: inline-block;}
        html {margin: auto; padding: 1em; max-width: 90em; border: 1px outset; color:black;}
    </style>
</head>
<body class='markdown-body'>

### Financial Data Extractor
Extract financial tags from xml, SEC submissions, xlbr, xlbri, or html

https://extract-xml-5kwedaonla-uc.a.run.app/extract-xml.html

##### Demo

<center><form enctype="multipart/form-data" method='post' action='/extract-xml'>
    <input type='radio' name='input_type' value='url' checked> url to extract: <input name='url' type='url'> <br>
    <input type='radio' name='input_type' value='file'> file to extract: <input name='file' type='file'> <br>
    output
    <select name='output'>
        <option type='radio' value='json' selected>json</option>
        <option type='radio' value='csv'>csv</option>
    </select><br>
    <input type='submit'><br>
    Enter url or fila path to the xml document that you want to extract its financial tags.
</form></center>

##### how to `get` it through browser?
if you have the url to your file:
https://extract-xml-5kwedaonla-uc.a.run.app/extract-xml?url=your-url

example: https://extract-xml-5kwedaonla-uc.a.run.app/extract-xml?url=https://www.sec.gov/Archives/edgar/data/1000045/0001564590-19-031992.txt


```js
// in js:
fetch(https://extract-xml-5kwedaonla-uc.a.run.app/extract-xml?url=your-url).then(function(tags){
    //do something with tags
})
// in python:
import pandas as pd
tags = pd.read_csv(https://extract-xml-5kwedaonla-uc.a.run.app/extract-xml?url=your-url)
```

##### How to get it in csv format
Add `\&format=csv` to the end of your query.

example: https://extract-xml-5kwedaonla-uc.a.run.app/extract-xml?url=https://www.sec.gov/Archives/edgar/data/1000045/0001564590-19-031992.txt&format=csv


##### how to use it with google sheets
in a cell write formula `=importdata(https://extract-xml-5kwedaonla-uc.a.run.app/extract-xml?url=your-url&format=csv)`

##### how to use the library
The extractor is written in python. Download file "extract_xbrl.py" to your project and then

```py
import xbrl, requests
xml_text = requests.get(url_to_xml_doc).content
tags = xbrl.Extract(xml_text)
```

</body>
</html>




