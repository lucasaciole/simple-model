# Copyright (c) 2017 Luiz Menezes
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

from typing import List


class ModelField:
    def __init__(self, model, name, value, allow_empty):
        self._model = model
        self.name = name
        self.value = value
        self.allow_empty = allow_empty

        try:
            self._validate = getattr(model, 'validate_{}'.format(name))
        except AttributeError:
            self._validate = None

    def validate(self):
        if not self._validate:
            return

        self._validate(self.value)

    def serialize(self):
        try:
            serialized = self.value.serialize()
        except AttributeError:
            serialized = None

        if isinstance(self.value, (List, tuple)):
            serialized = [field.serialize() for field in self.value]

        return serialized or self.value