import streamlit as st
import urllib.parse
from pathlib import Path

# إعداد الصفحة
st.set_page_config(
    page_title="مخبز البيت",
    page_icon="🥐",
    layout="wide"
)

# دالة لتحميل ملف CSS وحقنه في الصفحة
def load_css(file_name: str):
    css_path = Path(__file__).parent / file_name
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"CSS file {file_name} not found.")

# تحميل الـ CSS
load_css("style.css")

# عنوان الموقع
st.markdown('<h1 class="main-title">مخبز البيت</h1>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">مخبوزات منزلية طازجة يومياً - اطلب الآن عبر الموقع</div>',
    unsafe_allow_html=True
)

st.divider()

# ======================
# 1) تعريف قائمة المنتجات (ثابتة داخل الكود - بدون قاعدة بيانات)
# ======================
products = [
    {"id": 1, "name": "كيك شوكولاتة 1 كجم", "price": 35},
    {"id": 2, "name": "كيك فانيليا 1 كجم", "price": 32},
    {"id": 3, "name": "كرواسون زبدة (12 قطعة)", "price": 18},
    {"id": 4, "name": "خبز عربي (10 أرغفة)", "price": 8},
    {"id": 5, "name": "ميني بيتزا (10 قطع)", "price": 25},
    {"id": 6, "name": "سينابون (8 قطع)", "price": 28},
]

st.markdown('<h2 class="section-title">قائمة المخبوزات</h2>', unsafe_allow_html=True)
st.write("اختر الكمية لكل صنف ترغب في طلبه:")

quantities = {}
cols = st.columns(3)  # عرض المنتجات في 3 أعمدة

for index, p in enumerate(products):
    col = cols[index % 3]
    with col:
        # كرت المنتج
        st.markdown('<div class="product-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="product-name">{p["name"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="product-price">{p["price"]} دينار</div>', unsafe_allow_html=True)

        q = st.number_input(
            "الكمية",
            min_value=0,
            max_value=50,
            value=0,
            step=1,
            key=f"q_{p['id']}"
        )
        quantities[p["id"]] = q
        st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ======================
# 2) بيانات العميل والطلب
# ======================
st.markdown('<h2 class="section-title">بيانات الطلب</h2>', unsafe_allow_html=True)

col_info1, col_info2 = st.columns(2)

with col_info1:
    customer_name = st.text_input("الاسم الكامل")
    customer_phone = st.text_input("رقم الهاتف (واتساب)")
with col_info2:
    delivery_time = st.text_input("وقت/تاريخ التسليم المطلوب (مثال: غداً مساءً)")
    customer_address = st.text_area("العنوان (منطقة، شارع، معالم قريبة)")

note = st.text_area("ملاحظات إضافية (مثال: أقل سكر، بدون مكسرات، كتابة اسم على الكيك)")

st.markdown(
    '<p class="hint-text">ملاحظة: سيتم إرسال الطلب إلى واتساب المخبز، وسيتم تأكيده معك يدوياً.</p>',
    unsafe_allow_html=True
)

# ======================
# 3) تجهيز رسالة واتساب
# ======================
if st.button("تجهيز الطلب وإرساله عبر واتساب"):
    # المنتجات المختارة
    selected = [(p, quantities[p["id"]]) for p in products if quantities[p["id"]] > 0]

    if not selected:
        st.warning("الرجاء اختيار منتج واحد على الأقل.")
    elif not customer_name or not customer_phone:
        st.warning("الرجاء إدخال الاسم ورقم الهاتف.")
    else:
        lines = []
        lines.append("مرحباً، أريد طلب المخبوزات التالية:")
        lines.append("")

        total = 0
        for p, q in selected:
            line_total = p["price"] * q
            total += line_total
            lines.append(f"- {p['name']} × {q} = {line_total} دينار")

        lines.append("")
        lines.append(f"الإجمالي: {total} دينار")
        lines.append("")
        lines.append(f"الاسم: {customer_name}")
        lines.append(f"رقم الهاتف: {customer_phone}")
        if customer_address:
            lines.append(f"العنوان: {customer_address}")
        if delivery_time:
            lines.append(f"وقت/تاريخ التسليم المطلوب: {delivery_time}")
        if note:
            lines.append("")
            lines.append(f"ملاحظات إضافية: {note}")

        message = "\n".join(lines)
        encoded_message = urllib.parse.quote(message)

        # ضع هنا رقم الواتساب الخاص بك مع كود الدولة (مثال رقم ليبي)
        your_whatsapp_number = "218914671709"  # عدّلها لرقمك

        wa_link = f"https://wa.me/{your_whatsapp_number}?text={encoded_message}"

        st.success("تم تجهيز الطلب، اضغط على الزر بالأسفل لإرساله عبر واتساب:")
        st.markdown(
            f'<a class="wa-button" href="{wa_link}" target="_blank">إرسال الطلب عبر واتساب</a>',
            unsafe_allow_html=True
        )

