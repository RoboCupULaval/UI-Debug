# Under MIT License, see LICENSE.txt

from .DataIn import FormatPackageError
from .DataInLog import DataInLog
from .DataInSTA import DataInSTA
from .Draw.DrawLine import DrawLine

__author__ = 'RoboCupULaval'


class DataInFactory(object):

    def __init__(self):
        self._name = 'System'
        self._msg_bad_format = DataInLog(self._name, 2, {'level': 3, 'message': "Le format du paquet n'est pas conforme: "})

    def _get_msg_bad_format(self, **kargs):
        self._msg_bad_format.data['message'] = "Le format du paquet n'est pas conforme:\n" + str(kargs)
        return self._msg_bad_format

    def get_datain_object(self, name, type, data):
        if 0 <= type < 1000:
            try:
                return DataInLog(name, type, data)
            except FormatPackageError:
                return self._get_msg_bad_format(name=name, type=type, data=data)

        elif 1000 <= type < 3000:
            try:
                return DataInSTA(name, type, data)
            except FormatPackageError:
                return self._get_msg_bad_format(name=name, type=type, data=data)

        elif 3000 <= type < 5000:
            try:
                if type == 3001:
                    return DrawLine(name, type, data)
                else:
                    raise FormatPackageError

            except FormatPackageError:
                return self._get_msg_bad_format(name=name, type=type, data=data)

        elif 5000 <= type < 7000:
            try:
                return self._get_msg_bad_format(name=name, type=type, data=data)
            except FormatPackageError:
                return self._get_msg_bad_format(name=name, type=type, data=data)

        else:
            return self._get_msg_bad_format(name=name, type=type, data=data)
