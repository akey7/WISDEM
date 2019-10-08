# incomplete_input_dict['cable_specs_pd'] = pd.read_excel(input_xlsx, 'cable_specs')
            # incomplete_input_dict['crew'] = incomplete_input_dict['project_data']['crew']
            # incomplete_input_dict['crew_cost'] = incomplete_input_dict['project_data']['crew_price']

            # #read in RSMeans per diem:
            # crew_cost = incomplete_input_dict['project_data']['crew_price']
            # crew_cost = crew_cost.set_index("Labor type ID", drop=False)
            # incomplete_input_dict['rsmeans_per_diem'] = crew_cost.loc['RSMeans', 'Per diem USD per day']
            # incomplete_input_dict['cable_specs_pd'] = pd.read_excel(input_xlsx, 'cable_specs')

            # #Read development tab:
            # incomplete_input_dict['development_df'] = pd.read_excel(input_xlsx, 'development')

            # Set the list and dictionary values on the master dictionary
            # self.default_input_dict['season_construct'] = ['spring', 'summer', 'fall']
            # self.default_input_dict['time_construct'] = 'normal'
            # self.default_input_dict['hour_day'] = {'long': 24, 'normal': 10}
            # self.default_input_dict['operational_construction_time'] = self.default_input_dict['hour_day'][
            #     self.default_input_dict['time_construct']]