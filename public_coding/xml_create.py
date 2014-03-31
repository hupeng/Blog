#coding: utf-8
#xml config and operations
import types

#xml label attribute tag and value tag in dict
XML_ATTRIBUTE = 'xml_attribute'
XML_VALUE = 'xml_value'

class MyCreateXMLFromDict:
    #class option
    encoding = None
    xmlstring = None

    def _set_encoding(self, encode):
        if encode is  None:
            self.encoding = None
        else:
            self.encoding = encode[:]

    def _get_encoding(self):
        return self.encoding

    ##@ create xml format header 
    def _create_xml_header(self, newl=""):
        xmlhead=''
        if self._get_encoding() is None:
            xmlhead = ''.join('<?xml version="1.0" ?>'+newl)
        else:
            xmldata = '<?xml version="1.0" encoding="%s"?>%s' % (self.encoding, newl)
            xmlhead = ''.join(xmldata)
        return xmlhead

    ##@ create a xml node which has node value
    def _create_element(self, element, elename):
        nodestart = '<' + elename + '>'
        nodeend ='</' + elename + '>'
        return (nodestart + elename + nodeend)

    ##@ get a xml node start half
    def _add_node_addstart(self, nodename):
        return '<' + nodename

    ##@ get a xml node  end half of the start tag
    def _add_node_addend(self, nodename):
        return nodename + '>'

    ##@ get a xml node start tag
    def _add_node_start(self, nodename):
        return '<' + nodename + '>'

    ##@ get a xml node end tag
    def _add_node_end(self, nodename):
        return '</' + nodename + '>'

    ##@ get and set attributes of the xml node which has attributes
    def _append_attri(self, node, nodename):
        if XML_ATTRIBUTE in node:
            attrnodes = node[XML_ATTRIBUTE]
            if type(attrnodes) is types.StringType:
                self.xmlstring = self.xmlstring + self._add_node_addstart(nodename + ' ' + attrnodes)
            else:
                self.xmlstring = self.xmlstring + self._add_node_addstart(nodename + ' ' )
                for attr in attrnodes:
                    self.xmlstring = self.xmlstring + attr + '="' + attrnodes[attr] +'" '
                self.xmlstring = self._add_node_addend(self.xmlstring)
        else:
            self.xmlstring = self.xmlstring + self._add_node_start(nodename)

    ##@ create xml format node 
    def _create_node(self, parent):
        for child in parent:
            if child == XML_ATTRIBUTE:
                continue
            node = parent[child]                
            self._append_attri(node, child)
            if type(node) is types.StringType:
                self.xmlstring = self.xmlstring + node
            elif type(node) is types.ListType:
                bHaveStart = True
                for listnode in node:
                    if bHaveStart is True:
                        bHaveStart = False
                    else:
                        self.xmlstring = self.xmlstring + self._add_node_start(child)
                    self._create_node(listnode)
                    self.xmlstring = self.xmlstring + self._add_node_end(child)
                continue
            else:
                self._create_node(node)
            
            self.xmlstring = self.xmlstring + self._add_node_end(child)      

    ##@ create a xml format from a dict
    ##  you can set encoding and newl
    ##  if the param encoding is None , we will set 'UTF-8' as normal encoding setting
    def createXML(self, elements, encoding =None, newl=""):
        self.xmlstring =''
        #set encoding
        if encoding is None:
            encoding ='UTF-8'
        self._set_encoding(encoding)
        #get xml header
        xmlhead = self._create_xml_header(newl=newl)
        self.xmlstring = self.xmlstring + xmlhead
        #create xml body
        self._create_node(elements)
        #string encode
        if self._get_encoding() is not None:
            self.xmlstring = self.xmlstring.encode(self._get_encoding())
        return self.xmlstring
    

    
        
