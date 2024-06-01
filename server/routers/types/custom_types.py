from enum import Enum
from typing import Annotated
from sqlalchemy.orm import mapped_column

from sqlalchemy import String


class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    not_specified = "not specified"


str_20 = Annotated[str, mapped_column(String(20))]
