import os
import json
import sys

class FileReader:
    """
    This class reads the files in the directory and stores the file paths in a dictionary
    """
    def __init__(self, dp) -> None:
        self.directory_path = dp
        self.filedirectory = []
        self.directories = []
    def get_log_file_directories(self) -> None:
        """
        This function gets the directories in the Logoutput folder and stores them in a dictionary
        :return: None
        """
        # Specify the directory path
        sub_dirs = sorted(os.listdir(self.directory_path))
        # Iterate over the subdirectories
        for name in sub_dirs:
            if ('Graphs' != name) and ('CSVFiles' != name):
                if os.path.isdir(os.path.join(self.directory_path, name)):
                    # print('------------Adding Directory: ', os.path.join(self.directory_path, name), ' ------------')
                    self.directories.append(os.path.join(self.directory_path, name))
        
        return self.directories
    
    def get_log_file_paths(self) -> list:
        """
        This function reads the log files in the directory and stores the file paths in a dictionary
        :return: list of log file paths
        """
        file_names = os.listdir(self.directory_path)
        # Sort the file names based on modification time
        sorted_file_names = sorted(file_names, key=lambda x: os.path.getmtime(os.path.join(self.directory_path+'/'+x)))
        # Read the files in the sorted order
        for filename in sorted_file_names:
            # Construct the full file path
            file_path = os.path.join(self.directory_path+'/'+filename)
            print('------------Adding file: ', file_path, ' ------------')
            # Check if the path is a file
            if os.path.isfile(file_path):
                self.filedirectory.append(file_path)
        
        return self.filedirectory
    
    def get_csv_file_paths(self, path=None) -> list:
        """
        This function reads the CSV files in the directory and stores the file paths in a dictionary
        :return: list of CSV file paths
        """
        self.filedirectory = []
        actual_csv_file_path = self.directory_path if not path else path 
        actual_csv_file_path += '/CSVFiles'
        if os.path.isdir(actual_csv_file_path):
            file_names = os.listdir(actual_csv_file_path)

            # Sort the file names based on modification time
            sorted_file_names = sorted(file_names, key=lambda x: os.path.getmtime(os.path.join(actual_csv_file_path, x)))
            # Read the files in the sorted order
            for filename in sorted_file_names:
                # Construct the full file path
                if filename.endswith('.csv'):
                    file_path = os.path.join(actual_csv_file_path, filename)
                    # Check if the path is a file
                    if os.path.isfile(file_path):
                        self.filedirectory.append(file_path)

        return self.filedirectory

    def get_dcube_stat_csv_files(self, bv):
        """
            This function gathers all the csv files containing statisitcs for the dcube experiments
            and stores them in a dictionary with the key being the PHY layer used.
            :param bv: bit voting enabled or not
            :return: dictionary of csv files
        """

        dir_list = self.get_log_file_directories()
        phy_layer_csv_files = {'PHY_BLE_1M':[], 'PHY_BLE_2M':[], 'PHY_BLE_125K':[], 'PHY_BLE_500K':[], 'PHY_IEEE':[]}
        if bv:
            for dir in dir_list:
                dir = os.path.join(dir, 'With_BV')
                phy_dirs_list = os.listdir(dir)
                for phy_dir in phy_dirs_list:
                    csv_file_path = os.path.join(dir, phy_dir, f'statistics_{phy_dir}_bv.csv')
                    if os.path.exists(csv_file_path):
                        phy_layer_csv_files[phy_dir].append(csv_file_path)
                    
        else:
            for dir in dir_list:
                dir = os.path.join(dir, 'No_BV')
                phy_dirs_list = os.listdir(dir)
                for phy_dir in phy_dirs_list:
                    csv_file_path = os.path.join(dir, phy_dir, f'statistics_{phy_dir}_no_bv.csv')
                    if os.path.exists(csv_file_path):
                        phy_layer_csv_files[phy_dir].append(csv_file_path)
                               
        
        return phy_layer_csv_files

    def get_dcube_raw_csv_files(self, src, fwd, dst):
        
        dir_list = self.get_log_file_directories()
        phy_layer_csv_files = {'PHY_BLE_2M':[], 'PHY_BLE_1M':[], 'PHY_BLE_500K':[], 'PHY_BLE_125K':[]}
        phy_layer_csv_files_no_bv = {'PHY_BLE_2M':[], 'PHY_BLE_1M':[], 'PHY_BLE_500K':[], 'PHY_BLE_125K':[]}
        pair_dir_list = []

        for dir in dir_list:
            if src in dir and fwd in dir and dst in dir:
                print('------------Adding Directory: ', dir, ' ------------')
                pair_dir_list.append(dir)

        for dir in pair_dir_list:
            dir = os.path.join(dir, 'With_BV')
            phy_dirs_list = os.listdir(dir)
            for phy_dir in phy_dirs_list:
                files = os.listdir(os.path.join(dir, phy_dir))

                for file in files:
                    if 'logs' in file and os.path.isdir(os.path.join(dir, phy_dir, file)):
                        phy_layer_csv_files[phy_dir].append(self.get_csv_file_paths(os.path.join(dir, phy_dir, file)))

        for dir in pair_dir_list:
            dir = os.path.join(dir, 'No_BV')
            phy_dirs_list = os.listdir(dir)
            for phy_dir in phy_dirs_list:
                files = os.listdir(os.path.join(dir, phy_dir))
                for file in files:
                    if 'logs' in file and os.path.isdir(os.path.join(dir, phy_dir, file)):

                        phy_layer_csv_files_no_bv[phy_dir].append(self.get_csv_file_paths(os.path.join(dir, phy_dir, file)))
        
        return phy_layer_csv_files, phy_layer_csv_files_no_bv

    def get_dcube_csv_files_pair(self, bv, src, fwd, dst):
        """
            This function gathers all the csv files containing statisitcs for the dcube experiments
            based on specific node pairs and stores them in a dictionary with the key being the PHY layer used.
            :param bv: bit voting enabled or not
            :param src: source node id
            :param fwd: forwarder node id
            :param dst: destination node id
            :return: dictionary of csv files
        """
        dir_list = self.get_log_file_directories()
        phy_layer_csv_files = {'PHY_BLE_2M':[], 'PHY_BLE_1M':[], 'PHY_BLE_500K':[], 'PHY_BLE_125K':[]}
        pair_dir_list = []

        for dir in dir_list:
            if src in dir and fwd in dir and dst in dir:
                pair_dir_list.append(dir)

        if bv:
            for dir in pair_dir_list:
                dir = os.path.join(dir, 'With_BV')
                phy_dirs_list = os.listdir(dir)
                for phy_dir in phy_dirs_list:
                    csv_file_path = os.path.join(dir, phy_dir, f'statistics_{phy_dir}_bv.csv')
                    if os.path.exists(csv_file_path):
                        phy_layer_csv_files[phy_dir].append(csv_file_path)
                    
        else:
            for dir in pair_dir_list:
                dir = os.path.join(dir, 'No_BV')
                phy_dirs_list = os.listdir(dir)
                for phy_dir in phy_dirs_list:
                    csv_file_path = os.path.join(dir, phy_dir, f'statistics_{phy_dir}_no_bv.csv')
                    if os.path.exists(csv_file_path):
                        phy_layer_csv_files[phy_dir].append(csv_file_path)
        
        return phy_layer_csv_files

    def get_dcube_csv_files_pair_temperature(self, bv, src, fwd, dst):
        """
            This function gathers all the csv files containing statisitcs for the dcube experiments
            based on specific node pairs and stores them in a dictionary with the key being the PHY layer used.
            :param bv: bit voting enabled or not
            :param src: source node id
            :param fwd: forwarder node id
            :param dst: destination node id
            :return: dictionary of csv files
        """
        dir_list = self.get_log_file_directories()
        phy_layer_csv_files = {'PHY_BLE_2M':{}, 'PHY_BLE_1M':{}, 'PHY_BLE_500K':{}, 'PHY_BLE_125K':{}}
        pair_dir_list = []

        for dir in dir_list:
            if src in dir and fwd in dir and dst in dir:
                pair_dir_list.append(dir)

        if bv:
            for dir in pair_dir_list:
                dir = os.path.join(dir, 'With_BV')
                phy_dirs_list = os.listdir(dir)
                for phy_dir in phy_dirs_list:
                    files = os.listdir(os.path.join(dir, phy_dir))
                    for file in files:
                        if file.endswith('.csv'):
                            csv_file_path = os.path.join(dir, phy_dir, file)
                            if os.path.exists(csv_file_path):
                                temperature = file.split('_')[1]
                                if temperature not in phy_layer_csv_files[phy_dir]:
                                    phy_layer_csv_files[phy_dir][temperature] = []
                                phy_layer_csv_files[phy_dir][temperature].append(csv_file_path)
                    
        else:
            for dir in pair_dir_list:
                dir = os.path.join(dir, 'No_BV')
                phy_dirs_list = os.listdir(dir)
                for phy_dir in phy_dirs_list:
                    files = os.listdir(os.path.join(dir, phy_dir))
                    for file in files:
                        if file.endswith('.csv'):
                            csv_file_path = os.path.join(dir, phy_dir, file)
                            if os.path.exists(csv_file_path):
                                temperature = file.split('_')[1]
                                if temperature not in phy_layer_csv_files[phy_dir]:
                                    phy_layer_csv_files[phy_dir][temperature] = []
                                phy_layer_csv_files[phy_dir][temperature].append(csv_file_path)
        
        return phy_layer_csv_files