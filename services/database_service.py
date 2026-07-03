import pandas as pd
import oracledb

from config.database import *


class DatabaseService:

    def __init__(self):

        self.connection = None

    def connect(self):

        if self.connection is None:

            self.connection = oracledb.connect(
                user=USERNAME,
                password=PASSWORD,
                host=HOST,
                port=PORT,
                service_name=SERVICE_NAME
            )

        return self.connection

    def get_all_complaints(self):

        query = f"""
        SELECT *
        FROM {COMPLAINT_TABLE}
        """

        return pd.read_sql(query, self.connect())

    def get_closed_complaints(self):

        query = f"""
        SELECT *
        FROM {COMPLAINT_TABLE}
        WHERE STATUS_FLAG='R'
        """

        return pd.read_sql(query, self.connect())

    def get_pending_complaints(self):

        query = f"""
        SELECT *
        FROM {COMPLAINT_TABLE}
        WHERE STATUS_FLAG IN ('P','I')
        """

        return pd.read_sql(query, self.connect())

    def get_acknowledgements(self):

        query = f"""
        SELECT *
        FROM {ACK_TABLE}
        ORDER BY FDATE
        """

        return pd.read_sql(query, self.connect())

    def get_ticket(self, ticket_no):

        query = f"""
        SELECT *
        FROM {COMPLAINT_TABLE}
        WHERE TICKET_NO = :ticket
        """

        cursor = self.connect().cursor()

        try:

            cursor.execute(
                query,
                ticket=ticket_no
            )

            cols = [c[0] for c in cursor.description]

            rows = cursor.fetchall()

            return pd.DataFrame(
                rows,
                columns=cols
            )

        finally:

            cursor.close()

    def get_conversation(self, ticket_no):

        # Convert
        # 013-MT-2025-240101
        #        ↓
        #     240101

        asno = str(ticket_no).split("-")[-1].strip()

        query = f"""
        SELECT *
        FROM {ACK_TABLE}
        WHERE ASNO = :ticket
        ORDER BY FDATE
        """

        cursor = self.connect().cursor()

        try:

            cursor.execute(
                query,
                ticket=asno
            )

            cols = [c[0] for c in cursor.description]

            rows = cursor.fetchall()

            return pd.DataFrame(
                rows,
                columns=cols
            )

        finally:

            cursor.close()

    def execute(self, query, params=None):

        cursor = self.connect().cursor()

        try:

            cursor.execute(
                query,
                params or {}
            )

            self.connection.commit()

        except Exception:

            self.connection.rollback()

            raise

        finally:

            cursor.close()

    def close(self):

        if self.connection:

            self.connection.close()

            self.connection = None