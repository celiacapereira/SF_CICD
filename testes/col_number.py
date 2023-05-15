import connection as c


def col_number(df_insert):
    if  df_insert.shape[1] == 8:
        return "PASS"
    else:
        return "FAIL"
    
col_number(c.df_drop)         
