# ============================================
# FILE: student_grade_manager.py
# ============================================
# MAIN APPLICATION - Demonstrates all exam topics

import streamlit as st
import numpy as np
import pandas as pd
from grade_utils import calculate_grade, check_pass_fail, generate_summary
import json_utils

# Page configuration
st.set_page_config(page_title="Student Grade Manager", layout="wide")
st.title("📚 Student Grade Management System")
st.markdown("---")

# ============================================
# 1. INITIALIZE SESSION STATE (Simpan multiple data tanpa overwrite)
# ============================================
if 'students' not in st.session_state:
    st.session_state.students = []  # List for multiple records

if 'next_id' not in st.session_state:
    st.session_state.next_id = 1

# ============================================
# 2. FUNCTION DEFINITION (Define & Call function)
# ============================================
def calculate_average(scores):
    """Calculate average using NumPy"""
    arr = np.array(scores)  # NumPy array
    return np.mean(arr)  # np.mean()

def get_highest_score(scores):
    """Get highest score using NumPy"""
    arr = np.array(scores)
    return np.max(arr)  # np.max()

def display_student_card(student):
    """Display student information using dictionary"""
    st.write(f"**ID:** {student['id']}")
    st.write(f"**Name:** {student['name']}")
    st.write(f"**Math:** {student['math']}")
    st.write(f"**Science:** {student['science']}")
    st.write(f"**English:** {student['english']}")
    st.write(f"**Average:** {student['avg']:.2f}")
    status = "✅ PASS" if student['status'] == 'Pass' else "❌ FAIL"
    st.write(f"**Status:** {status}")

# ============================================
# 3. SIDEBAR - INPUT FORM
# ============================================
with st.sidebar:
    st.header("➕ Add New Student")
    
    # st.text_input() example
    name = st.text_input("Student Name", placeholder="Enter full name")
    
    # st.number_input() examples
    math_score = st.number_input("Math Score", min_value=0, max_value=100, value=70)
    science_score = st.number_input("Science Score", min_value=0, max_value=100, value=70)
    english_score = st.number_input("English Score", min_value=0, max_value=100, value=70)
    
    # st.radio() example
    grade_level = st.radio("Grade Level", ["Grade 10", "Grade 11", "Grade 12"])
    
    # Exception Handling (try-except + validate input kosong)
    def add_student():
        try:
            # Validate empty input
            if not name.strip():
                st.error("❌ Name cannot be empty! Please enter student name.")
                return
            
            # Create list of scores
            scores = [math_score, science_score, english_score]
            
            # Calculate average using function call
            avg = calculate_average(scores)
            
            # Get highest score
            highest = get_highest_score(scores)
            
            # Check pass/fail condition (if else)
            status = check_pass_fail(avg)
            
            # Calculate grade using function from module
            letter_grade = calculate_grade(avg)
            
            # Create dictionary (Simpan data dalam dictionary)
            student = {
                'id': st.session_state.next_id,
                'name': name,
                'math': math_score,
                'science': science_score,
                'english': english_score,
                'avg': avg,
                'highest': highest,
                'status': status,
                'grade': letter_grade,
                'level': grade_level
            }
            
            # Add to list (Simpan multiple records dalam list)
            st.session_state.students.append(student)
            st.session_state.next_id += 1
            
            # Save to JSON using module
            json_utils.save_to_json(st.session_state.students)
            
            st.success(f"✅ Student {name} added successfully!")
            st.balloons()
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    # st.button() example
    if st.button("➕ Add Student", type="primary"):
        add_student()

# ============================================
# 4. MAIN CONTENT - TABS
# ============================================
tab1, tab2, tab3, tab4 = st.tabs(["📋 Student List", "📊 Analytics", "📈 Graph", "💾 Data Management"])

# ============================================
# TAB 1: STUDENT LIST
# ============================================
with tab1:
    if len(st.session_state.students) > 0:
        # Create DataFrame using Pandas
        df = pd.DataFrame(st.session_state.students)
        
        # Add column (Pass/Fail as numeric for sorting)
        df['Pass Numeric'] = df['status'].apply(lambda x: 1 if x == 'Pass' else 0)
        
        # Display DataFrame
        st.subheader("📋 All Student Records")
        st.dataframe(df[['id', 'name', 'math', 'science', 'english', 'avg', 'grade', 'status', 'level']], 
                     use_container_width=True)
        
        # Sorting data (ascending/descending by average)
        st.subheader("🔄 Sort Students")
        sort_order = st.radio("Sort by Average:", ["Highest to Lowest", "Lowest to Highest"])
        
        if sort_order == "Highest to Lowest":
            sorted_df = df.sort_values('avg', ascending=False)  # ascending order = False
        else:
            sorted_df = df.sort_values('avg', ascending=True)   # ascending order = True
        
        st.dataframe(sorted_df[['name', 'avg', 'grade', 'status']], use_container_width=True)
        
        # Display individual student cards
        st.subheader("👨‍🎓 Individual Student Cards")
        for student in st.session_state.students:
            with st.expander(f"Student: {student['name']} (ID: {student['id']})"):
                display_student_card(student)
    else:
        st.info("ℹ️ No students added yet. Use the sidebar to add students.")

# ============================================
# TAB 2: ANALYTICS
# ============================================
with tab2:
    if len(st.session_state.students) > 0:
        df = pd.DataFrame(st.session_state.students)
        
        st.subheader("📊 Class Analytics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_class_score = np.mean(df['avg'])
            st.metric("📈 Class Average", f"{avg_class_score:.2f}")
        
        with col2:
            total_students = len(df)
            st.metric("👥 Total Students", total_students)
        
        with col3:
            pass_count = len(df[df['status'] == 'Pass'])
            pass_rate = (pass_count / total_students) * 100
            st.metric("✅ Pass Rate", f"{pass_rate:.1f}%")
        
        # Generate summary using module function
        summary = generate_summary(df)
        st.markdown("---")
        st.subheader("📝 Class Summary")
        st.write(summary)
        
    else:
        st.info("ℹ️ No data to display. Add students first.")

# ============================================
# TAB 3: GRAPH
# ============================================
with tab3:
    if len(st.session_state.students) > 0:
        df = pd.DataFrame(st.session_state.students)
        
        st.subheader("📊 Student Performance Graph")
        
        # Display basic graph/chart dalam Streamlit
        chart_data = df.set_index('name')[['math', 'science', 'english']]
        st.bar_chart(chart_data)
        
        # Line chart for averages
        st.subheader("📈 Average Score Trend")
        avg_data = df.set_index('name')['avg']
        st.line_chart(avg_data)
        
        # Pass/Fail pie chart data
        st.subheader("🥧 Pass/Fail Distribution")
        pass_fail_counts = df['status'].value_counts()
        st.write("**Pass:**", pass_fail_counts.get('Pass', 0), "students")
        st.write("**Fail:**", pass_fail_counts.get('Fail', 0), "students")
        
        # Display pass/fail proportion using progress bar
        pass_pct = (pass_fail_counts.get('Pass', 0) / len(df)) * 100
        st.progress(int(pass_pct))
        st.caption(f"Pass Rate: {pass_pct:.1f}%")
        
    else:
        st.info("ℹ️ Add students to see graphs.")

# ============================================
# TAB 4: DATA MANAGEMENT
# ============================================
with tab4:
    st.subheader("💾 Save & Load Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 Save to JSON"):
            json_utils.save_to_json(st.session_state.students)
            st.success("Data saved to students.json!")
    
    with col2:
        if st.button("📂 Load from JSON"):
            loaded_data = json_utils.load_from_json()
            if loaded_data:
                st.session_state.students = loaded_data
                if loaded_data:
                    st.session_state.next_id = max(s['id'] for s in loaded_data) + 1
                st.success(f"Loaded {len(loaded_data)} students!")
                st.rerun()
    
    st.markdown("---")
    
    if st.button("🗑️ Clear All Data", type="secondary"):
        st.session_state.students = []
        st.session_state.next_id = 1
        json_utils.save_to_json([])
        st.warning("All data cleared!")
        st.rerun()
    
    st.markdown("---")
    st.caption("💡 **Tip:** Data is automatically saved when adding students.")

# ============================================
# FOOTER - Output formatting example
# ============================================
st.markdown("---")
st.caption("📌 Student Grade Management System | Built with Streamlit")