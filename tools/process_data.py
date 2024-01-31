from typing import List

import pandas as pd
import re

shop_info_file = "data/all_shop_info.csv"
postcode_info_file = "data/kl_postcode.txt"
final_file = "data/final.csv"


def load_postcode():
    with open(postcode_info_file, "r", encoding="utf-8") as file:
        kl_postcode = file.read()

    kl_postcode = kl_postcode.split(",")
    kl_postcode = [int(i) for i in kl_postcode]
    return kl_postcode


def load_info(kl_postcode: List[int]):
    df = pd.read_csv(shop_info_file, keep_default_na=False)
    kl_shops = []
    for index, row in df.iterrows():
        address: str = row["Address"]
        if address:
            address = address.replace("\xa0", " ")
            address = address.replace('"', "")
            addresses = re.split(", | |,", address)
            for adde in reversed(addresses):
                if adde.isnumeric():
                    if int(adde) in kl_postcode:
                        opt = row["Operation Hour"]
                        opt = opt.replace("\xa0", " ")
                        opt = opt.replace('"', "")
                        kl_shops.append(
                            [row["Name"], address, opt, row["Latitude"], row["Longitude"]])
                        # kl_shops.append(
                        #     Shop(row["Name"], address, row["Operation Hour"], row["Latitude"], row["Longitude"]))
                        break

    print("Total valid shop:", len(kl_shops))
    return kl_shops


def write_file(kl_shops):
    df = pd.DataFrame(kl_shops, columns=["Outlet Name", "Address", "Operation Hour", "Latitude", "Longitude"])
    df.to_csv(final_file, index=False, encoding="utf-8")


if __name__ == "__main__":
    postcodes = load_postcode()
    shops = load_info(postcodes)
    write_file(shops)
