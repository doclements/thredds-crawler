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

   def do_setthredds(self, url):
      print "you wanted to explore %s" % url
      self.t_crawl = ThreddsCrawler(url)

   def do_get_top_level(self, line):
      print self.t_crawl.getTopLevel()

   def do_q(self, line):
      return self.do_quit('')
      
   def do_quit(self, line):
      return True


if __name__ == '__main__':
    ThreddsExplorer().cmdloop()