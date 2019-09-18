
''' extracts xbrl or xbrli tags that have context (period). 
how to use:
import xbrl
xbrl.extract(url: str) -> [ {k:v for k in [namespace, tag, startDate, endDate, unit, value]} ]

examples:
url = 'https://www.xbrl.org/ixbrl-samples/faurecia-info-by-segment-viewer.html'
url = 'https://www.sec.gov/Archives/edgar/data/1000045/0001564590-19-031992.txt'
tags = extract(url)
'''

from lxml import etree
import requests

def extract(url):
    def scale_value (row):
        try:
            value = float(row.get('text').replace(',', ''))
            value = -value if row.get('sign')=='-' else value
            scale = int(row.get('scale', 1))
            return (value * 10 ** scale)
        except:
            return row.get('text')
    try:
        cols = ['namespace', 'tag', 'endDate', 'startDate', 'unit', 'value']
        e = parse_url_to_etree (url)
        tags = decode_tags(e)
        endDates, startDates = decode_contextRef(e)
        unitRef = decode_unitRef(e)
        # embed referenced values
        for tag in tags:
            tag['endDate'] = endDates.get(tag.get('contextRef'))
            tag['startDate'] = startDates.get(tag.get('contextRef'))
            tag['unit'] = unitRef.get(tag.get('unitRef'))
            tag['value'] = scale_value(tag)
        # filter columns
        tags = [{k:v for k,v in tag.items() if k in cols} for tag in tags]
        return tags
    except:
        print('Error! could not extract {}'.format(url))
        return None


def parse_url_to_etree (url):
    r = requests.get(url)
    text = r.content
    text = text.replace(b'xmlns', b'empty')
    text = text.replace(b':', b'__')
    parser = etree.XMLParser(recover=True, ns_clean=False)
    e = etree.fromstring(text, parser=parser)
    return e


def etree_to_dict(el, recursive=True):
    d = {k:v for k,v in el.attrib.items()}
    d['text'] = el.text
    d['tag'] = el.tag
    children = el.getchildren()
    if len(children) and recursive: 
        d['children'] = [etree_to_dict(child) for child in children]
    return d


# to decode tags of gaap and ifrs
def decode_tags (e):
    tags = e.xpath("//*[@contextRef]") # if an element has contextRef it is considered a xbrl tag
    tag_records = [etree_to_dict(tag, recursive=False) for tag in tags]
    for record in tag_records:
        tag = record.get('name') or record.get('tag')
        record['namespace'], record['tag'] = tag.split('__', 1)
        record.pop('name', None) 
    return tag_records

# extract dates
def decode_contextRef (e):
    startDates = e.xpath('.//xbrli__context/xbrli__period/xbrli__startDate')
    startDates = {el.getparent().getparent().attrib['id']: el.text for el in startDates}
    endDates = e.xpath('.//xbrli__context/xbrli__period/xbrli__endDate')
    endDates = {el.getparent().getparent().attrib['id']: el.text for el in endDates}
    instants = e.xpath('.//xbrli__context/xbrli__period/xbrli__instant')
    instants = {el.getparent().getparent().attrib['id']: el.text for el in instants}
    endDates = {**instants, **endDates}
    return endDates, startDates

# decode units
def decode_unitRef(e):
    unitRef = e.xpath('.//xbrli__unit/xbrli__measure')
    unitRef = {el.getparent().attrib['id']: el.text.partition('__')[-1] for el in unitRef}
    return unitRef

def decode_symbol (e):
    symbols = e.xpath('.//dei__TradingSymbol')
    symbol = symbols[0].text.lower if len(symbols) else None
    return symbol

'''
ns = e.nsmap
ns.pop(None)

ix = [k for k in ns.values() if k.endswith('inlineXBRL')]
xbrli = [k for k in ns.values() if k.endswith('instance')]
ifrs_full = [k for k in ns.values() if k.endswith('ifrs-full')]
us_gaap = [k for k in ns.values() if k.endswith('ifrs-full')] 
'''

