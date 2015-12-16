# -*- coding: UTF-8 -*-

# TODO add http://paste.ubuntu.com/12524217/
# consider https://github.com/hallyn/qtile-config/blob/master/config.py

import os
import subprocess

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, hook, bar, widget

mod = 'mod4'
color_alert = '#ee9900'
color_frame = '#808080'

# kick a window to another screen (handy during presentations)
def kick_to_next_screen(qtile, direction=1):
	other_scr_index = (qtile.screens.index(qtile.currentScreen) + direction) % len(qtile.screens)
	othergroup = None
	for group in qtile.cmd_groups().values():
		if group['screen'] == other_scr_index:
			othergroup = group['name']
			break
	if othergroup:
		qtile.moveToGroup(othergroup)

class Commands(object):
	dmenu = 'dmenu_run -i -b -p ">>>" -fn "RobotoMono" -nb "#15181a" -nf "#fff" -sb "#333" -sf "#fff"'
	file_manager = 'nautilus --no-desktop'

# see http://docs.qtile.org/en/latest/manual/config/keys.html
keys = [
	# Switch between windows in current stack pane
	Key([mod], 'Tab', lazy.layout.down()),
	Key([mod, 'shift'], 'Tab', lazy.layout.up()),
	# Move windows up or down in current stack
	Key([mod, 'mod1'], 'Tab', lazy.layout.shuffle_down()),
	Key([mod, 'mod1', 'shift'], 'Tab', lazy.layout.shuffle_up()),
	# Switch window focus to other pane(s) of stack
	Key([mod, 'control'], 'Tab', lazy.layout.next()),
	Key([mod, 'control', 'shift'], 'Tab', lazy.layout.prev()),
	# Swap panes of split stack
	#Key([mod, 'shift'], 'space', lazy.layout.rotate()),
	# Change ratios
	Key([mod], 'h', lazy.layout.left()),
	Key([mod], 'l', lazy.layout.right()),
	Key([mod], 'j', lazy.layout.down()),
	Key([mod], 'k', lazy.layout.up()),
	Key([mod, 'shift'], 'h', lazy.layout.swap_left()),
	Key([mod, 'shift'], 'l', lazy.layout.swap_right()),
	Key([mod, 'shift'], 'j', lazy.layout.shuffle_down()),
	Key([mod, 'shift'], 'k', lazy.layout.shuffle_up()),
	# kick to next/prev screen
	Key([mod], "o", lazy.function(kick_to_next_screen)),
	Key([mod, "shift"], "o", lazy.function(kick_to_next_screen, -1)),
	# Toggle between split and unsplit sides of stack.
	# Split = all windows displayed
	# Unsplit = 1 window displayed, like Max layout, but still with
	# multiple stack panes
	#Key([mod, 'shift'], 'Return', lazy.layout.toggle_split()),
	Key([mod], 'Return', lazy.spawn('roxterm')),
	Key([mod], 'v', lazy.spawn('gvim')),
	Key([mod], 'l', lazy.spawn('xlock')),
	Key([], 'XF86Launch1', lazy.spawn('xlock')),
	Key([], 'XF86AudioMute', lazy.spawn('amixer -D pulse set Master toggle')),
	#Key([], 'XF86AudioMicMute', lazy.spawn('amixer -D pulse set Master toggle')),
	Key([], 'XF86AudioRaiseVolume', lazy.spawn('amixer -c 0 -q set Master 2dB+')),
	Key([], 'XF86AudioLowerVolume', lazy.spawn('amixer -c 0 -q set Master 2dB-')),
	# Switch groups
	Key([], 'XF86Back', lazy.screen.prev_group(skip_managed=True, )),
	Key([], 'XF86Forward', lazy.screen.next_group(skip_managed=True, )),
	Key([mod], 'XF86Back', lazy.screen.prev_group(skip_managed=True, )),
	Key([mod], 'XF86Forward', lazy.screen.next_group(skip_managed=True, )),
	Key([mod], 'Left', lazy.screen.prev_group(skip_managed=True, )),
	Key([mod], 'Right', lazy.screen.next_group(skip_managed=True, )),
	Key([mod], 'Escape', lazy.screen.togglegroup()),
	# Toggle between different layouts as defined below
	Key([mod], 'Up', lazy.next_layout()),
	Key([mod], 'Down', lazy.prev_layout()),
	Key([mod, 'shift'], 'space', lazy.prev_layout()),
	# lazy.group.setlayout('...
	Key([mod, 'shift'], 'c', lazy.window.kill()),
	# qtile maintenence
	Key([mod, 'shift'], 'e', lazy.spawn('gvim {}'.format(__file__))),
	Key([mod, 'shift'], 'r', lazy.restart()), # default is control! ;)
	Key([mod, 'shift'], 'q', lazy.shutdown()),
	Key([mod], 'space', lazy.spawn(Commands.dmenu)),
	Key([mod], 'e', lazy.spawn(Commands.file_manager)),
	Key([mod], 'f', lazy.window.toggle_floating()),
	Key([mod], 'm', lazy.window.toggle_fullscreen()),
	Key([mod], 'n', lazy.window.toggle_minimize()),
	#Key( [mod, 'shift'], '2', lazy.to_screen(1), lazy.group.toscreen(1)),
	]

# create groups
groups = [Group(i) for i in '1234567890']
for i in groups:
	# mod1 + letter of group = switch to group
	keys.append(
		Key([mod], i.name, lazy.group[i.name].toscreen())
	)

	# mod1 + shift + letter of group = switch to & move focused window to group
	keys.append(
		Key([mod, 'shift'], i.name, lazy.window.togroup(i.name))
	)

# see http://docs.qtile.org/en/latest/manual/ref/layouts.html
layouts = [
	layout.MonadTall(),
	layout.Max(),
	layout.Floating(border_focus=color_alert, border_normal=color_frame, ),
	#layout.Matrix(),
	layout.RatioTile(),
	#layout.Slice(),
	#layout.Stack(num_stacks=2),
	layout.Tile(border_focus=color_alert, border_normal=color_frame, ),
	layout.TreeTab(font='Corbel', fontsize=14),
	#layout.VerticalTile(),
	#layout.Zoomy(),
	]

widget_defaults = dict(
	font='Corbel',
	fontsize=14,
	)

class ThermalSensor(widget.ThermalSensor):
	def poll(self):
		temp_values = self.get_temp_sensors()
		if temp_values is None:
			return '---'
		no = int(float(temp_values.get(self.tag_sensor, [0])[0]))
		return '{}{}'.format(no, '°')#chr(0x1F321))

# see http://docs.qtile.org/en/latest/manual/ref/widgets.html
screens = [Screen(top=bar.Bar([
	widget.GroupBox(
		disable_drag=True,
		this_current_screen_border=color_frame,
		this_screen_border=color_frame,
		urgent_text=color_alert,
		),
    widget.sep.Sep(),
	widget.CurrentLayout(),
    widget.sep.Sep(),
	widget.Prompt(),
    widget.sep.Sep(),
	widget.TaskList(
		font='Corbel',
		border=color_frame,
		highlight_method='block',
		max_title_width=800,
		urgent_border=color_alert,
		),
    widget.sep.Sep(),
    widget.YahooWeather(location='Natick, MA', update_interval=60, metric=False, format='{condition_text} {condition_temp}° {wind_chill}°'),
    widget.sep.Sep(),
	widget.CPUGraph(
		graph_color=color_alert,
		fill_color='{}.5'.format(color_alert),
		border_color=color_frame,
		line_width=2,
		border_width=1,
		samples=60,
		),
	widget.MemoryGraph(
		graph_color=color_alert,
		fill_color='{}.5'.format(color_alert),
		border_color=color_frame,
		line_width=2,
		border_width=1,
		samples=60,
		),
	widget.NetGraph(
		graph_color=color_alert,
		fill_color='{}.5'.format(color_alert),
		border_color=color_frame,
		line_width=2,
		border_width=1,
		samples=60,
		),
	widget.Volume(theme_path='/usr/share/icons/Humanity/status/22', cardid=0),
    widget.sep.Sep(),
	widget.Systray(),
    widget.sep.Sep(),
	widget.Clock(
		format='%Y-%m-%d %H:%M %p',
		),
	], 24, ), ), ]

def detect_screens(qtile):
	while len(screens) < len(qtile.conn.pseudoscreens):
		screens.append(Screen(
		top=bar.Bar([
			widget.GroupBox(
				disable_drag=True,
				this_current_screen_border=color_frame,
				this_screen_border=color_frame,
				),
			widget.CurrentLayout(),
			widget.TaskList(
				font='Corbel',
				border=color_frame,
				highlight_method='block',
				max_title_width=800,
				urgent_border=color_alert,
				),
			], 32, ), ))

# Drag floating layouts.
mouse = [
	Drag([mod], 'Button1', lazy.window.set_position_floating(), start=lazy.window.get_position()),
	Drag([mod], 'Button3', lazy.window.set_size_floating(), start=lazy.window.get_size()),
	Click([mod], 'Button2', lazy.window.bring_to_front())
	]

# subscribe for change of screen setup, just restart if called
@hook.subscribe.screen_change
def restart_on_randr(qtile, ev):
	# TODO only if numbers of screens changed
	qtile.cmd_restart()

@hook.subscribe.startup_once
def autostart():
	subprocess.Popen(['feh', '--bg-fill', os.path.join(os.path.expanduser('~'), 'Downloads', 'Walls', '4.jpg')])
	subprocess.Popen(['mate-settings-daemon'])
	subprocess.Popen(['nm-applet'])

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
	border_focus=color_alert,
	border_normal=color_frame,
	float_rules=[dict(role='buddy_list', ), ],
	)
auto_fullscreen = True

def main(qtile):
	detect_screens(qtile)
