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
from gsextgsm import gs_externalgsm_process
from gsgsmrel import gs_gsmrel_process
from gsiublink import gs_iublink_process
from gslicense import gs_license_process
from gsnodebfunction import gs_nodebfunction_process
from gsnodeblocalcell import gs_nodeblocalcell_process
from gsnodebsectorcarrier import gs_nodebsectorcarrier_process
from gsutran import gs_utran_process


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
    gs_result_utrancell = []
    gs_result_rbs = []
    header_utrancell = [
        "RNC",
        "UtranCellId",
        "ManagedObjectClass",
        "Parameter",
        "OssValue",
        "BaselineValue",
        "Compliance",
    ]

    header_rbs = [
        "RBS",
        "MO",
        "ManagedObjectClass",
        "Parameter",
        "OssValue",
        "BaselineValue",
        "Compliance",
    ]
    # UtranCell
    utrancell_csv = os.path.join(source_folder, "UtranCell.csv")
    utrancell_data = txtfile_to_list(txtpath=utrancell_csv)
    # gsresult_utrancell = gs_process(
    gsresult_utrancell = gs_utran_process(
        txt_data=utrancell_data,
        gslist_data=gslist.gs_utrancell(),
        dt_col=enumlist.utrancell_col(),
        moc="UtranCell",
    )
    gs_result_utrancell.extend(gsresult_utrancell)

    # Rach
    rach_csv = os.path.join(source_folder, "Rach.csv")
    rach_data = txtfile_to_list(txtpath=rach_csv)
    gsresult_rach = gs_process(
        txt_data=rach_data,
        gslist_data=gslist.gs_rach(),
        dt_col=enumlist.rach_col(),
        moc="Rach",
    )
    gs_result_utrancell.extend(gsresult_rach)

    # Fach
    fach_csv = os.path.join(source_folder, "Fach.csv")
    fach_data = txtfile_to_list(txtpath=fach_csv)
    gsresult_fach = gs_process(
        txt_data=fach_data,
        gslist_data=gslist.gs_fach(),
        dt_col=enumlist.fach_col(),
        moc="Fach",
    )
    gs_result_utrancell.extend(gsresult_fach)

    # Pch
    pch_csv = os.path.join(source_folder, "Pch.csv")
    pch_data = txtfile_to_list(txtpath=pch_csv)
    gsresult_pch = gs_process(
        txt_data=pch_data,
        gslist_data=gslist.gs_pch(),
        dt_col=enumlist.pch_col(),
        moc="Pch",
    )
    gs_result_utrancell.extend(gsresult_pch)

    # Eul
    eul_csv = os.path.join(source_folder, "Eul.csv")
    eul_data = txtfile_to_list(txtpath=eul_csv)
    gsresult_eul = gs_process(
        txt_data=eul_data,
        gslist_data=gslist.gs_eul(),
        dt_col=enumlist.eul_col(),
        moc="Eul",
    )
    gs_result_utrancell.extend(gsresult_eul)

    # Hsdsch
    hsdsch_csv = os.path.join(source_folder, "Hsdsch.csv")
    hsdsch_data = txtfile_to_list(txtpath=hsdsch_csv)
    gsresult_hsdsch = gs_process(
        txt_data=hsdsch_data,
        gslist_data=gslist.gs_hsdsch(),
        dt_col=enumlist.hsdsch_col(),
        moc="Hsdsch",
    )
    gs_result_utrancell.extend(gsresult_hsdsch)

    # EutranFreqRelation
    eutran_csv = os.path.join(source_folder, "EutranFreqRelation.csv")
    eutran_data = txtfile_to_list(txtpath=eutran_csv)
    gsresult_eutran = gs_eutran_process(
        txt_data=eutran_data,
        gslist_data=gslist.gs_eutran(),
        dt_col=enumlist.eutran_col(),
        moc="EutranFreqRelation",
    )
    gs_result_utrancell.extend(gsresult_eutran)

    externalgsmcell_csv = os.path.join(source_folder, "ExternalGsmCell.csv")
    externalgsmcell_data = txtfile_to_list(txtpath=externalgsmcell_csv)
    gsresult_externalgsmcell = gs_externalgsm_process(
        txt_data=externalgsmcell_data,
        gslist_data=gslist.gs_externalgsmcell(),
        dt_col=enumlist.externalgsmcell_col(),
        moc="ExternalGsmCell",
    )
    gs_result_utrancell.extend(gsresult_externalgsmcell)

    gsmrelation_csv = os.path.join(source_folder, "GsmRelation.csv")
    gsmrelation_data = txtfile_to_list(txtpath=gsmrelation_csv)
    gsresult_gsmrelation = gs_gsmrel_process(
        txt_data=gsmrelation_data,
        gslist_data=gslist.gs_gsmrelation(),
        dt_col=enumlist.gsmrelation_col(),
        moc="UtranCell=",
    )
    gs_result_utrancell.extend(gsresult_gsmrelation)

    license_csv = os.path.join(source_folder, "License.csv")
    license_data = txtfile_to_list(txtpath=license_csv)
    gsresult_license = gs_license_process(
        txt_data=license_data,
        gslist_data=gslist.gs_license(),
        dt_col=enumlist.license_col(),
        moc="FeatureState",
    )
    gs_result_rbs.extend(gsresult_license)

    nodeblocalcell_csv = os.path.join(source_folder, "NodeBLocalCell.csv")
    nodeblocalcell_data = txtfile_to_list(txtpath=nodeblocalcell_csv)
    gsresult_nodeblocalcell = gs_nodeblocalcell_process(
        txt_data=nodeblocalcell_data,
        gslist_data=gslist.gs_nodeblocalcell(),
        dt_col=enumlist.nodeblocalcell_col(),
        moc="NodeBLocalCell",
    )

    gs_result_rbs.extend(gsresult_nodeblocalcell)

    nodebsectorcarrier_csv = os.path.join(
        source_folder, "NodeBSectorCarrier.csv"
    )
    nodebsectorcarrier_data = txtfile_to_list(txtpath=nodebsectorcarrier_csv)
    gsresult_nodebsectorcarrier = gs_nodebsectorcarrier_process(
        txt_data=nodebsectorcarrier_data,
        gslist_data=gslist.gs_nodebsectorcarrier(),
        dt_col=enumlist.nodebsectorcarrier_col(),
        moc="NodeBSectorCarrier",
    )

    gs_result_rbs.extend(gsresult_nodebsectorcarrier)

    nodebfunction_csv = os.path.join(source_folder, "NodeBFunction.csv")
    nodebfunction_data = txtfile_to_list(txtpath=nodebfunction_csv)
    gsresult_nodebfunction = gs_nodebfunction_process(
        txt_data=nodebfunction_data,
        gslist_data=gslist.gs_nodebfunction(),
        dt_col=enumlist.nodebfunction_col(),
        moc="NodeBFunction",
    )

    gs_result_rbs.extend(gsresult_nodebfunction)

    iublink_csv = os.path.join(source_folder, "IubLink.csv")
    iublink_data = txtfile_to_list(txtpath=iublink_csv)
    gsresult_iublink = gs_iublink_process(
        txt_data=iublink_data,
        gslist_data=gslist.gs_iublink(),
        dt_col=enumlist.iublink_col(),
        moc="",
    )

    gs_result_utrancell.extend(gsresult_iublink)

    result_file_utrancell = os.path.join(
        source_folder, "gs_result_utrancell_" + get_current_datetime() + ".csv"
    )
    with open(result_file_utrancell, "w", newline="") as f:
        write = csv.writer(f)
        write.writerow(header_utrancell)
        write.writerows(gs_result_utrancell)

    print("GS Result UtranCell save as: " + result_file_utrancell)

    result_file_rbs = os.path.join(
        source_folder, "gs_result_rbs_" + get_current_datetime() + ".csv"
    )
    with open(result_file_rbs, "w", newline="") as f:
        write = csv.writer(f)
        write.writerow(header_rbs)
        write.writerows(gs_result_rbs)

    print("GS Result RBS save as: " + result_file_rbs)


if __name__ == "__main__":
    main()
