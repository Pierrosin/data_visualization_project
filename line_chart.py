'''
    Contains some functions related to the creation of the line chart.
'''
import plotly.express as px
import hover_template

from template import THEME


def get_empty_figure():
    '''
        Returns the figure to display when there is no data to show.

        The text to display is : 'No data to display. Select a cell
        in the heatmap for more information.

    '''

    # TODO : Construct the empty figure to display. Make sure to 
    # set dragmode=False in the layout.
    
    # Create a scatter plot with no data points
    fig = px.scatter()

    # Ajouter un annotation de texte pour afficher le message lorsque les données sont vides
    fig.add_annotation(text="No data to display. Select a cell in the heatmap for more information.",
                       xref="paper", yref="paper",
                       x=0.5, y=0.5,
                       showarrow=False,
                       align="center")
    
    # Définir la configuration de la figure pour ne pas afficher les repères, les étiquettes et les lignes
    fig.update_xaxes(showticklabels=False, showgrid=False, visible=False)
    fig.update_yaxes(showticklabels=False, showgrid=False, visible=False)
    fig.update_layout(dragmode = False)

    return fig


def add_rectangle_shape(fig):
    '''
        Adds a rectangle to the figure displayed
        behind the informational text. The color
        is the 'pale_color' in the THEME dictionary.

        The rectangle's width takes up the entire
        paper of the figure. The height goes from
        0.25% to 0.75% the height of the figure.
    '''
    # TODO : Draw the rectangle

    # Add a shape (rectangle) to the figure
    fig.add_shape(
        type="rect",
        xref="paper", yref="paper",
        x0=0,
        y0=0.25,
        x1=1,
        y1=0.75,
        fillcolor=THEME['pale_color'],
        layer="above",
        line=dict(width=0)
    )
    
    return fig


def get_figure(line_data, arrond, year):
    '''
        Generates the line chart using the given data.

        The ticks must show the zero-padded day and
        abbreviated month. The y-axis title should be 'Trees'
        and the title should indicated the displayed
        neighborhood and year.

        In the case that there is only one data point,
        the trace should be displayed as a single
        point instead of a line.

        Args:
            line_data: The data to display in the
            line chart
            arrond: The selected neighborhood
            year: The selected year
        Returns:
            The figure to be displayed
    '''
    # TODO : Construct the required figure. Don't forget to include the hover template

    # Create the line chart using Plotly Express
    fig = px.line(line_data, x='Date_Plantation', y='Daily_Counts', 
                  labels={'Daily_Counts': 'Trees'},
                  title=f'Trees planted in {arrond} in {year}',
                  hover_name='Date_Plantation', hover_data={'Daily_Counts': True})
    
    if len(line_data) == 1:
        # If only one data point, display as a single point with visible marker
        fig.update_traces(mode='markers')
    
    # Add hover template
    fig.for_each_trace(lambda t: t.update(hovertemplate=hover_template.get_linechart_hover_template()))
        
    # Format x-axis labels to show day with zeros and abbreviated month
    fig.update_xaxes(tickformat='%d %b', title=None)

    return fig
