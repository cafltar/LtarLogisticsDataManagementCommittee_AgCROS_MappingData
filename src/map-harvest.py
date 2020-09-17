import pathlib
import pandas as pd
import datetime
from mapper import Mapper

def renameCrops(df:pd.DataFrame):
    df_out = df.copy()

    df_out["Crop_AgCROS"] = ""

    for key in Mapper.CROP_ABBRIV_TO_AGCROS:
        df_out.loc[(df["Crop"] == key), "Crop_AgCROS"] = Mapper.CROP_ABBRIV_TO_AGCROS[key]
        
    return df_out

def convertUnits(df:pd.DataFrame):
    df_out = df.copy()

    # Convert from g/m2 to kg/ha
    df_out["GrainYieldDryPerArea_AgCROS"] = df["GrainYieldDryPerArea"] * 10
    df_out["ResidueMassDryPerArea_AgCROS"] = df["ResidueMassDryPerArea"] * 10

    return df_out

def main(
    pathHarvestData: pathlib.Path,
    pathOutputDir: pathlib.Path
    ):

    ## Data Transformation
    harvest = pd.read_csv(
        pathHarvestData
    )

    df = (harvest
        .pipe(renameCrops)
        .pipe(convertUnits))

    # Write files
    date_today = datetime.datetime.now().strftime("%Y%m%d")

    df.to_csv(
        outputDir / "CookHarvest-AgCROS_{}.csv".format(date_today),
        index = False)

if __name__ == "__main__":
    # params
    inputDir = pathlib.Path.cwd() / "input"
    outputDir = pathlib.Path.cwd() / "output"

    inputPathHarvest = inputDir / "HY1999-2016_20200130_P3A1.csv"
    

    main(
        inputPathHarvest,
        outputDir
    )