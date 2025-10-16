from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, ForeignKey



if __name__ == "__main__":

    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

    metadata_obj = MetaData()

    user_table = Table(
        "user_account",
        metadata_obj,
        Column("id", Integer, primary_key = True),
        Column("name", String(30)),
        Column("fullName", String())
    )

    address_table = Table(
        "address",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("user_id", ForeignKey("user_account.id"), nullable=False),
        Column("email_addres", String, nullable=False)
    )

    metadata_obj.create_all(engine)

    with engine.begin() as conn:
        conn.execute(text("CREATE TABLE some_table (x int, y int)"))
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 1, "y": 1}, {"x": 2, "y": 4}, {"x": 10, "y": 10}],
        )

    with engine.begin() as conn:
        result = conn.execute(text("SELECT x, y FROM some_table"))
        for row in result:
            print(f"x: {row.x}  y: {row.y}")

    with engine.begin() as conn:
        result = conn.execute(
            text("SELECT x, y from some_table WHERE y > :y"),
            {"y" : 2}
        )
        for row in result:
            print(f"x: {row.x}  y: {row.y}")