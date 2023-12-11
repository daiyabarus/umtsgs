def gs_externalgsm_process(
    txt_data: list, gslist_data: list, dt_col: dict, moc: str
):
    gs_result = []

    for raw_data in txt_data:
        if str(raw_data).strip() == "" or "NodeId" in str(raw_data):
            continue

        u_data = str(raw_data).split("\t")
        NodeId = u_data[dt_col.get("NodeId", 0)]
        UtranCellId = u_data[dt_col.get("UtranCellId", 8)]
        ExternalGsmCellId = u_data[dt_col.get("ExternalGsmCellId", 3)]

        for gs_data in gslist_data:
            param = gs_data[0]
            baseline_value = gs_data[1]

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
                moc + "_" + ExternalGsmCellId,
                param,
                oss_value,
                baseline_value,
                compliance,
            ]

            gs_result.append(gs_data)

    return gs_result
