#!/usr/bin/env python

"""
does some stuff
"""

import urllib2
from lxml import etree
from jinja2 import Environment, FileSystemLoader
import os



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
      self.env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))


   def getTopLevel(self):
      xml_catalog = self._fetchXml('/catalog.xml')
      xml_root = etree.fromstring(xml_catalog)
      self.catalog['title'] = self._getNode(xml_root,'/catalog:catalog/@name')[0]
      services = [(x['base'], x['name']) for x in [dict(x.items()) for x in self._getNode(xml_root, '/catalog:catalog/catalog:service/catalog:service')]]
      for s in services:
         self.catalog['services'].append({
            'name' : s[1],
            'base' : s[0]
            })
      catalogs = zip(self._getNode(xml_root ,'/catalog:catalog/catalog:catalogRef/@xlink:href') , self._getNode(xml_root, '/catalog:catalog/catalog:catalogRef/@xlink:title'))
      catalog_index = 1
      for c in catalogs:
         self.catalog['top_level'].append({
            'id'    : catalog_index,
            'title' : c[1],
            'path'  : c[0]
            })
         catalog_index = catalog_index + 1
      
   def getSub(self,id):
      choice = [x for x in self.catalog['top_level'] if x['id'] is int(id)][0]
      print choice['path']

      xml = self._fetchXml(choice['path'])
      return xml
   def display_catalogs(self):
      return self.env.get_template('test.template').render(catalog=self.catalog)

   def print_datasets(self):
      return self.top_template % {'name':self.catalog.title, 'services':','.join([x[1] for x in self.services]), 'catalogs': self.catalogs}

   def _fetchXml(self, href):
      doc = urllib2.urlopen(self.url+href)
      xml = doc.read()
      doc.close()
      return xml

   def _getNode(self, root, xpath):
      return root.xpath(xpath, namespaces=self.namespaces)
       
