import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Nuclear Scenarios Assessment Toolbox"
        self.alias = ""
        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Nuclear Sector Scenarios Assessment Tool"
        self.description = """This is a GP service tool to
                              calculate Nuclear Sector Population Scenarios,
                              the user will provide a scenario layer for sectors,
                              a municipality layer for townships,
                              and a population point layer for analysis. """
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName="Please select the Result GDB workspace",
            name="wrkspace_select_feature",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input"
        )
        param0.defaultEnvironmentName = None
        param1 = arcpy.Parameter(
            displayName="Please Select Your Scenario Layer",
                        name="scenario_select_feature",
                        datatype="GPFeatureLayer",
                        parameterType="Required",
                        direction="Input"
        )
        param2 = arcpy.Parameter(
            displayName="Please select the municipality layer",
                        name="muni_select_feature",
                        datatype="GPFeatureLayer",
                        parameterType="Required",
                        direction="Input"
        )
        param2.defaultEnvironmentName = None
        param3 = arcpy.Parameter(
            displayName="Please select the population layer",
                        name="pop_select_feature",
                        datatype="GPFeatureLayer",
                        parameterType="Required",
                        direction="Input"
        )
        param3.defaultEnvironmentName = None

        params = [param0, param1, param2, param3]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def get_parcel_to_scenario_intersect(self, workspace: object,
                                         scenario_layer: object,
                                         muni_layer: object):
        # Select Municipalities that intersect with scenario sectors
        munis_intersect_scenario = arcpy.SelectLayerByLocation_management(muni_layer.valueAsText,
                                                                          "INTERSECT",
                                                                          scenario_layer.valueAsText)
        # Create temporary layer with selected municipalities
        path_to_view = workspace.valueAsText + '\\' + \
            'muni_ten_percent_' + str(scenario_layer.valueAsText)
        # Check if temp layer already exists, if so delete for new run
        if arcpy.Exists(path_to_view):
            arcpy.Delete_management(path_to_view)
        # copy results to temporary gdb for analysis
        result = arcpy.CopyFeatures_management(munis_intersect_scenario,
                                               path_to_view)
        return result

    def detect_munis_with_10_percent_pop(self, fc: str, pop_fc: object,
                                         scenario_layer: object,
                                         workspace: object):
        # Set field name for township name
        fields = ['NAMELSAD']
        # Set list for counties with atleast 10% population within scenario
        final_ten_percent_muni = []
        # Loop over intersected municpalities, select muni name for tracking
        with arcpy.da.SearchCursor(fc, fields) as list_of_munis:
            for muni in list_of_munis:
                muni_name = muni[0]
                # Select muni by name from temp layer
                selected_muni = arcpy.management.SelectLayerByAttribute(fc,
                                                                        'NEW_SELECTION',
                                                                        "NAMELSAD = '{}'".format(muni_name))
                stats_holding = []
                total_pop_stats_table = r"in_memory\total_pop_stats"
                # Select population within municipality
                total_pop_select = arcpy.SelectLayerByLocation_management(pop_fc.valueAsText,
                                                                          "WITHIN",
                                                                          selected_muni)
                if arcpy.Exists(total_pop_stats_table):
                    arcpy.Delete_management(total_pop_stats_table)
                # Get total population for municipality
                arcpy.Statistics_analysis(total_pop_select,
                                          total_pop_stats_table,
                                          [['popCell', "SUM"]])
                mean_field = "SUM_{0}".format('popCell')
                cursor = arcpy.SearchCursor(total_pop_stats_table,
                                            "",
                                            "",
                                            mean_field)
                row = cursor.next()
                mean_value = row.getValue(mean_field)
                stats_holding.append(mean_value)
                del cursor
                # Subselect population from selected muni where it falls within scenario
                ten_percent_pop_select = arcpy.SelectLayerByLocation_management(total_pop_select,
                                                                                "WITHIN",
                                                                                scenario_layer.valueAsText,
                                                                                '',
                                                                                'SUBSET_SELECTION')
                ten_percent_pop_stats_table = r"in_memory\ten_percent_pop_stats"
                if arcpy.Exists(ten_percent_pop_stats_table):
                    arcpy.Delete_management(ten_percent_pop_stats_table)
                # Get total population within subselection
                arcpy.Statistics_analysis(ten_percent_pop_select,
                                          ten_percent_pop_stats_table,
                                          [['popCell', "SUM"]])
                mean_field = "SUM_{0}".format('popCell')
                cursor = arcpy.SearchCursor(ten_percent_pop_stats_table,
                                            "",
                                            "",
                                            mean_field)
                arcpy.AddMessage(muni_name)
                row = cursor.next()
                if hasattr(row, 'getValue'):
                    mean_value = row.getValue(mean_field)
                    stats_holding.append(mean_value)
                else:
                    stats_holding.append(1)
                del cursor
                # Calculate to check if municipality has greater than 10% pop
                population_percentage = stats_holding[1]/stats_holding[0]*100
                if population_percentage > 10:
                    final_ten_percent_muni.append(muni_name)

        final_muni = arcpy.management.SelectLayerByAttribute(fc,
                                                             'NEW_SELECTION',
                                                             "NAMELSAD IN {}".format(tuple(final_ten_percent_muni)))
        if arcpy.Exists(workspace.valueAsText + '\\' + 'final_muni_ten_percent_' + str(scenario_layer.valueAsText)):
            arcpy.Delete_management(workspace.valueAsText + '\\' +
                                    'final_muni_ten_percent_' + str(scenario_layer.valueAsText))
        arcpy.CopyFeatures_management(final_muni,
                                      workspace.valueAsText + '\\' + 'final_muni_ten_percent_' + str(scenario_layer.valueAsText))
        if arcpy.Exists(fc):
            arcpy.Delete_management(fc)

    def main_func(self):
        return

    def execute(self, parameters, messages):
        # set env
        arcpy.AddMessage(
            "Please refresh page for results when process is complete.")
        arcpy.AddMessage('Processing...')
        fc = self.get_parcel_to_scenario_intersect(
            parameters[0], parameters[1], parameters[2])
        self.detect_munis_with_10_percent_pop(
            fc, parameters[3], parameters[1], parameters[0])
        arcpy.AddMessage('Analysis Complete...')
        return


if __name__ == '__main__':
    theTool = Tool()
