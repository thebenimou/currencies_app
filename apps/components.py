import dash_bootstrap_components as dbc
import dash_html_components as html


class ModernCard(dbc.Card):
    def __init__(self,  myTitle=None, *args, **kwargs):
        super(ModernCard, self).__init__(*args, **kwargs)
        self.className = "shadow"
        if "style" not in self.__dict__:
            self.style = {}
        # je rajoute un style (le user peut toujours en spécifier)
        self.style['border'] = "none"
        if type(self.children) != type([]):
            self.children = [self.children]
        if myTitle is not None:
            self.children = [
                html.H4(myTitle, className="card-title")]+self.children
