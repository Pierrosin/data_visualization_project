'''
    Contains some functions related to the creation of the heatmap.
'''
import plotly.express as px
import hover_template


def get_figure(data):
    '''
        Generates the heatmap from the given dataset.

        Make sure to set the title of the color bar to 'Trees'
        and to display each year as an x-tick. The x and y axes should
        be titled "Year" and "Neighborhood". 

        Args:
            data: The data to display
        Returns:
            The figure to be displayed.
    '''

    # TODO : Create the heatmap. Make sure to set dragmode=False in
    # the layout. Also don't forget to include the hover template.
 
    fig = px.imshow(data, x=data.columns, y=data.index)

    # Update layout
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Neighborhood',
        coloraxis_colorbar_title='Trees',
        xaxis=dict(tickmode='linear', tickvals=list(range(len(data.columns))), ticktext=data.columns),
        yaxis=dict(autorange='reversed'),
        dragmode=False
    )

    # Add hover template
    heatmap_hover_template = hover_template.get_heatmap_hover_template()
    fig.update_traces(hovertemplate=heatmap_hover_template)
    
    return fig
