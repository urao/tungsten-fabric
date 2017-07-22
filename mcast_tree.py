# This script will help to print the multicast tree build with vrouters as nodes.
# Usage python mcast_tree.py -h
#

#! /usr/bin/env python

import sys
import argparse
import socket, struct
from urllib2 import urlopen, URLError, HTTPError
from datetime import datetime
from lxml import etree
from prettytable import PrettyTable
import itertools

debug = False
vertex_map = {}
graph_dict = {}
missing_nodes = []

class Node:
    def __init__(self, name, parent, *data):
        self.name = name
        self.parent = parent
        self.data = data
        self.children = []
        self.is_root = False

    def __repr__(self):
        return 'Node '+repr(self.name)

    def dic(self):
        retval = {self:[]}
        for i in self.children:
            retval[self].append(i.dic())
        return retval

    def display(self): # Here
        pass

    def has_children(self):
        return bool(self.children)

    def get_parent(self):
        return self.parent

    def add_child(self, name, *data):
        child = Node(name, self,*data)
        self.children.append(child)
        return child

    def display(self): # Here
        if not self.children:
            return self.name

        child_strs = [child.display() for child in self.children]
        child_widths = [block_width(s) for s in child_strs]

        # How wide is this block?
        display_width = max(len(self.name),
                    sum(child_widths) + len(child_widths) - 1)

        # Determines midpoints of child blocks
        child_midpoints = []
        child_end = 0
        for width in child_widths:
            child_midpoints.append(child_end + (width // 2))
            child_end += width + 1

        # Builds up the brace, using the child midpoints
        brace_builder = []
        for i in xrange(display_width):
            if i < child_midpoints[0] or i > child_midpoints[-1]:
                brace_builder.append(' ')
            elif i in child_midpoints:
                brace_builder.append('+')
            else:
                brace_builder.append('-')
        brace = ''.join(brace_builder)

        name_str = '{:^{}}'.format(self.name, display_width)
        below = stack_str_blocks(child_strs)

        return name_str + '\n' + brace + '\n' + below

class Introspec:

    output_etree = []
    tbl_col_max_width = 60

    def __init__ (self, host, port, max_width):

        self.host_urls = list()
        self.host_list = host.split(',')
        for ips in self.host_list:
            self.host_urls.append("http://" + ips + ":" + str(port) + "/")
        self.tbl_col_max_width = int(max_width)


    # get instrosepc output
    def get (self, path):

        self.output_etree = []

        for host_url in self.host_urls:
            while True: 
                url = host_url + path.replace(' ', '%20')
                if debug: print "DEBUG: retriving url " + url
                try:
                    response = urlopen(url)
                except HTTPError as e:
                    print 'The server couldn\'t fulfill the request.'
                    print 'URL: ' + url
                    print 'Error code: ', e.code
                    sys.exit(1)
                except URLError as e:
                    print 'Failed to reach destination'
                    print 'URL: ' + url
                    print 'Reason: ', e.reason
                    sys.exit(1)
                else:
                    ISOutput = response.read()
                    response.close()


                self.output_etree.append(etree.fromstring(ISOutput))
                #print etree.tostring(self.output_etree[0], pretty_print=True)
             
                if 'Snh_PageReq?x=' in path:
                    break

                # some routes output from vrouter may have pagination
                pagination = self.output_etree[-1].xpath("//Pagination/req/PageReqData")
                if len(pagination):
                    if (pagination[0].find("next_page").text is not None):
                        all = pagination[0].find("all").text
                        if(all is not None):
                            path = 'Snh_PageReq?x=' + all
                            self.output_etree = []
                            continue
                        else:
                            print "Warning: all page in pagination is empty!"
                            break
                    else:
                        break

                next_batch = self.output_etree[-1].xpath("//next_batch")

                if not len(next_batch):
                    break

                if (next_batch[0].text and next_batch[0].attrib['link']):
                    path = 'Snh_' + next_batch[0].attrib['link'] + '?x=' + next_batch[0].text
                else:
                    break
            if debug: print "instrosepct get completes\n"

    # print the introspect output in a table. args lists interested fields.
    def printTbl(self, xpathExpr, *args):

        fields = args if len(args) else [ e.tag for e in self.output_etree[0].xpath(xpathExpr)[0]]

        tbl = PrettyTable(fields)
        tbl.align = 'l'
        tbl.max_width = self.tbl_col_max_width

        # start building the table
        for tree in self.output_etree:
            for item in tree.xpath(xpathExpr):
                row = []
                for field in fields:
                    f = item.find(field)
                    if f is not None:
                        if f.text:
                            row.append(f.text)
                        elif list(f):
                            for e in f:
                                row.append(self.elementToStr('', e).rstrip())
                        else:
                            row.append("n/a")
                    else:
                        row.append("non-exist")
                tbl.add_row(row)

        print tbl

    # print the introspect output in human readable text
    def printText(self, xpathExpr):
        for tree in self.output_etree:
            for element in tree.xpath(xpathExpr):
                print self.elementToStr('', element).rstrip()

    # convernt etreenode sub-tree into a string
    def elementToStr(self, indent, etreenode):
        elementStr=''

        if etreenode.tag == 'more':   #skip more element
            return elementStr

        if etreenode.text and etreenode.tag == 'element':
            return indent + etreenode.text + "\n"
        elif etreenode.text:
            return indent + etreenode.tag + ': ' + etreenode.text.replace('\n', '\n' + indent + (len(etreenode.tag)+2)*' ') + "\n"
        elif etreenode.tag != 'list':
            elementStr += indent + etreenode.tag + "\n"

        if 'type' in etreenode.attrib:
            if etreenode.attrib['type'] == 'list' and etreenode[0].attrib['size'] == '0':
                return elementStr

        for element in etreenode:
            elementStr += self.elementToStr(indent + '  ', element)

        return elementStr

    def make_dict_from_tree(self, element_tree):
        """Traverse the given XML element tree to convert it into a dictionary.
        :param element_tree: An XML element tree
        :type element_tree: xml.etree.ElementTree
        :rtype: dict
        """
        def internal_iter(tree, accum):
            """Recursively iterate through the elements of the tree accumulating
            a dictionary result.

            :param tree: The XML element tree
            :type tree: xml.etree.ElementTree
            :param accum: Dictionary into which data is accumulated
            :type accum: dict
            :rtype: dict
            """
            if tree is None:
                return accum

            if tree.getchildren():
                accum[tree.tag] = {}
                for each in tree.getchildren():
                    result = internal_iter(each, {})
                    if each.tag in accum[tree.tag]:
                        if not isinstance(accum[tree.tag][each.tag], list):
                            accum[tree.tag][each.tag] = [
                                accum[tree.tag][each.tag]
                            ]
                        accum[tree.tag][each.tag].append(result[each.tag])
                    else:
                        accum[tree.tag].update(result)
            else:
                accum[tree.tag] = tree.text

            return accum

        return internal_iter(element_tree, {})

    def getMcastRouteTable(self, xml_etree, xpathExpr):
        mcast_dict = list()
        for tree in xml_etree:
            for element in tree.xpath(xpathExpr):
                mcast_dict = self.make_dict_from_tree(element)
        return mcast_dict 
 
class Contrail_CLI:

    def __init__(self, parser, host, port, max_width):

        parser.add_argument('--host', default=host, help="Introspect host(default='%(default)s')")
        parser.add_argument('--port', default=port, help="Introspect port(default='%(default)s')")
        self.subparser = parser.add_subparsers()
        self.IST = Introspec(host, port, max_width)


class Control_CLI(Contrail_CLI):

    def __init__(self, parser, host, port, max_width):

        IShost = 'localhost' if host is None else host
        ISport ='8083' if port is None else port

        Contrail_CLI.__init__(self, parser, IShost, ISport, max_width)
        self.parse_args()

    def parse_args(self):

        ##multicast tree
        parser_sub = self.subparser.add_parser('multicast', help='Show multicast tree')
        parser_mcast = parser_sub.add_subparsers()

        parser_mcast_tree = parser_mcast.add_parser('tree', help='Show bum tree for VN')
        parser_mcast_tree.add_argument('search', nargs='?', default='', type=str, help='Search string') 
        parser_mcast_tree.set_defaults(func=self.SnhShowMulticastManagerReq)

        parser_mcast_path = parser_mcast.add_parser('path', help='Show mcast path between computes')
        parser_mcast_path.add_argument('start', nargs='?', default='', type=str, help='Start compute')
        parser_mcast_path.add_argument('end', nargs='?', default='', type=str, help='Start compute')
        parser_mcast_path.add_argument('search', nargs='?', default='', type=str, help='Search string')
        parser_mcast_path.set_defaults(func=self.SnhShowMulticastManagerReq)


    def SnhShowMulticastManagerReq(self, args):
        vn_name = ''
        self.IST.get('Snh_ShowMulticastManagerReq?search_string=' + args.search)
        xpath = '//ShowMulticastManager'
        for xml_tree in self.IST.output_etree: 
            mcast_dict = self.IST.getMcastRouteTable(xml_tree, xpath)
            #print "u1"
            #print mcast_dict
            if int(mcast_dict['ShowMulticastManager']['total_trees']) > 0 and mcast_dict['ShowMulticastManager']['name'] != '':
                vn_name = mcast_dict['ShowMulticastManager']['name'] 
        if vn_name: 
            path = 'Snh_ShowMulticastManagerDetailReq?x=' + vn_name 
        else:
            return
        self.IST.get(path)
        for mcast_tree in self.IST.output_etree: 
            level0_dict = self.IST.getMcastRouteTable(mcast_tree, '//level0_forwarders')
            #print level0_dict
            if not level0_dict or not level0_dict['level0_forwarders']['list']:
                continue
            createGraph(level0_dict)
            level1_dict = self.IST.getMcastRouteTable(mcast_tree, '//level1_forwarders')
            #print level1_dict
            if level1_dict['level1_forwarders']['list']:
                createGraph(level1_dict)
        #print "Multicast BUM tree: \n" 
        #pretty_tree(graph_dict)
        #print "Missing computes: ", missing_nodes

        try:
            if args.start and args.end:
                print "Path "+args.start+" ---> "+args.end+":" 
                print find_path(args.start, args.end)
        except AttributeError:
            print "Multicast BUM tree: \n"
            pretty_tree(graph_dict)
            print "Missing computes: ", missing_nodes

def is_ipv4(addr):
    try:
        socket.inet_pton(socket.AF_INET, addr)
    except socket.error:
        return False
    return True

def is_ipv6(addr):
    try:
        socket.inet_pton(socket.AF_INET6, addr)
    except socket.error:
        return False
    return True

def addressInNetwork(addr, prefix):
    ipaddr = struct.unpack('!L',socket.inet_aton(addr))[0]
    pure_prefix = prefix.split(':')[-1]  # strip RD info if any
    netaddr,bits = pure_prefix.split('/')
    netaddr = struct.unpack('!L',socket.inet_aton(netaddr))[0]
    netmask = ((1<<(32-int(bits))) - 1)^0xffffffff
    return ipaddr & netmask == netaddr & netmask

def addressInNetwork6(addr, prefix):
    addr_upper,addr_lower = struct.unpack('!QQ',socket.inet_pton(socket.AF_INET6, addr))
    #if debug: print "{0:b}".format(ip_lower)
    netaddr,bits = prefix.split('/')
    net_upper,net_lower = struct.unpack('!QQ',socket.inet_pton(socket.AF_INET6, netaddr))
    if int(bits) < 65 :
        netmask = ((1<<(64-int(bits))) - 1)^0xffffffffffffffff
        return addr_upper & netmask == net_upper & netmask
    elif addr_upper != net_upper:
        return False
    else:
        netmask = ((1<<(128-int(bits))) - 1)^0xffffffffffffffff
        return addr_lower & netmask == net_lower & netmask


def block_width(block):
    try:
        return block.index('\n')
    except ValueError:
        return len(block)


def stack_str_blocks(blocks):
    builder = []
    block_lens = [block_width(bl) for bl in blocks]
    split_blocks = [bl.split('\n') for bl in blocks]

    for line_list in itertools.izip_longest(*split_blocks, fillvalue=None):
        for i, line in enumerate(line_list):
            if line is None:
                builder.append(' ' * block_lens[i])
            else:
                builder.append(line)
            if i != len(line_list) - 1:
                builder.append(' ')  # Padding
        builder.append('\n')

    return ''.join(builder[:-1])


def createGraph(xml_dict):
    if not xml_dict:
       return
   #print "u3"
    #print xml_dict.items()
    for key, value in (xml_dict.items()):
        #print "u4"
        #print key, value
        if isinstance(value , dict):
            createGraph(value)
        elif not isinstance(value, list):
            return
        else: 
            for item in xml_dict[key]:
                #print "u5"
                #print item
                #self.graph_dict[(item['address'],item['label'])] = self.graph_dict.get((item['address'],item['label']), [])\
                #                                                   + self.process_links(item['links']['list']['ShowMulticastTreeLink'])
                if item['links']['list']:
                    graph_dict[item['address']] = graph_dict.get(item['address'], [])\
                                                                   + process_links(item['links']['list']['ShowMulticastTreeLink'])
                else:
                    missing_nodes.append(item['address'])

def process_links(links):
    link_list = []
    if isinstance(links, list):
        for item in links:
            #link_list.append((item['address'], item['label']))
            link_list.append(item['address'])
    else:
        #link_list.append((links['address'], links['label']))
        link_list.append(links['address'])
    #print "u6"
    #print link_list
    return link_list

def pretty_tree(graph_dict):
    j = 0 
    second_pass = False
    for i in range(2):
        for k in sorted(graph_dict):
            if k not in vertex_map and j==0:
                vertex_map[k] = Node(k, Node)
                vertex_map[k].is_root = True
                j+=1
            elif k not in vertex_map:
                continue
            for value in graph_dict[k]:
                if second_pass:
                    if isinstance(vertex_map[k].parent,Node) and\
                       vertex_map[k].parent.name != value and\
                       value not in [item.name for item in vertex_map[k].children]:
                           vertex_map[value] = vertex_map[k].add_child(value)
                    else:
                       continue
                elif not isinstance(vertex_map[k].parent,Node) or vertex_map[k].parent.name != value: 
                    vertex_map[value] = vertex_map[k].add_child(value)
        second_pass = True
    for vertex in vertex_map:
        if vertex_map[vertex].is_root:
            print vertex_map[vertex].display()

def find_path(start_vertex, end_vertex, path=None):
    """ find a path from start_vertex to end_vertex
        in graph """
    if path == None:
        path = []
    graph = graph_dict
    path = path + [start_vertex]
    if start_vertex == end_vertex:
        return path
    if start_vertex not in graph:
        return None
    for vertex in graph[start_vertex]:
        if vertex not in path:
            extended_path = find_path(vertex, end_vertex, path)
            if extended_path:
                return extended_path
    return None

def main():


    argv = sys.argv[1:]

    if '--version' in argv:
        print version
        sys.exit()

    host = None
    port = None


    try:
        host = argv[argv.index('--host') + 1]
    except ValueError:
        pass

    try:
        port = argv[argv.index('--port') + 1]
    except ValueError:
        pass

    try:
        max_width = argv[argv.index('--max-width') + 1]
    except ValueError:
        max_width = 60
        pass

    global debug
    if '--debug' in argv:
        debug = True

    parser = argparse.ArgumentParser(prog='ist', description='A script to make Contrail Introspect output CLI friendly.')
    parser.add_argument('--version', action="store_true", help="Show script version")
    parser.add_argument('--debug', action="store_true", help="debug mode")
    parser.add_argument('--max-width', type=int, default=60, help="max width per column")

    roleparsers = parser.add_subparsers()

    parse_ctr = roleparsers.add_parser('ctr', help='Show Control node info')
    Control_CLI(parse_ctr, host, port, max_width)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
