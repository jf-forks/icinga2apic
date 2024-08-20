"""
Copyright 2017 fmnisme@gmail.com, Copyright 2020 christian@jonak.org

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Icinga 2 API client

The Icinga 2 API allows you to manage configuration objects and resources in a simple,
programmatic way using HTTP requests.
"""

from __future__ import print_function

import logging

import pretiac
from pretiac.actions import Actions
from pretiac.configfile import ClientConfigFile
from pretiac.events import Events
from pretiac.exceptions import Icinga2ApiException
from pretiac.objects import Objects
from pretiac.status import Status

LOG = logging.getLogger(__name__)


class Client:
    """
    Icinga 2 Client class
    """

    objects: Objects
    actions: Actions
    events: Events
    status: Status
    version: str

    def __init__(
        self,
        url: str | None = None,
        username: str | None = None,
        password: str | None = None,
        timeout: str | None = None,
        certificate: str | None = None,
        key: str | None = None,
        ca_certificate: str | None = None,
        config_file: str | None = None,
    ) -> None:
        """
        initialize object
        """
        config_from_file = ClientConfigFile(config_file)
        if config_file:
            config_from_file.parse()
        self.url = url or config_from_file.url
        self.username = username or config_from_file.username
        self.password = password or config_from_file.password
        self.timeout = timeout or config_from_file.timeout
        self.certificate = certificate or config_from_file.certificate
        self.key = key or config_from_file.key
        self.ca_certificate = ca_certificate or config_from_file.ca_certificate
        self.objects = Objects(self)
        self.actions = Actions(self)
        self.events = Events(self)
        self.status = Status(self)
        self.version = pretiac.__version__

        if not self.url:
            raise Icinga2ApiException('No "url" defined.')
        if not self.username and not self.password and not self.certificate:
            raise Icinga2ApiException(
                "Neither username/password nor certificate defined."
            )
