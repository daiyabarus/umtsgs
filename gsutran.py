def gs_utran_process(
    txt_data: list, gslist_data: list, dt_col: dict, moc: str
):
    gs_result = []

    for raw_data in txt_data:
        if str(raw_data).strip() == "" or "NodeId" in str(raw_data):
            continue

        u_data = str(raw_data).split()
        NodeId = u_data[dt_col.get("NodeId", 0)]
        UtranCellId = u_data[dt_col.get("UtranCellId", 2)]
        uarfcnDl = u_data[dt_col.get("uarfcnDl", 195)]

        for gs_data in gslist_data:
            param = gs_data[0]
            baseline_value = gs_data[1]

            if baseline_value == "SUFFIX":
                if param == "loadSharingMargin":
                    if "1007" in uarfcnDl:
                        baseline_value = "20"
                    elif "1012" in uarfcnDl:
                        baseline_value = "20"
                    elif "1037" in uarfcnDl:
                        baseline_value = "20"
                    elif "4358" in uarfcnDl:
                        baseline_value = "20"
                    elif "4381" in uarfcnDl:
                        baseline_value = "20"
                    elif "4383" in uarfcnDl:
                        baseline_value = "20"
                    elif "4387" in uarfcnDl:
                        baseline_value = "20"
                else:
                    baseline_value = "0"

                if param == "qRxLevMin":
                    if "1007" in uarfcnDl:
                        baseline_value = "-115"
                    elif "1012" in uarfcnDl:
                        baseline_value = "-115"
                    elif "1037" in uarfcnDl:
                        baseline_value = "-115"
                    elif "4358" in uarfcnDl:
                        baseline_value = "-115"
                    elif "4381" in uarfcnDl:
                        baseline_value = "-115"
                    elif "4383" in uarfcnDl:
                        baseline_value = "-115"
                    elif "4387" in uarfcnDl:
                        baseline_value = "-115"
                else:
                    baseline_value = "-105"

                if param == "qHyst1":
                    if "1007" in uarfcnDl:
                        baseline_value = "8"
                    elif "1012" in uarfcnDl:
                        baseline_value = "8"
                    elif "1037" in uarfcnDl:
                        baseline_value = "8"
                    elif "4358" in uarfcnDl:
                        baseline_value = "8"
                    elif "4381" in uarfcnDl:
                        baseline_value = "8"
                    elif "4383" in uarfcnDl:
                        baseline_value = "8"
                    elif "4387" in uarfcnDl:
                        baseline_value = "8"
                else:
                    baseline_value = "4"

                if param == "qualMeasQuantity":
                    if "1007" in uarfcnDl:
                        baseline_value = "CPICH_EC_NO"
                    elif "1012" in uarfcnDl:
                        baseline_value = "CPICH_EC_NO"
                    elif "1037" in uarfcnDl:
                        baseline_value = "CPICH_EC_NO"
                    elif "4358" in uarfcnDl:
                        baseline_value = "CPICH_EC_NO"
                    elif "4381" in uarfcnDl:
                        baseline_value = "CPICH_EC_NO"
                    elif "4383" in uarfcnDl:
                        baseline_value = "CPICH_EC_NO"
                    elif "4387" in uarfcnDl:
                        baseline_value = "CPICH_EC_NO"
                else:
                    baseline_value = "RSCP"

                if param == "sInterSearch":
                    if "1007" in uarfcnDl:
                        baseline_value = "17"
                    elif "1012" in uarfcnDl:
                        baseline_value = "17"
                    elif "1037" in uarfcnDl:
                        baseline_value = "17"
                    elif "4358" in uarfcnDl:
                        baseline_value = "17"
                    elif "4381" in uarfcnDl:
                        baseline_value = "17"
                    elif "4383" in uarfcnDl:
                        baseline_value = "17"
                    elif "4387" in uarfcnDl:
                        baseline_value = "17"
                else:
                    baseline_value = "0"

                if param == "usedFreqThresh2dEcno":
                    if "1007" in uarfcnDl:
                        baseline_value = "-24"
                    elif "1012" in uarfcnDl:
                        baseline_value = "-24"
                    elif "1037" in uarfcnDl:
                        baseline_value = "-24"
                    elif "4358" in uarfcnDl:
                        baseline_value = "-24"
                    elif "4381" in uarfcnDl:
                        baseline_value = "-24"
                    elif "4383" in uarfcnDl:
                        baseline_value = "-24"
                    elif "4387" in uarfcnDl:
                        baseline_value = "-24"
                else:
                    baseline_value = "-20"

                if param == "usedFreqThresh2dRscp":
                    if "1007" in uarfcnDl:
                        baseline_value = "-115"
                    elif "1012" in uarfcnDl:
                        baseline_value = "-115"
                    elif "1037" in uarfcnDl:
                        baseline_value = "-115"
                    elif "4358" in uarfcnDl:
                        baseline_value = "-115"
                    elif "4381" in uarfcnDl:
                        baseline_value = "-115"
                    elif "4383" in uarfcnDl:
                        baseline_value = "-115"
                    elif "4387" in uarfcnDl:
                        baseline_value = "-115"
                else:
                    baseline_value = "-95"

            index_param = dt_col.get(param, -1)
            if index_param == -1:
                oss_value = "OSS_VALUE_NOT_FOUND"
            else:
                oss_value = u_data[index_param]

            if str(oss_value) == str(baseline_value):
                compliance = "MATCH"
            else:
                compliance = "MISMATCH"

            gs_data = [
                NodeId,
                UtranCellId,
                moc,
                param,
                oss_value,
                baseline_value,
                compliance,
            ]

            gs_result.append(gs_data)

    return gs_result
