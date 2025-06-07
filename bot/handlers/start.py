import calendar
import logging
from datetime import datetime
from datetime import timedelta

import pytz
from aiogram import Router, types, F
from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton

from webapp.models import UserProfile, Document

router = Router()


class UserStates(StatesGroup):
    WAITING_FOR_PHONE = State()
    WAITING_FOR_DOCUMENT = State()
    WAITING_FOR_DATE = State()
    DATE_YEAR = State()
    DATE_MONTH = State()
    DATE_DAY = State()


@router.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        "*Dostępne komendy:*\n\n"
        "/start - Rozpocznij pracę z botem i zarejestruj się\n"
        "/documents - Wyświetl listę wszystkich aktualnych dokumentów\n"
        "/analyze - Analizuj dokument przy użyciu sztucznej inteligencji\n"
        "/help - Wyświetl tę wiadomość pomocy\n\n"

        "*Jak korzystać z bota:*\n"
        "1. Zarejestruj się używając komendy /start i podaj swój numer telefonu\n"
        "2. Wyślij swój dokument\n"
        "3. Wybierz datę ważności dokumentu\n"
        "4. Bot automatycznie przypomni Ci o zbliżającym się terminie ważności:\n"
        "   - Powiadomienie w Telegramie na miesiąc przed\n"
        "   - SMS na 3 tygodnie przed\n"
        "   - Połączenie głosowe na 2 tygodnie przed\n"
        "5. Użyj komendy /analyze, aby uzyskać szczegółową analizę dokumentu i rekomendacje"
    )
    await message.answer(text, parse_mode="Markdown")


def get_user_by_telegram_message(message_or_callback):
    if hasattr(message_or_callback, 'from_user'):
        from_user = message_or_callback.from_user
    else:
        from_user = message_or_callback.from_user

    user = UserProfile.get_by_telegram_id(from_user.id)

    if not user and from_user.username:
        user = UserProfile.get_by_username(from_user.username)
        if user and not user.telegram_id:
            user.update_telegram_id(from_user.id)

    return user


@router.message(Command("documents"))
async def cmd_my_documents(message: Message):
    try:
        user = get_user_by_telegram_message(message)

        if not user:
            await message.answer("Nie jesteś zarejestrowany w systemie. Użyj /start aby się zarejestrować.")
            return

        documents = Document.get_by_user_id(user.id)

        if not documents:
            await message.answer("Nie masz żadnych dokumentów w systemie.")
            return

        response = "📄 *Twoje dokumenty:*\n\n"
        current_date = datetime.now(pytz.UTC)

        for i, doc in enumerate(documents, 1):
            response += f"*{i}. {doc.title}*\n"
            response += f"   Data dodania: {doc.created_at.strftime('%d.%m.%Y')}\n"

            if hasattr(doc, 'expiration_date') and doc.expiration_date:
                days_left = (doc.expiration_date - current_date).days
                expiration_date = doc.expiration_date.strftime('%d.%m.%Y')

                response += f"   Data ważności: {expiration_date}\n"

                if days_left > 30:
                    response += f"   Pozostało: {days_left} dni\n"
                elif days_left > 0:
                    response += f"   ⚠️ Pozostało tylko: {days_left} dni! ⚠️\n"
                elif days_left == 0:
                    response += f"   ⚠️ UWAGA: Dokument wygasa dzisiaj! ⚠️\n"
                else:
                    response += f"   ⛔ Dokument wygasł {abs(days_left)} dni temu! ⛔\n"
            else:
                response += "   Brak daty ważności\n"

            response += "\n"

        await message.answer(response, parse_mode="Markdown")

    except Exception as e:
        logging.error(f"Błąd w cmd_my_documents: {e}")
        await message.answer("Wystąpił błąd podczas pobierania dokumentów.")


async def save_user_contact(telegram_id, first_name, last_name, phone_number, username=None):
    try:
        # First try to find by telegram_id
        user = UserProfile.get_by_telegram_id(telegram_id)

        if not user and username:
            # If not found by telegram_id, try to find by username
            user = UserProfile.get_by_username(username)
            if user and not user.telegram_id:
                # User exists but doesn't have telegram_id - update it
                user.update_telegram_id(telegram_id)
                if user.phone != phone_number:
                    user.update_phone(phone_number)
                return user

        if not user:
            # Create new user if not found
            user = UserProfile.create(
                telegram_id=telegram_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                phone=phone_number
            )
        else:
            # Update existing user's phone if different
            if user.phone != phone_number:
                user.update_phone(phone_number)
        return user
    except Exception as e:
        logging.error(f"Błąd podczas zapisywania kontaktu: {e}")
        return None


async def save_document(user_id, file_id, name, mime_type, size, bot=None):
    try:
        document = Document.create(
            user_id=user_id,
            file_id=file_id,
            title=name,
            mime_type=mime_type,
            size=size
        )

        if bot:
            try:
                from bot.storage import GCSManager
                gcs_manager = GCSManager()

                gcs_path = await gcs_manager.upload_document(
                    telegram_bot=bot,
                    file_id=file_id,
                    user_id=user_id,
                    document_name=name
                )

                document.update_gcs_path(gcs_path)
                logging.info(f"Dokument {name} przesłany do GCS: {gcs_path}")
            except Exception as e:
                logging.error(f"Nie udało się przesłać dokumentu do GCS: {e}")

        return document
    except Exception as e:
        logging.error(f"Błąd podczas zapisywania dokumentu: {e}")
        return None


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

    try:
        # First try to find by telegram_id
        user = UserProfile.get_by_telegram_id(message.from_user.id)

        # If not found by telegram_id, try by username
        if not user and message.from_user.username:
            user = UserProfile.get_by_username(message.from_user.username)
            if user and not user.telegram_id:
                # User exists but doesn't have telegram_id - update it
                user.update_telegram_id(message.from_user.id)

        if user:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="Wyślij dokument")]],
                resize_keyboard=True,
                one_time_keyboard=True
            )
            await message.answer(
                f"Witaj ponownie, {user.first_name}! Możesz wysłać dokument.",
                reply_markup=keyboard
            )
            await state.update_data(user_id=user.id)
            await state.update_data(phone_number=user.phone)
            await state.set_state(UserStates.WAITING_FOR_DOCUMENT)
            return
    except Exception as e:
        logging.error(f"Błąd podczas sprawdzania użytkownika: {e}")

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Wyślij numer", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Cześć! Proszę najpierw o podanie numeru telefonu.", reply_markup=keyboard)
    await state.set_state(UserStates.WAITING_FOR_PHONE)


@router.message(UserStates.WAITING_FOR_PHONE, F.content_type == ContentType.CONTACT)
async def get_contact(message: types.Message, state: FSMContext):
    contact = message.contact
    name = f"{contact.first_name} {contact.last_name if contact.last_name else ''}"

    user = await save_user_contact(
        message.from_user.id,
        contact.first_name,
        contact.last_name,
        contact.phone_number,
        message.from_user.username
    )

    if not user:
        await message.answer("Wystąpił błąd podczas rejestracji. Spróbuj ponownie.")
        return

    await state.update_data(user_id=user.id)
    await state.update_data(phone_number=contact.phone_number)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Wyślij dokument")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(
        f"Dziękuję, {name.strip()}. Twój numer +{contact.phone_number} został zapisany.",
        reply_markup=keyboard
    )
    await state.set_state(UserStates.WAITING_FOR_DOCUMENT)


@router.message(UserStates.WAITING_FOR_DOCUMENT, F.text == "Wyślij dokument")
async def send_document_request(message: Message, state: FSMContext):
    await message.answer("Proszę wyślij dokument", reply_markup=ReplyKeyboardRemove())


@router.message(UserStates.WAITING_FOR_DOCUMENT, F.content_type == ContentType.DOCUMENT)
async def get_document(message: types.Message, state: FSMContext):
    document = message.document
    user_data = await state.get_data()

    doc = await save_document(
        user_data['user_id'],
        document.file_id,
        document.file_name,
        document.mime_type,
        document.file_size,
        bot=message.bot
    )

    if not doc:
        await message.answer("Wystąpił błąd podczas zapisywania dokumentu. Spróbuj ponownie.")
        return

    await state.update_data(document_id=doc.id)

    response_text = (
        f"Dokument otrzymany:\n"
        f"Nazwa: {document.file_name}\n"
        f"Rozmiar: {document.file_size} bajtów\n"
    )

    if hasattr(doc, 'gcs_uploaded') and doc.gcs_uploaded:
        response_text += "✅ Dokument został zapisany w bezpiecznym magazynie w chmurze.\n"
    else:
        response_text += "⚠️ Dokument został zapisany tylko w systemie Telegram.\n"

    await message.answer(response_text)

    current_year = datetime.now().year
    years_keyboard = []
    row = []

    for year in range(current_year, current_year + 3):
        row.append(InlineKeyboardButton(text=str(year), callback_data=f"year_{year}"))
        if len(row) == 3:
            years_keyboard.append(row)
            row = []

    if row:
        years_keyboard.append(row)

    markup = InlineKeyboardMarkup(inline_keyboard=years_keyboard)
    await message.answer("Wybierz rok ważności dokumentu:", reply_markup=markup)
    await state.set_state(UserStates.DATE_YEAR)


@router.callback_query(UserStates.DATE_YEAR)
async def process_year(callback_query: types.CallbackQuery, state: FSMContext):
    year = int(callback_query.data.split('_')[1])
    await state.update_data(exp_year=year)

    months_keyboard = []
    row = []

    for month in range(1, 13):
        month_name = calendar.month_name[month][:3]
        row.append(InlineKeyboardButton(text=month_name, callback_data=f"month_{month}"))
        if len(row) == 4:
            months_keyboard.append(row)
            row = []

    if row:
        months_keyboard.append(row)

    markup = InlineKeyboardMarkup(inline_keyboard=months_keyboard)
    await callback_query.message.edit_text(f"Rok: {year}. Teraz wybierz miesiąc:", reply_markup=markup)
    await state.set_state(UserStates.DATE_MONTH)


@router.callback_query(UserStates.DATE_MONTH)
async def process_month(callback_query: types.CallbackQuery, state: FSMContext):
    month = int(callback_query.data.split('_')[1])
    user_data = await state.get_data()
    year = user_data['exp_year']

    await state.update_data(exp_month=month)

    _, days_in_month = calendar.monthrange(year, month)

    days_keyboard = []
    row = []

    for day in range(1, days_in_month + 1):
        row.append(InlineKeyboardButton(text=str(day), callback_data=f"day_{day}"))
        if len(row) == 7:
            days_keyboard.append(row)
            row = []

    if row:
        days_keyboard.append(row)

    markup = InlineKeyboardMarkup(inline_keyboard=days_keyboard)
    month_name = calendar.month_name[month]
    await callback_query.message.edit_text(
        f"Rok: {year}, Miesiąc: {month_name}. Teraz wybierz dzień:",
        reply_markup=markup
    )
    await state.set_state(UserStates.DATE_DAY)


@router.callback_query(UserStates.DATE_DAY)
async def process_day(callback_query: types.CallbackQuery, state: FSMContext):
    day = int(callback_query.data.split('_')[1])
    user_data = await state.get_data()

    year = user_data['exp_year']
    month = user_data['exp_month']

    expiration_date = datetime(year, month, day, tzinfo=pytz.UTC)

    one_month_before = expiration_date - timedelta(days=30)
    three_weeks_before = expiration_date - timedelta(weeks=3)
    two_weeks_before = expiration_date - timedelta(weeks=2)

    try:
        document = Document.get_by_id(user_data['document_id'])
        if document:
            document.update_expiration_date(expiration_date)

            if "reminder_system" in callback_query.bot.data:
                reminder_system = callback_query.bot.data["reminder_system"]
                await reminder_system.schedule_document_reminders(
                    user_data['user_id'],
                    document.id,
                    expiration_date
                )
    except Exception as e:
        logging.error(f"Błąd podczas aktualizacji daty ważności dokumentu: {e}")

    await callback_query.message.edit_text(
        f"Dziękuję! Dokument ważny do: {day}.{month}.{year}\n\n"
        f"Przypomnienia zostały ustawione:\n"
        f"- Wiadomość w Telegram: {one_month_before.strftime('%d.%m.%Y')}\n"
        f"- SMS na numer +{user_data['phone_number']}: {three_weeks_before.strftime('%d.%m.%Y')}\n"
        f"- Połączenie głosowe: {two_weeks_before.strftime('%d.%m.%Y')}"
    )

    await state.clear()


@router.message(F.content_type == ContentType.DOCUMENT)
async def document_out_of_order(message: types.Message):
    await message.answer("Najpierw proszę podać numer telefonu. Wpisz /start aby rozpocząć.")


@router.message(F.text == "Wyślij dokument")
async def document_request_out_of_order(message: types.Message):
    await message.answer("Najpierw proszę podać numer telefonu. Wpisz /start aby rozpocząć.")


@router.message(Command("get_document"))
async def cmd_get_document(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Pokaż moje dokumenty", callback_data="show_documents")]
        ]
    )
    await message.answer(
        "Aby pobrać dokument, najpierw sprawdź listę swoich dokumentów:",
        reply_markup=keyboard
    )


@router.callback_query(lambda c: c.data == "show_documents")
async def show_documents_for_download(callback_query: types.CallbackQuery):
    try:
        user = UserProfile.get_by_telegram_id(callback_query.from_user.id)

        if not user:
            await callback_query.message.answer(
                "Nie jesteś zarejestrowany w systemie. Użyj /start aby się zarejestrować.")
            return

        documents = Document.get_by_user_id(user.id)

        if not documents:
            await callback_query.message.answer("Nie masz żadnych dokumentów w systemie.")
            return

        keyboard = []
        for doc in documents:
            if hasattr(doc, 'gcs_file_path') and doc.gcs_file_path:
                keyboard.append([
                    InlineKeyboardButton(
                        text=f"📄 {doc.title}",
                        callback_data=f"download_{doc.id}"
                    )
                ])

        if not keyboard:
            await callback_query.message.answer("Nie znaleziono dokumentów dostępnych do pobrania.")
            return

        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        await callback_query.message.answer(
            "Wybierz dokument, który chcesz pobrać:",
            reply_markup=markup
        )
    except Exception as e:
        logging.error(f"Błąd w show_documents_for_download: {e}")
        await callback_query.message.answer("Wystąpił błąd. Spróbuj ponownie.")


@router.callback_query(lambda c: c.data.startswith("download_"))
async def generate_download_link(callback_query: types.CallbackQuery):
    document_id = int(callback_query.data.split('_')[1])

    try:
        document = Document.get_by_id(document_id)

        if not document:
            await callback_query.message.answer("Nie znaleziono dokumentu.")
            return

        if not hasattr(document, 'gcs_file_path') or not document.gcs_file_path:
            await callback_query.message.answer(
                "Ten dokument nie jest dostępny do pobrania z chmury. "
                "Zapisany jest tylko w systemie Telegram."
            )
            return

        try:
            from bot.storage import GCSManager
            gcs_manager = GCSManager()

            download_url = gcs_manager.get_document_url(document.gcs_file_path, expire_time=3600)

            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="🔗 Pobierz dokument", url=download_url)]
                ]
            )

            await callback_query.message.answer(
                f"Link do pobrania dokumentu '{document.title}' jest ważny przez 1 godzinę:",
                reply_markup=keyboard
            )
        except Exception as e:
            logging.error(f"Błąd podczas generowania linku do pobrania: {e}")
            await callback_query.message.answer(
                "Wystąpił błąd podczas generowania linku do pobrania. Spróbuj ponownie później."
            )
    except Exception as e:
        logging.error(f"Błąd w generate_download_link: {e}")
        await callback_query.message.answer("Wystąpił błąd. Spróbuj ponownie.")


@router.message(Command("analyze"))
async def cmd_analyze_document(message: Message, state: FSMContext):
    try:
        user = UserProfile.get_by_telegram_id(message.from_user.id)

        if not user:
            await message.answer("Nie jesteś zarejestrowany. Użyj /start, aby się zarejestrować.")
            return

        documents = Document.get_by_user_id(user.id)

        if not documents:
            await message.answer("Nie masz żadnych dokumentów w systemie.")
            return

        keyboard = []
        for doc in documents:
            keyboard.append([InlineKeyboardButton(
                text=f"📄 {doc.title}",
                callback_data=f"analyze_{doc.id}"
            )])

        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        await message.answer("Wybierz dokument do analizy:", reply_markup=markup)
    except Exception as e:
        logging.error(f"Błąd w cmd_analyze_document: {e}")
        await message.answer("Wystąpił błąd. Spróbuj ponownie.")


@router.callback_query(lambda c: c.data and c.data.startswith("analyze_"))
async def analyze_document_callback(callback_query: types.CallbackQuery, crew_manager=None, **kwargs):
    document_id = int(callback_query.data.split('_')[1])

    await callback_query.message.edit_text("⏳ Analizuję dokument przy użyciu sztucznej inteligencji...")

    if not crew_manager:
        await callback_query.message.edit_text(
            "❌ System Crew AI nie jest dostępny. Skontaktuj się z administratorem."
        )
        return

    import asyncio

    async def run_analysis():
        results = await asyncio.to_thread(
            crew_manager.create_document_analysis_crew,
            document_id
        )
        return results

    try:
        results = await run_analysis()

        if results:
            await callback_query.message.edit_text(
                results,
                parse_mode="Markdown"
            )
        else:
            await callback_query.message.edit_text(
                "❌ Nie udało się przeprowadzić analizy. Spróbuj ponownie później."
            )
    except Exception as e:
        logging.error(f"Błąd podczas analizy dokumentu: {e}")
        await callback_query.message.edit_text(
            f"❌ Wystąpił błąd podczas analizy: {str(e)[:100]}..."
        )


@router.message(Command("report"))
async def cmd_document_report(message: Message, crew_manager=None, **kwargs):
    try:
        user = UserProfile.get_by_telegram_id(message.from_user.id)

        if not user:
            await message.answer("Nie jesteś zarejestrowany w systemie. Użyj /start aby się zarejestrować.")
            return

        documents = Document.get_by_user_id(user.id)

        if not documents:
            await message.answer("Nie masz żadnych dokumentów w systemie.")
            return

        processing_message = await message.answer("⏳ Generuję kompleksowy raport o Twoich dokumentach...")

        if not crew_manager:
            await processing_message.edit_text(
                "❌ System Crew AI nie jest dostępny. Skontaktuj się z administratorem."
            )
            return

        import asyncio

        async def run_report_generation():
            report = await crew_manager.generate_document_report(user.id)
            return report

        try:
            report = await run_report_generation()

            if report:
                if len(report) <= 4000:
                    await processing_message.edit_text(
                        report,
                        parse_mode="Markdown"
                    )
                else:
                    await processing_message.edit_text(
                        "📊 Twój raport dokumentów jest gotowy:",
                        parse_mode="Markdown"
                    )

                    parts = []
                    current_part = ""
                    for line in report.split('\n'):
                        if len(current_part) + len(line) + 1 > 3500:
                            parts.append(current_part)
                            current_part = line + '\n'
                        else:
                            current_part += line + '\n'

                    if current_part:
                        parts.append(current_part)

                    for i, part in enumerate(parts, 1):
                        await message.answer(
                            f"{part}\n\n(Część {i} z {len(parts)})",
                            parse_mode="Markdown"
                        )
            else:
                await processing_message.edit_text(
                    "❌ Nie udało się wygenerować raportu. Spróbuj ponownie później."
                )
        except Exception as e:
            logging.error(f"Błąd podczas generowania raportu: {e}")
            await processing_message.edit_text(
                f"❌ Wystąpił błąd podczas generowania raportu: {str(e)[:100]}..."
            )
    except Exception as e:
        logging.error(f"Błąd w cmd_document_report: {e}")
        await message.answer("Wystąpił błąd. Spróbuj ponownie.")
