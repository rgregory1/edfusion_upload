import pandas as pd
import numpy as np
from pathlib import Path
import time


def process_gradeprog():
    print("importing grade prog")
    df = pd.read_csv("incoming_files/03_5_PS_GradeProg.csv", dtype=str)

    # print(Path().absolute())

    df_error1 = pd.read_csv("resources/missing_end_dates.csv", dtype=str)
    df_error2 = pd.read_csv("resources/empty_end_dates.csv", dtype=str)

    df = df.append(df_error1)
    new_df = df.drop_duplicates(
        ["ADMINID", "ENRORGID", "PERMNUMBER", "GRADE"], keep="last"
    )
    final_df = new_df.append(df_error2)

    myFile = Path("incoming_files/03_5_PS_GradeProg.csv")

    print("renaming grade prog")
    myFile.rename(Path(myFile.parent, f"old-{myFile.stem}{myFile.suffix}"))
    time.sleep(2)

    print("exporting grade prog")
    final_df.to_csv("outgoing_files/03_5_PS_GradeProg.csv", index=False)

    print("finished")
