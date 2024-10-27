####################################################
#           Luminescence Analysis Tools
# GUI used to easily remove peak points from the plot data

# Features:
#   - Easily plot the data, and by selecting the unwanted points
# with the 'Point Selection Tool' and pressing 'Del', removes
# that point from the data, and you can further export it again.
#
# The data can be either a .txt or .asc file. 
# If .txt, X and Y must be separated by ',' in each row, and '.' as the float point
# If .asc, X and Y must be separated by '\t' in each row, and ',' as the float point
#
# By Allison Pessoa, Nano-Optics Laboratory.
# UFPE, Brazil.  June, 2021
####################################################
#Editing to test git cola
import sys

sys.path.append(r'/home/allison/Dropbox/4_Projetos/Projetos em andamento/Python Modules/Luminescence Data Analyser/')
from SpectraAnalyser import Spectrum

from guiqwt.plot import CurveDialog
from guiqwt.builder import make

from PyQt5.QtGui import QKeySequence
from guiqwt.tools import OpenFileTool, SelectPointTool, ExportItemDataTool


import os
import numpy as np

class OpenFileToolAlternative(OpenFileTool):
    def activate_command(self, plot, checked):
            """Activate tool"""
            filename = self.get_filename(plot)
            try:
                spectrum = Spectrum(filename)
                wavelength, intensity = spectrum.get_spectrum()
                short_title = os.path.basename(spectrum.filename)
                curve = make.curve(wavelength, intensity, title=short_title)
                plot.add_item(curve)
                plot.do_autoscale()
            except:
                pass
            if filename:
                self.SIG_OPEN_FILE.emit(filename)

###
class PlotConstructor():
    def __init__(self):
        pass

    def create_plot(self):
        self.win = CurveDialog(edit=False, toolbar=True, wintitle="CurveDialog test",
                          options=dict(title="Spectra", xlabel="Wavelength (nm)",
                                       ylabel="Intensity"))
        self.plot = self.win.get_plot()
        self.win.get_itemlist_panel().show()

        ###
        self.export_tool = self.win.add_tool(ExportItemDataTool)
        self.open_file_tool = self.win.add_tool(OpenFileToolAlternative)
        self.select_tool = self.win.add_tool(SelectPointTool)
        self.select_tool.on_active_item=True

        delete_point_action = self.win.create_action("Delete Point", triggered=self.delete_point, shortcut='Del')
        save_file_action = self.win.create_action("Save File", triggered=self.save_file, shortcut='s')
        self.plot.addAction(delete_point_action)
        self.plot.addAction(save_file_action)
        ###
        self.win.show()
        self.win.exec_()

    def delete_point(self):
        try:
            spiked_item = self.plot.get_active_item()
            x_data, y_data = spiked_item.get_data()
            x_selection, y_selection = self.select_tool.get_coordinates()
            index = list(x_data).index(x_selection)
            self.new_y_data = y_data
            self.new_y_data[index] = self.new_y_data[index-1]
            self.plot.add_item(make.curve(x_data, self.new_y_data, spiked_item.title()))
            self.plot.del_item(spiked_item)
            unspiked_item = self.plot.get_default_item()
            self.plot.select_item(unspiked_item)
            self.plot.set_active_item(unspiked_item)
        except:
            pass

    def save_file(self):

        spiked_item = self.plot.get_active_item()
        x_data, y_data = spiked_item.get_data()
        title = spiked_item.title().text()
        filename = self.open_file_tool.directory + '/' + title[:-4] + '.txt'
        data = np.transpose(spiked_item.get_data())
        np.savetxt(filename,data,delimiter=',')

if __name__ == "__main__":
    import guidata
    _app = guidata.qapplication()
    Plot = PlotConstructor()
    Plot.create_plot()
