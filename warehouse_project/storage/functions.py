import sqlite3
from django.db.models import Count


def create_all_clients_functions():
    # Получаем соединение с базой данных
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Создаем функции
    sql = """
        CREATE TABLE storage_clients (
        id SERIAL PRIMARY KEY,
        ‘FIO’ VARCHAR(255) NOT NULL,
        Email VARCHAR(255) UNIQUE NOT NULL,
        CHECK (email ~* '@mpei\.ru$')
        );

        CREATE OR REPLACE PROCEDURE insert_clients(‘FIO’ VARCHAR(255), email VARCHAR(255))
        AS $$
        BEGIN
            INSERT INTO storage_clients (‘FIO’, email)
            VALUES(fio, email);
        END;
        $$ LANGUAGE plpgsql;

        CREATE OR REPLACE FUNCTION select_clients()
        RETURNS TABLE(fio VARCHAR(255), email VARCHAR(255)) AS $$
        BEGIN
            RETURN QUERY
            SELECT c.‘FIO’, c.email FROM storage_clients c;
        END;
        $$ LANGUAGE plpgsql;

        CREATE OR REPLACE PROCEDURE update_clients(pk int, new_fio VARCHAR(255), new_email VARCHAR(255))
        AS $$
        BEGIN
            UPDATE storage_clients c
            SET ‘FIO’ = new_fio,
                email = new_email
            WHERE id = pk;
        END;
        $$ LANGUAGE plpgsql;

        CREATE OR REPLACE PROCEDURE delete_clients(pk int)
        AS $$
        BEGIN
            DELETE FROM storage_clients
            WHERE id = pk;
        END;
        $$ LANGUAGE plpgsql;

        CREATE OR REPLACE FUNCTION all_clients()
        RETURNS int AS $$
        DECLARE
            result int;
        BEGIN
            SELECT INTO result COUNT(*) FROM storage_clients;
            RETURN result;
        END;
        $$ LANGUAGE plpgsql;

        CREATE OR REPLACE VIEW sort20_clients AS
        SELECT ‘FIO’, email FROM storage_clients
        ORDER BY id DESC
        LIMIT 20;

        CREATE OR REPLACE FUNCTION notify_client_deletion()
        RETURNS TRIGGER AS $$
        BEGIN
            RAISE NOTICE 'Удаляется клиент: ID = %, ФИО = %, Email = %', OLD.id, OLD.‘FIO’, OLD.email;
            RETURN OLD;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER before_client_delete
        BEFORE DELETE ON storage_clients
        FOR EACH ROW
        EXECUTE FUNCTION notify_client_deletion();
        """

    cursor.execute(sql)
    conn.commit()
    conn.close()


# Вызываем функцию для создания функций базы данных
create_all_clients_functions()
