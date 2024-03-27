'''
    Provides the templates for the tooltips.
'''


def get_heatmap_hover_template():
    '''
        Sets the template for the hover tooltips in the heatmap.

        Contains three labels, followed by their corresponding
        value, separated by a colon : neighborhood, year and
        trees planted.

        The labels are font 'Roboto Slab' and bold. The values
        are font 'Roboto' and regular weight.
    '''
    # TODO : Define and return the hover template
    
    hover_template = (
        '<b style="font-family: Roboto Slab">Neighborhood</b> : <span style="font-family: Roboto; font-weight: normal">%{y}</span><br>' +
        '<b style="font-family: Roboto Slab">Year</b> : <span style="font-family: Roboto; font-weight: normal">%{x}</span><br>' +
        '<b style="font-family: Roboto Slab">Trees planted</b> : <span style="font-family: Roboto; font-weight: normal">%{z}</span><br>'
    )
    
    return hover_template + "<extra></extra>"

def get_linechart_hover_template():
    '''
        Sets the template for the hover tooltips in the heatmap.

        Contains two labels, followed by their corresponding
        value, separated by a colon : date and trees planted.

        The labels are font 'Roboto Slab' and bold. The values
        are font 'Roboto' and regular weight.
    '''
    # TODO : Define and return the hover template

    hover_template = (
        '<b style="font-family: Roboto Slab">Date</b> : <span style="font-family: Roboto; font-weight: normal">%{x}</span><br>' +
        '<b style="font-family: Roboto Slab">Trees</b> : <span style="font-family: Roboto; font-weight: normal">%{y}</span><br>'
    )
    
    return hover_template + "<extra></extra>"
