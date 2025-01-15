"""Qt components that do not fit the other categories."""

import warnings
from qtpy.QtCore import QObject, Property, Signal
from one.webclient import AlyxClient
from requests import HTTPError


class QAlyx(QObject):
    authenticationFailed = Signal(str)
    connectionFailed = Signal(str)

    def __init__(self, *args, base_url: str, **kwargs):
        super().__init__(*args, **kwargs)
        self._client = AlyxClient(base_url=base_url, silent=True)

    @Property(AlyxClient)
    def client(self) -> AlyxClient:
        return self._client

    @Property(bool)
    def isLoggedIn(self) -> bool:
        return self._client.is_logged_in

    def login(
        self, username: str, password: str | None, cache_token: bool = False
    ) -> bool:
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
                self.authenticationFailed.emit(username)

        # catch connection issues
        except ConnectionError as e:
            # QErrorMessage().showMessage(e.args[0])
            self.connectionFailed.emit(e.args[0])

        # catch authentication errors
        except HTTPError as e:
            if e.errno == 400:
                self.authenticationFailed.emit(username)
            else:
                raise e

        # return outcome of login attempt
        return self._client.is_logged_in and self._client.user == username
