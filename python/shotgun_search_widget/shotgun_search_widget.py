# Copyright (c) 2015 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import sgtk
from sgtk.platform.qt import QtCore, QtGui

search_completer = sgtk.platform.current_bundle().import_module(
    "search_completer"
)


class ShotgunSearchWidget(QtGui.QLineEdit):
    """
    A QT Widget deriving from :class:`~PySide.QtGui.QLineEdit` that creates
    a hierarchical search input box with auto completion.

    :signal: ``entity_selected(str, int)`` - Fires when someone selects an entity inside
            the search results. The returned parameters are entity type and entity id.

    :signal: ``entity_activated(str, int, str)`` - Fires when someone selects an
        entity inside the search results. Similar to ``entity_selected``, with
        the addition of the ``name`` of the activated entity being supplied.
    """
    def __init__(self, parent):
        """
        Uses the :class:``HierarchicalSearchCompleter`` as the completer for searching
        SG entities.

        :param parent: Qt parent object
        :type parent: :class:`~PySide.QtGui.QWidget`
        """

        # first, call the base class and let it do its thing.
        super(ShotgunSearchWidget, self).__init__(parent)

        # trigger the completer to popup as text changes
        self.textEdited.connect(self._search_edited)

        # Taken from https://wiki.qt.io/Delay_action_to_wait_for_user_interaction
        self._delay_timer = QtCore.QTimer(self)
        self._delay_timer.timeout.connect(self._finished_editing)
        self._delay_timer.setSingleShot(True)

    def set_bg_task_manager(self, task_manager):
        """
        Specify the background task manager to use to pull
        data in the background. Data calls
        to Shotgun will be dispatched via this object.

        :param task_manager: Background task manager to use
        :type  task_manager: :class:`~tk-framework-shotgunutils:task_manager.BackgroundTaskManager`
        """
        self.completer().set_bg_task_manager(task_manager)

    def _search_edited(self, _):
        """
        Called every time the user types something in the search box.
        """
        # This will fire _launch_search after 300 ms. If the user types something before it fires,
        # the timer restarts counting. This differs from the editingFinished event on a QLineEdit which
        # fires only when the user pressed enter. This fires when the user has finished typing for
        # a short period of time.
        self._delay_timer.start(300)

    def _finished_editing(self):
        """
        Launches the search in the completer.
        """
        self.completer().search(self.text())

    def destroy(self):
        """
        Should be called before the widget is closed.
        """
        self.completer().destroy()
