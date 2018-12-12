from influxdb import InfluxDBClient

class EnergyConnection:
    ENERGY_DB_HOST = 'localhost'
    ENERGY_DB_PORT = '8086'
    
    ENERGY_DB_USER = 'root'
    ENERGY_DB_PASSWORD = 'root'
    
    ENERGY_DB_ENERGY_MEASURE = 'energydb'


    client = InfluxDBClient(
        ENERGY_DB_HOST, 
        ENERGY_DB_PORT, 
        ENERGY_DB_USER, 
        ENERGY_DB_PASSWORD, 
        ENERGY_DB_ENERGY_MEASURE
        )
    
    def print_energy_readings(self):
        result = self.client.query('select * from energy_readings;')

        print("Result: {0}".format(result))
