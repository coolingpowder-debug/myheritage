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
        {"id": 3, "name": "สมศักดิ์ ใจดี", "gender": "ชาย", "birth_year": 1980, "father": "สมชาย ใจดี", "mother": "สมศรี ใจดี", "spouse": "วิไล รักพงศ์"},
    ]

# --- Sidebar เมนูหลัก ---
st.sidebar.image("https://img.icons8.com/color/96/family-man-woman-boy-girl.png", width=80)
st.sidebar.title("Family Legacy")
st.sidebar.markdown("ระบบบันทึกประวัติและลำดับเครือญาติ")

menu = st.sidebar.radio("เลือกเมนู", [
    "🌳 ผังครอบครัว", 
    "➕ เพิ่มสมาชิกใหม่", 
    "🗑️ ลบข้อมูลสมาชิก", 
    "🤖 ผู้ช่วย AI วิเคราะห์ความสัมพันธ์", 
    "⚙️ ตั้งค่าระบบ Supabase"
])

# --- หน้าที่ 1: ผังครอบครัว ---
if menu == "🌳 ผังครอบครัว":
    st.markdown('<p class="main-header">🌳 ผังความสัมพันธ์ครอบครัว</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">แสดงรายชื่อและสายสัมพันธ์ของสมาชิกในตระกูล</p>', unsafe_allow_html=True)
    
    # ช่องค้นหา
    search_query = st.text_input("🔍 ค้นหาชื่อสมาชิกในตระกูล...", "")
    
    # กรองข้อมูลตามคำค้นหา
    members = st.session_state['family_members']
    if search_query:
        filtered_members = [m for m in members if search_query.lower() in m['name'].lower()]
    else:
        filtered_members = members

    if not filtered_members:
        st.info("ไม่พบรายชื่อสมาชิกที่ค้นหา")
    else:
        # แสดงผลเป็น Card รายบุคคลพร้อมปุ่มลบด่วนในการ์ด
        col1, col2, col3 = st.columns(3)
        
        for index, row in enumerate(filtered_members):
            target_col = col1 if index % 3 == 0 else (col2 if index % 3 == 1 else col3)
            with target_col:
                st.markdown(f"""
                    <div class="card">
                        <h3>👤 {row['name']}</h3>
                        <p><b>เพศ:</b> {row['gender']} | <b>เกิด พ.ศ.:</b> {row['birth_year'] + 543}</p>
                        <hr style="margin: 8px 0;">
                        <p style="font-size: 0.9rem; color: #555; margin-bottom: 10px;">
                            <b>พ่อ:</b> {row['father']}<br>
                            <b>แม่:</b> {row['mother']}<br>
                            <b>คู่สมรส:</b> {row['spouse']}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
                # ปุ่มลบประจำการ์ด
                if st.button(f"🗑️ ลบ {row['name']}", key=f"card_del_{row['id']}"):
                    st.session_state['family_members'] = [m for m in st.session_state['family_members'] if m['id'] != row['id']]
                    st.success(f"ลบข้อมูลของ {row['name']} เรียบร้อยแล้ว!")
                    st.rerun()

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
            existing_names = [m["name"] for m in st.session_state['family_members']]
            existing_names.insert(0, "- ไม่มี / ไม่ระบุ -")
            
            father = st.selectbox("พ่อ", existing_names)
            mother = st.selectbox("แม่", existing_names)
            spouse = st.selectbox("คู่สมรส", existing_names)
            
        submitted = st.form_submit_button("💾 บันทึกข้อมูลลงฐานข้อมูล", use_container_width=True)
        
        if submitted:
            if name:
                new_id = max([m['id'] for m in st.session_state['family_members']], default=0) + 1
                new_member = {
                    "id": new_id,
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

# --- หน้าที่ 3: ลบข้อมูลสมาชิก (เมนูจัดการเฉพาะ) ---
elif menu == "🗑️ ลบข้อมูลสมาชิก":
    st.markdown('<p class="main-header">🗑️ จัดการลบข้อมูลสมาชิกที่ไม่ใช้</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">เลือกรายชื่อสมาชิกที่ต้องการลบออกจากระบบหรือข้อมูลตัวอย่าง</p>', unsafe_allow_html=True)
    
    if not st.session_state['family_members']:
        st.info("ไม่มีข้อมูลสมาชิกในระบบขณะนี้")
    else:
        member_options = {m['name']: m['id'] for m in st.session_state['family_members']}
        selected_to_delete = st.selectbox("เลือกรายชื่อสมาชิกที่ต้องการลบออก", list(member_options.keys()))
        
        col1, col2 = st.columns([1, 4])
        with col1:
            confirm_delete = st.button("ยืนยันการลบ", type="primary", use_container_width=True)
            
        if confirm_delete:
            target_id = member_options[selected_to_delete]
            st.session_state['family_members'] = [m for m in st.session_state['family_members'] if m['id'] != target_id]
            st.success(f"ลบข้อมูลของ '{selected_to_delete}' สำเร็จเรียบร้อยแล้วครับ!")
            st.rerun()

# --- หน้าที่ 4: ผู้ช่วย AI วิเคราะห์ความสัมพันธ์ ---
elif menu == "🤖 ผู้ช่วย AI วิเคราะห์ความสัมพันธ์":
    st.markdown('<p class="main-header">🤖 ผู้ช่วย Gemini AI วิเคราะห์ตระกูล</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">พิมพ์สอบถามความสัมพันธ์ หรือให้ AI ช่วยสรุปเรื่องราวตระกูลของคุณ</p>', unsafe_allow_html=True)
    
    user_prompt = st.text_area("💬 พิมพ์คำถามเกี่ยวกับญาติ (เช่น: สมศักดิ์ เป็นลูกใคร และมีความเกี่ยวข้องกับใครบ้าง?):")
    
    if st.button("✨ ให้ AI วิเคราะห์", use_container_width=True):
        if user_prompt:
            with st.spinner("Gemini กำลังวิเคราะห์ข้อมูลสายเลือด..."):
                st.info(f"จำลองคำตอบจาก Gemini AI สำหรับคำถาม: '{user_prompt}'")
                st.write("""
                จากการวิเคราะห์ฐานข้อมูลตระกูลปัจจุบัน:
                - ระบบได้ดึงข้อมูลสมาชิกที่คงเหลืออยู่ในฐานข้อมูลมาประมวลผลร่วมกับ Gemini เรียบร้อย
                *(สามารถเชื่อมต่อ Supabase และส่งโครงสร้าง JSON ทั้งหมดให้ Gemini API อ่านเพื่อตอบคำถามเชิงลึกได้ทันทีครับ)*
                """)
        else:
            st.warning("กรุณาพิมพ์คำถามก่อนกดวิเคราะห์")

# --- หน้าที่ 5: ตั้งค่าระบบ Supabase ---
elif menu == "⚙️ ตั้งค่าระบบ Supabase":
    st.markdown('<p class="main-header">⚙️ เชื่อมต่อฐานข้อมูล Supabase</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">ตั้งค่าการเชื่อมต่อ Backend เพื่อเก็บบันทึกข้อมูลอย่างถาวร</p>', unsafe_allow_html=True)
    
    with st.form("supabase_config"):
        supabase_url = st.text_input("Supabase Project URL", type="default", placeholder="https://xxxx.supabase.co")
        supabase_key = st.text_input("Supabase Anon / Service Key", type="password", placeholder="eyJhbGciOi...")
        
        save_config = st.form_submit_button("🔗 บันทึกการเชื่อมต่อ")
        if save_config:
            st.success("บันทึกการตั้งค่าสำเร็จ! (สามารถนำค่าเหล่านี้ไปใช้เชื่อมต่อกับไลบรารี `supabase-py` ได้ทันที)")
