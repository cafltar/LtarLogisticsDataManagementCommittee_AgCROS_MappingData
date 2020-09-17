import pathlib
import pandas as pd
import datetime
from mapper import Mapper

def explode_treatment_ids(df:pd.DataFrame):
    df_out = df.copy()

    df_out["Field_plot_ID"] = df["Field_plot_ID"].str.replace(" ","")
    df_out["Field_plot_ID"] = df_out["Field_plot_ID"].str.split(",").tolist()
    df_out = df_out.explode("Field_plot_ID").reset_index(drop=True)

    return df_out

def expand_treatment_shorthand(df:pd.DataFrame):
    df_out = df.copy()

    for key in Mapper.FIELDSTRIP_ABBRIV_TO_FIELDSTRIP_LIST:
        df_out.loc[(df_out["Field_plot_ID"] == key), "Field_plot_ID"] = Mapper.FIELDSTRIP_ABBRIV_TO_FIELDSTRIP_LIST[key]

    return df_out

def clean_treatment_ids(df:pd.DataFrame):
    df_out = df.copy()

    for key in Mapper.FIELDSTRIP_TO_TREATMENTID:
        df_out.loc[(df_out["Field_plot_ID"] == key), "Field_plot_ID"] = Mapper.FIELDSTRIP_TO_TREATMENTID[key]

    return df_out

def expand_treatment_ids(df:pd.DataFrame, georeferencePoints:pd.DataFrame):
    df_out = df.copy()

    # Expand Field_plot_ID (treatment ids) to georeference points
    df_out = df_out.drop_duplicates()
    df_out = df_out.merge(georeferencePoints, left_on="Field_plot_ID", right_on="TreatmentId", how="left")

    df_out = df_out.drop(columns = ["Field_plot_ID", "StartYear", "EndYear"])

    return df_out

def create_exp_unit_col(df:pd.DataFrame, georeferencePoints:pd.DataFrame):
    df_out = df.copy()

    df_out = (df_out
        .pipe(explode_treatment_ids) #handles cases like "A1, C"
        .pipe(expand_treatment_shorthand) #expands shorthand like "C" to "C1, C2,...C8"
        .pipe(explode_treatment_ids) #handles list created by clean_treatment_ids
        .pipe(clean_treatment_ids) #renames field+strip to treatmentid (C8 = C5)
        .pipe(expand_treatment_ids, georeferencePoints)) #merge georeference points (for agcros, they are the exp units) with treatmentIds

    return df_out

def create_crop_col(df:pd.DataFrame):
    df_out = df.copy()

    df_out["Crop_AgCROS"] = ""

    for key in Mapper.CROP_ABBRIV_TO_AGCROS:
        df_out.loc[(df["CropCAF"] == key), "Crop_AgCROS"] = Mapper.CROP_ABBRIV_TO_AGCROS[key]
        
    return df_out

def create_planting_density_col(df:pd.DataFrame):
    df_out = df.copy()

    # Convert lb/ac to kg/ha
    df_out["PlantDensity_AgCROS"] = df_out["planting_material_weight"] * 1.12085

    return df_out

def create_planting_depth_col(df:pd.DataFrame):
    df_out = df.copy()

    # Convert in to cm
    df_out["PlantingDepth_AgCROS"] = df_out["planting_depth"] * 2.54

    return df_out

def create_planting_method_col(df:pd.DataFrame):
    df_out = df.copy()

    df_out["PlantingMethod_AgCROS"] = df_out.apply(get_planting_method, axis=1)

    return df_out
    
def get_planting_method(row):
    drillConfig = row["drill_opener_configuration"]
    
    # if not defined by drill_opener_configuration, then likely "broadcast", which is in drill_opener_type
    if(pd.isnull(drillConfig)):
        drillConfig = row["drill_opener_type"]

    result = Mapper.DRILL_CONFIG_TO_PLANTING_METHOD_AGCROS[drillConfig]

    return result

def create_row_width_col(df:pd.DataFrame):
    df_out = df.copy()

    df_out["RowWidth_AgCROS"] = df_out.apply(get_row_width, axis=1)

    return df_out

def get_row_width(row):
    rowDescription = row["drill_row_description"]
    rowWidth = rowDescription.split("\"")[0]

    if(rowWidth == "broadcast"):
        rowWidth = 0

    # Convert from in to cm
    result = float(rowWidth) * 2.54

    return result

def main(
    pathToManagement: pathlib.Path,
    pathToTreatment: pathlib.Path,
    pathToOutputDir: pathlib.Path
    ):

    ## Data Transformation
    managementPlanting = pd.read_excel(
        pathToManagement,
        sheet_name="Plantings",
        usecols=[1,2,3,6,15,16,21,22,23,24,25],
        skiprows=3,
        skipfooter=9,
        na_values=[-99]
    )

    #managementFertilizer = pd.read_excel(
    #    pathToManagement,
    #    sheet_name="Fertilizers",
    #    
    #)

    treatments = pd.read_csv(
        pathToTreatment
    )

    df = (managementPlanting
        .pipe(create_exp_unit_col, treatments)
        .pipe(create_crop_col)
        .pipe(create_planting_density_col)
        .pipe(create_planting_depth_col)
        .pipe(create_planting_method_col)
        .pipe(create_row_width_col)
        .rename(columns={"ID2":"ExpUnitId_AgCROS"}))

    # Write files
    date_today = datetime.datetime.now().strftime("%Y%m%d")

    df.sort_values(by = "ExpUnitId_AgCROS").to_csv(
        outputDir / "CookManagement-AgCROS_{}.csv".format(date_today),
        index = False)

if __name__ == "__main__":
    # params
    inputDir = pathlib.Path.cwd() / "input"
    outputDir = pathlib.Path.cwd() / "output"

    inputManagement = inputDir / "CAF_LTAR_consolidated_mgmt_0.2_brc5_inl4_jww4.xlsx"
    inputTreatments = inputDir / "georeferencepoint_treatments_cookeast_1999-2016_20200605.csv"

    main(
        inputManagement,
        inputTreatments,
        outputDir
    )