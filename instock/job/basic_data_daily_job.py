#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import logging
import os.path
import sys

cpath_current = os.path.dirname(os.path.dirname(__file__))
cpath = os.path.abspath(os.path.join(cpath_current, os.pardir))
sys.path.append(cpath)
import instock.lib.run_template
import instock.core.tablestructure
import instock.lib.database
import instock.core.stockfetch
from instock.core.singleton_stock import stock_data

__author__ = 'myh '
__date__ = '2023/3/10 '


# 股票实时行情数据。
def save_nph_stock_spot_data(date, before=True):
    if before:
        return
    # 股票列表
    try:
        data = stock_data(date).get_data()
        if data is None or len(data.index) == 0:
            return

        table_name = instock.core.tablestructure.TABLE_CN_STOCK_SPOT['name']
        # 删除老数据。
        if instock.lib.database.checkTableIsExist(table_name):
            del_sql = f"DELETE FROM `{table_name}` where `date` = '{date}'"
            instock.lib.database.executeSql(del_sql)
            cols_type = None
        else:
            cols_type = instock.core.tablestructure.get_field_types(instock.core.tablestructure.TABLE_CN_STOCK_SPOT['columns'])

        instock.lib.database.insert_db_from_df(data, table_name, cols_type, False, "`date`,`code`")

    except Exception as e:
        logging.error(f"basic_data_daily_job.save_stock_spot_data处理异常：{e}")


# 基金实时行情数据。
def save_nph_etf_spot_data(date, before=True):
    if before:
        return
    # 股票列表
    try:
        data = instock.core.stockfetch.fetch_etfs(date)
        if data is None or len(data.index) == 0:
            return

        table_name = instock.core.tablestructure.TABLE_CN_ETF_SPOT['name']
        # 删除老数据。
        if instock.lib.database.checkTableIsExist(table_name):
            del_sql = f"DELETE FROM `{table_name}` where `date` = '{date}'"
            instock.lib.database.executeSql(del_sql)
            cols_type = None
        else:
            cols_type = instock.core.tablestructure.get_field_types(instock.core.tablestructure.TABLE_CN_ETF_SPOT['columns'])

        instock.lib.database.insert_db_from_df(data, table_name, cols_type, False, "`date`,`code`")
    except Exception as e:
        logging.error(f"basic_data_daily_job.save_nph_etf_spot_data处理异常：{e}")


def main():
    instock.lib.run_template.run_with_args(save_nph_stock_spot_data)
    instock.lib.run_template.run_with_args(save_nph_etf_spot_data)


# main函数入口
if __name__ == '__main__':
    main()
