import pandas as pd

main_df = pd.read_csv("../Data/Processed/05_Human_Readable.csv")
holidays_df = pd.read_csv("../Data/Processed/Holidays_Processed.csv")

main_df["merge_key"] = (
    main_df["Year"].astype(str)
    + "-"
    + main_df["Month"].astype(str)
    + "-"
    + main_df["Day"].astype(str)
)
holidays_df["merge_key"] = (
    holidays_df["Year"].astype(str)
    + "-"
    + holidays_df["Month"].astype(str)
    + "-"
    + holidays_df["Day"].astype(str)
)

holiday_dates = set(holidays_df["merge_key"])

main_df["isHoliday"] = main_df["merge_key"].apply(lambda x: 1 if x in holiday_dates else 0)

main_df = main_df.drop(columns=["merge_key"])
main_df.to_csv("../Data/Processed/06_With_Holidays.csv", index=False)
