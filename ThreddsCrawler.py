#!/usr/bin/env python

"""
does some stuff
"""

import urllib2
from lxml import etree


class ThreddsCrawler():
   """docstring for ThreddsCrawler"""
   def __init__(self, url):
      
      self.url = url
      self.namespaces = {
         'catalog' : 'http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0',
         'xlink'   : 'http://www.w3.org/1999/xlink'
      }
      self.top_template = """
      Name : %(name)s
      services : %(services)s
      catalogs : %(catalogs)s
      """
      self.catalog = {
      'base_url' : self.url
      }
      self.catalog['services'] = []
      self.catalog['top_level'] = []


   def getTopLevel(self):
      xml_catalog = self._fetchXml('/catalog.xml')
      xml_root = etree.fromstring(xml_catalog)
      title = self._getNode(xml_root,'/catalog:catalog/@name')[0]
      services = [(x['base'], x['name']) for x in [dict(x.items()) for x in self._getNode(xml_root, '/catalog:catalog/catalog:service/catalog:service')]]
      for s in services:
         self.catalog['services'].append({
            'name' : s[1],
            'base' : s[0]
            })
      catalogs = zip(self._getNode(xml_root ,'/catalog:catalog/catalog:catalogRef/@xlink:href') , self._getNode(xml_root, '/catalog:catalog/catalog:catalogRef/@xlink:title'))
      for c in catalogs:
         self.catalog['top_level'].append({
            'title' : c[1],
            'path'  : c[0]
            })
      return self.top_template % {'name':title, 'services':','.join([x[1] for x in services]), 'catalogs': catalogs}


   def _fetchXml(self, href):
      doc = urllib2.urlopen(self.url+href)
      xml = doc.read()
      doc.close()
      return xml

   def _getNode(self, root, xpath):
      return root.xpath(xpath, namespaces=self.namespaces)
       
