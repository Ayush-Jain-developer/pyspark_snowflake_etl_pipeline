from sqlalchemy import MetaData, Table, Column, String, Float, Integer

metadata = MetaData()

title_ratings = Table("title_ratings", metadata,
                      Column("tconst", String(20), primary_key=True),
                      Column("average_rating", Float),
                      Column("numvotes", Integer))


