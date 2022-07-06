import arcpy
import os


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
                                displayName="Please Input 2 mile sector layer",
                                name="scenario_two_mile",
                                datatype="GPFeatureLayer",
                                parameterType="Optional",
                                direction="Input"
        )

        param1 = arcpy.Parameter(
                                displayName="Select Scenario Sectors 2 Mile",
                                name="in_value_sectors_two_miles",
                                datatype="string",
                                parameterType="Optional",
                                direction="Input")
        # Set a value list of 1, 10 and 100
        param1.filter.type = "ValueList"
        param1.filter.list = ['A','B','C','D','E','F','G','H','J','K','L','M','N','P','Q','R']
        param1.multiValue  = True
        param1.defaultEnvironmentName = None

        param2 = arcpy.Parameter(
                                displayName="Please Input 5 mile sector layer",
                                name="scenario_five_mile",
                                datatype="GPFeatureLayer",
                                parameterType="Optional",
                                direction="Input"
        )

        param3 = arcpy.Parameter(
                                displayName="Select Scenario Sectors 5 Mile",
                                name="in_value_sectors_five_miles",
                                datatype="string",
                                parameterType="Optional",
                                direction="Input")
        # Set a value list of 1, 10 and 100
        param3.filter.type = "ValueList"
        param3.filter.list = ['A','B','C','D','E','F','G','H','J','K','L','M','N','P','Q','R']
        param3.multiValue  = True
        param3.defaultEnvironmentName = None

        param4 = arcpy.Parameter(
                                displayName="Please input 10 mile sector layer",
                                name="scenario_10_mile",
                                datatype="GPFeatureLayer",
                                parameterType="Optional",
                                direction="Input")

        param5 = arcpy.Parameter(
                                displayName="Select Scenario Sectors 10 Mile",
                                name="in_value_sectors_ten_miles",
                                datatype="string",
                                parameterType="Optional",
                                direction="Input")
        # Set a value list of 1, 10 and 100
        param5.filter.type = "ValueList"
        param5.filter.list = ['A','B','C','D','E','F','G','H','J','K','L','M','N','P','Q','R']
        param5.multiValue  = True
        param5.defaultEnvironmentName = None

        param6 = arcpy.Parameter(
                                displayName="Please select the Result GDB workspace",
                                name="wrkspace_select_feature",
                                datatype="DEWorkspace",
                                parameterType="Optional",
                                direction="Input")
        param6.defaultEnvironmentName = None
        
        param7 = arcpy.Parameter(
                                displayName="Please Select Your Scenario Layer",
                                name="scenario_select_feature",
                                datatype="GPFeatureLayer",
                                parameterType="Optional",
                                direction="Input")
        
        param8 = arcpy.Parameter(
            displayName="Please select the municipality layer",
                        name="muni_select_feature",
                        datatype="GPFeatureLayer",
                        parameterType="Optional",
                        direction="Input"
        )
        param8.defaultEnvironmentName = None
        
        param9 = arcpy.Parameter(
            displayName="Please select the population layer",
                        name="pop_select_feature",
                        datatype="GPFeatureLayer",
                        parameterType="Optional",
                        direction="Input"
        )
        param9.defaultEnvironmentName = None

        param10 = arcpy.Parameter(
                                displayName="Add Additional Municipalities for scenario (Input all that apply)",
                                name="in_value_additional_munis",
                                direction="Input",
                                datatype="string",
                                parameterType="Optional",
                                multiValue=True)
        

        params = [param0, param1, param2, param3, param4, param5, param6, param7, param8, param9, param10]
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

    def create_scenario(self,two_mile_layer: object, two_mile_sectors: object,
                        five_mile_layer: object, five_mile_sectors: object,
                        ten_mile_layer: object, ten_mile_sectors: object, workspace: object):
        arcpy.AddMessage(two_mile_layer)
        features_created = []
        # Execute Selection for two mile 
        if two_mile_sectors.value:
            out_featureclass_two_mile = os.path.join(arcpy.env.scratchGDB, 
                                                     'two_mile_sectors')
            two_mile_input_select = two_mile_sectors.valueAsText.split(';')
            two_mile_query = "Designation IN {}".format(tuple(two_mile_input_select))
            arcpy.AddMessage(two_mile_query)
            two_mile_final = arcpy.SelectLayerByAttribute_management(two_mile_layer.valueAsText, 
                                                                     'NEW_SELECTION', 
                                                                     two_mile_query)
            arcpy.CopyFeatures_management(two_mile_final,
                                          out_featureclass_two_mile)
            features_created.append(out_featureclass_two_mile)
        else: 
            two_mile_sectors.value = 'None'
        # Execute Selection for 5 mile 
        if five_mile_sectors.value:
            out_featureclass_five_mile = os.path.join(arcpy.env.scratchGDB, 
                                    'five_mile_sectors')
            five_mile_input_select = five_mile_sectors.valueAsText.split(';')
            five_mile_query = "Designation IN {}".format(tuple(five_mile_input_select))
            five_mile_final = arcpy.SelectLayerByAttribute_management(five_mile_layer.valueAsText, 
                                                                      'NEW_SELECTION', 
                                                                      five_mile_query)
            arcpy.CopyFeatures_management(five_mile_final,
                                          out_featureclass_five_mile)
            features_created.append(out_featureclass_five_mile)
        else: 
            five_mile_sectors.value = 'None'
        # Execute Selection for ten mile 
        if ten_mile_sectors.value:
            out_featureclass_ten_mile = os.path.join(arcpy.env.scratchGDB, 
                                    'ten_mile_sectors')
            ten_mile_input_select = ten_mile_sectors.valueAsText.split(';')
            ten_mile_query = "Designation IN {}".format(tuple(ten_mile_input_select))
            arcpy.AddMessage(ten_mile_query)
            ten_mile_final = arcpy.SelectLayerByAttribute_management(ten_mile_layer.valueAsText, 'NEW_SELECTION', 
                                        ten_mile_query)
            arcpy.CopyFeatures_management(ten_mile_final,
                                               out_featureclass_ten_mile)
            features_created.append(out_featureclass_ten_mile)
        else: 
            ten_mile_sectors.value = 'None'
        merge = os.path.join(arcpy.env.scratchGDB, 
                                    'merge')
        scenario_layer = arcpy.Merge_management(features_created, merge)
        return scenario_layer
        

    def get_parcel_to_scenario_intersect(self, workspace: object,
                                         scenario_layer: object,
                                         muni_layer: object):
        # Select Municipalities that intersect with scenario sectors
        munis_intersect_scenario = arcpy.SelectLayerByLocation_management(muni_layer.valueAsText,
                                                                          "INTERSECT",
                                                                          scenario_layer.valueAsText)
        # Create temporary layer with selected municipalities
        path_to_view = workspace.valueAsText + '\\' + 'muni_ten_percent_' + str(scenario_layer.valueAsText)
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
            arcpy.Delete_management(workspace.valueAsText + '\\' + 'final_muni_ten_percent_' + str(scenario_layer.valueAsText))
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
        self.create_scenario(parameters[0],parameters[1],
                             parameters[2],parameters[3],
                             parameters[4],parameters[5],parameters[6])
        # fc = self.get_parcel_to_scenario_intersect(
        #     parameters[1], parameters[2], parameters[3])
        # self.detect_munis_with_10_percent_pop(
        #     fc, parameters[4], parameters[2], parameters[1])
        # arcpy.AddMessage('Analysis Complete...')
        return


if __name__ == '__main__':
    theTool = Tool()
