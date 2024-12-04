# This module is a compatibility layer among different
# Python versions to load entry_points in a group.

import sys

def _iter_entry_points_group__pkg_resources(group):
	""" This is the old version, everyone loved, (or not)
	but now is deprecated in setuptools. It worked
	in Py2.7 and older Py3
	"""

	from pkg_resources import entry_points
	for entry in entry_points(group=group):
		yield entry

def _iter_entry_points_group__importlib_dict(group):
	""" This was the first version in importlib.metadata.
	A short lived api (3.8, 3.9) that returned a dictionary
	where the key was the group."""

	from importlib.metadata import entry_points
	for entry in entry_points()[group]:
		yield entry

def _iter_entry_points_group__importlib_selectable(group):
	""" This is the brand new api that does not
	work in all still supported Py3 versions."""

	from importlib.metadata import entry_points
	for entry in entry_points(group=group):
		yield entry

def entry_points_group(group):
	if sys.version_info < (3,8):
		return _iter_entry_points_group__pkg_resources(group)
	if sys.version_info < (3,10):
		return _iter_entry_points_group__importlib_dict(group)
	return _iter_entry_points_group__importlib_selectable(group)
	
def load_entry_points_group(group):
	return dict(
		(entry.name, entry.load())
		for entry in entry_points_group(group)
	)
		

