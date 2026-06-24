# Copyright (C) 2023-2026 Sebastien Rousseau.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Excel (.xlsx) writer for parsed ``bankstatementparser`` data.

Exposes :func:`write_xlsx`, which serialises parsed bank-statement
records (a pandas DataFrame, a list of
:class:`bankstatementparser.Transaction` objects, or a list of plain
dicts) to a polished ``.xlsx`` workbook.
"""

from __future__ import annotations

from .writer import write_xlsx

__all__ = ["write_xlsx", "__version__"]

__version__ = "0.0.10"
