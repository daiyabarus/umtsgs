def gs_nodeblocalcell_process(
    txt_data: list, gslist_data: list, dt_col: dict, moc: str
):
    gs_result = []

    for raw_data in txt_data:
        if str(raw_data).strip() == "" or "NodeId" in str(raw_data):
            continue

        u_data = str(raw_data).split()
        NodeId = u_data[dt_col.get("NodeId", 0)]
        NodeBLocalCellId = u_data[dt_col.get("NodeBLocalCellId", 3)]

        for gs_data in gslist_data:
            param = gs_data[0]
            baseline_value = gs_data[1]

            index_param = dt_col.get(param, -1)
            if index_param == -1:
                oss_value = "OSS_VALUE_NOT_FOUND"
            else:
                oss_value = u_data[index_param].strip()  # Added strip()

            # Debugging print statements
            # print(
            #     f"Param: {param}, OSS Value: {oss_value}, Baseline Value: {baseline_value}"
            # )

            if (
                oss_value.upper() == baseline_value.upper()
            ):  # Case-insensitive comparison
                compliance = "MATCH"
            else:
                compliance = "MISMATCH"

            gs_data = [
                NodeId,
                moc,
                "NodeBLocalCell=" + NodeBLocalCellId,
                param,
                oss_value,
                baseline_value,
                compliance,
            ]

            gs_result.append(gs_data)

    return gs_result
