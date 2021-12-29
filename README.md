# reportingslroo

This project is an evolution of the project started in the repository https://github.com/reinaqu/reportingslr. The Python scripts have been totally redesign to be object oriented


## Structure of the project folders

* **/src**: It contains the different Python modules of the project.
    * **Authors.py**: Module that contains a class that represents a list of authors.
    * **Dashboard.py**: Module that contains a class that represents a dashboard with the operations related to publications graphics. Only holds operations related to the publication.
    * **DashboardDataExtraction.py**: Module that contains a class that represents a dashboard with the operations related to graphics on extracted data. Only holds operations related to extracted data.
    * **DashboardLatex.py**: Module that contains a class that represents a dashboard with the operations related to latex generation. 
    * **DataExtraction.py**: Module that contains a class that represents a list of studies and the data extracted from those studies.
    * **Publications.py**: Module that contains a class that represents a list of studies and the data related to the publication itself of the studies.
    * **PublicationsQuality.py**: Module that contains a class that represents a list of studies and the data extracted from those studies.
    * **Venues.py**: Module that contains a class that represents a list of venues.
    * **common.py**: Module that contains a set of utility functions that are common to the rest of modules.
    * **configurations.py**: Module that contains a set of configurations needed to deal with the Excel datasheet management.
    * **dataframes.py**: Module with utility functions to deal with panda dataframes.
    * **
    
* **/data**: Contiene el dataset o datasets del proyecto
    * **poverty_data.csv**: Archivo con los datos de pobreza que van a ser explotados.