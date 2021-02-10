import pandas as pd
import numpy as np
from pathlib import Path
import time
import credentials


def special_present(stu_num, df):
    df_changes = df.loc[
        (df["PERMNUMBER"] == stu_num)
        & (df["DAILY_STATUS"] == "ABS")
        & (df["ABSCATID"].isnull())
    ].copy()

    df_changes["DAILY_STATUS"].replace("ABS", "PRS", inplace=True)
    df_changes["DSID_VALUE"].fillna("1", inplace=True)
    return df_changes


def process_att():
    print("importing ps att")
    df = pd.read_csv("incoming_files/03_7_PS_Att.csv", dtype=str)

    # get adjustments
    df_adjust = pd.read_csv("resources/att_adjustments.csv", dtype=str)

    # accomodate student with too many classes
    df_changes = special_present(credentials.spec_stu_1, df)

    # fix static special cases
    df = df.append([df_changes, df_adjust])
    final_df = df.drop_duplicates(
        ["ADMINID", "ENRORGID", "PERMNUMBER", "ATTEVENTDATE"], keep="last"
    )

    myFile = Path("incoming_files/03_7_PS_Att.csv")

    print("renaming ps att")
    myFile.rename(Path(myFile.parent, f"old-{myFile.stem}{myFile.suffix}"))
    time.sleep(2)

    print("exporting ps att")
    final_df.to_csv("outgoing_files/03_7_PS_Att.csv", index=False)

    print("finished")
