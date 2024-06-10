import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px
from dash.dependencies import Input, Output

# Load the data
file_path = 'results.xlsx'  # Ensure this is the correct path to your file
df = pd.read_excel(file_path)

# Initialize the Dash app
app = Dash(__name__)

# Layout of the Dashboard
app.layout = html.Div([
    html.H1("Student Performance Dashboard"),
    
    html.Div(id='highest-scorer-info'),
    
    html.H3("Select Subjects to View Pass/Fail Percentage"),
    dcc.Checklist(
        id='subject-checklist',
        options=[{'label': subject, 'value': subject} for subject in df.columns[1:7]],
        value=['Hindi', 'English', 'Science', 'Maths', 'History', 'Geograpgy'],
        labelStyle={'display': 'inline-block'}
    ),
    
    dcc.Graph(id='pass-fail-pie-chart'),
    
    html.H3("Select Students to View Pass/Fail Results"),
    dcc.Dropdown(
        id='student-dropdown',
        options=[{'label': student, 'value': student} for student in df['Student List']],
        multi=True,
        placeholder="Select Students"
    ),
    
    dcc.Graph(id='individual-pass-fail-bar'),
    
    dcc.Graph(id='individual-performance-bar')
])

# Callback to update the pass/fail pie chart based on selected subjects
@app.callback(
    Output('pass-fail-pie-chart', 'figure'),
    [Input('subject-checklist', 'value')]
)
def update_pass_fail_chart(selected_subjects):
    if not selected_subjects:
        return px.pie(title='No subject selected')
    
    df['Passed'] = df[selected_subjects].apply(lambda x: all(x >= 30), axis=1)
    pass_fail_counts = df['Passed'].value_counts().rename(index={True: 'Passed', False: 'Failed'})
    fig = px.pie(values=pass_fail_counts, names=pass_fail_counts.index, title='Pass/Fail Distribution',
                 color=pass_fail_counts.index, color_discrete_map={'Passed':'green', 'Failed':'red'})
    return fig

# Callback to update the individual pass/fail bar chart based on selected students
@app.callback(
    Output('individual-pass-fail-bar', 'figure'),
    [Input('student-dropdown', 'value'), Input('subject-checklist', 'value')]
)
def update_individual_pass_fail(selected_students, selected_subjects):
    if selected_students is None or len(selected_students) == 0:
        selected_students = df['Student List']
    filtered_df = df[df['Student List'].isin(selected_students)]
    
    # Calculate the number of subjects passed per student
    filtered_df['Subjects Passed'] = filtered_df[selected_subjects].apply(lambda x: (x >= 30).sum(), axis=1)
    filtered_df['Total Subjects'] = len(selected_subjects)
    
    fig = px.bar(filtered_df, x='Student List', y='Subjects Passed', title='Number of Subjects Passed by Students',
                 color='Subjects Passed', color_continuous_scale=['red', 'green'])
    fig.update_layout(yaxis=dict(range=[0, 6]))  # Set y-axis range to [0, 6]
    fig.update_coloraxes(cmin=0, cmax=6, colorbar_tickvals=list(range(7)))  # Set color bar limits to 0-6
    return fig

# Callback to update the individual performance bar chart based on selected students
@app.callback(
    Output('individual-performance-bar', 'figure'),
    [Input('student-dropdown', 'value'), Input('subject-checklist', 'value')]
)
def update_individual_performance(selected_students, selected_subjects):
    if selected_students is None or len(selected_students) == 0:
        selected_students = df['Student List']
    filtered_df = df[df['Student List'].isin(selected_students)]
    fig = px.bar(filtered_df, x='Student List', y=selected_subjects, title='Individual Performance by Subject')
    return fig

# Callback to display highest scorer information
@app.callback(
    Output('highest-scorer-info', 'children'),
    [Input('subject-checklist', 'value')]
)
def display_highest_scorer(selected_subjects):
    if len(selected_subjects) == len(df.columns[1:7]):
        df['Total Marks'] = df[selected_subjects].sum(axis=1)
        highest_scorer = df.loc[df['Total Marks'].idxmax()]
        highest_scorer_info = f"Highest Scorer: {highest_scorer['Student List']} with {highest_scorer['Total Marks']} marks."
        return html.Div([
            html.H2(highest_scorer_info)
        ])
    elif len(selected_subjects) == 1:
        subject = selected_subjects[0]
        highest_scorer = df.loc[df[subject].idxmax()]
        highest_scorer_info = f"Highest Scorer in {subject}: {highest_scorer['Student List']} with {highest_scorer[subject]} marks."
        return html.Div([
            html.H2(highest_scorer_info)
        ])
    else:
        return html.Div([
            html.H2("Select either all subjects or one subject to view highest scorer information.")
        ])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
# or