# -*- coding: utf-8 -*-
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

Icinga 2 API client exceptions
"""


class Icinga2ApiException(Exception):
    """
    Icinga 2 API exception class
    """

    def __init__(self, error):
        super(Icinga2ApiException, self).__init__(error)
        self.error = error

    def __str__(self):
        return str(self.error)


class Icinga2ApiRequestException(Icinga2ApiException):
    """
    Icinga 2 API Request exception class
    """

    response = {}

    def __init__(self, error, response):
        super(Icinga2ApiRequestException, self).__init__(error)
        self.response = response


class pretiaconfigFileException(Exception):
    """
    Icinga 2 API config file exception class
    """

    def __init__(self, error):
        super(pretiaconfigFileException, self).__init__(error)
        self.error = error

    def __str__(self):
        return str(self.error)
