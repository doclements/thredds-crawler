#!/usr/bin/env python

"""
The main entry point into the interactive Thredds Data Server
summmary generator.

The tool allows you to interactively explore a thredds instance, 
find out what data are available and through which service. It will 
also allow the generation of HTML and JSON summaries of Thredds offerings"""

import cmd
from ThreddsCrawler import ThreddsCrawler

class ThreddsExplorer(cmd.Cmd):
   """docstring for ThreddExplorer"""
   def __init__(self):
      cmd.Cmd.__init__(self)
      self.prompt = "> "

   def do_setthredds(self, url):
      print "you wanted to explore %s" % url
      self.t_crawl = ThreddsCrawler(url)

   def do_get_top_level(self, line):
      print self.t_crawl.getTopLevel()

   def do_debug(self, line):
      print self.t_crawl.catalog
   def do_q(self, line):
      return self.do_quit('')
   def do_1(self, line):
      print self.lastcmd
      if self.lastcmd is "get_top_level":
         print "you are allowed to do that now"
      else:
         pass
   def do_generate(self, line):
      gen = GenMenu(self.t_crawl)
      gen.cmdloop()

   def do_quit(self, line):
      return True

class GenMenu(cmd.Cmd):
   """docstring for GenMenu"""
   def __init__(self, catalog):
      cmd.Cmd.__init__(self)
      self.catalog = catalog
      self.prompt = "GEN > "

   def do_test(self,line):
      print self.catalog.catalog
   def do_quit(self, line):
      return True
      

if __name__ == '__main__':
    ThreddsExplorer().cmdloop()