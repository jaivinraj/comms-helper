import sqlalchemy as sa
from jinja2 import Template
import pandas as pd


def get_engine(
    user, password, host="comms-postgres", database="comms_database", schema=None
):
    # get postgres engine
    return sa.create_engine(
        f"postgresql://{user}:{password}@{host}:5432/{database}",
        connect_args={"options": "-csearch_path={}".format(schema)}
        if schema is not None
        else {},
    )


def get_table_creation_query(tablename, coldict, schema, index_cols=[], unique_cols=[]):
    q_params = {
        "schema": schema,
        "tablename": tablename,
        "cols": coldict,
        "index_cols": index_cols,
        "unique_str": {i: ("UNIQUE" if i in unique_cols else "") for i in coldict}
        #         "tempstr": "TEMP TABLE " if temp else "TABLE IF NOT EXISTS",
    }
    qj_tmplt = Template(
        """
        CREATE TABLE IF NOT EXISTS {{schema}}.{{tablename}}
            
            (
            id SERIAL PRIMARY KEY,
            {% for col in cols %}
            {{col}} {{cols[col]}} {{unique_str[col]}}
            {% if not loop.last %}
                ,
            {% endif %}
            {% endfor %}
            );
            {% for indcol in index_cols %}
            CREATE INDEX IF NOT EXISTS {{indcol}}_{{tablename}}_idx ON {{schema}}.{{tablename}} ({{indcol}});
            {% endfor %}
        
        """
    )
    return qj_tmplt.render(q_params)


def schema_exists(schema_name, user, password):
    engine = get_engine(user, password)
    check_query = "SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{}';".format(
        schema_name
    )
    with engine.connect() as conn:
        df = pd.read_sql(check_query, con=conn)
    if len(df) > 0:
        return True
    else:
        return False
