"""Graphical user interface components."""

from qtpy.QtWidgets import QPushButton
from qtpy.QtCore import Signal, Slot, Property


class StatefulButton(QPushButton):
    """A QPushButton that maintains an active/inactive state."""

    clickedWhileActive = Signal()  # type: Signal
    """Emitted when the button is clicked while it is in the active state."""

    clickedWhileInactive = Signal()  # type: Signal
    """Emitted when the button is clicked while it is in the inactive state."""

    stateChanged = Signal(bool)  # type: Signal
    """Emitted when the button's state has changed. The signal carries the new state 
    (True for active, False for inactive)."""

    def __init__(self, *args, active: bool = False, **kwargs):
        """Initialize the StatefulButton with the specified active state.

        Parameters
        ----------
        *args : tuple
            Positional arguments passed to QPushButton constructor.
        active : bool, optional
            Initial state of the button (default is False).
        **kwargs : dict
            Keyword arguments passed to QPushButton constructor.
        """
        super().__init__(*args, **kwargs)
        self._isActive = active
        self.clicked.connect(self._onClick)

    def getActive(self) -> bool:
        """Get the active state of the button.

        Returns
        -------
        bool
            True if the button is active, False otherwise.
        """
        return self._isActive

    @Slot(bool)
    def setActive(self, value: bool):
        """Set the active state of the button.

        Emits `stateChanged` if the state has changed.

        Parameters
        ----------
        value : bool
            The new active state of the button.
        """
        if self._isActive != value:
            self._isActive = value
            self.stateChanged.emit(self._isActive)

    active = Property(bool, fget=getActive, fset=setActive, notify=stateChanged)  # type: Property
    """The active state of the button."""

    @Slot()
    def _onClick(self):
        """Handle the button click event.

        Emits `clickedWhileActive` if the button is active,
        otherwise emits `clickedWhileInactive`.
        """
        if self._isActive:
            self.clickedWhileActive.emit()
        else:
            self.clickedWhileInactive.emit()
