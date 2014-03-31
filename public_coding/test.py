#coding: utf-8
#xml test
from xml_create import MyCreateXMLFromDict
from xmldom import DomCreateXMLFromDict, DomParseXMLToDict
from json_code import json_encode
from ctypes import *
from xmletree import EtreeParseXMLToDict,EtreeCreateXMLFromDict

if __name__ == "__main__":
    """
    xmlModel ={'opg':{'activitycode':'002',\
                      'processtime':'20110328',\
                      'actioncode':'0',\
                      'svccont':{'info':[{'uuid':'a14ee68026c3f9a2561935760c25319a'}]
                                 }
                      }
               }
    
    xmlModel ={'poi':{'xml_attribute':'type="userdefined" from="iphone" language="zh-cn" out="xml"',
                      'origin_type':'酒店', 'custom_type':'酒店', 'name':'厦门百翔酒店',
                      'address':'厦门软件园二期观日路1号','tel':'0592-6307888', 'adcode':'361008', 'town':'思明区',
                      'latitude':'24.490898', 'longitude':'118.175898', 'is_offset':'true',
                      'bind_road':'1100000', 'bind_cross':'1100000-1100001', 'bind_cross_type':'0',
                      'description':'百翔酒店', 'flag':'0x000001', 'use_type':'1'
                      }
               }
    xmlModel ={'poi':{'xml_attribute':{'type':'userdefined', 'from':'iphone', 'language':'zh-cn','out':'xml'},
                      'origin_type':r'酒店', 'custom_type':r'酒店', 'name':r'厦门百翔酒店',
                      'address':r'厦门软件园二期观日路1号','tel':'0592-6307888', 'adcode':'361008', 'town':r'思明区',
                      'latitude':'24.490898', 'longitude':'118.175898', 'is_offset':'true',
                      'bind_road':'1100000', 'bind_cross':'1100000-1100001', 'bind_cross_type':'0',
                      'description':r'百翔酒店', 'flag':'0x000001', 'use_type':'1'
                      }
               }
    """
    xmlModel ={'opg':{'activitycode':'002',\
                      'processtime':'20110328',\
                      'actioncode':'0',\
                      'svccont':{'list':[{'xml_attribute':{'size':'0'}}, {'info':{'uuid':'0002444'}}]
                                 }
                      }
               }
    '''
    xmlOperate = MyCreateXMLFromDict()
    #xmlOperate = DomCreateXMLFromDict()
    #xmlOperate = EtreeCreateXMLFromDict()
    xmldoc = xmlOperate.createXML(xmlModel, 'UTF-8')
    print 'xmldoc'
    print xmldoc
    '''
    dictOperate =EtreeParseXMLToDict()
    dicts = dictOperate.fromstring(xmldoc)
    print 'dicts'
    print dicts
        
    print 'json'
    json_result = json_encode(dicts)
    print json_result
