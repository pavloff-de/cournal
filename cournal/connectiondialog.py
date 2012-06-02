#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of Cournal.
# Copyright (C) 2012 Fabian Henze
# 
# Cournal is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Cournal is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Cournal.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, Gdk
from . import network

class ConnectionDialog(Gtk.Dialog):
    def __init__(self, parent, **args):
        Gtk.Dialog.__init__(self, **args)
        
        self.parent = parent
        self.content_area = self.get_content_area()
        grid = Gtk.Grid()
        self.server_port_entry = ServerPortEntry()
        second_row = Gtk.Box()
        image = Gtk.Image()
        label = Gtk.Label()
        smalllabel = Gtk.Label()

        second_row.pack_start(smalllabel, False, False, 0)
        second_row.pack_start(self.server_port_entry, False, True, 5)
        
        self.content_area.add(grid)
        grid.attach(image, 0, 0, 1, 3)
        grid.attach(label, 1, 0, 2, 1)
        grid.attach(second_row, 1, 1, 1, 1)
        
        self.set_modal(False)
        self.set_has_resize_grip(False)
        self.set_resizable(False)
        self.set_title("Connect to Server")
        self.set_transient_for(parent)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_button(Gtk.STOCK_CONNECT, Gtk.ResponseType.ACCEPT)
        self.set_default_response(Gtk.ResponseType.ACCEPT)
        grid.set_row_spacing(5)
        grid.set_column_spacing(10)
        grid.set_border_width(10)
        self.server_port_entry.set_activates_default(True)
        image.set_from_stock(Gtk.STOCK_NETWORK, Gtk.IconSize.DIALOG)
        label.set_text("Please enter the Name and port of the server, you want to connect to.")
        smalllabel.set_text("Server name:")
        
        self.show_all()
    
    def response_cb(self, widget, response_id):
        if response_id != Gtk.ResponseType.ACCEPT:
            self.destroy()
            return
        
        server = self.server_port_entry.get_server()
        port = self.server_port_entry.get_port()
        
        network.set_document(self.parent.document)
        d = network.connect(server, port)
        d.addCallbacks(self.on_connected, self.on_connection_failure)
        
    def on_connected(self, perspective):
        self.destroy()
    
    def on_connection_failure(self, reason):
        pass

    def run_nonblocking(self):
        self.connect('response', self.response_cb)
        self.show()

class ServerPortEntry(Gtk.EventBox):
    def __init__(self, **args):
        Gtk.EventBox.__init__(self, **args)
        
        frame = Gtk.Frame()
        server_port_align = Gtk.Box()
        self.server_entry = Gtk.Entry()
        colon_label = Gtk.Label()
        self.port_entry = Gtk.Entry()
        
        self.add(frame)
        frame.add(server_port_align)
        server_port_align.pack_start(self.server_entry, True, True, 0)
        server_port_align.pack_start(colon_label, False, False, 0)
        server_port_align.pack_start(self.port_entry, False, False, 0)
        
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(255,255,255,255))
        frame.set_shadow_type(Gtk.ShadowType.IN)
        
        self.server_entry.set_has_frame(False)
        self.server_entry.set_text("127.0.0.1")
        self.server_entry.set_width_chars(20)
        colon_label.set_text(":")
        self.port_entry.set_has_frame(False)
        self.port_entry.set_max_length(5)
        self.port_entry.set_width_chars(5)
        self.port_entry.set_text("6524")
        
        self.port_entry.connect("insert_text", self.port_entry_updated)

    def port_entry_updated(self, widget, text, length, position):
        if not text.isdigit():
            widget.emit_stop_by_name("insert_text")
            return

    def set_activates_default(self, setting):
        self.port_entry.set_activates_default(setting)
        self.server_entry.set_activates_default(setting)

    def get_server(self):
        return self.server_entry.get_text()
    
    def get_port(self):
        return int(self.port_entry.get_text())

# For testing purposes:
if __name__ == "__main__":
    dialog = ConnectionDialog(None)
    dialog.run()
