from gi.repository import Gtk, GObject, RB, Peas

from rb3compat import ActionGroup
from rb3compat import Action
from rb3compat import ApplicationShell
from rb3compat import is_rb3



ui_string = """
<ui>
    <menubar name="MenuBar">
        <menu name="ToolsMenu" action="Tools">
            <menuitem name="StopAfterCurrentTrack" action="StopAfterCurrentTrack"/>
        </menu>
    </menubar>
</ui>
"""

class StopAfterCurrentTrackPlugin (GObject.Object, Peas.Activatable):
    object = GObject.property(type=GObject.Object)

    def __init__(self):
        super(StopAfterCurrentTrackPlugin, self).__init__()

    def do_activate(self):
        print("Activating Plugin")
        self.stop_status = False
        shell = self.object
        self.appshell = ApplicationShell(shell)

        self.action_group = ActionGroup(shell, 'StopAfterCurrentTrackPluginActions')
        self.action = self.action_group.add_action(func=self.toggle_status,
                                                   action_name='StopAfterCurrentTrack',
                                                   label=_('Stop After'),
                                                   action_state=ActionGroup.TOGGLE,
                                                   action_type='app',
                                                   tooltip=_('Stop playback after current song'))
        self.appshell.insert_action_group(self.action_group)
        self.appshell.add_app_menuitems(ui_string, 'StopAfterCurrentTrackPluginActions', 'tools')
        self.action.set_active(False)
        self.action.set_sensitive(False)

        sp = shell.props.shell_player
        self.pec_id = sp.connect('playing-song-changed', self.playing_entry_changed)
        print("Plugin Activated")

    def do_deactivate(self):
        print("Deactivating Plugin")
        shell = self.object
        self.appshell.cleanup()
        sp = shell.props.shell_player
        sp.disconnect (self.pec_id)
        self.action_group = None
        self.action = None
        print("Plugin Deactivated")

    def toggle_status(self, action, param=None, data=None):
        if self.action.get_active():
            self.stop_status = True
        else:
            self.stop_status = False
        print(self.stop_status)

    def playing_entry_changed(self, sp, entry):
        print("Playing entry changed")
        print(entry)
        if entry is not None:
            self.action.set_sensitive(True)
            if self.stop_status:
                self.action.set_active(False)
                sp.pause()
        else:
            self.action.set_sensitive(False)

