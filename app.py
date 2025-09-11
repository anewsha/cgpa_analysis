import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import re

st.set_page_config(page_title="9-Pointer Habits Dashboard", layout="wide")

st.title("Habits of 9-Pointers Survey Analysis")
st.markdown("""
**Disclaimer:**  
- This data is collected via survey and is **not an implication of anything**.  
- Results represent only participants' responses.  
""")

st.markdown("👉 Want to participate? [Fill the survey here]https://forms.gle/LAEiF3QdYnnq9cUy9")

def df_cleaning(df):
    df.rename(columns={
    'Year?':'year',
     'Does your degree have a specialization?':"spl",
     '1. Class Notes?':"class_notes",
     '2. DA?':"da",
     '3. CGPA':"cgpa",
     '4. Number of Backlogs?':'backlogs',
     '5. Average Attendance? (%)':"attendance",
     '6. FFCS prep':"ffcs",
      '7. Exam Prep':"exam_prep",
      '8. Active member of Clubs/Chapters/Teams/Anything that involved Night-slips or ODs( events etc)?':"clubs_chapters",
      '9. Number of events participated in like Hackathons/Ideathons / Events related to my degree or career?':"competitions",
      "10. What's the perfect seat for your?":"seating_arrangement",
      '11. Bond with teachers.':"bond_teachers",
      '12. Study sources?':"study_material",
      '13. Any disciplinary action?':"disciplinary_action",
       '14. Hanging out with friends after classes?':"social_life",
       '15. Sleep and Exercise?':"lifestyle",
        '16. Study location?': "study_location",
        '17. Room type( dayscholar/ single bed/4bed/6bed etc)':"room_type"

    }, inplace=True)
    def clean_gpa(gpa):
        gpa = gpa.strip()
        s =  re.findall(r"\d| \d.\d|\d.\d\d", gpa)
        i = float((s[0] if isinstance(s,list) else s) if s else "-1")
        # i = float(.join(s).strip())
        # print(i)
        return i
    df['cgpa'] = df['cgpa'].apply(lambda x: x if (isinstance(x,float) or isinstance(x,int)) else clean_gpa(x))
    df = df.loc[(df['cgpa']>0) & (df['cgpa']<=10)].copy()
    df.drop(['Timestamp'], axis='columns', inplace=True)
    cat = [col for col in df.columns if df[col].dtype=='O']
    df[cat]= df[cat].fillna("Not Answered")
    num = [col for col in df.columns if col not in cat]
    df[num]= df[num].fillna(-1)
    df['cgpa_bool'] = df['cgpa'].apply(lambda x: "9-pointer" if x>=9 else "Non-9-pointer")
    df['attendance']=df['attendance'].apply(lambda x: f"{x*10}%")

    class_notes_dict = {
    "One notebook for all subjects. \"If I feel like it, I'll write\" [medium maintenance]": 'medium maintenance',
    'What notes? [no notes maintained]': 'no notes maintained',
    'I carry 3 colored pens to class. [Pro level notes]': 'Pro level notes',
    'I make notes that I can understand. [Well maintained]': 'Well maintained',
    'Not Answered': 'Not Answered'
}
    df['class_notes'] = df['class_notes'].replace(class_notes_dict)

    exam_prep_dict = {
    'I download the syllabus one day before. [Last minute prep]': 'Last minute prep',
    'I start anytime in the previous week of exam. [Good Prep]': 'Good Prep',
    "I've started my prep for FATs already.": "Excellent Prep",
    'Seeing the question paper is same as seeing syllabus. [Almost no prep]': 'Almost no prep',
    'Not Answered': 'Not Answered'
}
    df['exam_prep'] = df['exam_prep'].replace(exam_prep_dict)

    da_dict = {
    '5+ instances where submission was done one day before [Pro punctual]': 'Pro punctual',
    'Login: 11:55 => Submit: 11:59 [Saved in time]': 'Saved in time',
    "I panic if it's not done by 11pm. [On time]": 'On time',
    '5+ instances where submission through mail [missed deadlines]': 'missed deadlines',
    -1: 'Not Answered'
}
    df['da'] = df['da'].replace(da_dict)



    return df

def plot_item_vs_cgpa(df, column, barmode="group", normalize=True, sort9=True):
    # Group and count
    df_temp = df.groupby(column)["cgpa_bool"].value_counts().reset_index(name="count")

    # Percentages within each category
    df_temp["percentages"] = df_temp.groupby(column)["count"].transform(lambda x: x/x.sum()*100)

    # Decide which y to plot
    y_col = "percentages" if normalize else "count"

    # Sorting by % of 9-pointers
    if sort9 and "9-pointer" in df["cgpa_bool"].unique():
        order = (
            df_temp[df_temp["cgpa_bool"]=="9-pointer"]
            .sort_values("percentages", ascending=False)[column]
        )
    else:
        order = df_temp[column].unique()

    # Plot
    fig = px.bar(
        df_temp,
        x=column, y=y_col, color="cgpa_bool",
        text_auto=".1f",
        barmode=barmode,
        hover_data={"count": True, "percentages":":.1f"},
        color_discrete_map={
            "9-pointer": "#873260",
            "Non-9-pointer": "#DAA520",
        },
        category_orders={column: order, "cgpa_bool": ["9-pointer", "Non-9-pointer"]}
    )

    fig.update_layout(
        legend_title_text="CGPA Category",
        xaxis_title=column.replace("_", " ").title(),
        yaxis_title="Percentage" if normalize else "Count"
    )

    return fig


@st.cache_data
def load_data():
    
    df = pd.read_excel("Data.xlsx")
    df = df_cleaning(df)
    return df

df = load_data()


sections = {
    "Intro of Data": ["Branch", "year", "spl"],
    "Academics": ["da", "backlogs", "exam_prep", "study_material"],
    "Class Habits": ["class_notes", "attendance", "ffcs", "seating_arrangement", "study_location"],
    "Extra-curricular": ["clubs_chapters", "competitions"],
    "Social": ["bond_teachers", "disciplinary_action", "social_life", "lifestyle", "room_type"],
}



st.sidebar.header("📂 Choose Section")
selected_section = st.sidebar.radio("Select a category:", list(sections.keys()))

st.header(f"📊 {selected_section}")

for col in sections[selected_section]:
    st.subheader(col.replace("_", " ").title())
    
    if col in ["cgpa", "attendance", "backlogs", "competitions"]:  
        # Numeric → Boxplot
        fig = px.box(df, x="cgpa_bool", y=col, color="cgpa_bool",
                     color_discrete_map={"9-pointer":"#873260","Non-9-pointer":"#DAA520"})
    else:
        # Categorical → Stacked bar
        fig = plot_item_vs_cgpa(df, col, barmode="relative", normalize=True)
    
    st.plotly_chart(fig, use_container_width=True)