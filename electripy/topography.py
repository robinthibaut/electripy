# create a class to add topography information to the end of a profile defined by a text file
import numpy as np


class Topography:
    def __init__(self, profile: str, topography: str):
        """
        This class adds topography to the end of a profile defined by a text file.
        It saves the topography data in a separate text file.
        :param profile: the profile file to add topography to
        :param topography: the topography file to read
        """
        self.profile = profile
        self.topo_file = topography
        self.topo_list = []

    # create a function to read topography data from a text file. Topography data is in the form of: X(m), Y(m), Z(m)
    def read_topo(self):
        # read in the topography file
        with open(self.topo_file, 'r') as f:
            topo_data = f.readlines()
        # the file is a space delimited text file, so split the lines by spaces
        topo_data = [line.split() for line in topo_data]

        # convert the data to floats (some coordinates are strings starting with zeros, so remove them)
        def strip_zeros(x):
            """removes multiple zeros starting a string"""
            # count how many zeros are at the beginning of the string
            zeros = 0
            for char in x:
                if char == '0':
                    zeros += 1
                else:
                    break
            # remove the zeros
            x = x[zeros:]
            return x

        topo_data = [[float(strip_zeros(x)) for x in line] for line in topo_data]
        # create a 2D list to store the topography data [[0, z1], [d1, z2], [d3, z3], ...]
        topo_list = []
        # the starting elevation is 0, we have to compute the euclidean distance between the X and Y coordinates to
        # return the list of elevations for the profile
        topo_list.append([0, topo_data[0][2]])
        for i in range(1, len(topo_data)):
            # compute the euclidean distance between the current point and the previous point
            dist = np.linalg.norm(np.array(topo_data[i]) - np.array(topo_data[i - 1]))
            # dist = ((topo_data[i][0] - topo_data[i-1][0])**2 + (topo_data[i][1] - topo_data[i-1][1])**2)**0.5
            # add the distance to the previous elevation
            topo_list.append([topo_list[i - 1][0] + dist, topo_data[i][2]])
        self.topo_list = topo_list
        # return the list of elevations
        return topo_list

    # create a function to add topography to the profile
    def add_topo(self):
        header = "Topography in separate list"
        # at the end of the profile file, add the following:
        # header
        # 1
        # number of points
        # X(m),Z(m) for each point

        # read in the profile file. We just need to read it and add the topography to the end
        with open(self.profile, 'r') as f:
            profile_data = f.read()
            # add the header
            profile_data += "\n" + header + "\n" + "1\n" + str(len(self.topo_list)) + "\n"
            # add the topography data
            for point in self.topo_list:
                profile_data += str(point[0]) + "," + str(point[1]) + "\n"
            # add a 0 to the end of the profile data
            profile_data += "0\n"
            # add 4 zeros to the end of the profile data
            profile_data += "0,0,0,0\n"
        # write the profile file with the topography data
        # define a new file name
        new_file = self.profile[:-4] + "_topo.dat"
        with open(new_file, 'w') as f:
            f.write(profile_data)
        # return the new file name
        return new_file


# test the class
if __name__ == '__main__':
    # create a topography class
    # you need to input the profile file and the topography file
    # make sure that they match
    # just get the new file in the same folder as the profile file (_topo.dat)
    topo = Topography('/Users/robin/PycharmProjects/electripy/data/Project8_G7_1.dat',
                      '/Users/robin/PycharmProjects/electripy/data/Coordinate_P3.txt')
    # read the topography data
    topo_data = topo.read_topo()
    # print the total distance of the profile
    print(topo_data[-1][0])
    # print the topography data
    print(topo_data)
    # add the topography to the profile
    topo.add_topo()
