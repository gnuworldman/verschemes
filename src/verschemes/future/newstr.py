"""Custom future.types.newstr stuff."""

from future.types.newstr import newstr as _newstr
from future.utils import isidentifier as _isidentifier


class newstr(_newstr):

    """Fix for :class:`~future.types.newstr.newstr`.

    This implements :meth:`isidentifier`, which currently raises a
    `NotImplementedError` in `future`.

    """

    def isidentifier(self):
        return _isidentifier(self)
