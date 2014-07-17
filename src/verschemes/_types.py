# -*- coding: utf-8 -*-
"""verschemes._types module"""

from __future__ import absolute_import
from __future__ import unicode_literals

from future.utils import PY2 as _PY2

if _PY2:  # pragma: no coverage  # pragma: no branch
    from verschemes.future.newsuper import newsuper as super


class int_default_zero(int):

    def __new__(cls, *args, **kwargs):
        if args:
            if not args[0]:
                args = list(args)
                args[0] = 0
        elif 'x' in kwargs and not kwargs['x']:
            kwargs['x'] = 0
        return super().__new__(cls, *args, **kwargs)
