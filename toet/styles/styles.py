from reportlab.lib.styles import getSampleStyleSheet

all_styles = getSampleStyleSheet()


class Styles:

    @staticmethod
    def style(style='Normal', commands=[]):
        """
        Parameters:
            style: name of the desidered style

            commands: typle with style commands

            e.g. : [
                    ('fontName', 'Helvetica'),
                    ('fontSize', 12),
                    (''aligment',0')
                   ]
        """
        selected_style = getSampleStyleSheet()[style]
        for command in commands:
            attribute = command[0] 
            value = command[1]

            if isinstance(value, int):
                template_statement = 'selected_style.{}=int(str({}))'.format(attribute, value)
            elif isinstance(value, str):
                template_statement = 'selected_style.{}="{}"'.format(attribute,  value)
            elif isinstance(value, float):
                template_statement = 'selected_style.{}=float(str({}))'.format(attribute, value)

            exec(template_statement)

        return selected_style
