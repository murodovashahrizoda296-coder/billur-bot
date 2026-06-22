import telebot
import schedule
import time
import threading
from datetime import datetime

TOKEN = "8750154778:AAH2_kkv6vi0pYdvd_TQo-_ESdAV7SQ7Kcg"
ADMIN_ID = 6262761008
GROUP_USERNAME = "@billur_on"

bot = telebot.TeleBot(TOKEN)
user_states = {}

MAHSULOTLAR = (
    "BILLUR MAHSULOTLARI KATALOGI\n\n"
    "TOZALASH VOSITALARI:\n"
    "- Kuxnya Antijir 500gr - 13 000 som\n"
    "- Yogoch sprey 500gr - 12 000 som\n"
    "- Care Gloss 500gr - 13 000 som\n"
    "- Billur Krem 750gr - 21 000 som\n"
    "- Oyna tozalovchi 750gr - 10 000 som\n\n"
    "KIR YUVISH:\n"
    "- Asif Pro gel 4.5kg - 65 000 som\n"
    "- Bolalar kiyimi geli 1kg - 20 000 som\n"
    "- Kislorodli tozalovchi 300gr - 25 000 som\n\n"
    "SOVUN VA GIGIYENA:\n"
    "- Idish yuvish 500gr - 6 000 som\n"
    "- Universal sovun 630gr - 28 000 som\n"
    "- Atir sovun 140gr - 7 000 som\n\n"
    "MAXSUS:\n"
    "- Exotic Spray 500ml - 30 000 som\n"
    "- KROT quvur tozalovchi 200gr - 10 000 som\n"
    "- Havo yangilagich (Siren, Morskoy Briz, Posle Dojdya)\n\n"
    "Buyurtma: @billur_Yordamchingiz"
)

DOSTAVKA = (
    "YETKAZIB BERISH SHARTLARI\n\n"
    "Toshkent shahri:\n"
    "Narx: 10 000 som | Vaqt: 1-2 soat\n\n"
    "Toshkent viloyati:\n"
    "Narx: 20 000 som | Vaqt: 1 kun\n\n"
    "Boshqa viloyatlar:\n"
    "Narx: 30 000-50 000 som | Vaqt: 2-3 kun\n\n"
    "300 000 somdan yuqori buyurtmada DOSTAVKA BEPUL!"
)

HAQIDA = (
    "BILLUR BRENDI HAQIDA\n\n"
    "Billur - O'zbekistonda ishlab chiqariladigan\n"
    "uy-rozgor kimyo mahsulotlari brendi.\n\n"
    "- O'zbekistonda ishlab chiqariladi\n"
    "- Sertifikatlangan mahsulotlar\n"
    "- Oila va bolalar uchun xavfsiz\n"
    "- Keng assortiment\n"
    "- Qulay narx, yuqori sifat\n\n"
    "Billur - tozalikni sevganlar tanlovi!"
)

MASLAHATLAR = [
    "Bugungi maslahat: Idish yuvishda iliq suv ishlatish yogni 3x tezroq eritadi! Billur idish yuvish vositasi bilan birgalikda ishlating.",
    "Bugungi maslahat: Oynani tozalashda gazeta qogozi ishlating - pariq qoldirmaydi! Billur oyna tozalovchi bilan mukammal natija.",
    "Bugungi maslahat: Kir yuvishda rangli va oq kiyimlarni ajrating - ranglar saqlanadi! Billur geli bilan kiyimlaringiz yangiday.",
    "Bugungi maslahat: Vannaxonani haftada 2 marta tozalash bakteriyalardan himoya qiladi! Billur Care Gloss eng yaxshi yechim.",
    "Bugungi maslahat: Quvurlarni oyiga 1 marta Billur KROT bilan tozalang - tiqin muammosi bolmaydi!",
    "Bugungi maslahat: Uy havosini yangilash uchun Billur Exotic Spray ishlating - 1 purkashda xona xushboy boladi.",
    "Bugungi maslahat: Qollarni sovun bilan kamida 20 soniya yuvish kerak. Billur suyuq sovun qollaringizni yumshatadi.",
]

FAKTLAR = [
    "Qiziqarli fakt: Har kuni 30 daqiqa uy yigishtirish 700 kaloriya yoqadi - bu yugurish bilan barobar!",
    "Qiziqarli fakt: Oshxona lavabosi hojatxonadan kora bakteriyalarga boy bolishi mumkin. Billur Antijir bilan himoyalaning!",
    "Qiziqarli fakt: Konditsioner ishlatilgan kiyimlar 1.5 barobar uzoqroq xizmat qiladi. Billur konditsioner sinab koring!",
    "Qiziqarli fakt: Tartibli uy stress darajasini 20% kamaytiradi! Billur mahsulotlari bilan tozalash osonroq.",
    "Qiziqarli fakt: Havo muattar ishlatish xonadagi zararli bakteriyalarni 60% kamaytiradi! Billur havo yangilagich - sogom uy.",
]

POSTLAR = [
    "BUGUNGI MAHSULOT\n\nBillur Superactive ANTIJIR 500ml\n\nPlita va oshxonangizni yogdan tozalang!\n\n- 30 soniyada tasir qiladi\n- Kuchli superaktiv formula\n- Hidni yoq qiladi\n\nNarxi: 13 000 som\n\nBuyurtma: @billur_Yordamchingiz",
    "BUGUNGI MAHSULOT\n\nAsif Pro Gel - Kir yuvish 4.5kg\n\nKiyimlaringiz yangi chiqarilgandek bolsin!\n\n- 150 ta yuvinish - tejamkor!\n- Bahor nafasi xushoyi\n- Avtomat mashina uchun\n\nNarxi: 65 000 som\n\nBuyurtma: @billur_Yordamchingiz",
    "BUGUNGI MAHSULOT\n\nBillur Suyuq Sovun - Aloe Vera\n\nQollaringizni parvarish qiling!\n\n- Aloe vera bilan yumshatadi\n- Bolalar uchun xavfsiz\n- Yoqimli xushboy\n\nNarxi: 6 000 som\n\nBuyurtma: @billur_Yordamchingiz",
    "BUGUNGI MAHSULOT\n\nBillur KROT - Quvur tozalovchi\n\nTiqilgan quvurni 5 daqiqada oching!\n\n- 5 daqiqada tasir qiladi\n- Soch va yogni eritadi\n- Oshxona va hammom uchun\n\nNarxi: 10 000 som\n\nBuyurtma: @billur_Yordamchingiz",
    "BUGUNGI MAHSULOT\n\nBillur Exotic Spray 500ml\n\nUyingiz doim xushboy taratsin!\n\n- Gilam, parda, mato uchun\n- Yoqimsiz hidni yoqotadi\n- Uzoq vaqt ifor taratadi\n\nNarxi: 30 000 som\n\nBuyurtma: @billur_Yordamchingiz",
]

post_index = [0]
fakt_index = [0]
maslahat_index = [0]


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Mahsulotlar', 'Narxlar')
    keyboard.row('Buyurtma', 'Dostavka')
    keyboard.row('Brend haqida', 'Maslahat')
    bot.send_message(
        message.chat.id,
        "Assalomu alaykum, " + message.from_user.first_name + "!\n\n"
        "Billur Official Bot ga xush kelibsiz!\n\n"
        "Bu yerda siz:\n"
        "- Mahsulotlar haqida bilib olasiz\n"
        "- Qulay buyurtma bera olasiz\n"
        "- Foydali maslahatlar olasiz\n\n"
        "Quyidagi tugmalardan birini tanlang:",
        reply_markup=keyboard
    )


@bot.message_handler(commands=['mahsulotlar'])
@bot.message_handler(func=lambda m: m.text in ['Mahsulotlar', 'Narxlar'])
def mahsulotlar(message):
    bot.send_message(message.chat.id, MAHSULOTLAR)


@bot.message_handler(commands=['dostavka'])
@bot.message_handler(func=lambda m: m.text == 'Dostavka')
def dostavka(message):
    bot.send_message(message.chat.id, DOSTAVKA)


@bot.message_handler(commands=['haqida'])
@bot.message_handler(func=lambda m: m.text == 'Brend haqida')
def haqida(message):
    bot.send_message(message.chat.id, HAQIDA)


@bot.message_handler(commands=['maslahat'])
@bot.message_handler(func=lambda m: m.text == 'Maslahat')
def maslahat(message):
    idx = maslahat_index[0] % len(MASLAHATLAR)
    maslahat_index[0] += 1
    bot.send_message(message.chat.id, MASLAHATLAR[idx])


@bot.message_handler(commands=['buyurtma'])
@bot.message_handler(func=lambda m: m.text == 'Buyurtma' and m.chat.id not in user_states)
def buyurtma_start(message):
    user_states[message.chat.id] = {'step': 'ism'}
    bot.send_message(message.chat.id, "Buyurtma berish\n\nIsmingizni yozing:")


@bot.message_handler(func=lambda m: m.chat.id in user_states)
def buyurtma_process(message):
    chat_id = message.chat.id
    state = user_states.get(chat_id, {})
    step = state.get('step')

    if step == 'ism':
        user_states[chat_id]['ism'] = message.text
        user_states[chat_id]['step'] = 'mahsulot'
        bot.send_message(chat_id, "Rahmat!\n\nQaysi mahsulot kerak? (Mahsulot nomini yozing)")
    elif step == 'mahsulot':
        user_states[chat_id]['mahsulot'] = message.text
        user_states[chat_id]['step'] = 'manzil'
        bot.send_message(chat_id, "Qabul qilindi!\n\nManzilingizni yozing:")
    elif step == 'manzil':
        user_states[chat_id]['manzil'] = message.text
        user_states[chat_id]['step'] = 'telefon'
        bot.send_message(chat_id, "Ajoyib!\n\nTelefon raqamingizni yozing:\n(Misol: +998901234567)")
    elif step == 'telefon':
        user_states[chat_id]['telefon'] = message.text
        data = user_states[chat_id]
        buyurtma_text = (
            "YANGI BUYURTMA!\n\n"
            "Ism: " + data['ism'] + "\n"
            "Mahsulot: " + data['mahsulot'] + "\n"
            "Manzil: " + data['manzil'] + "\n"
            "Telefon: " + data['telefon'] + "\n"
            "Vaqt: " + datetime.now().strftime('%d.%m.%Y %H:%M')
        )
        bot.send_message(ADMIN_ID, buyurtma_text)
        bot.send_message(
            chat_id,
            "Buyurtmangiz qabul qilindi!\n\n"
            "@billur_Yordamchingiz siz bilan tez orada boglanadi!\n\n"
            "Billur ni tanlaganingiz uchun rahmat!"
        )
        del user_states[chat_id]


def send_morning_post():
    idx = fakt_index[0] % len(FAKTLAR)
    fakt_index[0] += 1
    try:
        bot.send_message(GROUP_USERNAME, FAKTLAR[idx])
    except Exception as e:
        print("Xato:", e)


def send_afternoon_post():
    idx = post_index[0] % len(POSTLAR)
    post_index[0] += 1
    try:
        bot.send_message(GROUP_USERNAME, POSTLAR[idx])
    except Exception as e:
        print("Xato:", e)


def send_evening_post():
    idx = maslahat_index[0] % len(MASLAHATLAR)
    maslahat_index[0] += 1
    try:
        msg = "Kechqurun maslahat\n\n" + MASLAHATLAR[idx] + "\n\nBillur mahsulotlari: @billur_Yordamchingiz"
        bot.send_message(GROUP_USERNAME, msg)
    except Exception as e:
        print("Xato:", e)


def run_scheduler():
    schedule.every().day.at("09:00").do(send_morning_post)
    schedule.every().day.at("14:00").do(send_afternoon_post)
    schedule.every().day.at("19:00").do(send_evening_post)
    while True:
        schedule.run_pending()
        time.sleep(60)


scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

print("Billur bot ishga tushdi!")
print("Bot: @billur_uz_bot")
print("Guruh: @billur_on")
print("Botni toxtatish uchun: Ctrl+C")

bot.infinity_polling()
@bot.message_handler(content_types=['photo'])
def get_photo_id(message):
    file_id = message.photo[-1].file_id
    bot.send_message(message.chat.id, "file_id: " + file_id)
