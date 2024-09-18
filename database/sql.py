import aiosqlite, logging
from settings import DEBUG, DB_FILE


# create database
async def create_database() -> None:
    try:
        async with aiosqlite.connect(DB_FILE) as db:
            # create table users
            await db.execute(f'''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tlg_id INTEGER UNIQUE,
                    username TEXT DEFAULT '', 
                    is_admin INTEGER DEFAULT 0,
                    main_msg_id INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP 
                )'''
            )
            # create table keys
            await db.execute(f'''
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tlg_id INTEGER,
                    uuid TEXT UNIQUE,
                    email TEXT,
                    level INTEGER DEFAULT 1,
                    key TEXT DEFAULT '',
                    enabled INTEGER DEFAULT 0, 
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP 
                )'''
            )
            await db.commit()
    except Exception as e:
        text = f'SQL: create database error: {e}'
        logging.error(text)
        if DEBUG: print(text)
        return None
    

# execute query
async def execute_query(sql_query: str, data: tuple = None, action: str = None) -> bool | int:
    try:
        async with aiosqlite.connect(DB_FILE) as db:
            cursor = await db.cursor()
            if data:
                await cursor.execute(sql_query, data)
            else:
                await cursor.execute(sql_query)
            await db.commit()
        if action == 'insert':
            return cursor.lastrowid
        return True
    except Exception as e:
        text = f'SQL: execute query error: {e}'
        logging.error(text)
        if DEBUG: print(text)
        return False


# execute selection query
async def execute_selection_query(sql_query: str, data: tuple = None) -> bool | list[aiosqlite.Row]:
    try:
        async with aiosqlite.connect(DB_FILE) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.cursor()
            if data:
                await cursor.execute(sql_query, data)
            else:
                await cursor.execute(sql_query)
            rows = await cursor.fetchall()
        return rows
    except Exception as e:
        text = f'SQL: execute selection query error: {e}'
        logging.error(text)
        if DEBUG: print(text)



# create user
async def create_user(tlg_id: int, username: str = '', is_admin: bool = False) -> bool | int:
    user = await get_user(tlg_id=tlg_id)
    if user:
        return user['id']
    sql_query = f"INSERT INTO users (tlg_id, username, is_admin) VALUES (?, ?, ?)"
    return await execute_query(sql_query, (tlg_id, username, is_admin), 'insert')

# get user
async def get_user(tlg_id: int) -> bool | aiosqlite.Row:
    sql_query = f"SELECT * FROM users WHERE tlg_id = ?"
    user = await execute_selection_query(sql_query, (tlg_id, ))
    return user[0] if user else False

# get user by id
async def get_user_by_id(id: int) -> bool | aiosqlite.Row:
    sql_query = f"SELECT * FROM users WHERE id = ?"
    user = await execute_selection_query(sql_query, (id, ))
    return user[0] if user else False

# update user   
async def update_user(tlg_id: int, columns: list, values: list) -> bool:
    set_clause = ", ".join([f"{column} = ?" for column in columns])
    sql_query = f"UPDATE users SET {set_clause} WHERE tlg_id = ?"
    return await execute_query(sql_query, (*values, tlg_id))

# update user by id   
async def update_user_by_id(id: int, columns: list, values: list) -> bool:
    set_clause = ", ".join([f"{column} = ?" for column in columns])
    sql_query = f"UPDATE users SET {set_clause} WHERE id = ?"
    return await execute_query(sql_query, (*values, id))

# get all users
async def get_users(admins: bool = False) -> bool | aiosqlite.Row:
    sign = '>' if admins else '<='
    return await execute_selection_query(f"SELECT * FROM users WHERE is_admin {sign} 0", ())



# add new client
async def add_new_client(tlg_id: int, uuid: str, email: str, level: int, enabled: bool = True) -> bool | int:
    sql_query = f"INSERT INTO clients (tlg_id, uuid, email, level, enabled) VALUES (?, ?, ?, ?, ?)"
    return await execute_query(sql_query, (tlg_id, uuid, email, level, enabled), 'insert')

# get all / disabled / enabled clients
async def get_clients(type: bool | None = True) -> bool | aiosqlite.Row:
    # get all clients
    if type is None:
        return await execute_selection_query("SELECT * FROM clients", ())
    # get disabled clients
    if not type:
        return await execute_selection_query("SELECT * FROM clients WHERE enabled = 0", ())
    # get enabled clients
    return await execute_selection_query("SELECT * FROM clients WHERE enabled = 1", ())

# update client   
async def update_client(tlg_id: int, columns: list, values: list) -> bool:
    set_clause = ", ".join([f"{column} = ?" for column in columns])
    sql_query = f"UPDATE clients SET {set_clause} WHERE tlg_id = ?"
    return await execute_query(sql_query, (*values, tlg_id))



# get user keys all / enabled / disabled
async def get_user_keys(tlg_id: int, enabled: bool = True) -> bool | aiosqlite.Row:
    sql_query = f"SELECT * FROM clients WHERE tlg_id = ? AND enabled = ?"
    if enabled is None:
        sql_query = f"SELECT * FROM clients WHERE tlg_id = ?"
        return await execute_selection_query(sql_query, (tlg_id, ))
    return await execute_selection_query(sql_query, (tlg_id, enabled))  
