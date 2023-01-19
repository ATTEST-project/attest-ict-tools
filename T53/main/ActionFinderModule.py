from collections import defaultdict
import pandas as pd
import json
import webbrowser
import os
import jinja2
import config


class ActionFinder:
    def __init__(self, indicator_folder=None, qtable_filename=None):
        self.indicator_folder = indicator_folder
        self.indicator_filenames = [os.path.join(indicator_folder, file) for file in os.listdir(indicator_folder) if file.endswith('.csv')]

        self.indicator_data = []
        for indicator_filename in self.indicator_filenames:
            df = pd.read_csv(
                    indicator_filename
                ).rename({
                    'Economic Impact'.upper(): 'EI',
                    'Life Assessment'.upper(): 'LA',
                    'Maintenance Stratgy'.upper(): 'MS'
                }, axis=1)

            print(df.head())
            self.indicator_data.append(df)

        self.indicator_categorical = [] # Indicators with categorical values
        self.indicator_results = None # Results with actions
        self.qtable_filename = qtable_filename
        self.qtable = pd.read_excel(qtable_filename, sheet_name='Q_table final')
        self.customDataActions = None
        self.foundAction = ""
        self.html_filenames = []

    def calculateHML(self):
        """Map indicator values from numerical to categorical"""
        for i, indicator_d in enumerate(self.indicator_data):
            self.indicator_categorical.append(indicator_d.copy())
            columns = self.indicator_categorical[i].columns[1:-1]
            def func(value):
                if 1.0 >= value >= 0.75:
                    return 'H'
                elif 0.75 > value >= 0.50:
                    return 'M'
                elif 0.50 > value >= 0.00:
                    return 'L'
                else:
                    raise ValueError("Data contains negative values")
            self.indicator_categorical[i].loc[:, columns] = self.indicator_categorical[i].loc[:, columns].applymap(func)

    def calculateAllPossibleAction(self):
        self.decisions = []
        for indicator_c in self.indicator_categorical:
            data_dict = {}
            columns = indicator_c.columns[1:-1]

            data2 = self.qtable.to_dict()

            if data2.get('Q_TABLE'):
                data2.pop('Q_TABLE')

            for i, x in enumerate(data2):
                if i < len(columns):
                    for i2, y in enumerate(data2[x]):
                        if i2 == 2:
                            data_dict[data2[x][y]] = list(data2[x].values())[3:]
                else:
                    for i2, y in enumerate(data2[x]):
                        if i2 == 1:
                            data_dict[data2[x][y]] = list(data2[x].values())[3:]

            df1 = pd.DataFrame(data_dict)

            json_rev_data = json.loads(df1.to_json(orient='records'))

            action = []

            for dictionary in json_rev_data:
                name_list = []
                value_list = []

                for key in dictionary:
                    if key not in indicator_c.columns[1:-1]:
                        name_list.append(key)
                        value_list.append(dictionary[key])

                max_value = max(value_list)

                action.append(name_list[value_list.index(max_value)])

            fields_to_pop = ['Add a redundant asset (backup)',
                            'Decrease its use rate. (More energy, more operations.)',
                            'Digitalization of the asset (soft sensors)',
                            'Increase its use rate. (More energy, more operations.)',
                            'Inspect current external aspect',
                            'Keep the current maintenance',
                            'Lengthen the maintenance cycle',
                            'Put in standby',
                            'Recycle (when subcomponents are in good conditions but not enough for the tasks assigned)',
                            'Relocation',
                            'Replacement',
                            'Shorten the maintenance cycle']

            for i, dictionary in enumerate(json_rev_data):
                dictionary['action'] = action[i]
                for fields in fields_to_pop:
                    dictionary.pop(fields)

            self.decisions.append(pd.DataFrame(json_rev_data))

    def findingAction(self):
        for i, indicator_filename in enumerate(self.indicator_filenames):
            columns = self.indicator_categorical[i].columns[1:-1].to_list()
            decisions = self.decisions[i].set_index(columns)
            actions = [decisions.loc[ind].array[0] for ind in self.indicator_categorical[i][columns].itertuples(index=False)]

            self.indicator_results = self.indicator_categorical[i].copy().loc[:, self.indicator_categorical[i].columns[:-1]]
            self.indicator_results.columns = list(map(str.upper, self.indicator_results.columns))

            #self.indicator_results.drop(columns[-1])
            # import ipdb
            # ipdb.set_trace()
            self.indicator_results['ACTION'] = actions
            folder_name = self.indicator_folder.split('/')[-1] if len(self.indicator_folder.split('/')) != 0 else self.indicator_folder.split('\\')[-1]
            # results_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Result', 'future_actions', folder_name)
            results_folder = config.output_dir_from_config_3 + os.path.sep
            os.makedirs(results_folder, exist_ok=True)
            print(f'Results folder (from Action): {results_folder}')

            barename = os.path.basename(os.path.splitext(indicator_filename)[0])
            results_filename = os.path.join(results_folder, barename)
            self.html_filename = results_filename + '.html'
            actions_filename = results_filename + '_actions.csv'
            self.indicator_results.to_csv(actions_filename)
            # self.indicator_results.to_html(self.html_filename, index=False)
            html_page = render_data(self.indicator_results)
            with open(self.html_filename, "w") as f:
                f.write(html_page)

            self.html_filenames.append(self.html_filename)

    def show(self):
        for html_filename in self.html_filenames:
            webbrowser.open(html_filename)

def render_data(data):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("../res/templates"),
        #autoescape=jinja2.select_autoescape(),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("template.html")
    html_page = template.render(data=data, root_folder=os.path.dirname(os.path.dirname(__file__)))
    return html_page


if __name__ == '__main__':
    indicator_filename = 'data/data.csv'
    qtable_filename = 'Q_learning_approach.xlsx'
    actionFinder = ActionFinder(indicator_filename=indicator_filename, qtable_filename=qtable_filename)
    
    actionFinder.calculateHML()
    actionFinder.calculateAllPossibleAction()
    actionFinder.findingAction()
    
    print(actionFinder.indicator_results)
    
