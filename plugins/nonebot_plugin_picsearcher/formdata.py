# -*- coding: utf-8 -*-
from typing import Any, Iterable, List, Optional

from aiohttp import FormData as _FormData
import aiohttp.multipart as multipart


class FormData(_FormData):
    def __init__(
        self,
        fields: Iterable[Any] = (),
        quote_fields: bool = True,
        charset: Optional[str] = None,
        boundary: Optional[str] = None
    ) -> None:
        self._writer = multipart.MultipartWriter("form-data", boundary=boundary)
        self._fields = []  # type: List[Any]
        self._is_multipart = False
        self._is_processed = False
        self._quote_fields = quote_fields
        self._charset = charset

        if isinstance(fields, dict):
            fields = list(fields.items())
        elif not isinstance(fields, (list, tuple)):
            fields = (fields,)
        self.add_fields(*fields)
