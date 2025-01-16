"""Qt components that do not fit the other categories."""

import warnings
from qtpy.QtCore import QObject, Property, Signal
from qtpy.QtWidgets import QMessageBox
from one.webclient import AlyxClient
from requests import HTTPError


class QAlyx(QObject):
    """A Qt wrapper for :class:`one.webclient.AlyxClient`."""

    tokenMissing = Signal(str)
    authenticationFailed = Signal(str)
    connectionFailed = Signal(str)
    loggedIn = Signal(str)
    loggedOut = Signal()
    statusChanged = Signal(bool)

    def __init__(self, base_url: str, parent: QObject | None = None):
        super().__init__(parent)
        self._client = AlyxClient(base_url=base_url, silent=True)

    @Property(AlyxClient)
    def client(self) -> AlyxClient:
        return self._client

    @Property(bool)
    def isLoggedIn(self) -> bool:
        return self._client.is_logged_in

    def login(
        self, username: str, password: str | None = None, cache_token: bool = False
    ) -> None:
        if self._client.is_logged_in and self._client.user == username:
            return

        # try to authenticate. upgrade warnings to exceptions so we can catch them.
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('error')
                self._client.authenticate(
                    username=username,
                    password=password,
                    cache_token=cache_token,
                    force=password is not None,
                )

        # catch missing password / token
        except UserWarning as e:
            if 'No password or cached token' in e.args[0]:
                self.tokenMissing.emit(username)
                return

        # catch connection issues: display a message box
        except ConnectionError as e:
            QMessageBox.critical(self.parent(), 'Connection Error', str(e))
            self.connectionFailed.emit(e.args[0])
            return

        # catch authentication errors
        except HTTPError as e:
            if e.errno == 400:
                print('auth')
                self.authenticationFailed.emit(username)
                return
            else:
                raise e

        # emit signals
        if self._client.is_logged_in and self._client.user == username:
            self.statusChanged.emit(True)
            self.loggedIn.emit(username)

    def logout(self):
        if not self._client.is_logged_in:
            return
        self._client.logout()
        self.statusChanged.emit(False)
        self.loggedOut.emit()
