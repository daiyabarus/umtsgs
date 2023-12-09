"""_summary_

Returns:
    tool_name: umts-gs
    author: endang.ismaya
    version: 0.0.1
    update : 0.0.2

"""
import csv
import datetime
import os
import sys

import enumlist
import gslist
from gscheck import gs_process
from gseutran import gs_eutran_process


def get_current_datetime():
    now = datetime.datetime.now()
    return now.strftime("%Y%m%d_%H%M%S")


def txtfile_to_list(txtpath: str) -> list:
    reader_line = []

    with open(txtpath, "r") as fl:
        liner = fl.readlines()

        for line in liner:
            cline = line.rstrip()

            reader_line.append(cline)

    return reader_line


def main():
    source_folder = sys.argv[1]
    gs_result_all = []
    header = [
        "RNC",
        "UtranCellId",
        "ManagedObjectClass",
        "Parameter",
        "OssValue",
        "BaselineValue",
        "Compliance",
    ]

    # UtranCell
    utrancell_csv = os.path.join(source_folder, "UtranCell.csv")
    utrancell_data = txtfile_to_list(txtpath=utrancell_csv)
    gsresult_utrancell = gs_process(
        txt_data=utrancell_data,
        gslist_data=gslist.gs_utrancell(),
        dt_col=enumlist.utrancell_col(),
        moc="UtranCell",
    )
    gs_result_all.extend(gsresult_utrancell)

    # Rach
    rach_csv = os.path.join(source_folder, "Rach.csv")
    rach_data = txtfile_to_list(txtpath=rach_csv)
    gsresult_rach = gs_process(
        txt_data=rach_data,
        gslist_data=gslist.gs_rach(),
        dt_col=enumlist.rach_col(),
        moc="Rach",
    )
    gs_result_all.extend(gsresult_rach)

    # Fach
    fach_csv = os.path.join(source_folder, "Fach.csv")
    fach_data = txtfile_to_list(txtpath=fach_csv)
    gsresult_fach = gs_process(
        txt_data=fach_data,
        gslist_data=gslist.gs_fach(),
        dt_col=enumlist.fach_col(),
        moc="Fach",
    )
    gs_result_all.extend(gsresult_fach)

    # Pch
    pch_csv = os.path.join(source_folder, "Pch.csv")
    pch_data = txtfile_to_list(txtpath=pch_csv)
    gsresult_pch = gs_process(
        txt_data=pch_data,
        gslist_data=gslist.gs_pch(),
        dt_col=enumlist.pch_col(),
        moc="Pch",
    )
    gs_result_all.extend(gsresult_pch)

    # Eul
    eul_csv = os.path.join(source_folder, "Eul.csv")
    eul_data = txtfile_to_list(txtpath=eul_csv)
    gsresult_eul = gs_process(
        txt_data=eul_data,
        gslist_data=gslist.gs_eul(),
        dt_col=enumlist.eul_col(),
        moc="Eul",
    )
    gs_result_all.extend(gsresult_eul)

    # Hsdsch
    hsdsch_csv = os.path.join(source_folder, "Hsdsch.csv")
    hsdsch_data = txtfile_to_list(txtpath=hsdsch_csv)
    gsresult_hsdsch = gs_process(
        txt_data=hsdsch_data,
        gslist_data=gslist.gs_hsdsch(),
        dt_col=enumlist.hsdsch_col(),
        moc="Hsdsch",
    )
    gs_result_all.extend(gsresult_hsdsch)

    # EutranFreqRelation
    eutran_csv = os.path.join(source_folder, "EutranFreqRelation.csv")
    eutran_data = txtfile_to_list(txtpath=eutran_csv)
    gsresult_eutran = gs_eutran_process(
        txt_data=eutran_data,
        gslist_data=gslist.gs_eutran(),
        dt_col=enumlist.eutran_col(),
        moc="EutranFreqRelation",
    )
    gs_result_all.extend(gsresult_eutran)

    result_file = "gs_result_" + get_current_datetime() + ".csv"
    with open(result_file, "w", newline="") as f:
        write = csv.writer(f)
        write.writerow(header)
        write.writerows(gs_result_all)

    print("GS Result save as: " + result_file)


if __name__ == "__main__":
    main()
