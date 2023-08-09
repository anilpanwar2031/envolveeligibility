

def main(data):
    """
        This function takes in a dictionary containing two lists: 'RcmEobClaimMaster' and 'RcmEobClaimDetail'.
        It modifies keys of the RcmEobClaimDetail.

        Args:
        - data: A dictionary containing two lists: 'RcmEobClaimMaster' and 'RcmEobClaimDetail'.

        Returns:
        - A modified 'data' dictionary with the changed keys in 'RcmEobClaimDetail'.
    """

    # Keys to modify in claim detail list
    keys=["Procedure","ProcedureDescription","DOS","Submitted","Paid"]
    temp=[]
    for i in range(len(data['RcmEobClaimDetail'])):
        final_dict = dict(zip(keys, list(data['RcmEobClaimDetail'][i].values())))
        temp.append(final_dict)
    data['RcmEobClaimDetail']=temp

    
    return data








