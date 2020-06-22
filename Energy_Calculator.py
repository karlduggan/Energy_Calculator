from datetime import date
from datetime import datetime
import os
import sys
import pickle

"""
Title: Energy Calculator
Author: Karl Duggan
Date: 10/02/2020

"""

class Calculator:
    def __init__(self):
        self.electric = None
        self.e_read_date = []
        self.e_reads = []
        self.e_consumption = []
        self.e_consumpTotal = 0
        self.e_cost_energy = []
        self.e_days_suppled = 0

        self.e_total_cost_standing = None
        self.e_total_cost_energy = None
        self.e_total_cost = None

        self.gas = None
        self.g_read_date = []
        self.g_reads = []
        self.g_consumption = []
        self.g_consumpTotal = 0
        self.g_cost_energy = []
        self.g_days_suppled = 0

        self.g_total_cost_standing = None
        self.g_total_cost_energy = None
        self.g_total_cost = None

        self.status = ' '

    def status_update(self, string):
        self.status = string

    def run(self):
        return self.menu()

    def menu(self):
        os.system('clear')

        print('------------- Energy Calculator -------------\n')
        print(' Status: '+self.status+'\n')
        print(' Please choose one of the following selections:\n')
        print(' 1 - New Project / Activate Energy \n 2 - Load Data \n 3 - Save Data \n 4 - Enter Reads \n 5 - Export Report \n 6 - Clear Memory \n 7 - Delete Previous Entry \n 8 - Exit')
         # testing read inputs 
        print('---------------------------------------------')
        print('Electric Reads Entered:', self.energy_valid('electric'),'\n', self.e_reads,'\n',self.e_read_date)
        print('Gas Reads Entered:', self.energy_valid('gas'), '\n', self.g_reads,'\n', self.g_read_date)

        menu_select = input('Enter your selection: \n')
        # Enter a new supply, gas or electric
        if menu_select == '1':
            self.activate_supply()
        # Load data from csv file
        if menu_select == '2':
            self.load_data()
        # Save current data to csv file
        if menu_select == '3':
            self.save_data()
        # Input read for either gas or electric
        if menu_select == '4':
            self.input_read()
        # Exports report out to a txt file
        if menu_select == '5':
            self.export_report()
        # Clears data to start new project
        if menu_select == '6':
            self.clear_data()
        # Deletes Previous entry
        if menu_select == '7':
            self.delete_lastEntry()
        # Close program
        if menu_select == '8':
            os.system('clear')
            sys.exit()
        else:
            self.status_update('----- Invalid: Menu Select -----')
            self.menu()

    def activate_supply(self):
        # should first check __load_data and upload data if avaliable 
        os.system('clear')

        print('\nPlease make your selection:')
        print('1 - Add Electric')
        print('2 - Add Gas')

        selection = input('\nEnter your selection: \n')
        # Add Electric
        if selection == '1':
            unit_rate = input('Enter Electric Unit Rate: \n')
            if len(unit_rate) != 0:
                standing_charge = input('Enter Electric Standing Charge: \n')
                if len(standing_charge) != 0:
                    self.electric = Electric_Energy(float(unit_rate), float(standing_charge))
                    self.status_update('--- Electric Added Successfully ---')
                    self.menu()
            
        # Add Gas
        if selection == '2':
            unit_rate = input('Enter Gas Unit Rate: \n')
            if len(unit_rate) != 0:
                standing_charge = input('Enter Gas Standing Charge: \n')
                if len(standing_charge) != 0:
                    conversion = input('Enter "metric" or "imperial": \n')
                    if len(conversion) != 0:
                        self.gas = Gas_Energy(float(unit_rate), float(standing_charge), conversion_type=conversion.lower())
                        self.status_update('--- Electric Added Successfully ---')
                        self.menu()
        else:
            self.status_update('----- Invalid: Activation -----')
            self.menu()

    def input_read(self):
        os.system('clear')
        select_energy = input('Please select E for electric or G for gas: \n')
        input_read = input('Please input the read: \n')
        input_date = input('Please input the date for read "DD,MM,YYYY" : \n')
        date = input_date.replace(',', '-')
        self._input_read(select_energy, float(input_read), date)
        self.status_update('----- Read Recorded -----')
        self.menu()
    
    def _input_read(self, energy_type, input_read, input_date):
        # Append the input data to the read list [] by choice of energy_type
        if self.enSelect(energy_type) == 'e':
            self.e_read_date.append(input_date)
            self.e_reads.append(float(input_read))
        if self.enSelect(energy_type) == 'g':
            self.g_read_date.append(input_date)
            self.g_reads.append(float(input_read))
        else:
            print('Please select E for electric or G for gas!')

    # return the total of standing charge by calculating days suppled * standing rate       
    def get_standingCharge(self, energy_type):
        if self.enSelect(energy_type) == 'e':
            self.e_total_cost_standing = self.e_days_suppled * self.electric.standing_charge
            return self.e_total_cost_standing

        if self.enSelect(energy_type) == 'g':
            self.g_total_cost_standing = self.g_days_suppled * self.gas.standing_charge
            return self.g_total_cost_standing
        else:
            self.status_update('----- Invalid: 02 -----')

    # Calculates the consumption with the unit rate
    def get_energyCost(self, energy_type):
        if self.enSelect(energy_type) == 'e':
            return self.electric.unit_rate * self.e_consumpTotal

        if self.enSelect(energy_type) == 'g':
            return self.gas.unit_rate * self.g_consumpTotal
        else:
            self.status_update('----- Invalid: 01 -----')

    # This function return the amount of energy used between currents and previous reads
    # and appends this to the consumption list. 
    def get_energyConsumption(self, energy_type):
        if self.enSelect(energy_type) == 'e':
            previous = 0.0
            for i in range(len(self.e_reads)):
                if previous != 0.0:
                    difference = float(self.e_reads[i]) - previous
                    self.e_consumption.append(difference)
                    previous = float(self.e_reads[i])
                else:
                    self.e_consumption.append(0.0)
                    previous = float(self.e_reads[i])

        if self.enSelect(energy_type) == 'g':
            previous = 0.0
            for i in range(len(self.g_reads)):
                if previous != 0.0:
                    difference = float(self.g_reads[i]) - previous
                    self.g_consumption.append(difference)
                    previous = float(self.g_reads[i])
                else:
                    self.g_consumption.append(0.0)
                    previous = float(self.g_reads[i])
        else:
            self.status_update('----- Invalid: Selection ------')

    # returns the total sum of consumption to the e/g_consumpTotal
    def calculate_consumptionSum(self, energy_type):
        if self.enSelect(energy_type) == 'e':
            self.e_consumpTotal = sum(self.e_consumption)
        if self.enSelect(energy_type) == 'g':
            self.g_consumpTotal = sum(self.g_consumption)
        else:
            self.status_update('----- Invalid -----')

    def get_daysSuppled(self, energy_type):
        if self.enSelect(energy_type) == 'e':
            self._calculate_daysSuppled(energy_type)
            return self.e_days_suppled
            
        if self.enSelect(energy_type) == 'g':
            self._calculate_daysSuppled(energy_type)
            return self.g_days_suppled

    def _calculate_daysSuppled(self, energy_type):
        dates = None
        output = None
        if self.enSelect(energy_type) == 'e':
            dates = self.e_read_date
            
        if self.enSelect(energy_type) == 'g':
            dates = self.g_read_date
           
        first_date = dates[0]
        last_date = dates[len(dates)-1]
        f_day, f_month, f_year = int(first_date[:2]), int(first_date[3:5]), int(first_date[6:10])
        l_day, l_month, l_year = int(last_date[:2]), int(last_date[3:5]), int(last_date[6:10])
        f_date = date(f_year, f_month, f_day)
        l_date = date(l_year, l_month, l_day)
        delta = l_date  - f_date
        output = delta.days

        if self.enSelect(energy_type) == 'e':
            self.e_days_suppled = output

        if self.enSelect(energy_type) == 'g':
            self.g_days_suppled = output

    # Load data method 
    def load_data(self):
        # Data to be assigned to class variables
        filename = 'energy_data.pkl'

        try: 
            with open(filename,'rb') as f:
                data_delivered = pickle.load(f)
                self.electric = pickle.load(f)
                self.gas = pickle.load(f)

                self._load_clear_data()
                self._loading_dataset(data_delivered)
        except:
            self.status_update('----- Invalid: No Data Found -----')

    def _loading_dataset(self, dataset):
        # Assign data to class variables
        self.e_reads = dataset['e_reads']
        self.e_read_date =dataset['e_read_date']
        self.g_reads = dataset['g_reads']
        self.g_read_date = dataset['g_read_date']
 
        print(dataset)
        # Update status
        self.status_update('----- Data Loaded -----')
        # Return to the main menu
        self.menu()

    # Save method
    def save_data(self):
        # Collects the data ready to be stored into a csv file
        data_collect = {'e_reads': None,
                        'e_read_date': None,
                        'g_reads': None,
                        'g_read_date': None}
        # Electric data
        data_collect['e_reads'] = self.e_reads
        data_collect['e_read_date'] = self.e_read_date
        # Gas Data
        data_collect['g_reads'] = self.g_reads
        data_collect['g_read_date'] = self.g_read_date

        elec_Data = self.electric
        gas_Data = self.gas
       
        filename = 'energy_data.pkl'
        try: 
            with open(filename,'wb') as f:
                pickle.dump(data_collect,f)
                pickle.dump(elec_Data,f)
                pickle.dump(gas_Data,f)
            self.status_update('----- Data Saved -----')
        except:
            self.status_update('----- Invalid -----')

        self.menu()

    # Will delete the last entries 
    def delete_lastEntry(self):
        os.system('clear')
        print('---- Delete Previous Entry ----')
        print('Please select one of the following:\n E - Electric \n G - Gas \n B - Both')
        select = input('Enter Here: \n')

    
        self._delete_lastEntry(select)
        self.menu()

    def _delete_lastEntry(self, select):
    
        e_entry = self.e_reads
        e_dateEntry = self.e_read_date
        g_entry = self.g_reads
        g_dateEntry = self.g_read_date

        if select.lower() == 'e':
            if e_entry != []:
                e_entry.pop()
                e_dateEntry.pop()
            self.status_update('----- Invalid -----')
        if select.lower() == 'g':
            if g_entry != []:
                g_entry.pop()
                g_dateEntry.pop()
            self.status_update('----- Invalid -----')
        if select.lower() == 'b':
            if e_entry != [] and g_entry != []:
                e_entry.pop()
                e_dateEntry.pop()
                g_entry.pop()
                g_dateEntry.pop()
            self.status_update('----- Invalid -----')
        else:
            self.status_update('----- Invalid -----')
        

    # Clear to start new project
    def clear_data(self):
        self.electric = None
        self.e_read_date = []
        self.e_reads = []
        self.e_consumption = []
        self.e_cost_energy = []
        self.e_days_suppled = 0
        self.e_total_cost_standing = None
        self.e_total_cost_energy = None
        self.e_total_cost = None
        self.gas = None
        self.g_read_date = []
        self.g_reads = []
        self.g_consumption = []
        self.g_cost_energy = []
        self.g_days_suppled = 0
        self.g_total_cost_standing = None
        self.g_total_cost_energy = None
        self.g_total_cost = None

        self.status_update('----- Data Cleared -----')
        self.menu()

    # Private clear all data for loading in new data from a dataset.
    def _load_clear_data(self):
        
        self.e_read_date = None
        self.e_reads = None
        self.e_consumption = []
        self.e_consumpTotal = 0
        self.e_cost_energy = None
        self.e_days_suppled = 0
        self.e_total_cost_standing = None
        self.e_total_cost_energy = None
        self.e_total_cost = None
        
        self.g_read_date = None
        self.g_reads = None
        self.g_consumption = []
        self.g_consumpTotal = 0
        self.g_cost_energy = None
        self.g_days_suppled = 0
        self.g_total_cost_standing = None
        self.g_total_cost_energy = None
        self.g_total_cost = None

    # Will print True or False if an energy have been activated
    def energy_valid(self, energy_type):
        if self.enSelect(energy_type) == 'e':
            if self.electric != None:
                return 'Energy Active'
            return 'Energy Deactive'

        if self.enSelect(energy_type) == 'g':
            if self.gas != None:
                return 'Energy Active'
            return 'Energy Deactive'

    # Get the total cost of energy by calculating total consumption with unit rate
    def calculate_totalEnergyCost(self, energy_type):
        if self.enSelect(energy_type) == 'e':
            self.e_total_cost_energy = self.electric.unit_rate * self.e_consumpTotal
        if self.enSelect(energy_type) == 'g':
            self.g_total_cost_energy = self.gas.unit_rate * self.g_consumpTotal


    # Get the total cost of ENERGY and STANDING CHARGE
    def get_totalCost(self, energy_type):
        if self.enSelect(energy_type) == 'e':
            self.e_total_cost = self.e_total_cost_energy + self.e_total_cost_standing
            return self.e_total_cost
        if self.enSelect(energy_type) == 'g':
            self.g_total_cost = self.g_total_cost_energy + self.g_total_cost_standing
            return self.g_total_cost

    def export_report(self):
        # This is method checks what energy is activated and assigns to the variables below
        elec_reads = None
        elec_dates = None
        elec_cost = None
        elec_standing_cost = []
        elec_consumption_total = []
        elec_total_cost = None
        
        gas_reads = None
        gas_dates = None
        gas_cost = None
        gas_standing_cost = [] 
        gas_consumption_total = []
        gas_total_cost = None
        gas_conversion = None

        # Checks if Electric is activated
        if self.electric != None:
            elec_reads = self.e_reads
            elec_dates = self.e_read_date
            self.calculate_consumptionSum('e')
            self.get_energyConsumption('e')
            elec_consumption = self.e_consumption
            elec_cost = self.get_energyCost('e')
            elec_standing_cost = self.get_standingCharge('e')
           
            # elec_total_cost
            
            ##### write function to generate a report of calculations ####
            self._export_report('Electric', elec_reads, elec_dates, elec_consumption)

        # Checks if Gas is activated
        if self.gas != None:
            gas_reads = self.g_reads
            gas_dates = self.g_read_date
            self.calculate_consumptionSum('g')
            self.get_energyConsumption('g')
            gas_consumption = self.g_consumption
            gas_cost = self.get_energyCost('g')
            gas_standing_cost = self.get_standingCharge('g')
            
            # gas_total_cost 

            ##### write function to generate a report of calculations ####
            self._export_report('Gas', gas_reads, gas_dates, gas_consumption)
        else:
            self.status_update('---- Invalid ----')

        
        self.status_update('--- Report Exported Successfully ---')
        self.menu()

    # list have to be entered into the parameters  
    def _export_report(self, energy_type, reads, dates, consumption):
        layout = ['Reads:','Dates:','Consumption:']

        # Fill the layout with the reads, dates and consumption
        for i in range(len(dates)):
        
            layout.append(reads[i])
            layout.append(dates[i])
            layout.append(consumption[i])

        with open(energy_type+'_Report.txt','w') as f:
            data = f
            # Header 
            data.write(energy_type + '\n')
            data.write('Date: ' + datetime.today().strftime('%d-%m-%y') + '\n')
            # Draw Separator
            [data.write('=') for i in range(53)] 

            for i in range(len(layout)):
                if i % 3 == 0:
                    data.write('\n'+str(layout[i]))
                else:
                    data.write(self.__report_spacing(str(layout[i-1])))
                    data.write(str(layout[i]))
                    data.write(self.__report_spacing(str(layout[i-1])))

            data.write('\n')
            data.write('\nTotal Consumption: '+ str(self._get_totalConsumption(energy_type)) + ' Units')
            data.write('\nTotal Days Suppled: '+ str(self.get_daysSuppled(energy_type)))
            data.write('\nEnergy Cost: £' + str('{0:.2f}'.format(self._get_energy_Cost(energy_type))))
            data.write('\nStanding Cost: £' + str('{0:.2f}'.format(self.get_standingCharge(energy_type))))
            data.write('\nTotal Cost: £' + str('{0:.2f}'.format(self.get_totalCost(energy_type))))
         

            self._clear_DataExport()

    # Clear data after export to stop calculation being added again if export selected again
    def _clear_DataExport(self):
      
        self.e_consumpTotal = 0
        self.e_days_suppled = 0
        self.e_consumption = []
        self.e_cost_energy = []
        self.e_total_cost_standing = None
        self.e_total_cost_energy = None
        self.e_total_cost = None

        self.g_consumpTotal = 0
        self.g_days_suppled = 0
        self.g_consumption = []
        self.g_cost_energy = []
        self.g_total_cost_standing = None
        self.g_total_cost_energy = None
        self.g_total_cost = None
  
    def _get_totalConsumption(self, energy_type):
        self.calculate_consumptionSum(energy_type)
        if self.enSelect(energy_type) == 'e':
            return self.e_consumpTotal
        if self.enSelect(energy_type) == 'g':
            return self.g_consumpTotal

    def _get_energy_Cost(self, energy_type):
        self.calculate_totalEnergyCost(energy_type)
        if self.enSelect(energy_type) == 'e':
            return self.e_total_cost_energy
        if self.enSelect(energy_type) == 'g':
            return self.g_total_cost_energy
        
    def __report_spacing(self, length_of_string):
        space = ' '
        spacing = (15 - len(length_of_string)) * space
        return spacing

    # Created enSelect to help clean up some of the code and stop repetition
    def enSelect(self, energy_type):
        e_list = ['elec','electric','e', '1']
        g_list = ['gas', 'g', '2']
        if energy_type.lower() in e_list:
            return 'e'
        if energy_type.lower() in g_list:
            return 'g'
        else:
            self.status_update('----- Invalid -----')

# Energy classes for both gas and electric
class Electric_Energy:
    def __init__(self, unit_rate, standing_charge):

        self.unit_rate = unit_rate
        self.standing_charge = standing_charge

    def get_energy_rate(self):
        return self.unit_rate

    def get_standing_rate(self):
        return self.standing_charge

class Gas_Energy:
    def __init__(self, unit_rate, standing_charge, conversion_type = None):
        self.unit_rate = unit_rate
        self.standing_charge = standing_charge
        self.conversion_type = conversion_type

    def get_energy_rate(self):
        return self.unit_rate

    def get_standing_rate(self):
        return self.standing_charge

    def get_conversion(self):
        conv_type = self.conversion_type
        if conv_type == 'imperial':
            print(conv_type)
            return self.__imperial_Conversion(self.get_energy_consumption()) * self.unit_rate
        if conv_type == 'metric':
            print(conv_type)
            return self.__metric_Conversion(self.get_energy_consumption()) * self.unit_rate

    def __imperial_Conversion(self, energy_consumed):
        multValue = energy_consumed * 2.83
        convFactor = multValue * 1.02264
        calrFactor = convFactor * 39.2
        convert = calrFactor / 3.6
        return convert

    def __metric_Conversion(self, energy_consumed):
        multValue = energy_consumed * 1.00
        convFactor = multValue * 1.02264
        calrFactor = convFactor * 39.2
        convert = calrFactor / 3.6
        return convert

if __name__ == '__main__':

    calculator_project = Calculator()
    calculator_project.run()




