# # are there any better viz? or having stacked bar chart only throughout okay, because it makes sense? 
# import streamlit as st
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# import plotly.express as px
# import plotly.graph_objects as go
from plotly.subplots import make_subplots
# import re
# st.set_page_config(page_title="9-Pointer Habits Dashboard", layout="wide")

# st.title("Habits of 9-Pointers Survey Analysis")

# # Embedded header tab with clickable link
# st.markdown(
#     """
#     <div style="background-color:#f0f2f6; padding:10px; border-radius:5px; margin-bottom:20px;">
#         👉 Want to participate?  
#         <a href="https://forms.gle/LAEiF3QdYnnq9cUy9" target="_blank" style="color:#873260; font-weight:bold;;">
#             Fill the survey here
#         </a>
#     </div>
#     """,
#     unsafe_allow_html=True
# )
# with st.expander("Disclaimer"):
#     st.markdown("""
# - This data was collected through a survey reflecting participants’ habits and opinions only.

# - The results do not imply causation or suggest that any particular habit guarantees academic success.

# - No assumptions or judgments should be made about individuals based on these responses.

# - Interpret the findings with an open mind and within the context of the surveyed group.
# """)

# with st.expander("Insights of of Data"):
#     st.markdown("""
#                 **Based on data till 13th September, 25**: Data might have updates. 
# -   **Major differences**
                
#                 - DA: 9 pointers do their DA much before the deadline and non 9 keep it for last minute. 
#                 - The lower attendance among 9-pointers suggests that they prioritize self-directed learning and efficient use of their time over simply being present in class. 
#                 - non-9-pointers are more inclined to use a single notebook for all subjects(84%), 9 pointers make 


# """)


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
      "10. What's the perfect seat for you?":"seating_arrangement",
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
    df = df.loc[(df['competitions']>0) & (df['cgpa']<=10)].copy()

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
    
    ffcs_dict = {"I check profs, slots and have backup timetables. [Pro ffcs-er]":"Pro ffcs-er",
       "I choose slots on the day of FFCS and hope they don't clash [Almost no prep]":"Almost no prep",
       "I have a timetable and tested for no clash [Good Prep]":"Good Prep",
       "I know good teachers and slots, but I don't check using tools like ffcsonthego [Medium prep]":"Medium prep"}
    df['ffcs'] = df['ffcs'].replace(ffcs_dict)

    seating_arrangement_dict = {
    'First/second bench': 'First/second bench',
    "If there is something beyond last bench, I'd choose that.": 'last bencher',
    'Somewhere in the middle': 'Somewhere in the middle',
    'No preference.': 'No preference.',
    'Not Answered': 'Not Answered'
}
    df['seating_arrangement'] = df['seating_arrangement'].replace(seating_arrangement_dict)

    study_location_dict = {
    'Room': 'Room',
    'Library': 'Library',
    "Friend's room [or library with friends]": "Friend's room (or library with friends)",
    'Not Answered': 'Not Answered'
}
    df['study_location'] = df['study_location'].replace(study_location_dict)

    clubs_chapters_dict = {
    'Yes, I just want OD': 'Only for OD',
    'Yes, but I compensate for my academics somehow.': 'Yes, compensate academics',
    'Yes, I want to gain experience.': 'Yes, for experience',
    'No': 'No',
    'Not Answered': 'Not Answered'
}
    df['clubs_chapters'] = df['clubs_chapters'].replace(clubs_chapters_dict)

    categories_dict = {
    '8+ hours | Exercise regularly': 'Very Healthy',
    '6-8 hours | Exercise a few times a week': 'Healthy',
    '4-6 hours | Occasionally exercise': 'Moderately Healthy',
    '8+ hours | Rarely exercise': 'Unhealthy (Over-sleep)',
    '<4 hours | Rarely exercise': 'Unhealthy (Sleep deprived)',
    'Not Answered': 'Not Answered'
}
    df['lifestyle'] = df['lifestyle'].replace(categories_dict)


    return df

# def plot_item_vs_cgpa(df, column, barmode="group", normalize=True, sort9=True):
#     # Group and count
#     df_temp = df.groupby(column)["cgpa_bool"].value_counts().reset_index(name="count")

#     # Percentages within each category
#     df_temp["percentages"] = df_temp.groupby(column)["count"].transform(lambda x: x/x.sum()*100)

#     # Decide which y to plot
#     y_col = "percentages" if normalize else "count"

#     # Sorting by % of 9-pointers
#     if sort9 and "9-pointer" in df["cgpa_bool"].unique():
#         order = (
#             df_temp[df_temp["cgpa_bool"]=="9-pointer"]
#             .sort_values("percentages", ascending=False)[column]
#         )
#     else:
#         order = df_temp[column].unique()

#     # Plot
#     fig = px.bar(
#         df_temp,
#         x=column, y=y_col, color="cgpa_bool",
#         text_auto=".1f",
#         barmode=barmode,
#         hover_data={"count": True, "percentages":":.1f %"},
#         color_discrete_map={
#             "9-pointer": "#873260",
#             "Non-9-pointer": "#DAA520",
#         },
#         category_orders={column: order, "cgpa_bool": ["9-pointer", "Non-9-pointer"]}
#     )

#     fig.update_layout(
#         legend_title_text="CGPA Category",
#         xaxis_title=column.replace("_", " ").title(),
#         yaxis_title="Percentage" if normalize else "Count"
#     )

#     return fig


# @st.cache_data
# def load_data():
    
#     df = pd.read_excel("Data.xlsx")
#     df = df_cleaning(df)
#     return df

# df = load_data()


# sections = {
#     "Intro of Data": ["Branch", "year", "spl"],
#     "Academics": ["da", "backlogs", "exam_prep", "study_material"],
#     "Class Habits": ["class_notes", "attendance", "ffcs", "seating_arrangement", "study_location"],
#     "Extra-curricular": ["clubs_chapters", "competitions"],
#     "Social": ["bond_teachers", "disciplinary_action", "social_life", "lifestyle", "room_type"],
# }



# st.sidebar.header("📂 Choose Section")
# selected_section = st.sidebar.radio("Select a category:", list(sections.keys()))

# st.header(f"📊 {selected_section}")

# for col in sections[selected_section]:
#     st.subheader(col.replace("_", " ").title())
    
#     if col in ["cgpa", "attendance", "backlogs", "competitions", "room_type"]:  
#         # Numeric → Boxplot
#         fig = px.box(df, x="cgpa_bool", y=col, color="cgpa_bool",
#                      color_discrete_map={"9-pointer":"#873260","Non-9-pointer":"#DAA520"})
#     else:
#         # Categorical → Stacked bar
#         fig = plot_item_vs_cgpa(df, col, barmode="relative", normalize=True)
    
#     st.plotly_chart(fig, use_container_width=True)
import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import re

st.set_page_config(page_title="9-Pointer Habits Dashboard", layout="wide")

st.title("Habits of 9-Pointers Survey Analysis")

# ---------- Disclaimer ----------
with st.expander("Disclaimer"):
    st.markdown("""
    - This data was collected through a survey reflecting participants’ habits and opinions only.
    - The results do not imply causation or suggest that any particular habit guarantees academic success.
    - No assumptions or judgments should be made about individuals based on these responses.
    - Interpret the findings with an open mind and within the context of the surveyed group.
    """)
st.markdown(
    """
    <div style="background-color:#f0f2f6; padding:10px; border-radius:5px; margin-bottom:20px;">
        👉 Want to participate?  
        <a href="https://forms.gle/LAEiF3QdYnnq9cUy9" target="_blank" style="color:#873260; font-weight:bold;;">
            Fill the survey here
        </a>
    </div>
    """,
    unsafe_allow_html=True
)


# ---------- Reusable plotting functions ----------
def plot_item_vs_cgpa(df, column, barmode="relative", normalize=True, sort9=True):
    df_temp = df.groupby(column)["cgpa_bool"].value_counts().reset_index(name="count")
    df_temp["percentages"] = df_temp.groupby(column)["count"].transform(lambda x: x/x.sum()*100)
    y_col = "percentages" if normalize else "count"

    if sort9 and "9-pointer" in df["cgpa_bool"].unique():
        order = (
            df_temp[df_temp["cgpa_bool"]=="9-pointer"]
            .sort_values("percentages", ascending=False)[column]
        )
    else:
        order = df_temp[column].unique()

    fig = px.bar(
        df_temp,
        x=column, y=y_col, color="cgpa_bool",
        text_auto=".1f",
        barmode=barmode,
        hover_data={"count": True, "percentages":":.1f %"},
        color_discrete_map={"9-pointer": "#873260","Non-9-pointer": "#DAA520"},
        category_orders={column: order, "cgpa_bool": ["9-pointer", "Non-9-pointer"]}
    )
    fig.update_layout(
        legend_title_text="CGPA Category",
        xaxis_title=column.replace("_", " ").title(),
        yaxis_title="Percentage" if normalize else "Count"
    )
    return fig


def plot_pie_charts(df, column):
    figs = {}
    for cgpa_type, color in zip(["9-pointer", "Non-9-pointer"], ["#873260", "#DAA520"]):
        df_subset = df[df["cgpa_bool"] == cgpa_type][column].value_counts().reset_index()
        categories_order = df[col].dropna().unique().tolist()
        df_subset.columns = [column, "count"]
        figs[cgpa_type] = px.pie(
            df_subset, names=column, values="count", category_orders= {column:categories_order},
            color_discrete_sequence=["#326387", "#B772E1", "#E38B63", "#E3E182","#55F9DE"],
            title=f"{cgpa_type} Distribution"
        )
        figs[cgpa_type].update_layout(
            legend=dict(traceorder="normal")  # ✅ legend follows category order
        )
    return figs


# ---------- Load Data ----------
@st.cache_data
def load_data():
    df = pd.read_excel("Data.xlsx")
    df = df_cleaning(df)
    # apply cleaning here
    return df

df = load_data()


# ---------- Sections ----------
sections = {
    "Intro of Data": ["Branch", "year", "spl"],
    "Academics": ["da", "backlogs", "exam_prep", "study_material"],
    "Class Habits": ["class_notes", "attendance", "ffcs", "seating_arrangement", "study_location"],
    "Extra-curricular": ["clubs_chapters", "competitions"],
    "Social": ["bond_teachers", "disciplinary_action", "social_life", "lifestyle", "room_type"],
}

# Sidebar section selection
st.sidebar.header("📂 Choose Section")
selected_section = st.sidebar.radio("Select a category:", list(sections.keys()))

# Tabs for each column
st.subheader(f"📊 {selected_section}")
tab_list = st.tabs([col.replace("_"," ").title() for col in sections[selected_section]])

# for tab, col in zip(tab_list, sections[selected_section]):
#     with tab:
#         # tab1, tab2 = st.tabs(["Comparative", "Individual"])
#         # with tab1:
#         #     if col in ["cgpa", "attendance", "backlogs", "competitions", "room_type"]:  
#         #         # Numeric → Boxplot
#         #         fig = px.box(df, x="cgpa_bool", y=col, color="cgpa_bool",
#         #                     color_discrete_map={"9-pointer":"#873260","Non-9-pointer":"#DAA520"})
#         #     else:
#         #         # Categorical → Stacked bar
#         #         fig = plot_item_vs_cgpa(df, col, barmode="relative", normalize=True)

#         #     fig.update_layout(
#         #         width=500,   # reduce width
#         #         height=350,  # reduce height
#         #         margin=dict(l=20, r=20, t=40, b=20)
#         #     )
#         #     st.plotly_chart(fig, use_container_width=True)
#         # figs = plot_pie_charts(df, col)
#         # with tab2:
#         #     col1, col2 = st.columns(2)
#         #     with col1:
#         #         st.plotly_chart(figs["9-pointer"], use_container_width=True)
#         #     with col2:
#         #         st.plotly_chart(figs["Non-9-pointer"], use_container_width=True)
#         col1, col2 = st.columns([2,1])
#         with col1:
#             st.subheader(col.replace("_", " ").title())

#             # Main stacked/grouped bar
#             if col in ["cgpa", "attendance", "backlogs", "competitions", "room_type"]:  
#                     # Numeric → Boxplot
#                     fig = px.box(df, x="cgpa_bool", y=col, color="cgpa_bool",
#                                 color_discrete_map={"9-pointer":"#873260","Non-9-pointer":"#DAA520"})
#             else:
#                 # Categorical → Stacked bar
#                 fig = plot_item_vs_cgpa(df, col, barmode="relative", normalize=True)
#             fig_bar = fig
#             fig_bar.update_layout(
#                     width=500,   # reduce width
#                     height=350,  # reduce height
#                     margin=dict(l=20, r=20, t=40, b=20)
#                 )
#             st.plotly_chart(fig_bar, use_container_width=True)
#         with col2:
#         # Pie charts (side by side)
#             figs = plot_pie_charts(df, col)
#             sub_fig = make_subplots(rows=2, cols=1, specs=[[{"type": "domain"}],
#                                            [{"type": "domain"}]])

#             for trace in figs["9-pointer"].data:
#                 sub_fig.add_trace(trace, row=1, col=1)
#             for trace in figs["Non-9-pointer"].data:
#                 sub_fig.add_trace(trace, row=2, col=1)

#             # Shared legend (union of categories)
#             sub_fig.update_traces(showlegend=True)
#             sub_fig.update_layout(
#                 height=700,
#                 legend=dict(orientation="v"),  # put legend at bottom
#                 margin=dict(l=20, r=20, t=40, b=40)
#             )

            # st.plotly_chart(sub_fig, use_container_width=True)
            # for label, fig_pie in figs.items():
            #     fig_pie.update_layout(
            #         height=200,
            #         margin=dict(l=10, r=10, t=30, b=10),
            #         legend=dict(
            #             orientation="h",
            #             y=-0.2, x=0.5, xanchor="center",
            #             font=dict(size=9)
            #         )
            #     )
            #     st.plotly_chart(fig_pie, use_container_width=True)


for tab, col in zip(tab_list, sections[selected_section]):
    with tab:
        st.subheader(col.replace("_", " ").title())

        col1, col2 = st.columns([2,1])  # left: bar/box, right: pies

        # --- Main plot ---
        with col1:
            if col in ["cgpa", "attendance", "backlogs", "competitions", "room_type"]:  
                fig_main = px.box(
                    df, x="cgpa_bool", y=col, color="cgpa_bool",color_discrete_map={"9-pointer":"#873260","Non-9-pointer":"#DAA520"}
                )
                fig_main.update_layout(
                    height=400,
                    margin=dict(l=20, r=20, t=60, b=20),
                    legend=dict(orientation="h", y=1.35, x=0.5, xanchor="center")
                )
                st.plotly_chart(fig_main, use_container_width=True)

            else:  # categorical → bar + pies
                fig_bar = plot_item_vs_cgpa(df, col, barmode="relative", normalize=True)
                fig_bar.update_layout(
                    height=400,
                    margin=dict(l=20, r=20, t=60, b=20),
                    legend=dict(orientation="h", y=1.35, x=0.5, xanchor="center")
                )
                st.plotly_chart(fig_bar, use_container_width=True)

        if col not in ["cgpa", "attendance", "backlogs", "competitions", "room_type", "Branch"]:
            with col2:
                figs = plot_pie_charts(df, col)  
                
                sub_fig = make_subplots(rows=2, cols=1, specs=[[{"type": "domain"}],
                                                            [{"type": "domain"}]])

                for trace in figs["9-pointer"].data:
                    sub_fig.add_trace(trace, row=1, col=1)

                for trace in figs["Non-9-pointer"].data:
                    sub_fig.add_trace(trace, row=2, col=1)

                sub_fig.update_layout(
                    annotations=[
                        dict(text="9-pointer", x=0.5, y=1.1, xref="paper", yref="paper", showarrow=False, font=dict(size=12)),
                        dict(text="Non-9-pointer", x=0.5, y=.48, xref="paper", yref="paper", showarrow=False, font=dict(size=12))
                    ],
                    height=600,
                    margin=dict(l=20, r=20, t=80, b=20),
                    legend=dict(
                        orientation="h", 
                        y=1.35, x=0.5, xanchor="center",
                        font=dict(size=10)
                    )
                )


                st.plotly_chart(sub_fig, use_container_width=True)

