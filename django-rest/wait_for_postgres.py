import os
import logging
import psycopg2

from time import time, sleep


start_time = time()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
check_timeout = os.getenv("POSTGRES_CHECK_TIMEOUT", 30)
check_interval = os.getenv("POSTGRES_CHECK_INTERVAL", 1)
interval_unit = "second" if check_interval == 1 else "seconds"

config = {
    "dbname": os.getenv("DATABASE_NAME", "customer_service"),
    "user": os.getenv("DATABASE_USER", "admin"),
    "password": os.getenv("DATABASE_PASSWORD", "Admin@2024"),
    "host": os.getenv("DATABASE_HOST", "postgres"),
    "port": os.getenv("DATABASE_PORT", "5432")
}


def pg_isready(host, user, password, dbname, port):
    # print all the config
    logger.info(f"host: {host}")
    logger.info(f"user: {user}")
    logger.info(f"password: {password}")
    logger.info(f"dbname: {dbname}")
    logger.info(f"port: {port}")

    while time() - start_time < check_timeout:
        try:
            conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            logger.info("Postgres is ready! ✨ 💅")
            sleep(15)
            conn.close()
            return True
        except psycopg2.OperationalError:
            logger.info(f"Postgres isn't ready. Waiting for {check_interval} {interval_unit}...")
            sleep(check_interval)

    logger.error(f"We could not connect to Postgres within {check_timeout} seconds.")
    return False


pg_isready(**config)
