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
            'catalog': 'http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0',
            'xlink': 'http://www.w3.org/1999/xlink'
        }
      #   self.top_template = """
      # Name : %(title)s
      # services : %(services)s
      # catalogs : %(catalogs)s
      # """
      #   self.catalog = {
      #       'base_url': self.url
      #   }
        #self.catalog['services'] = []
        #self.catalog['top_level'] = []
        
        self.env = Environment(
            loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

  
        xml_catalog = self._fetchXml('/catalog.xml')
        xml_root = etree.fromstring(xml_catalog)

        title = self._getNode(
            xml_root, '/catalog:catalog/@name')[0]
        services = [(x['base'], x['name'], x['serviceType']) for x in [dict(x.items()) for x in self._getNode(
            xml_root, '/catalog:catalog/catalog:service/catalog:service')]]
        
        catalogs = zip(self._getNode(xml_root, '/catalog:catalog/catalog:catalogRef/@xlink:href'),
                       self._getNode(xml_root, '/catalog:catalog/catalog:catalogRef/@xlink:title'))
        
        self.server = TDSServer(url, title)

        for s in services:
            self.server.add_service(TDSService(s[1], s[2], s[0]))
        catalog_index = 1
        for c in catalogs:
            self.server.add_catalog(TDSCatalog(c[0], c[1], catalog_index))
            catalog_index = catalog_index + 1

    def get_services(self, xml_root):
        return [(x['base'], x['name'], x['serviceType']) for x in [dict(x.items()) for x in self._getNode(
            xml_root, '/catalog:catalog/catalog:service/catalog:service')]]

    def get_datasets(self, xml_root):
        return [(x['name'], x['urlPath']) for x in [dict(x.items()) for x in self._getNode(xml_root, '/catalog:catalog/catalog:dataset/catalog:dataset')] if 'urlPath'  and 'name' in x]

    def get_catalogs(self, xml_root):
        return zip(self._getNode(xml_root, '/catalog:catalog//catalog:catalogRef/@xlink:href'),
                       self._getNode(xml_root, '/catalog:catalog//catalog:catalogRef/@xlink:title'))

    def getSub(self, id):
        choice = [
            x for x in self.server.catalogs if x.id is int(id)][0]
        #print choice
        xml = self._fetchXml(choice.url)
        self.populate_catalog(choice, xml)
        return choice

    def populate_catalog(self, catalog, xml):
        xml = etree.fromstring(xml)
        for s in self.get_services(xml):
           catalog.add_service(TDSService(s[1], s[2], s[0]))
        catalog_index = 1
        for c in self.get_catalogs(xml):
           _catalog = TDSCatalog(c[0], c[1], catalog_index)
           #self.populate_catalog()
           catalog.add_catalog(_catalog)
           catalog_index = catalog_index + 1
        for d in self.get_datasets(xml):
           catalog.add_dataset(TDSDataset(d[0],d[1])) 



    def display_catalogs(self):
        return self.env.get_template('test.template').render(catalog=self.server)

    def print_datasets(self):
        return self.top_template % {'name': self.server.title, 'services': ','.join([x[1] for x in self.server.services]), 'catalogs': self.catalogs}

    def _fetchXml(self, href):
        doc = urllib2.urlopen(self.url + href)
        xml = doc.read()
        doc.close()
        return xml

    def _getNode(self, root, xpath):
        return root.xpath(xpath, namespaces=self.namespaces)


class TDSServer(object):
   """docstring for TDSServer"""
   def __init__(self, url, title):
      super(TDSServer, self).__init__()
      self.url = url
      self.title = title
      self.catalogs = []
      self.services = []

   def add_catalog(self, catalog):
      self.catalogs.append(catalog)

   def add_service(self, services):
      self.services.append(services)


class TDSService(object):
   """docstring for TDSService"""
   def __init__(self, name, service_type, base_path):
      super(TDSService, self).__init__()
      self.name = name
      self.type = service_type
      self.path = base_path

   def __str__(self):
      attrs = vars(self)
      return ', '.join("%s: %s" % item for item in attrs.items())

      

class TDSDataset(object):
   """docstring for TDSDataset"""
   def __init__(self, name, url):
      super(TDSDataset, self).__init__()
      self.name = name
      self.urlPath = url
      self.catalogs = []
   
   def add_catalog(self, catalog):
      self.catalogs.append(catalog)   

   def __str__(self):
      attrs = vars(self)
      return ', '.join("%s: %s" % item for item in attrs.items())

      

class TDSCatalog(object):
   """docstring for TDSCatalog"""
   def __init__(self, url, title, id):
      super(TDSCatalog, self).__init__()
      self.id = id
      self.url = url
      self.title = title
      self.catalogs = []
      self.services = []
      self.datasets = []

   def add_catalog(self, catalog):
      self.catalogs.append(catalog)

   def add_dataset(self, dataset):
      self.datasets.append(dataset)

   def add_service(self, services):
      self.services.append(services)

   def __str__(self):
      attrs = vars(self)
      return ', '.join("%s: %s" % item for item in attrs.items())
