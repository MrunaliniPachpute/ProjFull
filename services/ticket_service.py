from services.database_service import DatabaseService


class TicketService:

    def __init__(self):

        self.db = DatabaseService()

    def approve_resolution(self, ticket_no, resolution):

        conn = self.db.connect()

        cursor = conn.cursor()

        try:

            # Convert ticket number to ASNO
            # Example:
            # 013-MT-2025-240101 -> 240101

            asno = str(ticket_no).split("-")[-1].strip()

            cursor.execute(
                """
                INSERT INTO ACKNOWLEDGEMENT
                (
                    ASNO,
                    REMARKS,
                    FDATE,
                    FLAG
                )
                VALUES
                (
                    :1,
                    :2,
                    SYSDATE,
                    'AI_ASSIST'
                )
                """,
                (
                    asno,
                    resolution
                )
            )

            cursor.execute(
                """
                UPDATE COMPLAIN_SYS_FEED
                SET
                    STATUS_FLAG = 'R',
                    RECT_BY     = 'AI_ASSIST',
                    RECT_DATE   = SYSDATE,
                    RECT_ECODE  = 'AI_ASSIST'
                WHERE TICKET_NO = :1
                """,
                (
                    ticket_no,
                )
            )

            conn.commit()

        except Exception:

            conn.rollback()

            raise

        finally:

            cursor.close()
            conn.close()

    def get_pending(self):

        return self.db.get_pending_complaints()