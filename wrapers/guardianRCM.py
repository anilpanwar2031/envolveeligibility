import sys
import os
import uuid

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from FileDownload import Downloader
import random, string
import tabula


def nameFormatter(teststring):
    if type(teststring) is str:
        firstname, lastname = teststring.strip().lower().split()
        return firstname.strip(), lastname.strip()


def main(data):
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<In GuardianRCM>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    if data["RcmEobClaimMaster"][0].get("url") and data["RcmEobClaimMaster"][0].get("ClaimNumber") != "" and \
            data["RcmEobClaimMaster"][0].get("Patient") != "" and data["RcmEobClaimMaster"][0].get(
        "DateOfService") != "" and data["RcmEobClaimMaster"][0].get("SubmittedCharges") != "":
        data['RcmEobClaimDetail'] = []
        file_path = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + ".pdf"
        # file_path = "3GAXV3KCM2.pdf"
        # print(file_path)
        input_file = data["RcmEobClaimMaster"][0]["url"].replace("%20", " ")
        print("input_file>>>>>>>>>>>>>>", input_file)
        Downloader('Revenue Cycle Management', file_path, input_file)
        dict_list = tabula.read_pdf(file_path, pages='all')
        # print("dict_list>>>>>>>>>>>>>>>>>>>>>>>",dict_list)

        PatientName = data["RcmEobClaimMaster"][0].get("Patient")
        firstname, lastname = PatientName.lower().split()

        # lst = []
        # for ind, tab in enumerate(dict_list):
        #     if any('Claim Number' and PatientName in col for col in tab.columns):
        #         new_columns_name = {}
        #         for i in range(len(tab.columns)):
        #             old_name = tab.columns[i]
        #             new_name = f'columns{i + 1}'
        #             new_columns_name[old_name] = new_name
        #             tab = tab.rename(columns=new_columns_name)
        #         lst.append(tab.to_dict('records'))

        lst = []
        for ind, tab in enumerate(dict_list):
            if any('Claim Number' in col for col in tab.columns):
                if len(tab) > 0 and len(tab.columns) > 1:
                    checkParam = tab.iloc[0][0]
                    if "Patient Name" in checkParam:
                        if nameFormatter(PatientName) == nameFormatter(checkParam.split("Patient Name")[-1]):
                            new_columns_name = {}
                            for i in range(len(tab.columns)):
                                old_name = tab.columns[i]
                                new_name = f'columns{i + 1}'
                                new_columns_name[old_name] = new_name
                                tab = tab.rename(columns=new_columns_name)
                            lst.append(tab.to_dict('records'))
        # print("lst>>>>>>>>>>>>>>>>>>>>>>",lst)
        temp_lst = []
        for i in range(len(lst)):
            for obj in lst[i]:
                if type(obj.get('columns1')) != float:
                    temp_lst.append(obj)
        # print("temp_lst>>>>>>>>>>>>>>>>>>>>>>", temp_lst)
        filtered_lst = []
        for i in range(len(temp_lst)):
            if not temp_lst[i]['columns1'].startswith('Patient Name') and not temp_lst[i]['columns1'].startswith(
                    'Planholder') and not temp_lst[i]['columns1'].startswith('Line Submitted') and not temp_lst[i][
                'columns1'].startswith('No.'):
                filtered_lst.append(temp_lst[i])
        # print("filtered_lst>>>>>>>>>>",filtered_lst)
        new_lst = []
        new_dict = {}
        for obj in filtered_lst:

            columns3 = str(obj.get('columns3')).replace('nan', '').split()
            columns4 = str(obj.get('columns4')).replace('nan', '').split()

            if 'columns6' in obj:
                columns6 = str(obj.get('columns6')).split()
                columns4 = obj.get('columns4').split()
                if len(columns6) == 3 and len(columns4) == 3:
                    new_dict = {
                        'SubmittedADACodesDescription': obj.get("columns1"),
                        'AltCode': obj.get("columns2"),
                        'ToothNo': obj.get("columns3"),
                        'DateOfService': columns4[0],
                        'SubmittedCharge': columns4[1],
                        'ConsideredCharge': columns4[2],
                        'CoveredCharge': obj.get("columns5"),
                        'DeductibleAmount': columns6[0],
                        'CoveragePercent': columns6[1],
                        'BenefitAmount': columns6[2]
                    }
                elif len(columns6) == 2 and len(columns4) == 3:
                    new_dict = {
                        'SubmittedADACodesDescription': obj.get("columns1"),
                        'AltCode': obj.get("columns2"),
                        'ToothNo': obj.get("columns3"),
                        'DateOfService': columns4[0],
                        'SubmittedCharge': columns4[1],
                        'ConsideredCharge': columns4[2],
                        'CoveredCharge': obj.get("columns5"),
                        'DeductibleAmount': "",
                        'CoveragePercent': columns6[0],
                        'BenefitAmount': columns6[1]
                    }
                elif len(columns6) == 1 and len(columns4) == 4:
                    new_dict = {
                        'SubmittedADACodesDescription': obj.get("columns1"),
                        'AltCode': obj.get("columns2"),
                        'ToothNo': obj.get("columns3"),
                        'DateOfService': columns4[0],
                        'SubmittedCharge': columns4[1],
                        'ConsideredCharge': columns4[2],
                        'CoveredCharge': columns4[3],
                        'DeductibleAmount': "",
                        'CoveragePercent': obj.get("columns5"),
                        'BenefitAmount': str(obj.get("columns6"))
                    }
                elif len(columns4) == 3:
                    columns4 = obj.get('columns4').split()
                    new_dict = {
                        'SubmittedADACodesDescription': obj.get("columns1"),
                        'AltCode': obj.get("columns2"),
                        'ToothNo': obj.get("columns3"),
                        'DateOfService': columns4[0],
                        'SubmittedCharge': columns4[1],
                        'ConsideredCharge': columns4[2],
                        'CoveredCharge': obj.get("columns5"),
                        'DeductibleAmount': obj.get("columns6"),
                        'CoveragePercent': obj.get("columns7"),
                        'BenefitAmount': str(obj.get("columns9"))
                    }
            elif len(columns3) == 3:
                columns2 = obj.get('columns2').split()
                columns4 = obj.get('columns4').split()
                new_dict = {
                    'SubmittedADACodesDescription': obj["columns1"],
                    'AltCode': "",
                    'ToothNo': columns2[0],
                    'DateOfService': columns2[1],
                    'SubmittedCharge': columns3[0],
                    'ConsideredCharge': columns3[1],
                    'CoveredCharge': columns3[2],
                    'DeductibleAmount': "",
                    'CoveragePercent': columns4[0],
                    'BenefitAmount': str(columns4[1])
                }
            elif len(columns4) == 4:
                columns5 = obj.get('columns5').split()
                new_dict = {
                    'SubmittedADACodesDescription': obj.get("columns1"),
                    'AltCode': "",
                    'ToothNo': obj.get('columns3'),
                    'DateOfService': columns4[0],
                    'SubmittedCharge': columns4[1],
                    'ConsideredCharge': columns4[2],
                    'CoveredCharge': columns4[3],
                    'DeductibleAmount': "",
                    'CoveragePercent': columns5[0],
                    'BenefitAmount': str(columns5[1])
                }


            else:
                columns3 = obj.get('columns3').split()
                columns4 = obj.get('columns4').split()
                new_dict = {
                    'SubmittedADACodesDescription': obj["columns1"],
                    'AltCode': "",
                    'ToothNo': obj.get("columns2"),
                    'DateOfService': columns3[0],
                    'SubmittedCharge': columns3[1],
                    'ConsideredCharge': columns3[2],
                    'CoveredCharge': columns3[3],
                    'DeductibleAmount': "",
                    'CoveragePercent': columns4[0],
                    'BenefitAmount': columns4[1]
                }
            if str(new_dict.get('AltCode')) == 'nan':
                new_dict['AltCode'] = str(new_dict.get('AltCode')).replace('nan', '')
            if str(new_dict.get('ToothNo')) == 'nan':
                new_dict['ToothNo'] = str(new_dict.get('ToothNo')).replace('nan', '')
            new_lst.append(new_dict)
        for i in new_lst:
            data['RcmEobClaimDetail'].append(i)

        ADACodes = ""
        Description = ""
        for i in range(len(data['RcmEobClaimDetail'])):
            for key, values in data['RcmEobClaimDetail'][i].items():
                if key == "SubmittedADACodesDescription":
                    cdtcodes_type_of_service = values
                    ADACodes, Description = cdtcodes_type_of_service.split("/", 1)
            data['RcmEobClaimDetail'][i]["ADACodes"] = ADACodes
            data['RcmEobClaimDetail'][i]["Description"] = Description
            del data['RcmEobClaimDetail'][i]["SubmittedADACodesDescription"]

        for obj in data['RcmEobClaimDetail']:
            ads_code = obj["ADACodes"].split()
            if len(ads_code) == 2:
                obj["ADACodes"] = ads_code[1]
        for obj in data["RcmEobClaimDetail"]:
            obj["RecordID"] = str(uuid.uuid4())
    else:
        data['RcmEobClaimDetail'] = []
        if data["RcmEobClaimMaster"][0].get("url"):
            data["RcmEobClaimMaster"][0]["url"] = ""

    if data.get("RcmEobClaimMaster"):
        for obj in data["RcmEobClaimMaster"]:
            obj["RecordID"] = str(uuid.uuid4())

    return data
