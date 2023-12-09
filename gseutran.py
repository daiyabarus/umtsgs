def gs_eutran_process(
    txt_data: list, gslist_data: list, dt_col: dict, moc: str
):
    gs_result = []

    for raw_data in txt_data:
        if str(raw_data).strip() == "" or "NodeId" in str(raw_data):
            continue

        u_data = str(raw_data).split()
        NodeId = u_data[dt_col.get("NodeId", 0)]
        UtranCellId = u_data[dt_col.get("UtranCellId", 2)]
        EutranFreqRelationId = u_data[dt_col.get("EutranFreqRelationId", 3)]

        for gs_data in gslist_data:
            param = gs_data[0]
            baseline_value = gs_data[1]

            if baseline_value == "SUFFIX":
                if param == "qQualMin":
                    if "LTE1075" in EutranFreqRelationId:
                        baseline_value = "-18"
                    elif "LTE5060" in EutranFreqRelationId:
                        baseline_value = "-34"
                    elif "LTE2025" in EutranFreqRelationId:
                        baseline_value = "-18"
                    elif "LTE2050" in EutranFreqRelationId:
                        baseline_value = "-18"
                    elif "LTE3050" in EutranFreqRelationId:
                        baseline_value = "-18"
                    elif "LTE1025" in EutranFreqRelationId:
                        baseline_value = "-18"
                    elif "LTE2000" in EutranFreqRelationId:
                        baseline_value = "-18"
                    elif "LTE2950" in EutranFreqRelationId:
                        baseline_value = "-18"
                    elif "LTE2350" in EutranFreqRelationId:
                        baseline_value = "-18"
                elif param == "qRxLevMin":
                    if "LTE1075" in EutranFreqRelationId:
                        baseline_value = "-110"
                    elif "LTE5060" in EutranFreqRelationId:
                        baseline_value = "-124"
                    elif "LTE2025" in EutranFreqRelationId:
                        baseline_value = "-118"
                    elif "LTE2050" in EutranFreqRelationId:
                        baseline_value = "-118"
                    elif "LTE3050" in EutranFreqRelationId:
                        baseline_value = "-116"
                    elif "LTE1025" in EutranFreqRelationId:
                        baseline_value = "-110"
                    elif "LTE2000" in EutranFreqRelationId:
                        baseline_value = "-118"
                    elif "LTE2950" in EutranFreqRelationId:
                        baseline_value = "-116"
                    elif "LTE2350" in EutranFreqRelationId:
                        baseline_value = "-118"
                elif param == "cellReselectionPriority":
                    if "LTE1075" in EutranFreqRelationId:
                        baseline_value = "5"
                    elif "LTE5060" in EutranFreqRelationId:
                        baseline_value = "5"
                    elif "LTE2025" in EutranFreqRelationId:
                        baseline_value = "6"
                    elif "LTE2050" in EutranFreqRelationId:
                        baseline_value = "6"
                    elif "LTE3050" in EutranFreqRelationId:
                        baseline_value = "2"
                    elif "LTE1025" in EutranFreqRelationId:
                        baseline_value = "5"
                    elif "LTE2000" in EutranFreqRelationId:
                        baseline_value = "6"
                    elif "LTE2950" in EutranFreqRelationId:
                        baseline_value = "2"
                    elif "LTE2350" in EutranFreqRelationId:
                        baseline_value = "6"
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
                moc + "_" + EutranFreqRelationId,
                param,
                oss_value,
                baseline_value,
                compliance,
            ]

            gs_result.append(gs_data)

    return gs_result
