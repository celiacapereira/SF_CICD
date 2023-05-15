
import connection as c

def is_null(df_insert): 
    if df_insert.isnull().values.any() == True:
            return "Fail"
    else:
        return "Pass"
    
is_null(c.df_drop) 
