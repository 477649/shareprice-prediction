import pandas as pd

def build_floorsheet_features(df):
    grouped = df.groupby(["Date", "Symbol"]).agg(
        TradeCount=("Transact No.", "count"),
        TotalQuantity=("Quantity", "sum"),
        TotalAmount=("Amount", "sum"),
        AvgRate=("Rate", "mean"),
        MaxRate=("Rate", "max"),
        MinRate=("Rate", "min"),
        UniqueBuyers=("Buyer", "nunique"),
        UniqueSellers=("Seller", "nunique"),
        MaxTradeQty=("Quantity", "max"),
    ).reset_index()

    grouped["AvgTradeSize"] = grouped["TotalQuantity"] / grouped["TradeCount"]
    grouped["AvgAmountPerTrade"] = grouped["TotalAmount"] / grouped["TradeCount"]
    grouped["QtyPerBuyer"] = grouped["TotalQuantity"] / grouped["UniqueBuyers"].replace(0, 1)
    grouped["QtyPerSeller"] = grouped["TotalQuantity"] / grouped["UniqueSellers"].replace(0, 1)

    return grouped

def merge_with_shareprice(floor_features, share_df):
    merged = pd.merge(
        share_df,
        floor_features,
        on=["Date", "Symbol"],
        how="left"
    )
    return merged
