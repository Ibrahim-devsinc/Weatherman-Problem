import os
"""This file Solves the Weatherman Problem using Pure Python"""
class Weatherman:
    def __init__(self):
         self.weather_data = []   #Initializing a List of Dictionaries

    def file_loading(self, folder_paths):
        for folder_path in folder_paths:
            location_name = os.path.basename(folder_path)  
            files = os.listdir(folder_path)  # Get all files in the folder
            for file_name in files:
                if file_name.endswith('.txt'):
                    file_path = os.path.join(folder_path, file_name)
                    with open(file_path, 'r') as file:
                        file_dict = {}    
                        column_names = []
                        line = file.readline()
                        while True:             # Loop until the first non-empty line is found
                            if line == '\n':
                                line = file.readline()
                                continue
                            if line.strip():
                                values = line.strip().split(',')
                                column_names.extend(values)
                                column_names, timezone = self.preprocess_timezones(column_names)
                                file_dict.update({key.strip():None for key in column_names})
                            break

                        lines = file.readlines()
                        for line in lines:
                            file_dict = self.set_all_values_to_none(file_dict)
                            if '<' in line:
                                continue
                            if line.strip():  # Check if the line is not empty
                                values = line.strip().split(',')
                                for key, val in zip(file_dict.keys(), values):
                                        if val == '':
                                            val = None
                                        file_dict[key] = val
                                file_dict['Location'] = location_name
                                file_dict['Timezone'] = timezone    
                                self.weather_data.append(file_dict)


    def remove_null(self, max_none_count = 6):
        """Removes the rows that have 6 missing values"""
        filtered_list = []
        filtered_list= [data_dict for data_dict in self.weather_data
                if sum(1 for value in data_dict.values() if value is None) < max_none_count]
        self.weather_data = filtered_list       

    def set_all_values_to_none(self,data_dict):
        return {key: None for key in data_dict}
    def preprocess_data(self, keys_to_remove):
        """
        Preprocess a list of dictionaries by removing specified keys from each dictionary.
        """
        processed_data = []
        
        for data_dict in self.weather_data:
            filtered_dict = {key: data_dict[key] for key in data_dict if key not in keys_to_remove}
            processed_data.append(filtered_dict)
        
        self.weather_data = processed_data
    
    def preprocess_timezones(self, column_list):
        """Function that replaces the PKT, GST and PKST with Date and adds a column of Timezone. 
        It Returns the column_list and the specific timezone to add to the added dictionary column(Timezone)"""
        if column_list[0] == 'PKT':
            column_list[0] = 'Date'
            column_list.append('Timezone') 
            return column_list, 'PKT'    
        elif column_list[0] == 'GST':
            column_list[0] = 'Date'
            column_list.append('Timezone')
            return column_list, 'GST'
        elif column_list[0] == 'PKST':
            column_list[0] = 'Date'
            column_list.append('Timezone')
            return column_list, 'PKST'

    def impute_data(self):
        """Imputes the missing values in the data"""
        for data in self.weather_data:
            if data['Max TemperatureC'] != None and data['Min TemperatureC'] != None and data['Mean TemperatureC'] == '':
                data['Mean TemperatureC'] = (int(data['Max TemperatureC']) + int(data['Min TemperatureC'])) / 2
            if data['Max Humidity'] != None and data['Min Humidity'] != None and data['Mean Humidity'] == '':
                data['Mean Humidity'] = (int(data['Max Humidity']) + int(data['Min Humidity'])) / 2

    def get_month(self, date):
        """Function to Return the Name of the month"""
        year, month, day = date.strip().split('-')
        month_dict = {'1' : 'Jan', '2' : 'Feb', '3' : 'Mar', '4' : 'Apr', '5' : 'May', '6' : 'Jun', '7' : 'Jul', '8' : 'Aug', '9' : 'Sep', '10' : 'Oct', '11' : 'Nov', '12' : 'Dec'}
        return month_dict[month], day
    
    def generate_max_report(self):
        """For a given year and location this function display the highest temperature and day, 
        lowest temperature and day, most humid day and humidity"""
        max_temp = 0 
        low_temp = 1000
        max_humid = 0
        location = input("Enter the location for which you want to generate this report from(Dubai, lahore, Murree): ")
        year = input("Enter the Year for which you want to check the weather report: ")
        for data_dict in self.weather_data:
            if location in data_dict['Location']:
                if year in data_dict['Date']:
                        if data_dict['Max TemperatureC'] != None and data_dict['Min TemperatureC'] != None and data_dict['Mean Humidity'] != None:
                            if float(data_dict['Max TemperatureC']) > max_temp:
                                max_temp = float(data_dict['Max TemperatureC'])
                                high_temp_index = self.weather_data.index(data_dict)
                            if float(data_dict['Min TemperatureC']) < low_temp:
                                low_temp = float(data_dict['Min TemperatureC'])
                                low_temp_index = self.weather_data.index(data_dict)
                            if float(data_dict['Mean Humidity']) > max_humid:
                                max_humid = float(data_dict['Mean Humidity'])
                                max_humid_index = self.weather_data.index(data_dict)
                    
        hight_temp_month, high_temp_day = self.get_month(self.weather_data[high_temp_index]['Date'])
        low_temp_month, low_temp_day = self.get_month(self.weather_data[low_temp_index]['Date'])
        max_humid_month, max_humid_day = self.get_month(self.weather_data[max_humid_index]['Date'])
        print(f"Highest Temperature in {location} on {high_temp_day} {hight_temp_month} was {max_temp} degree C")
        print(f"Lowest Temperature in {location} on {low_temp_day} {low_temp_month} was {low_temp} degree C")
        print(f"Most Humid in {location} on {max_humid_day} {max_humid_month} was {max_humid} %")


    def generate_average_report(self):
        """For a given month display the average highest temperature, 
        average lowest temperature, average humidity."""

        location = input("Enter the location for which you want to generate this report from(Dubai, lahore, Murree): ")
        input_data = input("Enter the Year and Month Space Separated for which you want to check the weather report: ")
        year, month = input_data.split()
        max_temp_sum = 0
        low_temp_sum = 0
        humidity_sum = 0
        num_of_days = 0
        for data_dict in self.weather_data:
            if location in data_dict['Location']:
                if (year + '-' + month) in data_dict['Date']:
                    max_temp_sum += float(data_dict['Max TemperatureC'])
                    low_temp_sum += float(data_dict['Min TemperatureC'])
                    humidity_sum += float(data_dict['Mean Humidity'])
                    num_of_days += 1   #Assuming that null values of a month is not counted, hence keeping track using counter
        average_high_temp = max_temp_sum / num_of_days
        average_low_temp = low_temp_sum / num_of_days
        average_humidity = humidity_sum / num_of_days
        print(f"Average Highest Temperature in {location} on this month was {round(average_high_temp,2)} degree C")
        print(f"Average Lowest Temperature in {location} on this month was {round(average_low_temp,2)} degree C")
        print(f"Average Humidity in {location} on this month was {round(average_humidity,2)} %")
    
    def monthly_temperature_barchart(self):
        """For a given month this function draws two horizontal bar charts on the console for the 
        highest and lowest temperature on each day. Highest in red and lowest in blue"""
        location = input("Enter the location for which you want to generate this report from(Dubai, lahore, Murree): ")
        input_data = input("Enter the Year and Month Space Separated for which you want to check the weather report: ")
        year, month = input_data.split()
        date = year + '-' + month
        month_dict = {'1' : 'Jan', '2' : 'Feb', '3' : 'Mar', '4' : 'Apr', '5' : 'May', '6' : 'Jun', '7' : 'Jul', '8' : 'Aug', '9' : 'Sep', '10' : 'Oct', '11' : 'Nov', '12' : 'Dec'}
        m = month_dict[month]
        print(m ,' ', year)
        RED = '\033[91m'
        BLUE = '\033[94m'
        for data_dict in self.weather_data:
            if location in data_dict['Location']:
                if date in data_dict['Date']:
                    if data_dict['Max TemperatureC'] != None and data_dict['Min TemperatureC'] != None:
                        month, day = self.get_month(data_dict['Date'])
                        print(day, end = '')
                        max_temp = data_dict['Max TemperatureC']
                        min_temp = data_dict['Min TemperatureC']
                        for i in range(int(max_temp)):
                            print(RED + '+' , end = '')
                        print('\033[0m', end = '')    #Resetting the color
                        print(str(int(max_temp)) + 'C', end = '')
                        print('\n')
                        print(day, end = '')
                        for i in range(int(min_temp)):
                            print(BLUE + '+' , end = '')
                        print('\033[0m', end = '')    #Resetting the color
                        print(str(int(min_temp)) + 'C', end = '')
                        print('\n')

    def each_day_report(self):
        """For a given month this function draws one horizontal bar chart on the console for 
        the highest and lowest temperature on each day"""

        location = input("Enter the location for which you want to generate this report from: ")
        input_data = input("Enter the Year and Month Space Separated for which you want to check the weather report: ")
        year, month = input_data.split()
        date = year + '-' + month
        month_dict = {'1' : 'Jan', '2' : 'Feb', '3' : 'Mar', '4' : 'Apr', '5' : 'May', '6' : 'Jun', '7' : 'Jul', '8' : 'Aug', '9' : 'Sep', '10' : 'Oct', '11' : 'Nov', '12' : 'Dec'}
        m = month_dict[month]
        print(m ,' ', year)
        
        RED = '\033[91m'
        BLUE = '\033[94m'
        for data_dict in self.weather_data:
            if location in data_dict['Location']:
                if date in data_dict['Date']:
                    if data_dict['Max TemperatureC'] != None and data_dict['Min TemperatureC'] != None:
                        month, day = self.get_month(data_dict['Date'])
                        print(day, end = '')
                        max_temp = data_dict['Max TemperatureC']
                        min_temp = data_dict['Min TemperatureC']
                        for i in range(int(min_temp)):
                            print(BLUE + '-' , end = '')
                        for i in range(int(max_temp)):
                            print(RED + '+' , end = '')
                        print('\033[0m', end = '')    #Resetting the color
                        print(str(int(min_temp)) + 'C', end = '')
                        print(' - ' , end = '')
                        print(str(int(max_temp)) + 'C', end = '')
                        print('\n')
                        
    def print_data(self):
        for data in self.weather_data:
            print(data)


if __name__ == "__main__":
    folder_paths = ['Dubai_weather', 'lahore_weather', 'Murree_weather']
    weatherman = Weatherman()
    weatherman.file_loading(folder_paths)
    keys_to_remove = ['Max Sea Level PressurehPa','Mean Sea Level PressurehPa','Dew PointC','MeanDew PointC','Min DewpointC','Max Wind SpeedKm/h','Mean Wind SpeedKm/h' ,'Min Sea Level PressurehPa','Max VisibilityKm','Mean VisibilityKm','Min VisibilitykM','Max Gust SpeedKm/h','Events','WindDirDegrees','Precipitationmm', 'CloudCover', 'PrecipitationCm', 'Precipitationmm']
    weatherman.preprocess_data(keys_to_remove)
    weatherman.remove_null()
    weatherman.impute_data()
    weatherman.print_data()
    weatherman.generate_max_report()
    weatherman.generate_average_report()
    weatherman.monthly_temperature_barchart()
    weatherman.each_day_report()
