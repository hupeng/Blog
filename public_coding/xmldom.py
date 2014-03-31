# -*- coding: utf-8 -*-
from xml.dom.minidom import Document, parse, parseString
from object_dict import object_dict
import types
import re


#xml label attribute tag and value tag in dict
XML_ATTRIBUTE = 'xml_attribute'
XML_VALUE = 'xml_value'


class DomCreateXMLFromDict(object):
    xmlstring=''
    encoding= None
    doc = None

    def __init__(self):
        self.doc = Document()
        self.xmlstring = ''
        self.encoding = None

    def _set_encoding(self, encode):
        self.encoding = encode[:]

    def _get_encoding(self):
        return self.encoding

    ##@ append a node 
    def _append_node(self,ele_child, element=None):
        if element is None:
            self.doc.appendChild(ele_child)
        else:
            element.appendChild(ele_child)
            
    ##@ append a node of attribute
    def _append_attri(self, element, node):
        if XML_ATTRIBUTE in element:
            attrnodes = element[XML_ATTRIBUTE]
            if type(attrnodes) is not types.StringType:
                for attr in attrnodes:
                    node.setAttribute(attr, attrnodes[attr])

    ##@ create nodes of tree
    def _create_node(self, elements, parent=None):
        for ele_node in elements:
            if ele_node == XML_ATTRIBUTE:
                continue
            if ele_node == XML_VALUE:
                for values in elements[ele_node]:
                    self._create_node(values, parent)
                continue
            element = elements[ele_node]
            node = self.doc.createElement(ele_node)
            self._append_attri(element, node)
            if type(element) is types.StringType:
                node_value = self.doc.createTextNode(element)
                node.appendChild(node_value)
            elif type(element) is types.ListType:
                for listnode in element:
                    self._create_node(listnode, node)
                    self._append_node(node, parent)
                    node = self.doc.createElement(ele_node)
                del node
                continue
            else:
                self._create_node(element,node)
                
            self._append_node(node, parent)

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
                                self.doc.toprettyxml(newl=newl, encoding=self._get_encoding() ) )
        return self.xmlstring



class DomParseXMLToDict(object):
    ##@delete dom create word
    XML_SUPERWORD=('\t', '\t\n', '\n', '\t\t', '\t\t\t')
    
    def __init__(self):
        pass

    ##@get node attribute and append to dict
    ## Save attrs and text, hope there will not be a child with same name
    def _append_attribute(self, node, node_tree = None):
        if node_tree is None:
            node_tree = object_dict()
        bCreateAttr = True
        for attr in node.attributes.keys():
            if bCreateAttr:
                node_tree[XML_ATTRIBUTE] = object_dict()
                bCreateAttr = False
            k,v = self._namespace_split(attr.encode(), node.getAttribute(attr).encode())
            node_tree[XML_ATTRIBUTE][k] = v
        return node_tree

    ##@Parse a xml node to dict
    def _parse_node(self, node):
        node_tree = object_dict()        
        #append attribute
        self._append_attribute(node, node_tree)
        if len(node.attributes.keys()) <1:
            node_dicts = node_tree
        else:
            node_tree[XML_VALUE] ={}
            node_dicts = node_tree[XML_VALUE]
        for child in node.childNodes:
            nodename = child.nodeName.encode()          
            if child.nodeType in (child.TEXT_NODE, child.CDATA_SECTION_NODE):
                nodeval = child.nodeValue.encode()
                if nodeval not in self.XML_SUPERWORD:
                    '''coding may be had error'''
                    node_tree = child.nodeValue.decode().encode()
                continue            
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
                nodenum = len(child.childNodes)
                if nodenum<1:
                    node_dicts[tag] = tree
                else:
                    if nodenum ==1:
                        if child.childNodes[0].nodeType in (child.TEXT_NODE, child.CDATA_SECTION_NODE):
                            node_dicts[tag] = tree
                        else:
                            node_dicts.pop(tag)
                            node_dicts[tag] = [tree]
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
        s = self.convert_to_utf(s)
        #if s:
        try:
            doc = parseString(s)
            t = doc.documentElement
            root_tag, root_tree = self._namespace_split(t.nodeName, self._parse_node(t))
            return object_dict({root_tag.encode(): root_tree})
        except:
            pass
        return object_dict({'parse_error': 'parse error'})


if __name__=='__main__':
    xmlparse = DomParseXMLToDict()
    xmlres = xmlparse.parse(unicode('E:\\NAVIUSER\\xmljson\\tomcat-users.xml'))
    
