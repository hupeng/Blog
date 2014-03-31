# -*- coding: utf-8 -*-
from xml.etree import ElementTree as ET
from object_dict import object_dict
import types
import re


#xml label attribute tag and value tag in dict
XML_ATTRIBUTE = 'xml_attribute'
XML_VALUE = 'xml_value'


class EtreeCreateXMLFromDict(object):
    xmlstring=''
    encoding= None
    doc = None

    def __init__(self):
        self.doc = None
        self.xmlstring = ''
        self.encoding = None

    def _set_encoding(self, encode):
        self.encoding = encode[:]

    def _get_encoding(self):
        return self.encoding
            
    ##@ append a node of attribute
    def _append_attri(self, element, node):
        if XML_ATTRIBUTE in element:
            attrnodes = element[XML_ATTRIBUTE]
            if type(attrnodes) is not types.StringType:
                for attr in attrnodes:
                    node.set(attr, attrnodes[attr])

    ##@ create nodes of tree
                
    def _create_node(self, elements, parent=None):
        for ele_node in elements:
            if ele_node == XML_ATTRIBUTE:
                continue
            if ele_node == XML_VALUE:
                #for values in elements[ele_node]:
                self._append_attri(elements[ele_node], parent)
                continue
            #print type(elements[ele_node]);print ':';print ele_node;print ':'; print elements[ele_node];
            element = elements[ele_node]
            node = None
            if type(element) is types.StringType:
                if parent is None:
                    node = ET.Element(ele_node)
                    self.doc=node
                else:
                    node = ET.SubElement(parent, ele_node)
                node.text = element
            elif type(element) is types.ListType:
                for listnode in element:
                    self._create_node({ele_node:listnode}, parent)
                continue
            elif type(element) is types.UnicodeType:
                if parent is None:
                    node = ET.Element(ele_node)
                    self.doc=node
                else:
                    node = ET.SubElement(parent, ele_node)
                node.text = element
            elif type(element) is types.FloatType:
                if parent is None:
                    node = ET.Element(str(ele_node))
                    self.doc=node
                else:
                    node = ET.SubElement(parent, str(ele_node))
                node.text = str(element)
            elif type(element) is types.LongType:
                if parent is None:
                    node = ET.Element(str(ele_node))
                    self.doc=node
                else:
                    node = ET.SubElement(parent, str(ele_node))
                node.text = str(element)
            elif type(element) is types.IntType:
                if parent is None:
                    node = ET.Element(ele_node)
                    self.doc=node
                else:
                    node = ET.SubElement(parent, ele_node)
                node.text = str(element)
            elif type(element) is types.NoneType:
                if parent is None:
                    node = ET.Element(ele_node)
                    self.doc=node
                else:
                    node = ET.SubElement(parent, ele_node)
                node.text = ''
            else:
                if parent is None:
                    node = ET.Element(ele_node)
                    self.doc=node
                else:
                    node = ET.SubElement(parent,ele_node)
                self._create_node(element,node)

    ##@ from dict create and return xml string 
    def createXML(self, elements, encoding =None, newl=""):
        self.xmlstring =''
        #set encoding
        if encoding is None:
            encoding ='UTF-8'
        self._set_encoding(encoding)
        #create xml doc
        self._create_node(elements)
        #get xml string
        self.xmlstring = re.sub(r'(<[^/][^<>]*[^/]>)\s*([^<>]{,40}?)\s*(</[^<>]*>)', r'\1\2\3',\
                                ET.tostring(self.doc, encoding=self.encoding) )
        if self.encoding in ('utf-8', 'us-ascii'):
            xmlhead = "<?xml version='1.0' encoding='%s'?>\n" % self.encoding
            self.xmlstring = xmlhead + self.xmlstring
        return self.xmlstring


class EtreeParseXMLToDict(object):
    ##@delete dom create word
    XML_SUPERWORD=('\t', '\t\n', '\n', '\t\t', '\t\t\t')
    
    def __init__(self):
        pass

    ##@get node attribute and append to dict
    ## Save attrs and text, hope there will not be a child with same name
    def _append_attribute(self, node, node_tree = None):
        if node_tree is None:
            node_tree = object_dict()
        if len(node.attrib.items()) <1:
           return node_tree
        node_tree[XML_ATTRIBUTE]=object_dict()
        itemdicts = node_tree[XML_ATTRIBUTE]
        for (attr,item) in node.attrib.items():
            k,v = self._namespace_split(attr, item)
            itemdicts[k] = v
        return node_tree

    ##@Parse a xml node to dict
    def _parse_node(self, node):
        node_tree = None
        #print node;print node.text
        if node.text:
            if node.text not in self.XML_SUPERWORD:
                '''coding may be had error'''
                node_tree = node.text
                return node_tree
        
        node_tree = object_dict()
        if len(node.attrib.items()) <1:
            node_dicts = node_tree
        else:
            node_tree[XML_VALUE] ={}
            node_dicts = node_tree[XML_VALUE]
        for child in node.getchildren():
            nodename = child.tag
            #Save childrens
            tag, tree = self._namespace_split(nodename, self._parse_node(child))
            """
            # the first time, so store it in dict
            if  tag not in node_tree: 
                node_tree[tag] = tree
                continue
            """
            # the first time, if the node have child so store it in list ,other raise  store it in dict
            
            if  tag not in node_dicts: 
                node_dicts[tag] = tree
                if len(child.getchildren())<1:
                    node_dicts[tag] = tree
                else:
                    node_dicts.pop(tag)
                    node_dicts[tag] = [tree]
                continue

            old = node_dicts[tag]
            if not isinstance(old, list):
                node_dicts.pop(tag)
                # multi times, so change old dict to a list
                node_dicts[tag] = [old]
            # add the new one
            node_dicts[tag].append(tree)
        #append attribute
        self._append_attribute(node, node_tree)
        return  node_tree

    ##@ namespace split
    def _namespace_split(self, tag, value):
        """
            Split the tag  '{http://cs.sfsu.edu/csc867/myscheduler}patients'
            ns = http://cs.sfsu.edu/csc867/myscheduler
            name = patients
        """
        result = re.compile("\{(.*)\}(.*)").search(tag)
        if result:
            value.namespace, tag = result.groups()
        return (tag, value)

    ##@parse a xml file to a dict
    def parse(self, file):
        f = open(file, 'r')
        return self.fromstring(f.read())

    ##@encode to utf-8"  python can not parase xml encoding like GBK encoding,
    ## so we must turn xml encoding to its nomal encoding
    def convert_to_utf(self,xmlstring):
        if not isinstance(xmlstring, unicode):
            xmlpost = xmlstring.find('?>', 0,50)
            if xmlpost>0:
                startpost = xmlstring.find('encoding=',0,xmlpost)
                if startpost >0:
                    start = startpost + len('encoding=')
                    endpost = xmlstring.find('"', start+2,start+10)
                    if endpost>0:
                        decoding = xmlstring[start+1:endpost]
                        xmlstring = xmlstring[:startpost] + 'encoding="UTF-8"' + xmlstring[endpost+1:]
                        try:
                            xmlstring = xmlstring.decode(decoding).encode()
                        except:
                            pass
                    else:
                        endpost = xmlstring.find('\'', start+2,start+10)
                        if endpost>0:
                            decoding = xmlstring[start+1:endpost]
                            xmlstring = xmlstring[:startpost] + 'encoding="UTF-8"' + xmlstring[endpost+1:]
                            try:
                                xmlstring = xmlstring.decode(decoding).encode()
                            except:
                                pass
                else:
                    xmlstring = xmlstring[:startpost] + 'encoding="UTF-8"' + xmlstring[startpost:]
        return xmlstring

    ##@parse a xml format string
    ## if failed ,it will return a error dict ,its tag is 'parse_error', and its value is 'parse error'
    def fromstring(self, s):
        xmlstring = self.convert_to_utf(s)
        #if xmlstring:
        try:
            t = ET.fromstring(xmlstring)
            root_tag, root_tree = self._namespace_split(t.tag, self._parse_node(t))
            return object_dict({root_tag.encode(): root_tree})
        except:
            pass
        return object_dict({'parse_error': 'parse error'})

if __name__=='__main__':
    print '444'
    xmlparse = EtreeParseXMLToDict()
    xmlres = xmlparse.parse(unicode('E:\\NAVIUSER\\xmljson\\tomcat-users.xml'))
    print xmlres#.opg.svccont[0].list[0].xml_value.get('info')[0]
    #print xmlres
    #print xmlres.opg.get('actioncode')
    
