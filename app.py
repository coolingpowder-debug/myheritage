import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Family Tree & Genealogy",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ตกแต่ง CSS เพิ่มเติมเพื่อให้หน้าตาดูโมเดิร์นและสะอาดตา
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# จำลองฐานข้อมูล (ปกติส่วนนี้จะเชื่อมต่อกับ Supabase)
if 'family_members' not in st.session_state:
    st.session_state['family_members'] = [
        {"id": 1, "name": "สมชาย ใจดี", "gender": "ชาย", "birth_year": 1950, "father": "-", "mother": "-", "spouse": "สมศรี ใจดี"},
        {"id": 2, "name": "สมศรี ใจดี", "gender": "หญิง", "birth_year": 1952, "father": "-", "mother": "-", "spouse": "สมชาย ใจดี"},
        {"id": 3, "name": "สมศักดิ์ ใจดี", "gender": "ชาย", "birth_year": 1980, "father": "สมชาย ใจดี", "mother": "สมศรี ใจดี", "spouse": "วิไล รัก,พงศ์"},
    ]

# --- Sidebar เมนูหลัก ---
st.sidebar.image("https://img.icons8.com/color/96/family-man-woman-boy-girl.png", width=80)
st.sidebar.title("Family Legacy")
st.sidebar.markdown("ระบบบันทึกประวัติและลำดับเครือญาติ")

menu = st.sidebar.radio("เลือกเมนู", ["🌳 ผังครอบครัว", "➕ เพิ่มสมาชิกใหม่", "🤖 ผู้ช่วย AI วิเคราะห์ความสัมพันธ์", "⚙️ ตั้งค่าระบบ Supabase"])

# --- หน้าที่ 1: ผังครอบครัว ---
if menu == "🌳 ผังครอบครัว":
    st.markdown('<p class="main-header">🌳 ผังความสัมพันธ์ครอบครัว</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">แสดงรายชื่อและสายสัมพันธ์ของสมาชิกในตระกูล</p>', unsafe_allow_html=True)
    
    # แสดงข้อมูลแบบตารางสวยงาม
    df = pd.DataFrame(st.session_state['family_members'])
    
    # ช่องค้นหา
    search_query = st.text_input("🔍 ค้นหาชื่อสมาชิกในตระกูล...", "")
    if search_query:
        df = df[df['name'].str.contains(search_query, na=False)]
    
    # แสดงผลเป็น Card รายบุคคล
    col1, col2, col3 = st.columns(3)
    
    for index, row in df.iterrows():
        with (col1 if index % 3 == 0 else col2 if index % 3 == 1 else col3):
            st.markdown(f"""
                <div class="card">
                    <h3>👤 {row['name']}</h3>
                    <p><b>เพศ:</b> {row['gender']} | <b>เกิด พ.ศ.:</b> {row['birth_year'] + 543}</p>
                    <hr style="margin: 8px 0;">
                    <p style="font-size: 0.9rem; color: #555;">
                        <b>พ่อ:</b> {row['father']}<br>
                        <b>แม่:</b> {row['mother']}<br>
                        <b>คู่สมรส:</b> {row['spouse']}
                    </p>
                </div>
            """, unsafe_allow_html=True)

# --- หน้าที่ 2: เพิ่มสมาชิกใหม่ ---
elif menu == "➕ เพิ่มสมาชิกใหม่":
    st.markdown('<p class="main-header">➕ เพิ่มข้อมูลสมาชิกในครอบครัว</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">กรอกข้อมูลประวัติและเลือกความสัมพันธ์เพื่อบันทึกลงฐานข้อมูล</p>', unsafe_allow_html=True)
    
    with st.form("add_member_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("ชื่อ - นามสกุล")
            gender = st.selectbox("เพศ", ["ชาย", "หญิง", "อื่นๆ"])
            birth_year = st.number_input("ปีเกิด (ค.ศ.)", min_value=1900, max_value=2026, value=1990)
            
        with col2:
            # ดึงรายชื่อที่มีอยู่มาทำ Dropdown เชื่อมโยงความสัมพันธ์
            existing_names = [m["name"] for m in st.session_state['family_members']]
            existing_names.insert(0, "- ไม่มี / ไม่ระบุ -")
            
            father = st.selectbox("พ่อ", existing_names)
            mother = st.selectbox("แม่", existing_names)
            spouse = st.selectbox("คู่สมรส", existing_names)
            
        submitted = st.form_submit_button("💾 บันทึกข้อมูลลงฐานข้อมูล", use_container_width=True)
        
        if submitted:
            if name:
                new_member = {
                    "id": len(st.session_state['family_members']) + 1,
                    "name": name,
                    "gender": gender,
                    "birth_year": birth_year,
                    "father": father if father != "- ไม่มี / ไม่ระบุ -" else "-",
                    "mother": mother if mother != "- ไม่มี / ไม่ระบุ -" else "-",
                    "spouse": spouse if spouse != "- ไม่มี / ไม่ระบุ -" else "-"
                }
                st.session_state['family_members'].append(new_member)
                st.success(f"บันทึกข้อมูลของ {name} สำเร็จเรียบร้อย!")
            else:
                st.error("กรุณากรอกชื่อ-นามสกุลก่อนบันทึก")

# --- หน้าที่ 3: ผู้ช่วย AI วิเคราะห์ความสัมพันธ์ ---
elif menu == "🤖 ผู้ช่วย AI วิเคราะห์ความสัมพันธ์":
    st.markdown('<p class="main-header">🤖 ผู้ช่วย Gemini AI วิเคราะห์ตระกูล</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">พิมพ์สอบถามความสัมพันธ์ หรือให้ AI ช่วยสรุปเรื่องราวตระกูลของคุณ</p>', unsafe_allow_html=True)
    
    user_prompt = st.text_area("💬 พิมพ์คำถามเกี่ยวกับญาติ (เช่น: สมศักดิ์ เป็นลูกใคร และมีความเกี่ยวข้องกับใครบ้าง?):")
    
    if st.button("✨ ให้ AI วิเคราะห์", use_container_width=True):
        if user_prompt:
            with st.spinner("Gemini กำลังวิเคราะห์ข้อมูลสายเลือด..."):
                # จุดนี้สามารถนำ API Key ของ Gemini มาใส่เพื่อเรียกใช้งานจริงผ่าน google.generativeai
                st.info(f"จำลองคำตอบจาก Gemini AI สำหรับคำถาม: '{user_prompt}'")
                st.write("""
                จากการวิเคราะห์ฐานข้อมูลตระกูล **ใจดี**:
                - **สมศักดิ์ ใจดี** เป็นบุตรชายแท้ๆ ของ **สมชาย ใจดี** และ **สมศรี ใจดี**
                - มีศักดิ์เป็นทายาทรุ่นที่ 2 ของครอบครัว
                *(คุณสามารถเชื่อมต่อ Gemini API จริงตรงนี้เพื่อให้อ่านข้อมูลทั้งหมดจาก Supabase แล้วตอบคำถามได้อย่างแม่นยำครับ)*
                """)
        else:
            st.warning("กรุณาพิมพ์คำถามก่อนกดวิเคราะห์")

# --- หน้าที่ 4: ตั้งค่าระบบ Supabase ---
elif menu == "⚙️ ตั้งค่าระบบ Supabase":
    st.markdown('<p class="main-header">⚙️ เชื่อมต่อฐานข้อมูล Supabase</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">ตั้งค่าการเชื่อมต่อ Backend เพื่อเก็บบันทึกข้อมูลอย่างถาวร</p>', unsafe_allow_html=True)
    
    with st.form("supabase_config"):
        supabase_url = st.text_input("Supabase Project URL", type="default", placeholder="https://xxxx.supabase.co")
        supabase_key = st.text_input("Supabase Anon / Service Key", type="password", placeholder="eyJhbGciOi...")
        
        save_config = st.form_submit_button("🔗 บันทึกการเชื่อมต่อ")
        if save_config:
            st.success("บันทึกการตั้งค่าสำเร็จ! (สามารถนำค่าเหล่านี้ไปใช้เชื่อมต่อกับไลบรารี `supabase-py` ได้ทันที)")
