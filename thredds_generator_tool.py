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

    def do_setup(self, url):
        if len(url) < 1:
            url = "https://vortices.npm.ac.uk/thredds/"
        print "you wanted to explore %s" % url
        self.t_crawl = ThreddsCrawler(url)
        self.t_crawl.getTopLevel()

    def do_catalogs(self, line):
        print self.t_crawl.display_catalogs()

    def do_debug(self, line):
        print self.t_crawl.catalog

    def do_q(self, line):
        return self.do_quit('')

    def do_template(self, line):
        print self.t_crawl.t_test()

    def do_generate(self, line):
        gen = GenMenu(self.t_crawl)
        gen.cmdloop()

    def do_getdataset(self, arg):
        print arg
        if int(arg) in [x['id'] for x in self.t_crawl.catalog['top_level']]:
            print self.t_crawl.getSub(arg)
        else:
            print "ERROR : please select a number from the below"
            self.do_datasets('')

    def do_quit(self, line):
        return True


class GenMenu(cmd.Cmd):

    """docstring for GenMenu"""

    def __init__(self, catalog):
        cmd.Cmd.__init__(self)
        self.catalog = catalog
        self.prompt = "GEN > "

    def do_test(self, line):
        print self.catalog.catalog

    def do_quit(self, line):
        return True


if __name__ == '__main__':
    ThreddsExplorer().cmdloop()
