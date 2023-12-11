#!/usr/bin/python
# PASSED: 2023 12 08
import os
import re
import sys
import time

import enmscripting

session = enmscripting.open()
myOSS = os.popen(
    r"cat /etc/hosts | grep rogers | tail -1 | sed -e 's/\s/\./g' | awk -F'.'"
    r" '{print $8}'"
).read()

basePath = sys.path[0]
homedir = os.path.expanduser("~")
OutputDir = (
    homedir
    + "/umts-gs-oss-ver_1/"
    + myOSS.upper().rstrip().replace("DNS", "")
    + "_UMTS_AUDIT_"
    + time.strftime("%d%m%y")
    + "/"
)

cell_list = []
nodelist = []

print(sys.argv[1])
with open(sys.argv[1]) as f:
    for line in f:
        cell_list.append(line.strip())

print(sys.argv[2])
with open(sys.argv[2]) as j:
    for line in j:
        nodelist.append(line.strip())

if not os.path.exists(OutputDir):
    os.mkdir(OutputDir)
else:
    os.system("rm " + OutputDir + "*.csv")

os.chdir(OutputDir)


def append(elements):
    result = ";".join(elements)
    return result


nodeappend = append(nodelist)

command1 = (
    "cmedit get *RNC* Utrancell.(absPrioCellRes, accessClassesBarredCs,"
    " accessClassesBarredPs, accessClassNBarred, admBlockRedirection,"
    " administrativeState, amrNbSelector, amrWbRateDlMax, amrWbRateUlMax,"
    " anrIafUtranCellConfig, anrIefUtranCellConfig, aseDlAdm,"
    " aseLoadThresholdUlSpeech, aseUlAdm, autoAcbEnabled,"
    " autoAcbMaxPsClassesToBar, autoAcbMinRcssrInput, autoAcbRcssrThresh,"
    " autoAcbRcssrWeight, autoAcbRtwpThresh, autoAcbRtwpWeight, bchPower,"
    " cellReserved, codeLoadThresholdDlSf128, compModeAdm, ctchAdmMargin,"
    " ctchOccasionPeriod, dchIflsMarginCode, dchIflsMarginPower,"
    " dchIflsThreshCode, dchIflsThreshPower, dlCodeAdm, dlCodeOffloadLimit,"
    " dlCodePowerCmEnabled, dlPowerOffloadLimit, dmcrEnabled, dnclEnabled,"
    " eulNonServingCellUsersAdm, eulServingCellUsersAdm,"
    " eulServingCellUsersAdmTti2, fachMeasOccaCycLenCoeff, ganHoEnabled,"
    " hardIfhoCorr, hcsSib3Config, hcsUsage, hoType, hsdpaUsersAdm,"
    " hsdpaUsersOffloadLimit, hsIflsDownswitchTrigg, hsIflsHighLoadThresh,"
    " hsIflsMarginUsers, hsIflsSpeechMultiRabTrigg, hsIflsThreshUsers,"
    " hsIflsTrigger, iFCong, iFHyst, iflsCpichEcnoThresh, iflsMode,"
    " inactivityTimerEnhUeDrx, individualOffset, interFreqFddMeasIndicator,"
    " interPwrMax, interRate, loadBasedHoSupport, loadSharingGsmFraction,"
    " loadSharingGsmThreshold, loadSharingMargin, maximumTransmissionPower,"
    " maxPwrMax, maxRate, maxTxPowerUl, minimumRate, minPwrMax, minPwrRl,"
    " nOutSyncInd, pathlossThreshold, primarySchPower, primaryTpsCell, pwrAdm,"
    " pwrLoadThresholdDlSpeech, qHyst1, qHyst2, qQualMin, qRxLevMin,"
    " qualMeasQuantity, rateSelectionPsInteractive, releaseRedirect,"
    " releaseRedirectEutraTriggers, releaseRedirectHsIfls, reportingRange1a,"
    " reportingRange1b, rlFailureT, rrcLcEnabled, rwrEutraCc,"
    " secondaryCpichPower, secondarySchPower, servDiffRrcAdmHighPrioProfile,"
    " sf128Adm, sf16Adm, sf16AdmUl, sf16gAdm, sf32Adm, sf4AdmUl, sf64AdmUl,"
    " sf8Adm, sf8AdmUl, sf8gAdmUl, sHcsRat, sInterSearch, sIntraSearch,"
    " sRatSearch, standAloneSrbSelector, timeToTrigger1a, timeToTrigger1b,"
    " transmissionScheme, treSelection, usedFreqThresh2dEcno,"
    " usedFreqThresh2dRscp, uarfcndl, uarfcnul) -t"
)
command2 = (
    "cmedit get *RNC* Rach.(administrativestate, aichPower,"
    " aichTransmissionTiming, constantValueCprach, maxPreambleCycle, nb01Max,"
    " nb01Min, powerOffsetP0, powerOffsetPpm, preambleRetransMax,"
    " preambleSignatures, scramblingCodeWordNo, spreadingFactor,"
    " subChannelNo) -t"
)
command3 = (
    "cmedit get *RNC* Fach.(administrativestate, maxFach1Power, maxFach2Power,"
    " pOffset1Fach, pOffset3Fach, sccpchOffset) -t"
)
command4 = (
    "cmedit get *RNC*"
    " Pch.(administrativestate,pchPower,pichPower,sccpchOffset) -t"
)
command5 = (
    "cmedit get *RNC* Eul.(administrativestate, edchTti2Support,"
    " eulDchBalancingEnabled, eulDchBalancingLoad, eulDchBalancingOverload,"
    " eulDchBalancingReportPeriod, eulDchBalancingSupport,"
    " eulDchBalancingSuspendDownSw, eulDchBalancingTimerNg,"
    " eulLoadTriggeredSoftCong, eulMaxTargetRtwp, eulTdSchedulingSupport,"
    " improvedL2Support, numEagchCodes, numEhichErgchCodes,"
    " pathlossThresholdEulTti2, releaseAseUlNg, threshEulTti2Ecno) -t"
)
command6 = (
    "cmedit get *RNC* Hsdsch.(administrativestate, codeThresholdPdu656,"
    " cqiFeedbackCycle, deltaAck1, deltaAck2, deltaCqi1, deltaCqi2,"
    " deltaNack1, deltaNack2, enhUeDrxSupport, enhancedL2Support,"
    " hsAqmCongCtrlSpiSupport, hsAqmCongCtrlSupport, hsFachSupport,"
    " hsMeasurementPowerOffset, initialAckNackRepetitionFactor,"
    " initialCqiRepetitionFactor, numHsPdschCodes, numHsScchCodes,"
    " qam64MimoSupport, qam64Support) -t"
)
# NOTE: update redirectionOrder
command7 = (
    "cmedit get *RNC* EutranFreqRelation.(cellReselectionPriority, qRxLevMin,"
    " qQualMin, threshHigh, threshHigh2, redirectionorder) -t"
)
command8 = (  # INFO: update start
    "cmedit get "
    + nodeappend
    + " NodeBSectorCarrier.(cellRange, eulMaxOwnUuLoad,"
    " eulMaxRotCoverage, eulThermalLevelPrior, eulNoiseFloorLock) -t"
)
command9 = "cmedit get " + nodeappend + " NodeBLocalCell.(*) -t"
command10 = (
    "cmedit get "
    + nodeappend
    + " NodeBFunction.(eul2msFirstSchedStep, eulLowRate, eulMaxAllowedSchRate,"
    " eulMaxShoRate, eulNonServHwRate, eulNoReschUsers, eulTargetRate) -t"
)
command11 = (
    "cmedit get "
    + nodeappend
    + " FeatureState.(FeatureStateId==CXC4020001, licenseState,featureState);"
    " FeatureState.(FeatureStateId==CXC4020002, licenseState,featureState);"
    " FeatureState.(FeatureStateId==CXC4020003, licenseState,featureState);"
    " FeatureState.(FeatureStateId==CXC4020008, licenseState,featureState);"
    " FeatureState.(FeatureStateId==CXC4020011, licenseState,featureState);"
    " FeatureState.(FeatureStateId==CXC4020013, licenseState,featureState);"
    " FeatureState.(FeatureStateId==CXC4020014, licenseState,featureState);"
    " FeatureState.(FeatureStateId==CXC4020025, licenseState,featureState);"
    " FeatureState.(FeatureStateId==CXC4020030, licenseState,featureState);"
    " FeatureState.(FeatureStateId==CXC4020040, licenseState,featureState);"
    " FeatureState.(FeatureStateId==CXC4020042, licenseState,featureState);"
    " FeatureState.(FeatureStateId==CXC4020016, licenseState,featureState);"
    " FeatureState.(FeatureStateId==CXC4020075, licenseState,featureState);"
    " FeatureState.(FeatureStateId==CXC4040009, licenseState,featureState);"
    " FeatureState.(FeatureStateId==CXC4012016, licenseState,featureState);"
    " FeatureState.(FeatureStateId==CXC4020051, licenseState,featureState);"
    " FeatureState.(FeatureStateId==CXC4011018, licenseState,featureState);"
    " FeatureState.(FeatureStateId==CXC4020102, licenseState,featureState);"
    " FeatureState.(FeatureStateId==CXC4011823, licenseState,featureState);"
    " FeatureState.(FeatureStateId==CXC4020005, licenseState,featureState);"
    " FeatureState.(FeatureStateId==CXC4020022, licenseState,featureState);"
    " FeatureState.(FeatureStateId==CXC4020031, licenseState,featureState);"
    " FeatureState.(FeatureStateId==CXC4020005, licenseState,featureState);"
    " FeatureState.(FeatureStateId==CXC4020103, licenseState,featureState);"
    " FeatureState.(FeatureStateId==CXC4020010, licenseState,featureState) -t"
)
command12 = (
    "cmedit get *RNC* IubLink.(IubLinkId, rbsId, administrativeState, dlHwAdm,"
    " controlPlaneTransportOption, dlHwAdm, l2EstReqRetryTimeNbapC,"
    " l2EstReqRetryTimeNbapD, reservedBy, ulHwAdm,"
    " userPlaneTransportOption) -t"
)
command13 = (
    "cmedit get *RNC* ExternalGsmCell.(bandIndicator,"
    " maxTxPowerUl,qRxLevMin, individualOffset, reservedBy) -t"
)
command14 = (
    "cmedit get *RNC* GsmRelation.(qOffset1sn, mobilityRelationType) -t"
)

output1 = OutputDir + "UtranCell.csv"
output2 = OutputDir + "Rach.csv"
output3 = OutputDir + "Fach.csv"
output4 = OutputDir + "Pch.csv"
output5 = OutputDir + "Eul.csv"
output6 = OutputDir + "Hsdsch.csv"
output7 = OutputDir + "EutranFreqRelation.csv"
output8 = OutputDir + "NodeBSectorCarrier.csv"
output9 = OutputDir + "NodeBLocalCell.csv"
output10 = OutputDir + "NodeBFunction.csv"
output11 = OutputDir + "License.csv"
output12 = OutputDir + "IubLink.csv"
output13 = OutputDir + "ExternalGsmCell.csv"
output14 = OutputDir + "GsmRelation.csv"

terminal = session.terminal()
result1 = terminal.execute(command1)
result2 = terminal.execute(command2)
result3 = terminal.execute(command3)
result4 = terminal.execute(command4)
result5 = terminal.execute(command5)
result6 = terminal.execute(command6)
result7 = terminal.execute(command7)
result8 = terminal.execute(command8)
result9 = terminal.execute(command9)
result10 = terminal.execute(command10)
result11 = terminal.execute(command11)
result12 = terminal.execute(command12)
result13 = terminal.execute(command13)
result14 = terminal.execute(command14)
# result15 = terminal.execute(command15)


def contains(list_of_strings_to_check, line):
    for string in list_of_strings_to_check:
        if string in line:
            return False
    return True


list_of_strings = ["SubNetwork,SubNetwork", "instance(s)", "Error", "Scope:"]


def contains_cell(cell_list, line):
    for string in cell_list:
        if string in line:
            return True
    return False


# NOTE: Utrancell.csv split.
def split_absPrioCellRes(line):
    match = re.search(
        r"sPrioritySearch1=(\d+),\s*measIndFach=(\w+),\s*sPrioritySearch2=(\d+),\s*threshServingLow=(\d+),\s*cellReselectionPriority=(\d+)",
        line,
    )
    return match.groups() if match else ("", "", "", "", "")


def split_accessClasses(line):
    matches = re.findall(r"\[(.*?)\]", line)
    values = []
    for match in matches:
        values.extend(match.split(", "))
    return values


def split_admBlockRedirection(line):
    match = re.search(r".*{gsmRrc=(\w+), speech=(\w+), rrc=(\w+)}.*", line)
    return match.groups() if match else ("", "", "")


def split_anrIafUtranCellConfig(line):
    match = re.search(
        r".*{sib11IafAnclEnabled=(\w+), relationRemoveEnabled=(\w+),"
        r" relationAddEnabled=(\w+), anrEnabled=(\w+)}.*",
        line,
    )
    return match.groups() if match else ("", "", "", "")


def split_anrIefUtranCellConfig(line):
    match = re.search(
        r".*{anrEnabled=(\w+), sib11IefAnclEnabled=(\w+)}.*", line
    )
    return match.groups() if match else ("", "")


def split_aseLoadThresholdUlSpeech(line):
    match = re.search(
        r".*{amr12200=(\d+), amrWb8850=(\d+), amr5900=(\d+), amr7950=(\d+),"
        r" amrWb12650=(\d+)}.*",
        line,
    )
    return match.groups() if match else ("", "", "", "", "")


def split_hcsSib3Config(line):
    match = re.search(
        r".*{sSearchHcs=(-?\d+), hcsPrio=(\d+), qHcs=(\d+)}.*", line
    )
    return match.groups() if match else ("", "", "")


def split_hcsUsage(line):
    match = re.search(r".*{idleMode=(\w+), connectedMode=(\w+)}.*", line)
    return match.groups() if match else ("", "")


def split_hsIflsDownswitchTrigg(line):
    match = re.search(
        r".*{toFach=(\w+), fastDormancy=(\w+), toUra=(\w+)}.*", line
    )
    return match.groups() if match else ("", "", "")


def split_hsIflsTrigger(line):
    match = re.search(r"fromUra=(.*?), fromFach=(.*?)\}", line)
    return match.groups() if match else ("", "", "")


def split_pwrLoadThresholdDlSpeech(line):
    match = re.search(
        r".*{amr12200=(\d+), amrWb8850=(\d+), amr5900=(\d+), amr7950=(\d+),"
        r" amrWb12650=(\d+)}.*",
        line,
    )
    return match.groups() if match else ("", "", "", "", "")


def split_rateSelectionPsInteractive(line):
    match = re.search(
        r".*{dlPrefRate=(\d+), channelType=(\w+), ulPrefRate=(\d+)}.*", line
    )
    return match.groups() if match else ("", "", "")


def split_releaseRedirectEutraTriggers(line):
    match = re.search(
        r".*{dchToFach=(\w+), csFallbackDchToFach=(\w+), fachToUra=(\w+),"
        r" fastDormancy=(\w+), csFallbackCsRelease=(\w+),"
        r" normalRelease=(\w+)}.*",
        line,
    )
    return match.groups() if match else ("", "", "", "", "", "")


def transform_line_utrancell(line):
    data = line.split("\t")

    (
        sprioritysearch1,
        measindfach,
        sprioritysearch2,
        threshservinglow,
        cellreselectionpriority,
    ) = split_absPrioCellRes(data[3])
    barredcsaccessclasses = split_accessClasses(data[4])
    barredpsaccessclasses = split_accessClasses(data[5])
    nbarredaccessclasses = split_accessClasses(data[6])
    gsmrrc, speech, rrc = split_admBlockRedirection(data[7])
    anrIafUtranCellConfig = split_anrIafUtranCellConfig(data[12])
    anrIefUtranCellConfig = split_anrIefUtranCellConfig(data[13])
    aseLoadThresholdUlSpeech = split_aseLoadThresholdUlSpeech(data[15])
    hcssib3config = split_hcsSib3Config(data[46])
    hcsusage = split_hcsUsage(data[47])
    hsiflsdownswitchtrigg = split_hsIflsDownswitchTrigg(data[51])
    hsIflsTrigger = split_hsIflsTrigger(data[56])
    pwrloadthresholddlspeech = split_pwrLoadThresholdDlSpeech(data[82])
    rateselectionpsinteractive = split_rateSelectionPsInteractive(data[88])
    releaseredirecteutratriggers = split_releaseRedirectEutraTriggers(data[90])

    transpose_data = (
        [
            str(data[0]),
            str(data[1]),
            str(data[2]),
            sprioritysearch1,
            measindfach,
            sprioritysearch2,
            threshservinglow,
            cellreselectionpriority,
        ]
        + list(barredcsaccessclasses)
        + list(barredpsaccessclasses)
        + list(nbarredaccessclasses)
        + [gsmrrc, speech, rrc]
        + data[8:12]
        + list(anrIafUtranCellConfig)
        + list(anrIefUtranCellConfig)
        + [str(data[14])]
        + list(aseLoadThresholdUlSpeech)
        + data[16:46]
        + list(hcssib3config)
        + list(hcsusage)
        + data[48:51]
        + list(hsiflsdownswitchtrigg)
        + data[52:56]
        + list(hsIflsTrigger)
        + data[57:82]
        + list(pwrloadthresholddlspeech)
        + data[83:88]
        + list(rateselectionpsinteractive)
        + [str(data[89])]
        + list(releaseredirecteutratriggers)
        + data[91:123]
    )

    joined_data = "\t".join(str(item) for item in transpose_data)

    return [joined_data]


if result1.is_command_result_available():
    filename = open(output1, "w")
    header = None
    for line in result1.get_output():
        if "NodeId" in line:
            header = line.split("\t")
            header = [
                col.replace(
                    "absPrioCellRes",
                    "absPrioCellRes.sPrioritySearch1\t"
                    "absPrioCellRes.measIndFach\t"
                    "absPrioCellRes.sPrioritySearch2\t"
                    "absPrioCellRes.threshServingLow\t"
                    "absPrioCellRes.cellReselectionPriority",
                )
                .replace(
                    "accessClassesBarredCs",
                    "accessClassesBarredCs0\t"
                    "accessClassesBarredCs1\t"
                    "accessClassesBarredCs2\t"
                    "accessClassesBarredCs3\t"
                    "accessClassesBarredCs4\t"
                    "accessClassesBarredCs5\t"
                    "accessClassesBarredCs6\t"
                    "accessClassesBarredCs7\t"
                    "accessClassesBarredCs8\t"
                    "accessClassesBarredCs9\t"
                    "accessClassesBarredCs10\t"
                    "accessClassesBarredCs11\t"
                    "accessClassesBarredCs12\t"
                    "accessClassesBarredCs13\t"
                    "accessClassesBarredCs14\t"
                    "accessClassesBarredCs15",
                )
                .replace(
                    "accessClassesBarredPs",
                    "accessClassesBarredPs0\t"
                    "accessClassesBarredPs1\t"
                    "accessClassesBarredPs2\t"
                    "accessClassesBarredPs3\t"
                    "accessClassesBarredPs4\t"
                    "accessClassesBarredPs5\t"
                    "accessClassesBarredPs6\t"
                    "accessClassesBarredPs7\t"
                    "accessClassesBarredPs8\t"
                    "accessClassesBarredPs9\t"
                    "accessClassesBarredPs10\t"
                    "accessClassesBarredPs11\t"
                    "accessClassesBarredPs12\t"
                    "accessClassesBarredPs13\t"
                    "accessClassesBarredPs14\t"
                    "accessClassesBarredPs15",
                )
                .replace(
                    "accessClassNBarred",
                    "accessClassNBarred0\t"
                    "accessClassNBarred1\t"
                    "accessClassNBarred2\t"
                    "accessClassNBarred3\t"
                    "accessClassNBarred4\t"
                    "accessClassNBarred5\t"
                    "accessClassNBarred6\t"
                    "accessClassNBarred7\t"
                    "accessClassNBarred8\t"
                    "accessClassNBarred9\t"
                    "accessClassNBarred10\t"
                    "accessClassNBarred11\t"
                    "accessClassNBarred12\t"
                    "accessClassNBarred13\t"
                    "accessClassNBarred14\t"
                    "accessClassNBarred15",
                )
                .replace(
                    "admBlockRedirection",
                    "admBlockRedirection.gsmRrc\t"
                    "admBlockRedirection.speech\t"
                    "admBlockRedirection.rrc",
                )
                .replace(
                    "anrIafUtranCellConfig",
                    "anrIafUtranCellConfig.sib11IafAnclEnabled\t"
                    "anrIafUtranCellConfig.relationRemoveEnabled\t"
                    "anrIafUtranCellConfig.relationAddEnabled\t"
                    "anrIafUtranCellConfig.anrEnabled",
                )
                .replace(
                    "anrIefUtranCellConfig",
                    "anrIefUtranCellConfig.anrEnabled\t"
                    "anrIefUtranCellConfig.sib11IefAnclEnabled",
                )
                .replace(
                    "aseLoadThresholdUlSpeech",
                    "aseLoadThresholdUlSpeech.amr12200\t"
                    "aseLoadThresholdUlSpeech.amrWb8850\t"
                    "aseLoadThresholdUlSpeech.amr5900\t"
                    "aseLoadThresholdUlSpeech.amr7950\t"
                    "aseLoadThresholdUlSpeech.amrWb12650",
                )
                .replace(
                    "hcsSib3Config",
                    "hcsSib3Config.sSearchHcs\t"
                    "hcsSib3Config.hcsPrio\t"
                    "hcsSib3Config.qHcs",
                )
                .replace(
                    "hcsUsage",
                    "hcsUsage.idleMode\thcsUsage.connectedMode",
                )
                .replace(
                    "hsIflsDownswitchTrigg",
                    "hsIflsDownswitchTrigg.toFach\t"
                    "hsIflsDownswitchTrigg.fastDormancy\t"
                    "hsIflsDownswitchTrigg.toUra",
                )
                .replace(
                    "hsIflsTrigger",
                    "hsIflsTrigger.fromUra\thsIflsTrigger.fromFach",
                )
                .replace(
                    "pwrLoadThresholdDlSpeech",
                    "pwrLoadThresholdDlSpeech.amr12200\t"
                    "pwrLoadThresholdDlSpeech.amrWb8850\t"
                    "pwrLoadThresholdDlSpeech.amr5900\t"
                    "pwrLoadThresholdDlSpeech.amr7950\t"
                    "pwrLoadThresholdDlSpeech.amrWb12650",
                )
                .replace(
                    "rateSelectionPsInteractive",
                    "rateSelectionPsInteractive.dlPrefRate\t"
                    "rateSelectionPsInteractive.channelType\t"
                    "rateSelectionPsInteractive.ulPrefRate",
                )
                .replace(
                    "releaseRedirectEutraTriggers",
                    "releaseRedirectEutraTriggers.dchToFach\t"
                    "releaseRedirectEutraTriggers.csFallbackDchToFach\t"
                    "releaseRedirectEutraTriggers.fachToUra\t"
                    "releaseRedirectEutraTriggers.fastDormancy\t"
                    "releaseRedirectEutraTriggers.csFallbackCsRelease\t"
                    "releaseRedirectEutraTriggers.normalRelease",
                )
                for col in header
            ]
            filename.write("\t".join(header) + "\n")
        elif contains(list_of_strings, line):
            if contains_cell(cell_list, line):
                transpose_lines = transform_line_utrancell(line)
                for t_line in transpose_lines:
                    filename.write(t_line + "\n")
    filename.close()
else:
    print("Failure for command")
    print(result1._result_lines)

if result2.is_command_result_available():
    filename = open(output2, "w")
    for line in result2.get_output():
        if "NodeId" in line:
            filename.write(line + "\n")
        elif contains(list_of_strings, line):
            if contains_cell(cell_list, line):
                filename.write(
                    line.replace("[", "")
                    .replace("]", "")
                    .replace("{", "")
                    .replace("}", "")
                    + "\n"
                )
    filename.close()
else:
    print("Failure for command")
    print(result2._result_lines)

if result3.is_command_result_available():
    filename = open(output3, "w")
    for line in result3.get_output():
        if "NodeId" in line:
            filename.write(line + "\n")
        elif contains(list_of_strings, line):
            if contains_cell(cell_list, line):
                filename.write(
                    line.replace("[", "")
                    .replace("]", "")
                    .replace("{", "")
                    .replace("}", "")
                    + "\n"
                )
    filename.close()
else:
    print("Failure for command")
    print(result3._result_lines)

if result4.is_command_result_available():
    filename = open(output4, "w")
    for line in result4.get_output():
        if "NodeId" in line:
            filename.write(line + "\n")
        elif contains(list_of_strings, line):
            if contains_cell(cell_list, line):
                filename.write(
                    line.replace("[", "")
                    .replace("]", "")
                    .replace("{", "")
                    .replace("}", "")
                    + "\n"
                )
    filename.close()
else:
    print("Failure for command")
    print(result4._result_lines)

if result5.is_command_result_available():
    filename = open(output5, "w")
    for line in result5.get_output():
        if "NodeId" in line:
            filename.write(line + "\n")
        elif contains(list_of_strings, line):
            if contains_cell(cell_list, line):
                filename.write(
                    line.replace("[", "")
                    .replace("]", "")
                    .replace("{", "")
                    .replace("}", "")
                    + "\n"
                )
    filename.close()
else:
    print("Failure for command")
    print(result5._result_lines)

if result6.is_command_result_available():
    filename = open(output6, "w")
    for line in result6.get_output():
        if "NodeId" in line:
            filename.write(line + "\n")
        elif contains(list_of_strings, line):
            if contains_cell(cell_list, line):
                filename.write(
                    line.replace("[", "")
                    .replace("]", "")
                    .replace("{", "")
                    .replace("}", "")
                    + "\n"
                )
    filename.close()
else:
    print("Failure for command")
    print(result6._result_lines)

if result7.is_command_result_available():
    filename = open(output7, "w")
    for line in result7.get_output():
        if "NodeId" in line:
            filename.write(line + "\n")
        elif contains(list_of_strings, line):
            if contains_cell(cell_list, line):
                filename.write(
                    line.replace("[", "")
                    .replace("]", "")
                    .replace("{", "")
                    .replace("}", "")
                    + "\n"
                )
    filename.close()
else:
    print("Failure for command")
    print(result7._result_lines)

if result8.is_command_result_available():
    filename = open(output8, "w")
    for line in result8.get_output():
        if "NodeId" in line:
            filename.write(line + "\n")
        elif contains(list_of_strings, line):
            if contains_cell(nodelist, line):
                filename.write(
                    line.replace("[", "")
                    .replace("]", "")
                    .replace("{", "")
                    .replace("}", "")
                    + "\n"
                )
    filename.close()
else:
    print("Failure for command")
    print(result8._result_lines)

if result9.is_command_result_available():
    filename = open(output9, "w")
    for line in result9.get_output():
        if "NodeId" in line:
            filename.write(line + "\n")
        elif contains(list_of_strings, line):
            if contains_cell(nodelist, line):
                filename.write(
                    line.replace("[", "")
                    .replace("]", "")
                    .replace("{", "")
                    .replace("}", "")
                    + "\n"
                )
    filename.close()
else:
    print("Failure for command")
    print(result9._result_lines)

if result10.is_command_result_available():
    filename = open(output10, "w")
    for line in result10.get_output():
        if "NodeId" in line:
            filename.write(line + "\n")
        elif contains(list_of_strings, line):
            if contains_cell(nodelist, line):
                filename.write(
                    line.replace("[", "")
                    .replace("]", "")
                    .replace("{", "")
                    .replace("}", "")
                    + "\n"
                )
    filename.close()
else:
    print("Failure for command")
    print(result10._result_lines)

if result11.is_command_result_available():
    filename = open(output11, "w")
    for line in result11.get_output():
        if "NodeId" in line:
            filename.write(line + "\n")
        elif contains(list_of_strings, line):
            if contains_cell(nodelist, line):
                filename.write(
                    line.replace("[", "")
                    .replace("]", "")
                    .replace("{", "")
                    .replace("}", "")
                    + "\n"
                )
    filename.close()
else:
    print("Failure for command")
    print(result11._result_lines)

if result12.is_command_result_available():
    filename = open(output12, "w")
    for line in result12.get_output():
        if "NodeId" in line:
            filename.write(line + "\n")
        elif contains(list_of_strings, line):
            if contains_cell(nodelist, line):
                filename.write(
                    line.replace("[", "")
                    .replace("]", "")
                    .replace("{", "")
                    .replace("}", "")
                    + "\n"
                )
    filename.close()
else:
    print("Failure for command")
    print(result12._result_lines)


# NOTE: IUBLINK split
def find_reserved_by(line):
    reserved_matches = re.findall(r",UtranCell=(\w+)", line)
    return reserved_matches


def split_transport_options(option):
    match = re.search(r"ipv4=(\w+),\s*atm=(\w+)", option)
    return match.groups() if match else ("", "")


def transform_line(line):
    data = line.split("\t")
    control_ipv4, control_atm = split_transport_options(data[4])
    user_ipv4, user_atm = split_transport_options(data[11])
    reserved_by_values = find_reserved_by(data[9])

    transformed_lines = []
    for reserved_by_value in reserved_by_values:
        transformed_data = [
            data[0],
            data[1],
            data[2],
            data[3],
            control_ipv4,
            control_atm,
            data[5],
            data[6],
            data[7],
            data[8],
            reserved_by_value,
            data[10],
            user_ipv4,
            user_atm,
        ]
        transformed_lines.append("\t".join(transformed_data))

    return transformed_lines


if result12.is_command_result_available():
    filename = open(output12, "w")
    header = None
    for line in result12.get_output():
        if "NodeId" in line:
            header = line.split("\t")
            header = [
                col.replace(
                    "controlPlaneTransportOption",
                    "controlPlaneTransportOption.ipv4\t"
                    "controlPlaneTransportOption.atm",
                )
                .replace(
                    "userPlaneTransportOption",
                    "userPlaneTransportOption.ipv4\t"
                    "userPlaneTransportOption.atm",
                )
                .replace("reservedBy", "UtranCellId")
                for col in header
            ]
            filename.write("\t".join(header) + "\n")
        elif contains(list_of_strings, line):
            if contains_cell(nodelist, line):
                transformed_lines = transform_line(line)
                for transformed_line in transformed_lines:
                    filename.write(transformed_line + "\n")
    filename.close()
else:
    print("Failure for command")
    print(result12._result_lines)

#  NOTE: ExternalGsmCell
if result13.is_command_result_available():
    filename = open(output13, "w")
    header = None
    for line in result13.get_output():
        if "NodeId" in line:
            header = line.replace("reservedBy", "UtranCellId")
            filename.write(header + "\n")
        elif contains(list_of_strings, line):
            utrancell_values = find_reserved_by(line)
            for utrancell in utrancell_values:
                data = line.strip().split("\t")

                cols = (
                    data[0],
                    data[1],
                    data[2],
                    data[3],
                    data[4],
                    data[5],
                    data[6],
                    data[7],
                    utrancell,
                )
                transformed_line = "\t".join(cols)
                if contains_cell(cell_list, utrancell):
                    filename.write(transformed_line + "\n")
    filename.close()
else:
    print("Failure for command")
    print(result13._result_lines)

if result14.is_command_result_available():
    filename = open(output14, "w")
    for line in result14.get_output():
        if "NodeId" in line:
            filename.write(line + "\n")
        elif contains(list_of_strings, line):
            if contains_cell(cell_list, line):
                filename.write(
                    line.replace("[", "")
                    .replace("]", "")
                    .replace("{", "")
                    .replace("}", "")
                    + "\n"
                )
    filename.close()
else:
    print("Failure for command")
    print(result14._result_lines)


enmscripting.close(session)
