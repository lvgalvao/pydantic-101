from datetime import date
from enum import Enum

import pandas as pd
from pydantic import (BaseModel, EmailStr, ValidationError, confloat,
                      conint, constr, field_validator)

# Estrutura necessária do Pydantic para validar os dados
class SalesModel(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    email: EmailStr
    age: conint(ge=18, le=99)
    salary: confloat(ge=0)
    is_employee: bool
    department: Enum("HR","FINANCE","IT","SALES")
    joining_date: date
    percentage_value: confloat(ge=0, le=100)

    @field_validator('percentage_value')
    def validate_percentage(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Percentage value must be between 0 and 100')
        return round(v, 2)

# Lendo os dados do arquivo JSON
data = pd.read_json('data/sales_records.json')
records = data.to_dict('records')

# Gerando listas vazias para armazenar os registros válidos e inválidos
valid_records = []
invalid_records_log = []

# Função para validar cada registro um dos registros
def process_record(record, valid_records, invalid_records_log):
    try:
        validated_record = SalesModel(**record)
        valid_records.append(validated_record.model_dump())
    except ValidationError as e:
        invalid_records_log.append({'record': record, 'error': str(e)})


for record in records:
    process_record(record, valid_records, invalid_records_log)

# Salvar registros válidos em CSV e registros inválidos em um log
valid_df = pd.DataFrame(valid_records)
valid_df.to_csv('data/valid_records.csv', index=False)

with open('data/invalid_records.log', 'w') as log_file:
    for log_entry in invalid_records_log:
        log_file.write(str(log_entry) + '\n')
