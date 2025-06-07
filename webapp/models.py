import uuid
from datetime import datetime

from webapp.database import get_db


class UserProfile:
    def __init__(self, id=None, phone=None, description=None, role='member',
                 created_at=None, updated_at=None, user_id=None, telegram_id=None,
                 username=None, first_name=None, last_name=None, email=None):
        self.id = id
        self.phone = phone
        self.description = description
        self.role = role
        self.created_at = created_at
        self.updated_at = updated_at
        self.user_id = user_id
        self.telegram_id = telegram_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    @classmethod
    def get_by_telegram_id(cls, telegram_id: int):
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT up.id,
                                   up.phone,
                                   up.description,
                                   up.role,
                                   up.created_at,
                                   up.updated_at,
                                   up.user_id,
                                   up.telegram_id,
                                   u.username,
                                   u.first_name,
                                   u.last_name,
                                   u.email
                            FROM evoicebot_app_userprofile up
                                     LEFT JOIN auth_user u ON up.user_id = u.id
                            WHERE up.telegram_id = %s
                            """, (telegram_id,))
                row = cur.fetchone()
                if row:
                    return cls(*row)
                return None

    @classmethod
    def get_by_username(cls, username: str):
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT up.id,
                                   up.phone,
                                   up.description,
                                   up.role,
                                   up.created_at,
                                   up.updated_at,
                                   up.user_id,
                                   up.telegram_id,
                                   u.username,
                                   u.first_name,
                                   u.last_name,
                                   u.email
                            FROM evoicebot_app_userprofile up
                                     LEFT JOIN auth_user u ON up.user_id = u.id
                            WHERE u.username = %s
                            """, (username,))
                row = cur.fetchone()
                if row:
                    return cls(*row)
                return None

    def update_telegram_id(self, telegram_id: int):
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            UPDATE evoicebot_app_userprofile
                            SET telegram_id = %s,
                                updated_at  = %s
                            WHERE id = %s
                            """, (telegram_id, datetime.now(), self.id))
                conn.commit()
                self.telegram_id = telegram_id

    @classmethod
    def create(cls, telegram_id: int, first_name: str, last_name: str = None,
               username: str = None, phone: str = None):
        with get_db() as conn:
            with conn.cursor() as cur:
                # Check if user with this username already exists
                user_id = None
                target_username = username or f"tg_{telegram_id}"

                cur.execute("SELECT id FROM auth_user WHERE username = %s", (target_username,))
                existing_user = cur.fetchone()

                if existing_user:
                    user_id = existing_user[0]
                    # Update existing user's info
                    cur.execute("""
                                UPDATE auth_user
                                SET first_name = %s,
                                    last_name  = %s
                                WHERE id = %s
                                """, (first_name, last_name or '', user_id))
                else:
                    # Create new auth_user
                    cur.execute("""
                                INSERT INTO auth_user
                                (username, first_name, last_name, email, is_staff, is_active, is_superuser,
                                 date_joined, password, last_login)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
                                """, (target_username, first_name, last_name or '',
                                      '', False, True, False, datetime.now(), '', None))
                    user_id = cur.fetchone()[0]

                # Check if profile already exists for this user
                cur.execute("SELECT id FROM evoicebot_app_userprofile WHERE user_id = %s", (user_id,))
                existing_profile = cur.fetchone()

                if existing_profile:
                    # Update existing profile with telegram_id and phone
                    cur.execute("""
                                UPDATE evoicebot_app_userprofile
                                SET telegram_id = %s,
                                    phone       = %s,
                                    updated_at  = %s
                                WHERE user_id = %s RETURNING id
                                """, (telegram_id, phone, datetime.now(), user_id))
                    profile_id = cur.fetchone()[0]
                else:
                    # Create new profile
                    cur.execute("""
                                INSERT INTO evoicebot_app_userprofile
                                    (phone, role, created_at, updated_at, user_id, telegram_id)
                                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
                                """, (phone, 'member', datetime.now(), datetime.now(), user_id, telegram_id))
                    profile_id = cur.fetchone()[0]

                conn.commit()
                return cls.get_by_id(profile_id)

    @classmethod
    def get_by_id(cls, profile_id: int):
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT up.id,
                                   up.phone,
                                   up.description,
                                   up.role,
                                   up.created_at,
                                   up.updated_at,
                                   up.user_id,
                                   up.telegram_id,
                                   u.username,
                                   u.first_name,
                                   u.last_name,
                                   u.email
                            FROM evoicebot_app_userprofile up
                                     LEFT JOIN auth_user u ON up.user_id = u.id
                            WHERE up.id = %s
                            """, (profile_id,))
                row = cur.fetchone()
                if row:
                    return cls(*row)
                return None

    def update_phone(self, phone: str):
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            UPDATE evoicebot_app_userprofile
                            SET phone      = %s,
                                updated_at = %s
                            WHERE id = %s
                            """, (phone, datetime.now(), self.id))
                conn.commit()
                self.phone = phone


class Document:
    def __init__(self, id=None, uuid=None, title=None, description=None, file=None,
                 file_type=None, created_at=None, updated_at=None, deadline=None,
                 project_id=None, team_id=None, ai_description=None, ai_audio=None,
                 file_id=None, mime_type=None, size=None, user_profile_id=None,
                 expiration_date=None, telegram_reminder_sent=False,
                 sms_reminder_sent=False, call_reminder_sent=False,
                 call_attempts=0, call_message_listened=False, last_call_date=None,
                 gcs_file_path=None, gcs_uploaded=False):
        self.id = id
        self.uuid = uuid
        self.title = title
        self.description = description
        self.file = file
        self.file_type = file_type
        self.created_at = created_at
        self.updated_at = updated_at
        self.deadline = deadline
        self.project_id = project_id
        self.team_id = team_id
        self.ai_description = ai_description
        self.ai_audio = ai_audio
        self.file_id = file_id
        self.mime_type = mime_type
        self.size = size
        self.user_profile_id = user_profile_id
        self.user_id = user_profile_id  # Alias for compatibility
        self.expiration_date = expiration_date
        self.telegram_reminder_sent = telegram_reminder_sent
        self.sms_reminder_sent = sms_reminder_sent
        self.call_reminder_sent = call_reminder_sent
        self.call_attempts = call_attempts
        self.call_message_listened = call_message_listened
        self.last_call_date = last_call_date
        self.gcs_file_path = gcs_file_path
        self.gcs_uploaded = gcs_uploaded
        self.name = title  # Alias for compatibility

    @classmethod
    def create(cls, user_id: int, file_id: str, title: str, mime_type: str = None,
               size: int = None):
        with get_db() as conn:
            with conn.cursor() as cur:
                doc_uuid = str(uuid.uuid4())
                cur.execute("""
                            INSERT INTO evoicebot_app_document
                            (uuid, title, file, file_type, created_at, updated_at,
                             file_id, mime_type, size, user_profile_id, telegram_reminder_sent,
                             sms_reminder_sent, call_reminder_sent, call_attempts,
                             call_message_listened, gcs_uploaded)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
                            """, (doc_uuid, title, '', 'pdf', datetime.now(), datetime.now(),
                                  file_id, mime_type, size, user_id, False, False, False, 0, False, False))
                doc_id = cur.fetchone()[0]
                conn.commit()
                return cls.get_by_id(doc_id)

    @classmethod
    def get_by_id(cls, doc_id: int):
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT id,
                                   uuid,
                                   title,
                                   description,
                                   file,
                                   file_type,
                                   created_at,
                                   updated_at,
                                   deadline,
                                   project_id,
                                   team_id,
                                   ai_description,
                                   ai_audio,
                                   file_id,
                                   mime_type, size, user_profile_id, expiration_date, telegram_reminder_sent, sms_reminder_sent, call_reminder_sent, call_attempts, call_message_listened, last_call_date, gcs_file_path, gcs_uploaded
                            FROM evoicebot_app_document
                            WHERE id = %s
                            """, (doc_id,))
                row = cur.fetchone()
                if row:
                    return cls(*row)
                return None

    @classmethod
    def get_by_user_id(cls, user_id: int):
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT id,
                                   uuid,
                                   title,
                                   description,
                                   file,
                                   file_type,
                                   created_at,
                                   updated_at,
                                   deadline,
                                   project_id,
                                   team_id,
                                   ai_description,
                                   ai_audio,
                                   file_id,
                                   mime_type, size, user_profile_id, expiration_date, telegram_reminder_sent, sms_reminder_sent, call_reminder_sent, call_attempts, call_message_listened, last_call_date, gcs_file_path, gcs_uploaded
                            FROM evoicebot_app_document
                            WHERE user_profile_id = %s
                            ORDER BY created_at DESC
                            """, (user_id,))
                rows = cur.fetchall()
                return [cls(*row) for row in rows]

    @classmethod
    def get_expiring_documents(cls):
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT id,
                                   uuid,
                                   title,
                                   description,
                                   file,
                                   file_type,
                                   created_at,
                                   updated_at,
                                   deadline,
                                   project_id,
                                   team_id,
                                   ai_description,
                                   ai_audio,
                                   file_id,
                                   mime_type, size, user_profile_id, expiration_date, telegram_reminder_sent, sms_reminder_sent, call_reminder_sent, call_attempts, call_message_listened, last_call_date, gcs_file_path, gcs_uploaded
                            FROM evoicebot_app_document
                            WHERE expiration_date IS NOT NULL
                            """, ())
                rows = cur.fetchall()
                return [cls(*row) for row in rows]

    def update_expiration_date(self, expiration_date: datetime):
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            UPDATE evoicebot_app_document
                            SET expiration_date = %s,
                                updated_at      = %s
                            WHERE id = %s
                            """, (expiration_date, datetime.now(), self.id))
                conn.commit()
                self.expiration_date = expiration_date

    def update_telegram_reminder_sent(self, sent: bool = True):
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            UPDATE evoicebot_app_document
                            SET telegram_reminder_sent = %s,
                                updated_at             = %s
                            WHERE id = %s
                            """, (sent, datetime.now(), self.id))
                conn.commit()
                self.telegram_reminder_sent = sent

    def update_sms_reminder_sent(self, sent: bool = True):
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            UPDATE evoicebot_app_document
                            SET sms_reminder_sent = %s,
                                updated_at        = %s
                            WHERE id = %s
                            """, (sent, datetime.now(), self.id))
                conn.commit()
                self.sms_reminder_sent = sent

    def update_call_reminder_sent(self, sent: bool = True):
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            UPDATE evoicebot_app_document
                            SET call_reminder_sent = %s,
                                updated_at         = %s
                            WHERE id = %s
                            """, (sent, datetime.now(), self.id))
                conn.commit()
                self.call_reminder_sent = sent

    def increment_call_attempts(self):
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            UPDATE evoicebot_app_document
                            SET call_attempts  = call_attempts + 1,
                                last_call_date = %s,
                                updated_at     = %s
                            WHERE id = %s
                            """, (datetime.now(), datetime.now(), self.id))
                conn.commit()
                self.call_attempts += 1
                self.last_call_date = datetime.now()

    def update_call_message_listened(self, listened: bool = True):
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            UPDATE evoicebot_app_document
                            SET call_message_listened = %s,
                                updated_at            = %s
                            WHERE id = %s
                            """, (listened, datetime.now(), self.id))
                conn.commit()
                self.call_message_listened = listened

    def update_gcs_path(self, gcs_path: str):
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            UPDATE evoicebot_app_document
                            SET gcs_file_path = %s,
                                gcs_uploaded  = %s,
                                updated_at    = %s
                            WHERE id = %s
                            """, (gcs_path, True, datetime.now(), self.id))
                conn.commit()
                self.gcs_file_path = gcs_path
                self.gcs_uploaded = True


class VoiceCall:
    def __init__(self, id=None, sid=None, to_number=None, from_number=None,
                 message_text=None, status='initiated', duration=None, cost=None,
                 created_at=None, updated_at=None, answered_at=None, ended_at=None,
                 document_id=None, user_profile_id=None, confirmation_received=False):
        self.id = id
        self.sid = sid
        self.to_number = to_number
        self.from_number = from_number
        self.message_text = message_text
        self.status = status
        self.duration = duration
        self.cost = cost
        self.created_at = created_at
        self.updated_at = updated_at
        self.answered_at = answered_at
        self.ended_at = ended_at
        self.document_id = document_id
        self.user_profile_id = user_profile_id
        self.confirmation_received = confirmation_received

    @classmethod
    def create(cls, sid: str, to_number: str, from_number: str, message_text: str,
               document_id: int = None, user_profile_id: int = None):
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            INSERT INTO evoicebot_app_voicecall
                            (sid, to_number, from_number, message_text, status, created_at,
                             updated_at, document_id, user_profile_id, confirmation_received)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
                            """, (sid, to_number, from_number, message_text, 'initiated',
                                  datetime.now(), datetime.now(), document_id, user_profile_id, False))
                call_id = cur.fetchone()[0]
                conn.commit()
                return cls.get_by_id(call_id)

    @classmethod
    def get_by_id(cls, call_id: int):
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT id,
                                   sid,
                                   to_number,
                                   from_number,
                                   message_text,
                                   status,
                                   duration,
                                   cost,
                                   created_at,
                                   updated_at,
                                   answered_at,
                                   ended_at,
                                   document_id,
                                   user_profile_id,
                                   confirmation_received
                            FROM evoicebot_app_voicecall
                            WHERE id = %s
                            """, (call_id,))
                row = cur.fetchone()
                if row:
                    return cls(*row)
                return None

    def update_status(self, status: str):
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            UPDATE evoicebot_app_voicecall
                            SET status     = %s,
                                updated_at = %s
                            WHERE id = %s
                            """, (status, datetime.now(), self.id))
                conn.commit()
                self.status = status


User = UserProfile
