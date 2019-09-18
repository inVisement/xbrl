# xbrl
extract financial tags and information from XBRL or XBRLinline

It is a very light python code that extract all tags (such as us-gaap or ix or dei or ifrs tags) for given url that contains XBRL or XBRLinline document. This is useful for extracting financial statements that corporates submit to SEC.

## How To Use
Install this module (download on your local machine) or
pip install git+https://github.com/inVisement/xbrl

import xbrl
xbrl(url)

## Example
``` python
url = 'https://www.xbrl.org/ixbrl-samples/faurecia-info-by-segment-viewer.html'
url = 'https://www.sec.gov/Archives/edgar/data/1000045/0001564590-19-031992.txt'

dict = xbrl.extract(url)

### to dataframe
df = pd.DataFrame(dict)
```
