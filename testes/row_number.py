import connection as c


def row_number(df_insert):
    if  df_insert.shape[0] == 891:
        return "PASS"
    else:
        return "FAIL"
    
row_number(c.df_drop)     
