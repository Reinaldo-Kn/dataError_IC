#from DUSTAI.csv generate a graph of the Temperatura column

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np



def main():
    #read DUSTAI.csv, use the column Temperatura and plot it, knowing that the column has a comma instead of a dot
    df = pd.read_csv('DUSTAI.csv', sep = ';', decimal = ',')
    df['Temperatura'].plot()
    plt.show()
    #print(df['Temperatura'])   
    
    

if __name__ == '__main__':
    main()
    