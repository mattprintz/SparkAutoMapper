import re
from typing import Optional, List

from pyspark.sql import Column, DataFrame
# noinspection PyUnresolvedReferences
from pyspark.sql.functions import col

from spark_auto_mapper.data_types.array_base import AutoMapperArrayLikeBase


class AutoMapperDataTypeColumn(AutoMapperArrayLikeBase):
    def __init__(self, value: str):
        super().__init__()
        if len(value) > 0 and value[0] == "[":
            self.value: str = value[1:-1]  # skip the first and last characters
        else:
            self.value = value

    def get_column_spec(
        self, source_df: Optional[DataFrame], current_column: Optional[Column]
    ) -> Column:
        if isinstance(self.value, str):
            if not self.value.startswith("a.") and not self.value.startswith(
                "b."
            ):
                # prepend with "b." in case the column exists in both a and b tables
                # noinspection RegExpSingleCharAlternation
                elements: List[str] = re.split(r"\.|\[|]", self.value)
                my_column: Optional[Column] = None
                for element in elements:
                    if element != "_" and element != "":
                        my_column = my_column[element if not element.isnumeric(
                        ) else int(element)] if my_column is not None else col(
                            "b." + self.value
                        )
                return my_column
            else:
                return col(self.value)

        raise ValueError(f"value: {self.value} is not str")
