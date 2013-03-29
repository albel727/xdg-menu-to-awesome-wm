xdg-menu-to-awesome-wm
======================

Converts a xdg-menu like gnome menu awesome wm format

How To
======================
```bash
$ python awesome-xdg-menu.py > ~/.config/awesome/menu.lua
```

You can also specify a list of .menu files, from which to compose your menu. 
See /etc/xdg/menus/ (may be os-dependent) for the list of available menus.

```bash
$ python awesome-xdg-menu.py applications.menu settings.menu > ~/.config/awesome/menu.lua
```

After you have to add "menu.lua" in your "rc.lua", mine look like this:

```lua
-- {{{ Menu
-- Create a laucher widget and a main menu

myawesomemenu = {
   { "manual", terminal .. " -e man awesome" },
   { "fluxbox", "/bin/bash /home/valens_a/bin/reflux" },
   { "edit config", editor_cmd .. " " .. awful.util.getdir("config") .. "/rc.lua" },
   { "restart", awesome.restart },
   { "quit", awesome.quit }
}

-- Load our generated menu into "myappmenu"
-- require("menu") add the file "menu.lua"
myappmenu = require("menu")
mymainmenu = awful.menu({ items = { { "awesome", myawesomemenu, beautiful.awesome_icon },
-- The next line add our menu (myappmenu)
	        	  	    { "app", myappmenu, beautiful.awesome_icon },
                                    { "open terminal", terminal }
                                  }
                        })

mylauncher = awful.widget.launcher({ image = image(beautiful.awesome_icon),
                                     menu = mymainmenu })


-- }}}
```

Additionally, you can specify a list of .desktop files, to have a flat menu generated from them.
This may be useful to generate entirely customized menus.
For example, this is how one can have the same launchers as in Gnome 2 panel:

```bash
$ python awesome-xdg-menu.py ~/.gnome2/panel2.d/default/launchers/* > ~/.config/awesome/launchers.lua
```

After that you can add them as launchers into your awesome panel. This is how I do it:

```lua
myapplaunchers = require("launchers")

mylaunchers = {}
for i, info in ipairs(myapplaunchers) do
  mylaunchers[i] = awful.widget.launcher({ image = info[3], command = info[2] })
end

mywibox[s].widgets = {
  widget_foo,
  awful.util.table.join( mylaunchers, { layout = awful.widget.layout.horizontal.leftright }),
  widget_bar
}
```
