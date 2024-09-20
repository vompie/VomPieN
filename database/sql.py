import aiosqlite

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
                    user_lvl INTEGER DEFAULT 0,
                    main_msg_id INTEGER DEFAULT 0,
                    is_banned INTEGER DEFAULT 0,
                    referals INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP 
                )'''
            )
            # create table deeplinks
            await db.execute(f'''
                CREATE TABLE IF NOT EXISTS deeplinks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tlg_id INTEGER,
                    type TEXT, 
                    is_used INTEGER DEFAULT 0,
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
                    is_enabled INTEGER DEFAULT 0, 
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP 
                )'''
            )
            await db.commit()
    except Exception as e:
        text = f'SQL: create database error: {e}'
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
        if DEBUG: print(text)



# create user
async def create_user(tlg_id: int, username: str = '') -> bool | int:
    sql_query = f"INSERT INTO users (tlg_id, username) VALUES (?, ?)"
    return await execute_query(sql_query, (tlg_id, username), 'insert')

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

# get all users
async def get_users(admins: bool = False) -> bool | aiosqlite.Row:
    sign = '>' if admins else '<='
    return await execute_selection_query(f"SELECT * FROM users WHERE user_lvl {sign} 0", ())

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



# create deeplink
async def create_deeplink(tlg_id: int, type: str) -> bool | int:
    sql_query = f"INSERT INTO deeplinks (tlg_id, type) VALUES (?, ?)"
    return await execute_query(sql_query, (tlg_id, type), 'insert')

# get deeplink
async def get_deeplink(id: int) -> bool | aiosqlite.Row:
    sql_query = f"SELECT * FROM deeplinks WHERE id = ?"
    deeplink = await execute_selection_query(sql_query, (id, ))
    return deeplink[0] if deeplink else False

# update deeplink
async def update_deeplink(id: int, columns: list, values: list) -> bool:
    set_clause = ", ".join([f"{column} = ?" for column in columns])
    sql_query = f"UPDATE deeplinks SET {set_clause} WHERE id = ?"
    return await execute_query(sql_query, (*values, id))    

# increment referals
async def increment_referals(tlg_id: int) -> bool:
    sql_query = f"UPDATE users SET referals = referals + 1 WHERE tlg_id = ?"
    return await execute_query(sql_query, (tlg_id,))    



# add new client
async def add_new_client(tlg_id: int, uuid: str, email: str, level: int, enabled: bool = True) -> bool | int:
    sql_query = f"INSERT INTO clients (tlg_id, uuid, email, level, is_enabled) VALUES (?, ?, ?, ?, ?)"
    return await execute_query(sql_query, (tlg_id, uuid, email, level, enabled), 'insert')

# get client 
async def get_client(id: int) -> bool | aiosqlite.Row:
    sql_query = f"SELECT * FROM clients WHERE id = ?"
    user = await execute_selection_query(sql_query, (id, ))
    return user[0] if user else False

# get all / disabled / enabled clients
async def get_clients(type: bool | None = True) -> bool | aiosqlite.Row:
    # get all clients
    if type is None:
        return await execute_selection_query("SELECT * FROM clients", ())
    # get disabled clients
    if not type:
        return await execute_selection_query("SELECT * FROM clients WHERE is_enabled = 0", ())
    # get enabled clients
    return await execute_selection_query("SELECT * FROM clients WHERE is_enabled = 1", ())

# update client
async def update_client(id: int, columns: list, values: list) -> bool:
    set_clause = ", ".join([f"{column} = ?" for column in columns])
    sql_query = f"UPDATE clients SET {set_clause} WHERE id = ?"
    return await execute_query(sql_query, (*values, id))

# update client by tlg id   
async def update_client_by_tlg_id(tlg_id: int, columns: list, values: list) -> bool:
    set_clause = ", ".join([f"{column} = ?" for column in columns])
    sql_query = f"UPDATE clients SET {set_clause} WHERE tlg_id = ?"
    return await execute_query(sql_query, (*values, tlg_id))

# delete client
async def delete_client(id: int) -> bool:
    sql_query = f"DELETE FROM clients WHERE id = ?"
    return await execute_query(sql_query, (id,))



# get user keys: all / enabled / disabled
async def get_user_keys(tlg_id: int, enabled: bool = True) -> bool | aiosqlite.Row:
    sql_query = f"SELECT * FROM clients WHERE tlg_id = ? AND is_enabled = ?"
    if enabled is None:
        sql_query = f"SELECT * FROM clients WHERE tlg_id = ?"
        return await execute_selection_query(sql_query, (tlg_id, ))
    return await execute_selection_query(sql_query, (tlg_id, enabled))  

# get user keys by id: all / enabled / disabled
async def get_user_keys_by_user_id(id: int, enabled: bool = True) -> bool | aiosqlite.Row:
    user = await get_user_by_id(id=id)
    if not user:
        return False
    tlg_id = user['tlg_id']
    sql_query = f"SELECT * FROM clients WHERE tlg_id = ? AND is_enabled = ?"
    if enabled is None:
        sql_query = f"SELECT * FROM clients WHERE tlg_id = ?"
        return await execute_selection_query(sql_query, (tlg_id, ))
    return await execute_selection_query(sql_query, (tlg_id, enabled)) 

# get user left join keys by tlg id: all / enabled / disabled
async def get_user_left_join_keys(tlg_id: int) -> bool | aiosqlite.Row:
    user_selectable = 'users.id as uid, users.tlg_id, username, user_lvl, is_banned, referals, users.created_at as users_created_at'
    client_selectable = 'clients.id as cid, uuid, email, level, key, is_enabled, clients.created_at as clients_created_at'
    selectable = f"{user_selectable}, {client_selectable}"
    sql_query = f"SELECT {selectable} FROM users LEFT JOIN clients ON users.tlg_id = clients.tlg_id WHERE users.tlg_id = ?"
    return await execute_selection_query(sql_query, (tlg_id, ))

# get user left join keys by user id: all / enabled / disabled
async def get_user_left_join_keys_by_user_id(id: int) -> bool | aiosqlite.Row:
    user_selectable = 'users.id as uid, users.tlg_id, username, user_lvl, is_banned, referals, users.created_at as users_created_at'
    client_selectable = 'clients.id as cid, uuid, email, level, key, is_enabled, clients.created_at as clients_created_at'
    selectable = f"{user_selectable}, {client_selectable}"
    sql_query = f"SELECT {selectable} FROM users LEFT JOIN clients ON users.tlg_id = clients.tlg_id WHERE users.id = ?"
    return await execute_selection_query(sql_query, (id, ))
