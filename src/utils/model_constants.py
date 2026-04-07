from typing import Annotated

from sqlalchemy import String
from sqlalchemy.orm import mapped_column

str_30 = Annotated[str, mapped_column(String(30), nullable=False)]
int_pk = Annotated[int, mapped_column(primary_key=True)]
