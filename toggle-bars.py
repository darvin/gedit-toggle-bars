from gettext import gettext as _

import gtk
import gedit

# Menu item example, insert a new item in the Tools menu
ui_str = """<ui>
  <menubar name="MenuBar">
    <menu name="ViewMenu" action="View">
      <placeholder name="ViewOps_2">
        <menuitem name="ToggleBars" action="ToggleBars"/>
      </placeholder>
    </menu>
  </menubar>
</ui>
"""
class ToggleBarsWindowHelper:
    def __init__(self, plugin, window):
        self._window = window
        self._plugin = plugin

        # Insert menu items
        self._insert_menu()

    def deactivate(self):
        # Remove any installed menu items
        self._remove_menu()

        self._window = None
        self._plugin = None
        self._action_group = None

    def _insert_menu(self):
        # Get the GtkUIManager
        manager = self._window.get_ui_manager()

        # Create a new action group
        self._action_group = gtk.ActionGroup("ToggleBarsPluginActions")
        self._action_group.add_toggle_actions([("ToggleBars", None, _("Both bars"),
                                         "F2", _("Toggle side and bottom bars"),
                                         self.on_toggle_bars)])
        

        # Insert the action group
        manager.insert_action_group(self._action_group, -1)

        # Merge the UI
        self._ui_id = manager.add_ui_from_string(ui_str)

    def _remove_menu(self):
        # Get the GtkUIManager
        manager = self._window.get_ui_manager()

        # Remove the ui
        manager.remove_ui(self._ui_id)

        # Remove the action group
        manager.remove_action_group(self._action_group)

        # Make sure the manager updates
        manager.ensure_update()

    def update_ui(self):
        self._action_group.set_sensitive(self._window.get_active_document() != None)
        self._action_group.get_action("ToggleBars").set_active(
            self._window.get_side_panel().get_visible() and self._window.get_bottom_panel().get_visible())

    def on_toggle_bars(self, action):
        visible = action.get_active()
        self._window.get_side_panel().set_visible(visible)
        self._window.get_bottom_panel().set_visible(visible)

        
        
class ToggleBarsPlugin(gedit.Plugin):
    def __init__(self):
        gedit.Plugin.__init__(self)
        self._instances = {}

    def activate(self, window):
        self._instances[window] = ToggleBarsWindowHelper(self, window)

    def deactivate(self, window):
        self._instances[window].deactivate()
        del self._instances[window]

    def update_ui(self, window):
        self._instances[window].update_ui()
