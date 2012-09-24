#!/usr/bin/python
#
# Copyright (C) 2008  Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author(s): Luke Macken <lmacken[at]redhat.com>
#            Miroslav Lichvar <mlichvar[at]redhat.com>
#            Edward Sheldrake <ejsheldrake[at]gmail.com>
#	     Arnaud Valensi <arnaud.valensi[at]gmail.com>
import types
import xdg.Menu, xdg.DesktopEntry, xdg.Config
import re, sys, os
from xml.sax.saxutils import escape

icons = True

try:
	from gi.repository import Gtk
except ImportError:
	icons = False

def icon_attr(entry):
	if icons is False:
		return None 

	name = entry.getIcon()

	#awesome can't load ico icons, and fails to show whole submenu, containing them
	if name.endswith(".ico"):
		return None

	if os.path.exists(name):
		return name

	# work around broken .desktop files
	# unless the icon is a full path it should not have an extension
	name = re.sub('\..{3,4}$', '', name)

	for size in [32, 22, 16]:
		# imlib2 cannot load svg
		iconinfo = theme.lookup_icon(name, size, Gtk.IconLookupFlags.NO_SVG)
		if iconinfo:
			iconfile = iconinfo.get_filename()
			iconinfo.free()
			if iconfile:
				return iconfile
	return None

def entry_name(entry):
	return entry.getName()

def generate_awesome_menu(entry):
	if isinstance(entry, xdg.Menu.Menu) and entry.Show is True:
		submenu = map(generate_awesome_menu, entry.getEntries())
		return (entry_name(entry), submenu, icon_attr(entry))
	elif isinstance(entry, xdg.Menu.MenuEntry) and entry.Show is True:
		second = re.sub(' -caption "%c"| -caption %c', ' -caption "%s"' % entry_name(entry.DesktopEntry), entry.DesktopEntry.getExec())
		second = re.sub(' [^ ]*%[fFuUdDnNickvm]', '', second)
		if entry.DesktopEntry.getTerminal():
			second = 'xterm -title "%s" -e %s' % \
				(entry_name(entry.DesktopEntry), second)
		first = entry_name(entry.DesktopEntry).replace('"', '')
		first = first.replace('"', '\\"')
		second = second.replace('"', '\\"')
		return (first, second, icon_attr(entry.DesktopEntry))

def generate_main_menu(menu_list, level):
	indent = " "*level*2

	i = 0
	for entry in menu_list:
		comma = " " if i == 0 else ","
		i += 1
		print "%s%s { \"%s\"" % (indent, comma, entry[0])
		if type(entry[1]) is list:
			print "%s  , {" % indent
			generate_main_menu(entry[1], level+2)
			print "%s    }" % indent
		else:
			print "%s  , \"%s\"" % (indent, entry[1])


		if entry[2] is not None:
			print "%s  , \"%s\"" % (indent, entry[2])
		print "%s  }" % indent


#main proc:
if len(sys.argv) > 1:
	menufile = sys.argv[1] + '.menu'
else:
	menufile = 'applications.menu'

# fix unicode issue when streaming to pipe
if sys.stdout.encoding is None:
	import codecs
	writer = codecs.getwriter("utf-8")
	sys.stdout = writer(sys.stdout)

lang = os.environ.get('LANG')
if lang:
	xdg.Config.setLocale(lang)

# lie to get the same menu as in GNOME
xdg.Config.setWindowManager('GNOME')

if icons:
	theme = Gtk.IconTheme.get_default()

menu = xdg.Menu.parse(menufile)

menu_list = map(generate_awesome_menu, menu.getEntries())

print 'myappmenu = {'
generate_main_menu(menu_list, 0)
print '}'

