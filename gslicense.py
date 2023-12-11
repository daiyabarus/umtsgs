def gs_license_process(
    txt_data: list, gslist_data: list, dt_col: dict, moc: str
):
    gs_result = []

    for raw_data in txt_data:
        if str(raw_data).strip() == "" or "NodeId" in str(raw_data):
            continue

        u_data = str(raw_data).split()
        NodeId = u_data[dt_col.get("NodeId", 0)]
        FeatureStateId = u_data[dt_col.get("FeatureStateId", 3)]
        LicenseState = u_data[dt_col.get("featureState", 4)]

        for gs_data in gslist_data:
            gs_id, gs_status = gs_data

            if FeatureStateId == gs_id:
                compliance = (
                    "MATCH" if LicenseState == gs_status else "MISMATCH"
                )
                gs_data = [
                    NodeId,
                    moc,
                    "FeatureState=" + FeatureStateId,
                    gs_id,
                    LicenseState,
                    gs_status,
                    compliance,
                ]
                gs_result.append(gs_data)

    return gs_result
