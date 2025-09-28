import streamlit as st
import pandas as pd
import mysql.connector
import hashlib
from datetime import datetime

#-----------------------------------------------------------
# ✅ Set page config at very top (first Streamlit command)
#-----------------------------------------------------------

st.set_page_config(layout="wide")
#----------------------------
# DB Connection 
#----------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="0007",
        database="client_query_db"
    )
#----------------------------
# Dataset Inserting 
#----------------------------
def insert_queries_from_csv(csv_path="C:/Users/saran/Downloads/sample_queries_250.csv"):
    if "csv_inserted" in st.session_state and st.session_state["csv_inserted"]:
        return  # already inserted

    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now()
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        email = row.get("email")
        mobile = str(row.get("mobile")) if pd.notna(row.get("mobile")) else None
        heading = row.get("query_heading")
        description = row.get("query_description")
        status = row.get("status", "Open")
        query_created_time = pd.to_datetime(row.get("query_created_time"))
        query_closed_time = pd.to_datetime(row.get("query_closed_time")) if pd.notna(row.get("query_closed_time")) else None
        cursor.execute("""SELECT id FROM queries 
            WHERE email=%s AND query_heading=%s AND query_description=%s AND query_created_time=%s
        """, (email, heading, description, query_created_time)) # Skip duplicates (ignore query_closed_time in WHERE)
        if cursor.fetchone():
            continue
        cursor.execute("""INSERT INTO queries 
            (email, mobile, query_heading, query_description, query_created_time, status, query_closed_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s)""", (email,mobile,heading,description,query_created_time,status,query_closed_time)) # Inserting query  
        conn.commit()
    cursor.close()
    conn.close()
    st.session_state["csv_inserted"] = True

#----------------------------
# Hashing Password
#----------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#----------------------------
# User Registration
#----------------------------
def register_user(username, password, email, role):
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    cursor.execute("INSERT INTO users (username, password, email, role) VALUES (%s, %s, %s, %s)",
                   (username, hashed_pw, email, role))
    conn.commit()
    cursor.close()
    conn.close()

#----------------------------
# User Authentication 
#----------------------------
def authenticate(username, password, email, role):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    hashed_pw = hash_password(password)
    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s AND email=%s AND role=%s",
        (username, hashed_pw, email, role)
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

#--------------------------------
# Insert Query (Client Side)
#--------------------------------
def insert_query(email, mobile, heading, description, image_binary=None):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now()
    cursor.execute("""
        INSERT INTO queries 
        (email, mobile, query_heading, query_description, query_created_time, status, query_closed_time, image)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (email, mobile, heading, description, now, 'Open', None, image_binary))
    conn.commit()
    cursor.close()
    conn.close()

#------------------------------------
# Query Management (Support Side) 
#------------------------------------
def get_queries(filter_status=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    if filter_status:
        cursor.execute("SELECT * FROM queries WHERE status=%s", (filter_status,))
    else:
        cursor.execute("SELECT * FROM queries")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(rows)

#----------------------------
# Qurey closing
#----------------------------
def close_query(query_id):
    con = get_connection()
    cursor = con.cursor()
    now = datetime.now()
    cursor.execute("UPDATE queries SET status='Closed', query_closed_time=%s WHERE id=%s", (now, query_id))
    con.commit()
    cursor.close()
    con.close()

#----------------------------
# styling Streamlit App
#----------------------------
def add_custom_css():
    st.markdown(
        """
        <style>
        /* ---------- Background Styling ---------- */
        .stApp {background: linear-gradient(135deg, #e0f7fa, #e1bee7, #bbdefb);background-size: 400% 400%;animation: gradientBG 15s ease infinite;}
        @keyframes gradientBG {0% {background-position: 0% 50%;}50% {background-position: 100% 50%;}100% {background-position: 0% 50%;}}
        
        /* ---------- Input Text Fields ---------- */
        .stTextInput > div > div > input,.stTextArea > div > textarea,.stSelectbox > div > div {font-size: 17px;transition: all 0.3s ease-in-out;}

        /* Hover / Focus Effect */
        .stSelectbox > div > div:hover {border-color: #0056b3;box-shadow: 0px 0px 8px #1e90ff;transform: scale(1.02);}

        /* ---------- 🔘Buttons ---------- */
        div.stButton > button {background: linear-gradient(135deg, #ffffff, #e3f2fd);border-radius: 12px;padding: 9px 15px;transition: all 0.3s ease-in-out;}

        div.stButton > button:hover {
            background: linear-gradient(135deg, rgba(230,230,250,0.6), rgba(173, 216, 230,0.45));backdrop-filter: blur(14px);-webkit-backdrop-filter: blur(14px);
            color: blue;border-color: blue ; transform: scale(1.05);box-shadow: 0px 0px 8px #1e90ff;}

         /* 🎨 Customize st.form only */
        div.stForm {background: linear-gradient(135deg, rgba(230,230,250,0.6), rgba(173, 216, 230,0.45));backdrop-filter: blur(14px);-webkit-backdrop-filter: blur(14px);
            padding: 30px;border-radius: 20px;box-shadow: 0 6px 20px rgba(0,0,0,0.08);border: 2.5px solid #90caf9;}

        /* 🔘 Button Default - transparent with red border & red text */
        div.stForm button {background:linear-gradient(135deg, #ffffff, #e3f2fd);font-weight: bold ;border-radius: 12px ;padding: 9px 15px ;transition: all 0.3s ease-in-out ;box-shadow: none ;}
        
        /* 🔘 Hover - change border & text color only */
        div.stForm button:hover {color: red ;border-color: red ;background:transparent ;transform: scale(1.05);box-shadow: 0px 0px 5px red;}
        </style>
        """,
        unsafe_allow_html=True)
    
#----------------------------
# Register UI
#----------------------------    
def show_register():
    add_custom_css()
    col1, col2, col3 = st.columns([2, 5, 2])
    with col2:
        with st.form("register_form"):   # --- Register Form ---
            st.subheader("👤 User Register")
            st.markdown("<h5>Username</h5>", unsafe_allow_html=True)
            username = st.text_input("", key="register_username", placeholder="Enter your username", label_visibility="collapsed") #Username
            st.markdown("<h5>Password</h5>", unsafe_allow_html=True)
            password = st.text_input("", type='password', key="register_password", placeholder="Enter your password", label_visibility="collapsed") #Password
            st.markdown("<h5>Email ID</h5>", unsafe_allow_html=True)
            email = st.text_input("", key="register_email", placeholder="Enter your Email", label_visibility="collapsed") #Email ID
            st.markdown("<h5>Role</h5>", unsafe_allow_html=True)
            role = st.selectbox("Role", ["- - Select Role - -", "Client", "Support"], key="register_role", index=0, label_visibility="collapsed") #Role
            submitted = st.form_submit_button("Register")
            if submitted:
                if not username or not password or not email or role == "- - Select Role - -":
                    st.error("⚠️ Please enter all details (Username, Password, Email, Role)!")
                elif '@gmail.com' not in email:
                    st.error('⚠️ Please Enter valid Email ID')
                elif len(password) < 8:
                    st.error("⚠️ Password must be at least 8 characters long")
                else:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT id, email, username FROM users WHERE email=%s OR username=%s", (email, username)) #Unique Username and Email
                    existing_user = cursor.fetchone()
                    if existing_user:
                        if existing_user[1] == email:
                            st.error("⚠️ Email already registered! Please use another email.")
                        elif existing_user[2] == username:
                            st.error("⚠️ Username already taken! Please choose another username.")
                    else:
                        register_user(username, password, email, role)
                        st.success("✅ Registered successfully!")
                        st.session_state["page"] = "login"
                        st.rerun()
                    cursor.close()
                    conn.close()
#---------------------------
#    Login UI
#---------------------------
def show_login():
    add_custom_css()
    col1, col2, col3 = st.columns([2, 5, 2])
    with col2:
        with st.form("login_form"):  # --- Login Form ---
            st.subheader("🔐 User Login")
            st.markdown("<h5>Username</h5>", unsafe_allow_html=True)
            username = st.text_input("", key="login_username", placeholder="Enter your username", label_visibility="collapsed")                 # Username
            st.markdown("<h5>Password</h5>", unsafe_allow_html=True)
            password = st.text_input("", type='password', key="login_password", placeholder="Enter your password", label_visibility="collapsed")# Password
            st.markdown("<h5>Role</h5>", unsafe_allow_html=True)
            role = st.selectbox("Role", ["- - Select Role - -", "Client", "Support"], key="login_role", index=0, label_visibility="collapsed")  # Role
            submitted = st.form_submit_button("Login")      # --- Submit Query Button ---
            if submitted:
                if not username or not password or role == "- - Select Role - -":
                    st.error("⚠️ Please enter all details (Username, Password, Role)!")
                else:  # To Fetch email from DB for this username & role
                    conn = get_connection()
                    cursor = conn.cursor(dictionary=True)
                    cursor.execute("SELECT email FROM users WHERE username=%s AND role=%s", (username, role))
                    result = cursor.fetchone()
                    cursor.close()
                    conn.close()
                    if result:
                        email_from_db = result["email"]
                        user = authenticate(username, password, email_from_db, role)
                        if user:
                            st.session_state["role"] = user["role"]
                            st.session_state["username"] = user["username"]
                            st.session_state["email"] = user["email"]
                            st.success(f"✅ Login successful! Redirecting to {user['role']} dashboard...")
                            st.session_state["page"] = "client" if user["role"] == "Client" else "support"
                            st.rerun()
                        else:
                            st.error("❌ Invalid credentials!")
                    else:
                        st.error("❌ User not found!")
#--------------------
# Client View       
#--------------------
def show_client_dashboard():
    username = st.session_state.get("username", "")
    registered_email = st.session_state.get("email", "")
    col1, col2, col3 = st.columns([4, 50, 2])
    with col2:  # Get username and email from session
        st.title("📩 Client Query Dashboard")
    col1, col2, col3 = st.columns([4, 10, 2])
    with col2:
        st.subheader("👤 Client Details") # ---------------- Client Details ----------------
        st.markdown(f"### 👋 Welcome {username}")
        st.markdown(f"##### Registered Email ✉︎ : {registered_email}")
        with st.form("client_query_form"):
            st.subheader("📝 Submit a New Query 👇 ")  # ---------------- Client Query Submission Form ----------------
            st.markdown("<h5>Email ID</h5>", unsafe_allow_html=True)
            email_input = st.text_input("",value=registered_email,key="input_email",placeholder="Enter your registered Email",label_visibility="collapsed")
            st.markdown("<h5>Mobile Number</h5>", unsafe_allow_html=True)
            mobile = st.text_input("",key="mobile",placeholder="Enter your Mobile Number",label_visibility="collapsed")
            st.markdown("<h5>Query Heading</h5>", unsafe_allow_html=True)
            heading = st.text_input("",key="query_head",placeholder="Enter your Query Heading",label_visibility="collapsed")
            st.markdown("<h5>Query Description</h5>", unsafe_allow_html=True)
            desc = st.text_area("",key="query_desc",placeholder="Enter your Query Description",label_visibility="collapsed")
            st.markdown("<h5>Upload Screenshot (optional)</h5>", unsafe_allow_html=True)
            image_file = st.file_uploader("",type=["jpg", "png"],key="Screenshot",label_visibility="collapsed")
            image_binary = image_file.read() if image_file else None
            submitted = st.form_submit_button("Submit Query")
            if submitted:
                if not email_input or not mobile or not heading or not desc:
                    st.error("⚠️ Please fill in all fields before submitting!")
                elif len(mobile) != 10 or not mobile.isdigit():
                    st.error("⚠️ Please enter a valid 10-digit mobile number")
                elif email_input.strip().lower() != registered_email.strip().lower():
                    st.error("⚠️ The email you entered does not match your registered email!")
                else:
                    insert_query(email_input.strip().lower(), mobile, heading, desc, image_binary)
                    st.success("✅ Query submitted successfully!")
                    st.session_state.clear()
                    for key in ["mobile", "query_head", "query_desc", "input_email", "Screenshot"]:  
                        if key in st.session_state:
                            del st.session_state[key]
    col1, col2, col3 = st.columns([4, 50, 2])
    with col2:
        st.subheader("📂 Your Submitted Queries") # ---------------- Client’s Queries Table ----------------
        df = get_queries()   # fetch all queries
        if not df.empty:
            client_queries = df[df["email"].str.lower() == registered_email.lower()]
            if not client_queries.empty:
                client_queries_display = (client_queries.drop(columns=["image"])
                if "image" in client_queries.columns else client_queries)
                st.dataframe(client_queries_display, use_container_width=True, hide_index=True)
            else:
                st.info("📭 You have not submitted any queries yet.")

        if st.button("Logout"):  # --- Logout Button (outside form) ---
            st.session_state.clear()
            st.session_state["page"] = "login"
            st.rerun()

#--------------------
# Support Team View       
#--------------------
def show_support_dashboard():
    col1, col2, col3 = st.columns([4, 50, 2])
    with col2:
        st.title("👨‍💻 Support Team Dashboard")
        username = st.session_state.get("username", "")
        st.markdown(f"## 👋 Welcome {username}")
    df = get_queries()
    st.subheader("📊 System Metrics") # --- Metrics ---
    total_queries = len(df)
    open_queries_count = len(df[df["status"] == "Open"]) if not df.empty else 0
    closed_queries_count = len(df[df["status"] == "Closed"]) if not df.empty else 0

    col_metric1, col_metric2, col_metric3 = st.columns(3)
    col_metric1.metric("📌 Total Queries", total_queries)
    col_metric2.metric("🔴 Open Queries", open_queries_count)
    col_metric3.metric("🟢 Closed Queries", closed_queries_count)

    st.subheader("📂 Manage Queries") # --- Manage Queries ---
    filter_status = st.radio("🔍︎ Filter by Status", ["All", "Open", "Closed"],key="support_filter", index=0, horizontal=True)
    status = None if filter_status == "All" else filter_status # Filter queries
    df = get_queries(filter_status=status)

    if not df.empty:
        df_display = df.drop(columns=["image"]) if "image" in df.columns else df
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        open_queries = df[df["status"] == "Open"]
        if not open_queries.empty:
            query_options = ["- -  Select a Query - -"] + open_queries["id"].tolist() # --- Add default placeholder Select a Query ---
            query_to_close = st.selectbox("Select Query to View / Close",query_options,key="selected_query")

            if query_to_close != "- -  Select a Query - -": # Only show form if a real query is selected
                query_details = open_queries[open_queries["id"] == query_to_close].iloc[0]
                with st.form("close_query_form"):     # --- Client Query Detalis Form ---
                    st.markdown(f"**Query Heading:** {query_details['query_heading']}")
                    st.markdown(f"**Description:** {query_details['query_description']}")
                    st.markdown(f"**Status:** {query_details['status']}")
                    st.markdown(f"**Submitted By:** {query_details['email']}")

                    if query_details["image"] is not None: # Show image if attached
                        st.image(query_details["image"], caption="📷 Attached Screenshot", width=500)
                    else:
                        st.info("📭 No image attached for this query")
                    close_btn = st.form_submit_button("🚀Update Query")  # Close query button
                    if close_btn:
                        close_query(query_to_close)
                        st.success(f"✅ Query {query_to_close} closed successfully!")
                        st.rerun()
        else:
            st.info("No open queries found")

    if st.button("Logout"): # --- Logout Button (outside form) ---
        st.session_state.clear()
        st.session_state["page"] = "login"
        st.rerun()

#--------------------
# Main App      
#--------------------
def main():
    add_custom_css()
    st.title("💼Client Query Management System")
    if "page" not in st.session_state:
        st.session_state["page"] = "login"  # default page
    if "role" not in st.session_state:
        st.session_state["role"] = None
    if "username" not in st.session_state:
        st.session_state["username"] = None

    page = st.session_state["page"]
    
    if page in ["client", "support"]:
        insert_queries_from_csv()

    if page == "register": 
        show_register()
        col1, col2, col3 = st.columns([2, 5, 2])
        with col2:
            if st.button("Login"):
                st.session_state["page"] = "login" # Switch to Login Page
                st.rerun()
    elif page == "login":
        show_login()
        col1, col2, col3 = st.columns([2, 5, 2])
        with col2:
            if st.button("Register"):
                st.session_state["page"] = "register" # Switch to LoginRegister Page
                st.rerun()
    elif st.session_state["page"] == "client":
        show_client_dashboard()
    elif st.session_state["page"] == "support":
        show_support_dashboard()

if __name__ == "__main__":
     main()