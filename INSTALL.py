import os

print('Python Morpheus installation script:')
os.system("sudo apt-get install g++ cmake cmake-curses-gui xsltproc libxml2-utils doxygen git zlib1g-dev libboost-dev "
          "libboost-program-options-dev libtiff5-dev libsbml5-dev qttools5-dev libqt5svg5-dev qtwebengine5-dev "
          "libqt5sql5-sqlite gnuplot  ")
print('Give me the installation path where morpheus main folder should be install to; press enter for default.')
install_dir = '/home/' + os.getuid()
print(install_dir)
new_dir = input("Installation directory:")
while len(new_dir) > 0 and not os.path.isfile(new_dir):
    print("An Error occured. This may not be a valid file! Please try again.")
    new_dir = input('Installation directory:')
