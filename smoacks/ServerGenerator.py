# ServerGenerator.py - Creates an object implementing a Connexion API
import os
from jinja2 import Environment, Template, FileSystemLoader
from smoacks.sconfig import sconfig

class ServerGenerator:
    def __init__(self, app_objects):
        self._app_objects = app_objects

    def get_import(self, app_object):
        return "from dm.{} import {}".format(app_object.name, app_object.name)

    def getJinjaDict(self):
        # Establish constant values and the overall dictionary structure
        result = {
            'dmImports': [],
            'objects': [],
            'clis': [],
            'gensubdir': sconfig['structure']['gensubdir']
        }
        # Loop through the properties and update the structure where needed
        set_first_table = False
        for objName in self._app_objects:
            result['dmImports'].append(self.get_import(self._app_objects[objName]))
            if not set_first_table:
                set_first_table = True
                result['first_table_name'] = objName
            result['clis'].append(
                "'" + sconfig['env_defaults']['smoacks_app_cli_prefix'] + \
                '_add_{}'.format(self._app_objects[objName].getSnakeName()) + \
                '={}.cli.add_{}'.format(sconfig['env_defaults']['smoacks_app_name'],
                                        self._app_objects[objName].getSnakeName()) + "'"
            )
            result['objects'].append({
                'name': objName,
                'snake_name': self._app_objects[objName].getSnakeName() + 's',
                'table_name': objName
            })
        result.update(sconfig['env_defaults'])
        return result

    def render(self):
        env = Environment(
            loader = FileSystemLoader('templates')
        )
        my_dict = self.getJinjaDict()
        template = env.get_template('DataModel.jinja')
        filedir = os.path.join(sconfig['structure']['root'], sconfig['structure']['datamodeldir'])
        tmf_file_name = os.path.join(filedir, '__init__.py') 
        if not os.path.isfile(tmf_file_name):
            tmf_file = open(tmf_file_name, "w")
            tmf_file.close()
        outfile = open(os.path.join(filedir, 'DataModel.py'), "w")
        outfile.write(template.render(my_dict))
        outfile.close()
        template2 = env.get_template('login.jinja')
        filedir2 = os.path.join(sconfig['structure']['root'], sconfig['structure']['apiobjectdir'])
        outfile2 = open(os.path.join(filedir2, 'login.py'), "w")
        outfile2.write(template2.render(my_dict))
        outfile2.close()
        template3 = env.get_template('test-login-api.jinja')
        filedir3 = os.path.join(sconfig['structure']['root'], sconfig['structure']['testdir'])
        outfile3 = open(os.path.join(filedir3, 'test-login-api.py'), "w")
        outfile3.write(template3.render(my_dict))
        outfile3.close()
        template4 = env.get_template('setup.jinja')
        filedir4 = sconfig['structure']['root']
        outfile4 = open(os.path.join(filedir4, 'setup.py'), 'w')
        outfile4.write(template4.render(my_dict))
        outfile4.close()
