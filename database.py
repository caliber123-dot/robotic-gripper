import sqlite3
from datetime import datetime

DB_NAME = "gripper.db"


# =========================
# CONNECT DATABASE
# =========================
def get_connection():

    conn = sqlite3.connect(DB_NAME)

    conn.row_factory = sqlite3.Row

    return conn


# =========================
# CREATE TABLE
# =========================
def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gripper_inputs (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        gripper INTEGER,
        shape INTEGER,
        event TEXT,

        material TEXT,

        time_value REAL,

        theta_function TEXT,

        spring_mode TEXT,

        length REAL,
        breadth REAL,
        width REAL,

        radius REAL,

        rmajor REAL,
        rminor REAL,

        k_common REAL,
        k_finger REAL,

        f1k1 REAL,
        f1k2 REAL,

        f2k1 REAL,
        f2k2 REAL,

        f3k1 REAL,
        f3k2 REAL,

        f4k1 REAL,
        f4k2 REAL,

        thk1 REAL,
        thk2 REAL,
        thk3 REAL,

        total_force REAL,

        created_at TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS spring_constants (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        gripper INTEGER,

        shape INTEGER,

        material TEXT,

        time_value REAL,

        theta_function TEXT,
                   
        spring_key TEXT,

        spring_value REAL,
                   
        UNIQUE(
            gripper,
            shape,
            material,
            time_value,
            theta_function,
            spring_key,
            spring_value 
        )        
    )
    """)

    conn.commit()

    conn.close()


# =========================
# INSERT DATA
# =========================
def save_input(data):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
    INSERT INTO gripper_inputs (

        gripper,
        shape,
        event,
        material,
        time_value,
        theta_function,
        spring_mode,

        length,
        breadth,
        width,

        radius,

        rmajor,
        rminor,

        k_common,
        k_finger,

        f1k1,
        f1k2,

        f2k1,
        f2k2,

        f3k1,
        f3k2,

        f4k1,
        f4k2,

        thk1,
        thk2,
        thk3,

        total_force,

        created_at

    )

    VALUES (
?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
)

    """,
        (
            data.get("gripper"),
            data.get("shape"),
            data.get("event"),
            data.get("material"),
            data.get("time"),
            data.get("func"),
            data.get("mode"),
            data.get("length"),
            data.get("breadth"),
            data.get("width"),
            data.get("radius"),
            data.get("Rmajor"),
            data.get("Rminor"),
            data.get("k_common"),
            data.get("k_finger"),
            # data.get("k_thumb1"),
            # data.get("k_thumb2"),
            # data.get("k_thumb3"),
            data.get("f1k1"),
            data.get("f1k2"),
            data.get("f2k1"),
            data.get("f2k2"),
            data.get("f3k1"),
            data.get("f3k2"),
            data.get("f4k1"),
            data.get("f4k2"),
            data.get("Thk1"),
            data.get("Thk2"),
            data.get("Thk3"),
            data.get("total"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )

    conn.commit()

    conn.close()


# =========================
# GET SAVED DATA
# =========================
def get_saved_input(gripper, shape, material, time_value, theta_function, spring_mode):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """

    SELECT *

    FROM gripper_inputs

    WHERE gripper = ?
    AND shape = ?
    AND material = ?
    AND time_value = ?
    AND theta_function = ?
    AND spring_mode = ?

    ORDER BY id DESC

    LIMIT 1

    """,
        (gripper, shape, material, time_value, theta_function, spring_mode),
    )

    row = cursor.fetchone()

    conn.close()

    return dict(row) if row else None


# ============================ Graph Data =========================
def get_saved_input_graph(gripper, shape, material, theta_function, spring_mode):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """

    SELECT *

    FROM gripper_inputs

    WHERE gripper = ?
    AND shape = ?
    AND material = ?   
    AND theta_function = ?
    AND spring_mode = ?

    ORDER BY id DESC

    LIMIT 1

    """,
        (gripper, shape, material, theta_function, spring_mode),
    )

    row = cursor.fetchone()

    conn.close()

    return dict(row) if row else None


# ============================ Compare Data =========================
def get_saved_input_compare(gripper, shape, theta_function, time_value, spring_mode):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """

    SELECT *

    FROM gripper_inputs

    WHERE gripper = ?
    AND shape = ?
    AND time_value = ?
    AND theta_function = ?
    AND spring_mode = ?

    ORDER BY id DESC

    LIMIT 1

    """,
        (gripper, shape, time_value, theta_function, spring_mode),
    )

    row = cursor.fetchone()

    conn.close()

    return dict(row) if row else None


def get_saved_input_graph_all(gripper, shape, material, theta_function, spring_mode):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """

    SELECT *

    FROM gripper_inputs

    WHERE gripper = ?
    AND shape = ?
    AND material = ?
    AND theta_function = ?
    AND spring_mode = ?

    ORDER BY time_value ASC

    """,
        (gripper, shape, material, theta_function, spring_mode),
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


# =========================
# UPDATE DUPLICATE DATA
# =========================
def update_input(record_id, data):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """

    UPDATE gripper_inputs

    SET

        k_common = ?,
        k_finger = ?,

        f1k1 = ?,
        f1k2 = ?,

        f2k1 = ?,
        f2k2 = ?,

        f3k1 = ?,
        f3k2 = ?,

        f4k1 = ?,
        f4k2 = ?,

        thk1 = ?,
        thk2 = ?,
        thk3 = ?,
        total_force = ?           

    WHERE id = ?

    """,
        (
            data.get("k_common"),
            data.get("k_finger"),
            data.get("f1k1"),
            data.get("f1k2"),
            data.get("f2k1"),
            data.get("f2k2"),
            data.get("f3k1"),
            data.get("f3k2"),
            data.get("f4k1"),
            data.get("f4k2"),
            data.get("Thk1"),
            data.get("Thk2"),
            data.get("Thk3"),
            data.get("total"),
            record_id,
        ),
    )

    conn.commit()

    conn.close()


# =========================
# CHECK DUPLICATE ENTRY
# =========================
def is_duplicate(data):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """

    SELECT id

    FROM gripper_inputs

    WHERE
        gripper = ? 
        AND shape = ?
        AND material = ?
        AND time_value = ?
        AND theta_function = ?
        AND spring_mode = ?        

    LIMIT 1

    """,
        (
            data.get("gripper"),
            data.get("shape"),
            data.get("material"),
            data.get("time"),
            data.get("func"),
            data.get("mode"),
        ),
    )

    row = cursor.fetchone()

    conn.close()

    # return row is not None
    return row["id"] if row else None


# To add Spring Constant values to the database, we can create a new function that updates the existing record with the calculated spring constants. This function can be called after the spring constants are calculated in the application logic.
# accrordind to gripper, shape, material, time, theta function and spring mode we can update the spring constant values in the database.
# to create add_spring_constants table column is id, gripper, spring_value  to the database.
# =========================
# SAVE SPRING CONSTANT check before insert
# =========================


def save_spring_constants2222(gripper, spring_data):

    conn = get_connection()

    cursor = conn.cursor()

    rows = [(gripper, item["spring_key"], item["spring_value"]) for item in spring_data]

    cursor.executemany(
        """

    INSERT OR IGNORE INTO spring_constants
    (
        gripper,
        spring_key,
        spring_value
    )

    VALUES (?, ?, ?)

    """,
        rows,
    )

    conn.commit()

    conn.close()


def save_spring_constants(
    gripper, shape, material, time_value, theta_function, spring_data
):

    conn = get_connection()
    cursor = conn.cursor()

    rows = [
        (
            gripper,
            shape,
            material,
            time_value,
            theta_function,
            item["spring_key"],
            item["spring_value"],
        )
        for item in spring_data
    ]

    cursor.executemany(
        """

    INSERT OR IGNORE INTO spring_constants
    (
        gripper,
        shape,
        material,
        time_value,
        theta_function,
        spring_key,
        spring_value
    )

    VALUES (?, ?, ?, ?, ?, ?, ?)

    """,
        rows,
    )

    conn.commit()
    conn.close()


# =========================
# GET SPRING CONSTANTS
# =========================


def get_spring_constants222(gripper, spring_key):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT DISTINCT spring_value
        FROM spring_constants
        WHERE gripper = ?
        AND spring_key = ?
        ORDER BY spring_value
    """,
        (gripper, spring_key),
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_spring_constants(gripper, shape, material, theta_function, spring_key):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """

        SELECT DISTINCT spring_value, time_value

        FROM spring_constants

        WHERE gripper = ?
        AND shape = ?
        AND material = ?
        AND theta_function = ?
        AND spring_key = ?

        ORDER BY spring_value

    """,
        (gripper, shape, material, theta_function, spring_key),
    )

    rows = cursor.fetchall()

    conn.close()

    # return rows
    return [dict(row) for row in rows]


# ========================== to Get time to comparison ddl==============
def get_comparison_time(gripper, shape, theta_function):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT DISTINCT time_value
        FROM spring_constants
        WHERE gripper = ?
        AND shape = ?
        AND theta_function = ?
        ORDER BY time_value
    """,
        (gripper, shape, theta_function),
    )

    rows = cursor.fetchall()

    conn.close()

    return rows
# =====================================================================
def get_comparison_time1(gripper, shape, material ,theta_function):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT DISTINCT time_value
        FROM spring_constants
        WHERE gripper = ?
        AND shape = ?
        AND material = ?
        AND theta_function = ?
        ORDER BY time_value
    """,
        (gripper, shape, material, theta_function),
    )

    rows = cursor.fetchall()

    conn.close()

    return rows
# ============================== Get ALl Equal=====================================
def get_comparison_all_equal(gripper, shape, material ,theta_function, time_value):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT DISTINCT spring_value
        FROM spring_constants
        WHERE gripper = ?
        AND shape = ?
        AND material = ?
        AND time_value = ?
        AND theta_function = ?
        ORDER BY spring_value
    """,
        (gripper, shape, material, time_value, theta_function),
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


# ======================== New for Pending===========================
def get_spring_constants_comparison(gripper, shape, theta_function, time, spring_key):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """

        SELECT DISTINCT spring_value, time_value

        FROM spring_constants

        WHERE gripper = ?
        AND shape = ?        
        AND theta_function = ?
        AND time_value = ?
        AND spring_key = ?

        ORDER BY spring_value

    """,
        (gripper, shape, theta_function, time, spring_key),
    )

    rows = cursor.fetchall()

    conn.close()

    # return rows
    return [dict(row) for row in rows]
